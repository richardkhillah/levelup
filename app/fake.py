from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models.models import User
from .models.blog import Post
from .models.township import source, item, Source, Farming, Imported

fake = Faker()
i = 0

def user():
    u = User(email=fake.email(),
             username=fake.user_name(),
             password='password',
             confirmed=True,
             name=fake.name(),
             location=fake.city(),
             about_me=fake.text(),
             member_since=fake.past_date())
    return u

def item():
    source_count = Source.query.count()
    i = Imported(name=fake.name(),
                required_level=randint(0, 100),
                time_to_make="faketime",
                source_id=randint(0, source_count-1))
    return i

def source():
    s = Farming(name=fake.name(),
                required_level=randint(0, 100),
                time_to_make="faketime",
                total_quantity=1,
                required_population=randint(0, 23000),
                purchase_cost=randint(0, 800000))
    return s


def users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='password',
                 confirmed=True,
                 name=fake.name(),
                 location=fake.city(),
                 about_me=fake.text(),
                 member_since=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def posts(count=100):
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(body=fake.text(),
                 timestamp=fake.past_date(),
                 author=u)
        db.session.add(p)
    db.session.commit()
