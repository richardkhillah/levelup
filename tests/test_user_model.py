import unittest
import time
from app import create_app, db
from app.models.models import User, AnonymousUser, Role, Permission

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

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
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        u1 = User(password='cat')
        u2 = User(password='dog')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))

    def test_valid_reset_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_password_token()
        self.assertTrue(User.reset_password(token, 'dog'))
        self.assertTrue(u.verify_password('dog'))
        self.assertFalse(u.verify_password('cat'))

    def test_invalid_reset_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_password_token()
        self.assertFalse(User.reset_password(token + 'a', 'dog'))
        self.assertTrue(u.verify_password('cat'))

    def test_valid_email_change_token(self):
        u = User(email='drew@example.com', password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_change_email_token('david@example.com')
        self.assertTrue(u.change_email(token))
        self.assertTrue(u.email == 'david@example.com')

    def test_invalid_email_change_token(self):
        u1 = User(email='drew@example.com', password='cat')
        u2 = User(email='susan@example.com', password='cat')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_change_email_token('john@gmail.com')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == 'susan@example.com')

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
