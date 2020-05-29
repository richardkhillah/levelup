from flask import render_template, session, redirect, url_for, flash
from flask import current_app, abort

from datetime import datetime

from . import main
from .forms import NameForm
from .. import db
from ..models.models import User
from ..email import send_email

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)
