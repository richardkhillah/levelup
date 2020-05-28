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


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

from app.models.models import Role, User

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

#
# comment this out if you fork this repo
# 
@app.cli.command()
@click.argument('commands', nargs=-1)
def load(commands):
    # https://click.palletsprojects.com/en/7.x/arguments/
    from devtools.load_users import load_dict

    def usage():
        click.echo('Usage: flask load-users COMMAND...')
        click.echo("Try 'flask load-users help' for help.")
        click.echo('')

    if commands:
        for c in commands:
            try:
                load_dict[c]()
            except:
                usage()
                click.echo("Error: No such command '{}'".format(c))
    else:
        usage()
