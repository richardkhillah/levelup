from flask import render_template, session, redirect, url_for, flash
from flask_login import login_required, current_user
from flask import current_app, abort
from .forms import EditProfileForm

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

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data =  current_user.name
    form.location.data =  current_user.location
    form.about_me.data =  current_user.about_me
    return render_template('edit_profile.html', form=form)
