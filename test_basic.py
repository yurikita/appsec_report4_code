import os
import unittest
from config import basedir
from app import app
from models import User
from flask_login import current_user
from flask import url_for

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.client = app.test_client()
        self.assertEqual(app.debug, False)
        
    def tearDown(self):
        pass

    #Tests
    def register(self, uname, pword, mfa):
        return self.client.post('/register', data = dict(uname = uname, pword = pword, mfa = mfa), follow_redirects = True) 

    def login(self, uname, pword, mfa):
        return self.client.post('/login', data = dict(uname=uname, pword=pword, mfa=mfa), follow_redirects=True)

    def logout(self):
        return self.client.post('/logout', follow_redirects=True)

    def spell_check(self, test_file):
        with open(test_file, "r") as f:
            inputtext = f.read()
            f.close()
        return self.client.post('/spell_check', data = dict(inputtext=inputtext))

    def test_register(self):
        with self.client:
            response = self.register('test2@nyu.edu', 'password', '000000000')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"id=\'success\'>\n\t\tsuccess<br>", response.data)
    
    def test_password_failure_login(self):
        with self.client:
            self.register('test@nyu.edu', 'password', '000000000')
            response = self.login('test@nyu.edu', 'password0', '00000000')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"id=\'result\'>\n\t\tIncorrect<br>", response.data)

    def test_2fa_failure_login(self):
        with self.client:
            self.register('test@nyu.edu', 'password', '000000000')
            response = self.login('test@nyu.edu', 'password', '12345')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"id=\'result\'>\n\t\tTwo-factor failure", response.data)

    def test_login(self):
        with self.client:
            self.register('test@nyu.edu', 'password', '000000000')
            response = self.login('test@nyu.edu', 'password', '000000000')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"id=\'result\'>\n\t\tSuccess<br>", response.data)

    def test_logout(self):
        with self.client:
            response = self.logout()
            self.assertEqual(response.status_code, 200)

    def test_register_twice(self):
        with self.client:
            response = self.register('test2@nyu.edu', 'password', '000000000')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"id=\'success\'>\n\t\tfailure<br>", response.data)

    def test_spell_1(self):
        with self.client:
            self.register('test@nyu.edu', 'password', '000000000')
            self.login('test@nyu.edu', 'password', '000000000')
            response = self.spell_check('tests/test1.txt')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"id=\'textout\'>\n\t\tTake a sad sogn and make it better. Remember to let her under your skyn, then you begin to make it betta.\n", response.data)
            self.assertIn(b"id=\'misspelled\'>\n\t\tsogn, skyn, betta", response.data)

    def test_spell_unauthorized(self):
        with self.client:
            response = self.spell_check('tests/test1.txt')
            self.assertNotEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
