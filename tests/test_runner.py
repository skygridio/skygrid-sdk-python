import unittest

#import the library to test
import sys
sys.path.insert(0, '../')
import skygrid

config = None

def loadConfig(filename):
	with open(filename) as cf:
		config = json.loads("".join(cf.readlines()))

class TestLogin(unittest.TestCase):
	def test_loginProj1User1(self):
		project = skygrid.Project('')
		self.assertTrue(False)

	def test_loginProj1User2(self):
		self.assertTrue(False)

	def test_loginProj2User1(self):
		self.assertTrue(False)

	def test_falseuser(self):
		self.assertTrue(False)

	def test_falseuserfalseproj(self):
		self.assertTrue(False)

class TestLogoff(unittest.TestCase):
	def test_logoffProj1User1(self):
		self.assertTrue(False)

	def test_logoffProj1User2(self):
		self.assertTrue(False)

	def test_logoffProj2User1(self):
		self.assertTrue(False)

	def test_logoffP1U1_notloggedin(self):
		self.assertTrue(False)

	def test_logoff_nonexistent(self):
		self.assertTrue(False)

class TestSignup(unittest.TestCase):
	def test_newSignup(self):
		self.assertTrue(False)

	def test_alreadyExistingSignup(self):
		self.assertTrue(False)

	def test_doubleSignup(self):
		self.assertTrue(False)

#TODO: this isn't even implemented, so need to implement first
class TestLoginMaster(unittest.TestCase):
	def test_broken(self):
		self.assertTrue(False)

class TestFetchUser(unittest.TestCase):
	def test_fetch_existing(self):
		self.assertTrue(False)

	def test_fetch_nonexist(self):
		self.assertTrue(False)		

#TODO: not 100% in knowing how the query strings work
class TestFindUsers(unittest.TestCase):
	def test_broken(self):
		self.assertTrue(False)

class TestDeleteUser(unittest.TestCase):
	def test_create_delete(self):
		self.assertTrue(False)

	def test_delete_non_existant(self):
		self.assertTrue(False)

#TODO: not 100% how the queries work
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

class TestDelSchema(unittest.TestCase):
	def test_del_schema_p1(self):
		self.assertTrue(False)

	def test_del_schema_nonexist(self):
		self.assertTrue(False)

#TODO: find out query strings for find devices
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
	unittest.main()