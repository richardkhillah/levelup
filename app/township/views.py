from flask import render_template, session, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask import current_app, abort

from . import township
from .forms import NewTownForm, EditTownForm
from .. import db
from ..models.models import User
from ..decorators import admin_required

from ..models.township import Source, Item, Town, Unlock

@township.route('/home')
@login_required
def landing():
    if not current_user.town:
        # TODO: possibly redirect to register-town page
        abort(404)
    # TODO: encapsulate this in Town with some method, refactor landing.html
    unlock = Unlock()
    unlock.level = current_user.town.level + 1
    unlock.sources = Source.query.filter_by(required_level=unlock.level).all()
    unlock.items = Item.query.filter_by(required_level=unlock.level).all()

    return render_template('township/landing.html',
                            user=current_user._get_current_object(),
                            town=current_user.town, unlock=unlock)

@township.route('/source/<source_name>')
@login_required
def source(source_name):
    source = Source.query.filter_by(name=source_name).first()
    return render_template('township/source.html', source=source)



@township.route('/item/<item_name>')
@login_required
def item(item_name):
    item = Item.query.filter_by(name=item_name).first()
    ingredients = [
        {
            # popover on names to get quick stats on them
            'name': 'ingredient 1 name',
            'quantity': '1',
            # other info as wanted.
        },
        {
            # popover on names to get quick stats on them
            'name': 'ingredient 2 name',
            'quantity': '2',
            # other info as wanted.
        },
        {
            # popover on names to get quick stats on them
            'name': 'ingredient 3 name',
            'quantity': '3',
            # other info as wanted.
        },

    ]
    return render_template('township/item.html', item=item,
        ingredients=ingredients)




@township.route('/source/<source_name>/popup')
@login_required
def source_popup(source_name):
    source = Source.query.filter_by(name=source_name).first_or_404()
    return render_template('township/source_popup.html',
                user=current_user._get_current_object(),
                name=source_name, source=source)

@township.route('/item/<item_name>/popup')
@login_required
def item_popup(item_name):
    return render_template('township/item_popup.html',
                user=current_user, name=item_name)

@township.route('/register-town', methods=['GET', 'POST'])
@login_required
def register_town():
    # if user has town already, redirect to .landing
    if current_user.town is not None:
        return redirect(url_for('.landing'))

    form = NewTownForm()
    if form.validate_on_submit():
        town = Town(name=form.town_name.data,
                    level=form.level.data,
                    population=form.population.data,
                    population_cap=form.population_cap.data,
                    coins=form.coins.data,
                    township_cash=form.township_cash.data)
        town.owner = current_user
        db.session.add(town)

        flash('Form Submitted')
        return redirect(url_for('.landing'))
    return render_template('township/register_town.html', form=form)

@township.route('/edit-town/', methods=['GET', 'POST'])
@login_required
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
