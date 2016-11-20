import unittest

# import the library to test
import sys

sys.path.insert(0, '../')
import skygrid

# used for testing credentials
config = None
# whether we run the api calls that require a master key
testMasterFns = False


def load_config(filename):
    import json
    with open(filename) as cf:
        global config
        config = json.loads("".join(cf.readlines()))


class TestLogin(unittest.TestCase):
    def test_loginProj1User1(self):
        project = skygrid.Project(config["projects"]["project1"]["id"], api='rest')
        self.assertIsNotNone(project._project_id)
        usr1 = config["projects"]["project1"]["users"][0]
        project.login(usr1["email"], usr1["password"])

        self.assertEqual(usr1["email"], project._user["email"])

        self.assertIsNotNone(project._user["token"])

    def test_loginProj1User2(self):
        project = skygrid.Project(config["projects"]["project1"]["id"], api='rest')
        self.assertIsNotNone(project._project_id)
        usr1 = config["projects"]["project1"]["users"][1]
        project.login(usr1["email"], usr1["password"])

        self.assertEqual(usr1["email"], project._user["email"])
        self.assertEqual(usr1["id"], project._user["id"])
        self.assertIsNotNone(project._user["token"])

    def test_loginProj2User1(self):
        project = skygrid.Project(config["projects"]["project2"]["id"], api='rest')
        self.assertIsNotNone(project._project_id)
        usr1 = config["projects"]["project2"]["users"][0]
        project.login(usr1["email"], usr1["password"])

        self.assertEqual(usr1["email"], project._user["email"])
        self.assertEqual(usr1["id"], project._user["id"])
        self.assertIsNotNone(project._user["token"])

    def test_falseuser(self):
        project = skygrid.Project(config["projects"]["project1"]["id"], api='rest')
        self.assertIsNotNone(project._project_id)
        try:
            project.login("missing@mail.com", "password")
        except skygrid.AuthenticationError:
            return
        self.fail("Invalid user did not trip AuthenticationError")

    def test_falseuserfalseproj(self):
        try:
            project = skygrid.Project("non_exist")
            usr1 = config["projects"]["project1"]["users"][0]
            project.login(usr1["email"], usr1["password"])
        except skygrid.ProjectError:
            return
        self.fail("Initialised invalid project")


class TestLogoff(unittest.TestCase):
    def test_logoffProj1User1(self):
        project = skygrid.Project(config["projects"]["project1"]["id"], api='rest')
        usr1 = config["projects"]["project1"]["users"][0]
        project.login(usr1["email"], usr1["password"])
        project.logout()
        self.assertIsNone(project._user)

    def test_logoffProj1User2(self):
        project = skygrid.Project(config["projects"]["project1"]["id"], api='rest')
        usr1 = config["projects"]["project1"]["users"][1]
        project.login(usr1["email"], usr1["password"])
        project.logout()
        self.assertIsNone(project._user)

    def test_logoffProj2User1(self):
        project = skygrid.Project(config["projects"]["project2"]["id"], api='rest')
        usr1 = config["projects"]["project2"]["users"][0]
        project.login(usr1["email"], usr1["password"])
        project.logout()
        self.assertIsNone(project._user)

    def test_logoffP1_notloggedin(self):
        # should not throw any exceptions - logout
        project = skygrid.Project(config["projects"]["project1"]["id"], api='rest')
        self.assertIsNone(project._user)
        project.logout()
        self.assertIsNone(project._user)

if testMasterFns:
    class TestSignup(unittest.TestCase):
        def test_newSignup(self):
            project = skygrid.Project(config["projects"]["project3"]["id"], api='rest')
            project.signup("newmail@mail.com", "testmail2")
            # do not log in the user
            self.assertIsNone(project._user)
            project.login("newmail@mail.com", "testmail2")
            u_id = project._user["id"]
            self.assertIsNotNone(project._user)
            project._api.request("deleteUser", {"userId": u_id})
            project.logout()
            self.assertIsNone(project._user)

        def test_alreadyExistingSignup(self):
            project = skygrid.Project(config["projects"]["project3"]["id"], api='rest')
            usr1 = config["projects"]["project3"]["users"][0]
            project.signup(usr1["email"], usr1["password"])

        def test_doubleSignup(self):
            project = skygrid.Project(config["projects"]["project3"]["id"], api='rest')
            project.signup("newmail@mail.com", "testmail2")
            project.signup("newmail@mail.com", "testmail2")
            project.login("newmail@mail.com", "testmail2")

    # TODO: this isn't even implemented, so need to implement first
    class TestLoginMaster(unittest.TestCase):
        def test_broken(self):
            self.assertTrue(False)

        def test_logout(self):
            self.fail()

        def test_login_incorrect(self):
            self.fail()

    class TestFetchUser(unittest.TestCase):
        def test_fetch_existing(self):
            project = skygrid.Project(config["projects"]["project1"]["id"], api='rest')
            user1 = config["projects"]["project1"]["users"][0]
            new_user = project.user(user1["id"])
            # self.assertEqual(new_user._data["email"], user1["email"])
            self.assertEqual(new_user._data["id"], user1["id"])

        def test_fetch_nonexist(self):
            project = skygrid.Project(config["projects"]["project1"]["id"], api='rest')
            new_user = project.user("nonexisty")
            self.assertIsNone(new_user)

        def test_fetch_no_users(self):
            project = skygrid.Project(config["projects"]["project4"]["id"], api='rest')
            new_user = project.user("nonexisty")
            self.assertIsNone(new_user)

    # TODO: not 100% in knowing how the query strings work
    class TestFindUsers(unittest.TestCase):
        def test_broken(self):
            self.assertTrue(False)

    # TODO: finish
    class TestDeleteUser(unittest.TestCase):
        def test_create_delete(self):
            self.assertTrue(False)

        def test_delete_non_existent(self):
            self.assertTrue(False)


# TODO: not 100% how the queries work
class TestFindDevSchemas(unittest.TestCase):
    def test_broken(self):
        self.assertTrue(False)


class TestAddDevSchema(unittest.TestCase):
    def test_add_new(self):
        self.assertTrue(False)

    def test_add_existing(self):
        self.assertTrue(False)


class TestFetchDevSchema(unittest.TestCase):
    def test_fetch_existing(self):
        self.assertTrue(False)

    def test_fetch_nonexist(self):
        self.assertTrue(False)


class TestUpdateSchema(unittest.TestCase):
    def test_update_new(self):
        self.assertTrue(False)

    def test_update_existing_delete(self):
        self.assertTrue(False)

if testMasterFns:
    class TestDelSchema(unittest.TestCase):
        def test_del_schema_p1(self):
            self.assertTrue(False)

        def test_del_schema_nonexist(self):
            self.assertTrue(False)


# TODO: find out query strings for find devices
class TestFindDevices(unittest.TestCase):
    def test_broken(self):
        self.assertTrue(False)


class TestAddDevice(unittest.TestCase):
    def test_add_dev_schema1(self):
        self.assertTrue(False)

    def test_add_dev_nonexist_schema(self):
        self.assertTrue(False)


class TestUpdateDevice(unittest.TestCase):
    def test_update_existing(self):
        self.assertTrue(False)

    def test_update_nonexist(self):
        self.assertTrue(False)


class TestDeleteDevice(unittest.TestCase):
    def test_add_del(self):
        self.assertTrue(False)

    def test_del_nonexist(self):
        self.assertTrue(False)


class TestFetchHistory(unittest.TestCase):
    def test_get_history_valid(self):
        self.assertTrue(False)

    def test_fetch_history_logging_off(self):
        self.assertTrue(False)

    def test_fetch_history_nonexist_device(self):
        self.assertTrue(False)


if __name__ == "__main__":
    load_config("testconfig.json")
    unittest.main()
