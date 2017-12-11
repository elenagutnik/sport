from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    SelectField, DateField, SelectMultipleField, IntegerField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, InputRequired
from wtforms import ValidationError
from ..models import Role, User
from .models import *
from .. import db

class EditDisciplineForm(FlaskForm):
    ru_name = StringField('Название дисциплины', validators=[Required()])
    en_name = StringField('Discipline title', validators=[Required()])
    fiscode = StringField('FIS code')
    submit = SubmitField('Submit')

class EditGenderForm(FlaskForm):
    ru_name = StringField('Название', validators=[Required()])
    en_name = StringField('Title', validators=[Required()])
    fiscode = StringField('FIS code')
    submit = SubmitField('Submit')

class EditTDRoleForm(FlaskForm):
    name = StringField('Title', validators=[Required()])
    submit = SubmitField('Submit')

class EditStatusForm(FlaskForm):
    name = StringField('Abbreviation', validators=[Required()])
    description = StringField('Description')
    submit = SubmitField('Submit')

class EditMarkForm(FlaskForm):
    name = StringField('Abbreviation', validators=[Required()])
    description = StringField('Description')
    submit = SubmitField('Submit')

class EditNationForm(FlaskForm):
    name = StringField('Abbreviation', validators=[Required()])
    ru_description = StringField('Russion Title')
    en_description = StringField('English Title')
    submit = SubmitField('Submit')

class EditCategoryForm(FlaskForm):
    name = StringField('Abbreviation', validators=[Required()])
    description = StringField('Description')
    level = StringField('Level (Integer 0-4)')
    submit = SubmitField('Submit')

class EditTDForm(FlaskForm):
    ru_firstname = StringField('Имя', validators=[Required()])
    en_firstname = StringField('First Name')
    ru_lastname = StringField('Фамилия', validators=[Required()])
    en_lastname = StringField('Last Name')
    ru_nation = StringField('Страна')
    en_nation = StringField('Nation')
    tdnumber = StringField('TD Number', validators=[Required()])
    tdrole_ref = SelectField('TDRole', coerce=int)
#    tdrole_ref = SelectField('TDRole',choices = [(role.id, role.name) for role in TDRole.query.all()])
#    tdrole_ref.choices = [(role.id, role.name) for role in TDRole.query.all()]
#    tdrole_ref.choices = [('1', 'C++'), ('2', 'Python')]
    submit = SubmitField('Submit')
#    tdrole_ref.choices = [(tdrole.id, tdrole.name) for role in TDRole.query.order_by(TDRole.name).all()]

class EditRaceBase(FlaskForm):
    eventname = StringField('Event Name (in FIS Calendar)', validators=[Required()])
    racedate = DateField('Race date', format='%d.%m.%Y')
    place = StringField('Place')
    gender_ref = SelectField('Gender', coerce=int)
    nation_ref = SelectField('Nation', coerce=int)
    category_ref = SelectField('Category', coerce=int)
    discipline_ref = SelectField('Discipline', coerce=int)
    season = StringField('Season')
    sector = StringField('Sector (AL)')
    codex = StringField('Codex')
    speedcodex = StringField('Race codex of speed race for Super Combined')
    training = StringField('Number of Training')
    submit = SubmitField('Submit')

class EditRaceJury(FlaskForm):
    jury_ref = SelectField('Jury', coerce=int, validators=[InputRequired()])
    jury_function_ref = SelectField('Type', coerce=int, validators=[InputRequired()])

    # phonenbr = StringField('Phone number')
    # email = StringField('E-mail', validators=[Email()])

    submit = SubmitField('Add')


class EditCompetitorBase(FlaskForm):
    ru_lastname = StringField('Russian surname', validators=[InputRequired()])
    en_lastname = StringField('English surname', validators=[InputRequired()])

    ru_firstname = StringField('Russian name', validators=[InputRequired()])
    en_firstname = StringField('English name', validators=[InputRequired()])

    fis_code = StringField('English name', validators=[InputRequired()])

    gender_ref = SelectField('Gender', coerce=int, validators=[InputRequired()])
    birth = DateField('Birthday date', format='%d.%m.%Y')
    nation_code_ref = SelectField('Nation', coerce=int, validators=[InputRequired()])
    national_code = StringField('national_code')

    NSA = StringField('NSA')
    category_ref = SelectField('Category', coerce=int, validators=[InputRequired()])

    points = StringField('Points')# Не понятно
    fis_points = StringField('Points')

    submit = SubmitField('Submit')

class EditRaceCompetitor(FlaskForm):
    competitor_ref = SelectField('Competitor', coerce=int, validators=[InputRequired()])

    age_class = StringField('Age class')
    chip = StringField('Chip')
    bib = IntegerField('Bib')

    submit = SubmitField('Add')

class EditJuryBase(FlaskForm):
    ru_lastname = StringField('Russian surname', validators=[InputRequired()])
    en_lastname = StringField('English surname', validators=[InputRequired()])

    ru_firstname = StringField('Russian name', validators=[InputRequired()])
    en_firstname = StringField('English name', validators=[InputRequired()])

    nation_ref = SelectField('Nation', coerce=int, validators=[InputRequired()])
    phonenbr = StringField('Phone number', validators=[InputRequired()])
    email = StringField('E-mail', validators=[InputRequired(), Email()])

    submit = SubmitField('Submit')