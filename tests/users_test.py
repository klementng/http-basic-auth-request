import unittest
import os
import importlib

os.environ["CONFIG_DIR"] = "./tests/data"
os.environ["SETTINGS_PATH"] = "./tests/data/settings.yml"
import server.users

class TestYAML(unittest.TestCase):

    def setUp(self) -> None:
        os.environ["CONFIG_DIR"] = "./tests/data"
        os.environ["SETTINGS_PATH"] = "./tests/data/settings.yml"
        os.environ["USERS_DB_PATH"] = "./tests/data/settings.yml"
        os.environ["USERS_DB_MODE"] = "YAML"

        importlib.reload(server.users)

        self.user = 'test1'
        self.pw = 'password'

        with open(os.environ["USERS_DB_PATH"],'rb') as f:
            self.data = f.read()
    
    def tearDown(self) -> None:
        with open(os.environ["USERS_DB_PATH"],'wb') as f:
            f.write(self.data)
    
    def test_add_user(self):
        server.users.add_user(self.user,self.pw)
        pw = server.users._get_password(self.user)
        self.assertNotEqual(pw,None)
    
    def test_verify_password(self):
        self.test_add_user()
        status = server.users.verify_password(self.user,self.pw)
        self.assertEqual(status,True)

    def test_delete_user(self):
        self.test_add_user()
        server.users.delete_user("test1")
        
        pw = server.users._get_password("test1")
        self.assertEqual(pw,None)

    def test_edit_user(self):
        self.test_add_user()
        
        server.users.edit_user(self.user,self.pw+"1")
        status = server.users.verify_password(self.user,self.pw+"1")
        self.assertEqual(status,True)


class TestDB(unittest.TestCase):

    def setUp(self) -> None:
        os.environ["CONFIG_DIR"] = "./tests/data"
        os.environ["SETTINGS_PATH"] = "./tests/data/settings.yml"
        os.environ["USERS_DB_PATH"] = "./tests/data/users.db"
        os.environ["USERS_DB_MODE"] = "SQLITE3"

        importlib.reload(server.users)

        self.user = 'test1'
        self.pw = 'password'

        with open(os.environ["USERS_DB_PATH"],'rb') as f:
            self.data = f.read()
    
    def tearDown(self) -> None:
        with open(os.environ["USERS_DB_PATH"],'wb') as f:
            f.write(self.data)
    
    def test_add_user(self):
        server.users.add_user(self.user,self.pw)
        pw = server.users._get_password(self.user)
        self.assertNotEqual(pw,None)
    
    def test_verify_password(self):
        self.test_add_user()
        status = server.users.verify_password(self.user,self.pw)
        self.assertEqual(status,True)

    def test_delete_user(self):
        self.test_add_user()
        server.users.delete_user("test1")
        
        pw = server.users._get_password("test1")
        self.assertEqual(pw,None)

    def test_edit_user(self):
        self.test_add_user()
        
        server.users.edit_user(self.user,self.pw+"1")
        status = server.users.verify_password(self.user,self.pw+"1")
        self.assertEqual(status,True)

if __name__ == "__main__":
    unittest.main()