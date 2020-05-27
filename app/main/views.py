from flask import render_template, session, redirect, url_for, flash, current_app
from datetime import datetime

from . import main
from .forms import NameForm
from .. import db
from ..models.models import User
from ..email import send_email

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
