import os
import click
from app import create_app, db
from flask_migrate import Migrate

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app('development')
migrate = Migrate(app, db)

from app.models.models import Role, User, Permission, Post

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission, Post=Post)

from app.models.township import tm_dict
@app.shell_context_processor
def inject_sources():
    return tm_dict

@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command()
@click.argument('commands', nargs=-1)
def dev(commands):
    """Create & destroy dummy db objects"""
    # https://click.palletsprojects.com/en/7.x/arguments/
    from config import basedir
    path = basedir+'/devtools'
    if not os.path.exists(path):
        raise RuntimeError(f'{path} does not exist.')

    from devtools import fake
    if not commands:
        click.echo('Usage: flask dev COMMAND...')
        click.echo("Try 'flask dev help' for help.")
        click.echo('')
    else:
        fake.run(commands)
