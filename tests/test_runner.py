import unittest

# import the library to test
import sys
sys.path.insert(0, '../')
import skygrid

# used for testing credentials
config = None
# if provided, run the master key tests
master_key = None
with open("../../master_key.txt", 'r') as mk:
    master_key = mk.readline().strip()


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
        except skygrid.SkygridException:
            return
        self.fail("Initialised invalid project")


class TestLogoff(unittest.TestCase):
    def test_logoffProj1User1(self):
        project = skygrid.Project(config["projects"]["project1"]["id"], api='rest')
        usr1 = config["projects"]["project1"]["users"][0]
        project.login(usr1["email"], usr1["password"])
        project.logout()
        self.assertIsNone(project._user)
        self.assertIsNone(project._api._token)

    def test_logoffProj1User2(self):
        project = skygrid.Project(config["projects"]["project1"]["id"], api='rest')
        usr1 = config["projects"]["project1"]["users"][1]
        project.login(usr1["email"], usr1["password"])
        project.logout()
        self.assertIsNone(project._user)
        self.assertIsNone(project._api._token)

    def test_logoffProj2User1(self):
        project = skygrid.Project(config["projects"]["project2"]["id"], api='rest')
        usr1 = config["projects"]["project2"]["users"][0]
        project.login(usr1["email"], usr1["password"])
        project.logout()
        self.assertIsNone(project._user)
        self.assertIsNone(project._api._token)

    def test_logoffP1_notloggedin(self):
        # should not throw any exceptions - logout
        project = skygrid.Project(config["projects"]["project1"]["id"], api='rest')
        self.assertIsNone(project._user)
        self.assertIsNone(project._api._token)
        project.logout()
        self.assertIsNone(project._user)
        self.assertIsNone(project._api._token)


class TestSignup(unittest.TestCase):
    """
    *Priv functions are the same as other functions, just logged into a non-master account
    """
    def test_newSignup(self):
        if master_key is not None:
            project = skygrid.Project(config["projects"]["project3"]["id"], api='rest')
            project.login_master(master_key)
            project.signup("newmail@mail.com", "testmail2")
            # do not log in the user
            self.assertIsNone(project._user)
            project.login("newmail@mail.com", "testmail2")
            u_id = project._user["id"]
            self.assertIsNotNone(project._user)
            project._api.request("deleteUser", {"userId": u_id})
            project.logout()
            self.assertIsNone(project._user)
        # also test without master key, no login
        project = skygrid.Project(config["projects"]["project3"]["id"], api='rest')
        try:
            project.signup("newmail2@mail.com", "testmail2")
        except skygrid.AuthenticationError:
            return
        self.fail("signup should have failed without master key")

    def test_newSignupPriv(self):
        # same as prev test, but logging in with non-master
        project = skygrid.Project(config["projects"]["project3"]["id"], api='rest')
        user1 = config["projects"]["project3"]["users"][0]
        project.login(user1["email"], user1["password"])
        try:
            project.signup("newmail2@mail.com", "testmail2")
        except skygrid.AuthenticationError:
            return
        self.fail("signup should have failed without master key")

    def test_alreadyExistingSignup(self):
        usr1 = config["projects"]["project3"]["users"][0]

        if master_key is not None:
            project = skygrid.Project(config["projects"]["project3"]["id"], api='rest')
            project.login_master(master_key)
            flipped = False
            try:
                project.signup(usr1["email"], usr1["password"])
            except skygrid.SkygridException:
                flipped = True
            self.assertTrue(flipped, "Already Existing signup did not fail with master key")

        project = skygrid.Project(config["projects"]["project3"]["id"], api='rest')
        try:
            project.signup(usr1["email"], usr1["password"])
        except skygrid.AuthenticationError:
            return
        self.fail("signup should have failed without master key")

    def test_alreadyExistingSignupPriv(self):
        project = skygrid.Project(config["projects"]["project3"]["id"], api='rest')
        user1 = config["projects"]["project3"]["users"][0]
        project.login(user1["email"], user1["password"])
        try:
            project.signup(user1["email"], user1["password"])
        except skygrid.AuthenticationError:
            return
        self.fail("signup should have failed without master key")

    def test_signup_retval(self):
        self.fail("implement me")

    def test_signup_retval_priv(self):
        self.fail("implement me")


class TestLoginMaster(unittest.TestCase):
    def test_login(self):
        if master_key:
            project = skygrid.Project(config["projects"]["project3"]["id"], api='rest')
            project.login_master(master_key)
            self.assertEqual(project._master_key, master_key)

            # try and access something that a master key can only do
            x = project.users()
            self.assertIsNotNone(x)

    def test_logout(self):
        # TODO: haven't quite decided if we should delete master key on logout
        self.fail()

    def test_login_incorrect(self):
        if master_key:
            project = skygrid.Project(config["projects"]["project3"]["id"], api='rest')
            project.login_master("falsum")

            try:
                project.users()
            except skygrid.AuthenticationError:
                return

            self.fail("Access without a master key did not fail when querying all users")


class TestFetchUser(unittest.TestCase):
    def test_fetch_existing(self):
        if master_key is not None:
            project = skygrid.Project(config["projects"]["project3"]["id"], api='rest')
            project.login_master(master_key)
            user1 = config["projects"]["project3"]["users"][0]
            new_user = project.user(user1["id"])
            self.assertEqual(new_user._data["email"], user1["email"])
            self.assertEqual(new_user._data["id"], user1["id"])

        user1 = config["projects"]["project1"]["users"][0]
        project = skygrid.Project(config["projects"]["project1"]["id"], api='rest')
        try:
            project.user(user1["id"])
        except skygrid.AuthenticationError:
            return
        self.fail("fetching user without masterkey did not throw an error")

    def test_fetch_existing_priv(self):
        # test fetching some other user's login
        # do not test fetching own, as we don't care about auth issues with that
        user1 = config["projects"]["project1"]["users"][0]
        user2 = config["projects"]["project1"]["users"][1]
        project = skygrid.Project(config["projects"]["project1"]["id"], api='rest')
        project.login(user2["email"], user2["password"])

        try:
            project.user(user1["id"])
        except skygrid.AuthenticationError:
            return
        self.fail("fetching user without masterkey did not throw an error")

    def test_fetch_nonexist(self):
        if master_key is not None:

            project = skygrid.Project(config["projects"]["project3"]["id"], api='rest')
            project.login_master(master_key)
            failtest = False
            try:
                project.user("nonexisty")
            except skygrid.SkygridException:
                failtest = True

            if not failtest:
                self.fail("Requesting invalid user did not throw exception")

        project = skygrid.Project(config["projects"]["project1"]["id"], api='rest')
        try:
            project.user("nonexisty")
        except skygrid.AuthenticationError:
            return
        self.fail("fetching non-existent does not throw exception")

    def test_fetch_nonexist_priv(self):
        project = skygrid.Project(config["projects"]["project1"]["id"], api='rest')
        user1 = config["projects"]["project1"]["users"][0]
        project.login(user1["email"], user1["password"])
        try:
            project.user("nonexisty")
        except skygrid.AuthenticationError:
            return
        self.fail("fetching non-existent does not throw exception")


# TODO: not 100% in knowing how the query strings work, also requires master token
class TestFindUsers(unittest.TestCase):

    def test_query_all(self):

        # fetch all,

        # assert the number is correct, and id's match

        self.fail()

    def test_broken(self):
        self.assertTrue(False)


class TestDeleteUser(unittest.TestCase):
    def test_create_delete(self):

        if master_key:
            # create a user, and make sure we can delete it
            project = skygrid.Project(config["projects"]["project3"]["id"])
            project.login_master(master_key)

            x = project.signup("uniqueuser1989@mail.com", "vespuccibeach3")
            self.assertIsNotNone(x)
            x.delete()

            with self.assertRaises(skygrid.SkygridException):
                x.fetch()

        # for these un-authed ones, try and delete pre-existing ones
        project = skygrid.Project(config["projects"]["project3"]["id"])
        with self.assertRaises(skygrid.AuthenticationError):
            x = skygrid.User(project._api, "cUpz2tNR")
            x.delete()

        project = skygrid.Project(config["projects"]["project3"]["id"])
        user = config["projects"]["project3"]["users"][0]
        project.login(user["email"], user["password"])
        with self.assertRaises(skygrid.AuthenticationError):
            x = skygrid.User(project._api, "cUpz2tNR")
            x.delete()

    def test_delete_non_existent(self):
        if master_key:
            # delete an invalid id user
            project = skygrid.Project(config["projects"]["project3"]["id"])
            project.login_master(master_key)

            x = skygrid.User(project._api, "hello")

            with self.assertRaises(skygrid.SkygridException):
                x.delete()

        project = skygrid.Project(config["projects"]["project3"]["id"])
        x = skygrid.User(project._api, "hello")

        with self.assertRaises(skygrid.SkygridException):
            x.delete()

        project = skygrid.Project(config["projects"]["project3"]["id"])
        user1 = config["projects"]["project3"]["users"][0]
        project.login(user1["email"], user1["password"])
        x = skygrid.User(project._api, "hello")

        with self.assertRaises(skygrid.SkygridException):
            x.delete()

    def test_create_login_delete(self):
        if master_key:
            project = skygrid.Project(config["projects"]["project3"]["id"])
            project.login_master(master_key)

            x = project.signup("inituser@mail.com", "mailhouse")
            project.login("inituser@mail.com", "mailhouse")
            x.delete()

            with self.assertRaises(skygrid.SkygridException):
                x.fetch()


# TODO: not 100% how the queries work
class TestFindDevSchemas(unittest.TestCase):
    def test_broken(self):
        self.assertTrue(False)


# TODO: add dev schema, requires master_token
class TestAddDevSchema(unittest.TestCase):
    def test_add_new(self):
        self.assertTrue(False)

    def test_add_existing(self):
        self.assertTrue(False)


class TestFetchDevSchema(unittest.TestCase):
    def test_fetch_existing(self):
        project = skygrid.Project(config["projects"]["project1"]["id"], api='rest')
        sc = project.schema("hyUWjvpZ")
        self.assertIsNotNone(sc)
        self.assertIsNotNone(sc._data)
        s_conf = config["projects"]["project1"]["schemas"][0]
        self.assertEqual(sc.name, s_conf["name"])
        self.assertEqual(sc.id, s_conf["id"])
        self.assertEqual(len(s_conf["fields"]), len(sc._data["properties"].keys()))
        for pname in sc._data['properties']:
            self.assertIn(pname, s_conf["fields"])
            self.assertEqual(s_conf[pname], sc._data['properties'][pname]['type'])
            self.assertIn('default', sc._data['properties'][pname])

    def test_fetch_logged_in(self):
        project = skygrid.Project(config["projects"]["project1"]["id"], api='rest')
        user1 = config["projects"]["project1"]["users"][0]
        project.login(user1["email"], user1["password"])
        sc = project.schema("hyUWjvpZ")
        self.assertIsNotNone(sc)
        self.assertIsNotNone(sc._data)
        s_conf = config["projects"]["project1"]["schemas"][0]
        self.assertEqual(sc.name, s_conf["name"])
        self.assertEqual(sc.id, s_conf["id"])
        self.assertEqual(len(s_conf["fields"]), len(sc._data["properties"].keys()))
        for pname in sc._data['properties']:
            self.assertIn(pname, s_conf["fields"])
            self.assertEqual(s_conf[pname], sc._data['properties'][pname]['type'])
            self.assertIn('default', sc._data['properties'][pname])

    def test_fetch_nonexist(self):
        project = skygrid.Project(config["projects"]["project1"]["id"], api='rest')
        try:
            project.schema("missingschema")
        except skygrid.SkygridException:
            return
        self.fail("schema should have thrown exception")


# TODO: update schema, also requires master token
class TestUpdateSchema(unittest.TestCase):
    def test_update_new(self):

        self.assertTrue(False)

    def test_update_existing_delete(self):
        self.assertTrue(False)


# TODO: test del schema, also requires master token
class TestDelSchema(unittest.TestCase):
    def test_del_schema_p1(self):
        self.assertTrue(False)

    def test_del_schema_nonexist(self):
        self.assertTrue(False)


# TODO: find out query strings for find devices
class TestFindDevices(unittest.TestCase):
    def test_broken(self):
        self.assertTrue(False)


class TestRawDeviceCreate(unittest.TestCase):
    def test_device_fetch_correct_id(self):
        proc = config["projects"]["project1"]
        project = skygrid.Project(proc["id"])
        doc = proc["devices"][0]
        s_id = doc["schema"]
        dev = skygrid.Device(project._api, doc["id"]).fetch()
        schema = None
        for x in proc["schemas"]:
            if x["id"] == s_id:
                schema = x
                break
        self.assertIsNotNone(schema, "test broken, please ignore")
        self.assertEqual(len(dev.properties()), len(schema["fields"]))
        self.assertIsNotNone(dev)

    def test_device_invalid_id(self):

        proc = config["projects"]["project1"]
        project = skygrid.Project(proc["id"])

        dev = skygrid.Device(project._api, "inwalid")

        with self.assertRaises(skygrid.SkygridException):
            dev.fetch()

    def test_device_invalid_proj(self):
        project = skygrid.Project("invalid project")
        dev = skygrid.Device(project._api, "invalid")

        with self.assertRaises(skygrid.SkygridException):
            dev.fetch()

    def test_device_object_emplace(self):

        proc = config["projects"]["project1"]
        project = skygrid.Project(proc["id"])
        # TODO: this doesn't change, nor throw an exception
        # perhaps this is simply because there is nothing queued to push
        # oh fuck this is because when we send data to skygrid, it doesn't consider the ones
        # passed in - this can be real confusing, however this complicates constructing from data
        # if we don't allow passing in values like this.
        self.fail("device constructor broken - refer to this test")
        dev = skygrid.Device(project._api, {'id': proc["devices"][0]["id"], \
                                            'properties': {"PropertyA": "Hi", "PropertyB": 100}})
        dev.save()

        # self.fail("unimplemented")

    def test_device_object_emplace_incorrect_schema(self):
        # refer to previous test why this is unimplemented
        self.fail("unimplemented")

class TestDeviceFunctions(unittest.TestCase):
    def test_constructor1(self):
        # construct with id

        # fetch

        # assert contained data is correct
        self.fail("unimplemented")

    def test_constructor2(self):
        # construct with object

        # save/fetch

        # assert contained data is correct
        self.fail("unimplemented")

    def test_id(self):

        # construct with id, fetch

        # assert that the id is intact

        self.fail("unimplemented")

    def test_completeness(self):

        # construct with id, don't fetch,

        # assert not complete

        # fetch

        # assert complete

        self.fail("unimplemented")

    def test_dirty(self):

        # construct with id, fetch

        # assert not dirty

        # make a change

        # assert dirty

        # discard changes

        # assert not dirty

        # make name change

        # assert dirty

        self.fail("unimplemented")

    def test_log(self):

        # check whether the log is on for a device with logging on

        # setting it off

        # check that log is on

        # discard the changes

        # set it off

        # save it

        # fetch

        # check log is off

        # set it back on and save

        # assert that it is on

        self.fail("unimplemented")

    def test_name(self):

        # initialise device by id

        # assert name is off

        # fetch

        # assert name is correct

        # set name to be the same name

        # save

        self.fail("unimplemented")

    def test_schema(self):
        self.fail("unimplemented")

    def test_properties(self):
        self.fail("unimplemented")

    def test_property_check(self):
        self.fail("unimplemented")

    def test_saving(self):
        self.fail("unimplemented")

    def test_fetch(self):
        #also test fetch_if_needed
        self.fail("unimplemented")

    def test_history(self):
        self.fail("unimplemented")

    def test_delete(self):
        self.fail("unimplemented")

    def test_discard_changes(self):
        self.fail("unimplemented")


# TODO: add device
class TestAddDevice(unittest.TestCase):
    def test_add_dev_schema1(self):
        probj, user, project = setup_project_valid()

        dev = project.add_device("My New Device V2", schema_id=probj["schemas"][0]["id"])
        self.assertIsNotNone(dev)
        self.assertEqual(dev['name'], "My New Device V2")

        # TODO: assert the fields match the schema

        dev.delete()

    def test_add_dev_nonexist_schema(self):
        self.fail("unimplemented")

    def test_add_dev_not_logged_in(self):
        self.fail("unimplemented")

    def test_add_dev_master_key(self):
        self.fail("unimplemented")


# TODO: update device
class TestUpdateDevice(unittest.TestCase):
    def test_update_existing(self):
        self.fail("unimplemented")
        # probj, user, project = setup_project_valid()
        #
        # dev = project.add_device("New device V3.14", schema_id=probj["schemas"][0]["id"])
        #
        # res = project.device(dev.id)
        # self.assertIsNotNone(res)
        #
        # # TODO set property test?
        # dev.set("prop", 123)
        # self.assertIsNotNone(dev.get("prop"))
        # self.assertEqual(dev.get("prop"), 123)
        #
        # self.save(["prop"])
        #
        # dev.set("prop", 321)

        # self.assertTrue(False)

    def test_update_nonexist(self):
        self.fail("unimplemented")
        # probj, user, project = setup_project_valid()
        #
        # dev = project.add_device("New device V3.14", schema_id=probj["schemas"][0]["id"])
        #
        # self.assertIsNotNone(project.devices())
        #
        # with self.assertRaises(skygrid.exception.SkygridException):
        #     dev.get('prop')
        #
        # with self.assertRaises(skygrid.exception.SkygridException):
        #     dev.fetch()



# TODO: perhaps this /should/ require a masterkey
class TestDeleteDevice(unittest.TestCase):
    def test_add_del(self):
        self.assertTrue(False)

    def test_del_nonexist(self):
        self.assertTrue(False)


# TODO: fetch hist
class TestFetchHistory(unittest.TestCase):
    def test_get_history_valid(self):



        self.assertTrue(False)

    def test_fetch_history_logging_off(self):
        self.assertTrue(False)

    def test_fetch_history_nonexist_device(self):
        self.assertTrue(False)


class TestServerTime(unittest.TestCase):
    def test_get_valid(self):
        from datetime import datetime
        # simply should test whether the return type is correct
        project = skygrid.Project(config["projects"]["project1"]["id"])
        res = project.get_time()
        self.assertIsNotNone(res)
        self.assertIsInstance(res, datetime)


def setup_project_valid(proj="project1"):
    probj = config["projects"][proj]
    user = probj["users"][0]
    project = skygrid.Project(probj["id"])
    project.login(user["email"], user["password"])
    return probj, user, project

if __name__ == "__main__":
    load_config("testconfig.json")
    unittest.main()
