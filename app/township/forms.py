from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextField, SelectField,
                    BooleanField, IntegerField)
from wtforms.validators import DataRequired, Length, Email, Regexp, NumberRange

class NewTownForm(FlaskForm):
    town_name = StringField('Town Name', \
        validators=[DataRequired(), Length(1, 64)])
    level = IntegerField('Level', \
        validators=[DataRequired(), NumberRange(min=1)])
    population = IntegerField('Population', \
        validators=[DataRequired(), NumberRange(1, 22775)])
    population_cap = IntegerField('Population Cap', \
        validators=[DataRequired(), NumberRange(1, 22775)])
    coins = IntegerField('Coins', \
        validators=[DataRequired(), NumberRange(min=0)])
    township_cash = IntegerField('Township Cash', \
        validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')

class EditTownForm(FlaskForm):
    town_name = StringField('Town Name', \
        validators=[DataRequired(), Length(1, 64)])
    level = IntegerField('Level', \
        validators=[DataRequired(), NumberRange(min=1)])
    population = IntegerField('Population', \
        validators=[DataRequired(), NumberRange(1, 22775)])
    population_cap = IntegerField('Population Cap', \
        validators=[DataRequired(), NumberRange(1, 22775)])
    coins = IntegerField('Coins', \
        validators=[DataRequired(), NumberRange(min=0)])
    township_cash = IntegerField('Township Cash', \
        validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')
