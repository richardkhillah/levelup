from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField
from wtforms import SelectField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, NumberRange
from ..models.models import Role

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextField('About me')
    submit = SubmitField('Submit')

class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                            Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                        'Usernames must have only letters, '
                                        'numbers, dots or underscores')])
    role = SelectField('Role', coerce=int)
    confirmed = BooleanField('Confirmed')
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(r.id, r.name)
                        for r in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

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
