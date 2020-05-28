import unittest
import time
from app import create_app, db
from app.models.models import User, AnonymousUser, Role, Permission

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_valid_confirmation_token(self):
        pass

    def test_invalid_confirmation_token(self):
        pass

    def test_expired_confirmation_token(self):
        pass

    def test_valid_reset_token(self):
        pass

    def test_invalid_reset_token(self):
        pass

    def test_valid_email_change_token(self):
        pass

    def test_invalid_email_change_token(self):
        pass

    def test_duplicate_email_change_token(self):
        pass

    def test_user_roles(self):
        pass

    def test_moderator_role(self):
        pass

    def test_administrator_role(self):
        pass

    def test_roles_and_permissions(self):
        Role.insert_roles()
        u = User(email='john@example.com', password='cat')
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))
