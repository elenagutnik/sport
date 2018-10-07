from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, \
    SelectField, DateField, IntegerField, DateTimeField, HiddenField, DecimalField
from wtforms_components import TimeField

from wtforms.validators import Required, Email, InputRequired, Optional, NumberRange, Regexp

class RaceBaseForm(FlaskForm):
    eventname = StringField('Event Name (in FIS Calendar)', validators=[InputRequired()])
    racedate = DateTimeField('Race date', format='%d.%m.%Y %H:%M', render_kw={"class": "race_datepicker"})
    place = StringField('Place')
    distance = IntegerField('Distance')
    description = StringField('Description')
    submit = SubmitField('Submit')

class DeviceBaseForm(FlaskForm):
    src_dev = StringField('src_dev', validators=[InputRequired()])
    name = StringField('Device Name', validators=[InputRequired()])
    submit = SubmitField('Submit')

class JuryBaseForm(FlaskForm):
    ru_lastname = StringField('Lastname (Rus)', validators=[InputRequired()])
    ru_firstname = StringField('Firstname (Rus)', validators=[InputRequired()])
    en_lastname = StringField('Lastname (Eng)', validators=[InputRequired()])
    en_firstname = StringField('Firstname (Eng)', validators=[InputRequired()])
    jury_type_ref = SelectField('Jury type', coerce=int)
    event_code = StringField('Event code (System)', validators=[InputRequired()])
    submit = SubmitField('Submit')