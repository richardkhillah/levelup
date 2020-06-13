from flask import render_template, session, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask import current_app, abort

from . import township
from .forms import NewTownForm, EditTownForm
from .. import db
from ..models.models import User
from ..decorators import admin_required

from ..models.township import Source, Item, Town

@township.route('/home')
@admin_required
def landing():
    if not current_user.town:
        # TODO: possibly redirect to register-town page
        abort(404)
    # TODO: encapsulate this in Town with some method, refactor landing.html
    next_level = current_user.town.level + 1
    sources = Source.query.filter_by(required_level=next_level).all()
    items = Item.query.filter_by(required_level=next_level).all()
    unlock = {
        'level': next_level,
        'sources': sources,
        'items': items,
    }

    return render_template('township/landing.html', user=current_user,
        town=current_user.town, unlock=unlock)

@township.route('/source/<source_name>')
@admin_required
def source(source_name):
    source = Source.query.filter_by(name=source_name).first()
    return render_template('township/source.html', source=source)



@township.route('/item/<item_name>')
@admin_required
def item(item_name):
    item = {}
    return render_template('township/item.html', item=item)




@township.route('/source/<source_name>/popup')
@admin_required
def source_popup(source_name):
    source = Source.query.filter_by(name=source_name).first_or_404()
    return render_template('township/source_popup.html',
                user=current_user, name=source_name, source=source)

@township.route('/item/<item_name>/popup')
@admin_required
def item_popup(item_name):
    return render_template('township/item_popup.html',
                user=current_user, name=item_name)

@township.route('/register-town', methods=['GET', 'POST'])
@admin_required
def register_town():
    form = NewTownForm()
    if form.validate_on_submit():
        town = Town(name=form.town_name.data,
                    level=form.level.data,
                    population=form.population.data,
                    population_cap=form.population_cap.data,
                    coins=form.coins.data,
                    township_cash=form.township_cash.data)
        # TODO: assign a user_id to this town and update databse
        db.session.add(town)
        # db.session.commit()
        # current_user.town_id = town.id

        flash('Form Submitted')
        return redirect(url_for('.landing'))
    return render_template('township/register_town.html', form=form)

@township.route('/edit-town/', methods=['GET', 'POST'])
@admin_required
def edit_town():
    town = Town.query.get_or_404(current_user.id)
    form = EditTownForm()
    if form.validate_on_submit():
        town.name = form.town_name.data
        town.level = form.level.data
        town.population = form.population.data
        town.population_cap = form.population_cap.data
        town.coins = form.coins.data
        town.township_cash = form.township_cash.data
        db.session.add(town)
        flash("Success! Your town has been updated.")
        return redirect(url_for('.landing'))
    form.town_name.data = town.name
    form.level.data = town.level
    form.population.data = town.population
    form.population_cap.data = town.population_cap
    form.coins.data = town.coins
    form.township_cash.data = town.township_cash
    return render_template('township/edit_town.html', form=form)
