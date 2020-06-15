import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

import sys
import click
from app import create_app, db
from flask_migrate import Migrate

app = create_app('development')
migrate = Migrate(app, db)

from app.models.models import User, Follow, Role, Permission, Post, Comment

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Follow=Follow, Role=Role,
                Permission=Permission, Post=Post, Comment=Comment)

from app.models.township import tm_dict
@app.shell_context_processor
def inject_sources():
    return tm_dict

@app.cli.command()
@click.option('--coverage/--no-coverage', default=False,
              help='Run tests under code coverage.')
@click.argument('test_names', nargs=-1)
def test(coverage, test_names):
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(sys.argv))

    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade
    from app.models.models import Role, User

    # migrate db to latest revision
    upgrade()

    # create user roles
    Role.insert_roles()

    # create self-follows for all users
    User.add_self_follows()

devtools_path = os.path.join(os.path.dirname(__file__), 'devtools')
if os.path.exists(devtools_path):
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
        from devtools import load_township_assets
        if not commands:
            click.echo('Usage: flask dev COMMAND...')
            click.echo("Try 'flask dev help' for help.")
            click.echo('')
        else:
            # fake.run(commands)
            load_township_assets.run(commands)
