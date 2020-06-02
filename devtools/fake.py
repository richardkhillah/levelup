import os

# envrionment variables
BASE_DIR=os.path.abspath(os.path.dirname(__file__))
SAVE_DIR='fakedata'
FILE_TYPE='JSON'
FILE_EXT='.json'
PRIMARY_FILENAME='fake-users'

# configuration file
class Config:
    basedir = BASE_DIR
    savedir = SAVE_DIR
    primary_filename=PRIMARY_FILENAME
    file_type=FILE_TYPE
    file_ext=FILE_EXT

    @property
    def path(self):
        filename = self.primary_filename + self.file_ext
        return '/'.join([self.basedir, self.savedir, filename])
    @path.setter
    def path(self):
        raise AttributeError('path is a computed property')

# https://faker.readthedocs.io/en/stable/locales/en_US.html#faker-providers-misc
from faker import Faker
fake = Faker()
config = Config()

import json

def create_users(num_users=5):
    """Create fake users and save them to disk."""
    users = []
    for i in range(num_users):
        location = fake.city() + ', ' + fake.state_abbr()
        users.append(
            {
                'username': fake.user_name(),
                'email': fake.email(),
                'password': 'password',
                'confirmed': True,
                'name': fake.name(),
                'location': location,
                'about_me': fake.paragraph()
            })

    with open(config.path, 'w') as f:
        json.dump(users, f, indent=2)

def destroy_users():
    """Remove users in user dict from db then destroy user dict."""
    remove_users()

    import os
    os.remove(config.path)

def load_users():
    """Load users from fake-users.json into the registered app-level database."""
    data = None

    if not os.path.exists(config.path):
        raise FileNotFoundError('Error: file {} not found'\
                .format(config.path))
    with open(config.path, 'r') as f:
        try:
            data = json.load(f)
        except Exception as e:
            raise e

    from app import db
    from app.models.models import User

    users = User.query.all()
    user_emails = [u.email for u in users] or []
    for d in data:
        if d['email'] in user_emails:
            continue
        u = User(username=d['username'], email=d["email"],
                password=d["password"], confirmed=d["confirmed"],
                name=d["name"], location=d["location"], about_me=d["about_me"])
        db.session.add(u)
    db.session.commit()

def remove_users():
    """Remove from db users created using create_users."""
    f = open(config.path, 'r')
    users = json.load(f)
    f.close()

    user_emails = []
    if users:
        user_emails = [u["email"] for u in users]

    from app import db
    from app.models.models import User
    for u in User.query.all():
        if u.email in user_emails:
            db.session.delete(u)
    db.session.commit()

# module help
def usage():
    print('Usage: flask dev COMMAND...')
    print('')
    print('A general utility script for generating fake users.')
    print('')
    print('Commands:')
    print('  create_users   ' + create_users.__doc__)
    print('  destroy_users  ' + destroy_users.__doc__)
    print('  load_users     ' + load_users.__doc__)
    print('  remove_users   ' + remove_users.__doc__)
    print('  help           ' + help.__doc__)

def help():
    """Print this message"""
    return usage()

fake_dict = dict(
    create_users=create_users,
    destroy_users=destroy_users,
    load_users=load_users,
    remove_users=remove_users,
    help=usage,
)

def run(commands):
    for c in commands:
        try:
            fake_dict[c]()
        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print(e)
            usage()
            print("Error: No such command '{}'".format(c))
