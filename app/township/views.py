from flask import render_template, session, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask import current_app, abort

from . import township
from .. import db
from ..models.models import User
from ..decorators import admin_required

from ..models.township import Source, Item

@township.route('/landing')
@admin_required
def landing():
    user = User.query.get(1)
    town = {
        'name': "Windsor",
        'level': 86,
        'population': 17845,
        'population_cap': 17845,
        'coin': 830635,
        'cash': 1490
    }
    next_level = town['level'] + 1
    sources = Source.query.filter_by(required_level=next_level).all()
    items = Item.query.filter_by(required_level=next_level).all()

    unlock = {
        'level': next_level,
        'sources': sources,
        'items': items,
        # 'items': [
        #     {
        #         'name': "Tea Bags",
        #         'source_name': 'Paper Factory',
        #         'prodcution_time': "9m45s",
        #     },
        #     {
        #         'name': "Chocolate Bar",
        #         'source_name': 'Candy Factory',
        #         'prodcution_time': "3h30m",
        #     },
        #     {
        #         'name': "Tea Pot",
        #         'source_name': 'Kitchenware Factory',
        #         'prodcution_time': "2h15m",
        #     },
        # ],
    }
    return render_template('township/landing.html', user=user,
        town=town, unlock=unlock)

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
