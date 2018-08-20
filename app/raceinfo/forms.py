from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, \
    SelectField, DateField, IntegerField, DateTimeField, HiddenField, DecimalField
from wtforms_components import TimeField

from wtforms.validators import Required, Email, InputRequired, Optional, NumberRange, Regexp
from .validators import FunctionAllowed


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
    level = IntegerField('Level (Integer 0-4)', [NumberRange(min=0, max=4)])
    submit = SubmitField('Submit')

class EditWeatherForm(FlaskForm):
    time = TimeField('Time', validators=[Optional()])
    place = StringField('place')
    weather = StringField('weather')
    snow = StringField('snow')
    temperatureair = DecimalField('Air temperature', validators=[Optional()], places=2, rounding=None)
    temperaturesnow = DecimalField('Snow temperature', validators=[Optional()],places=2, rounding=None)
    humiditystart = IntegerField('Humidity start',validators=[Optional()])
    windspeed = DecimalField('Wind speed', validators=[Optional()], places=2, rounding=None)
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
    eventname = StringField('Event Name (in FIS Calendar)', validators=[InputRequired()])
    race_type = SelectField('Race type', choices=[('True', 'Team competition'), ('False', 'Individual competition')])
    racedate = DateTimeField('Race date', format='%d.%m.%Y %H:%M', render_kw={"class": "race_datepicker"})
    place = StringField('Place')
    gender_ref = SelectField('Gender', coerce=int)
    nation_ref = SelectField('Nation', coerce=int)
    category_ref = SelectField('Category', coerce=int)
    discipline_ref = SelectField('Discipline', coerce=int)
    result_method_ref = SelectField('Resault method', coerce=int)
    run_order_method_ref = SelectField('Order list method', coerce=int)
    numbers_of_runs = IntegerField('Number of runs', default=1)
    season = IntegerField('Season')
    # sector = StringField('Sector (AL)')
    codex = IntegerField('Codex')
    speedcodex = IntegerField('Race codex of speed race for Super Combined', [Optional()])
    submit = SubmitField('Submit')

class EditRaceAdditional(FlaskForm):
    usedfislist = StringField('Used fis list')
    appliedpenalty = StringField('Applied penalty')
    calculatedpenalty = IntegerField('Calculated penalty')
    fvalue = IntegerField('Fvalue')
    # - - Course
    # - - Weather
    timingby = StringField('Timing by')
    dataprocessingby = StringField('Data processing by')
    softwarecompany = StringField('Software company')
    softwarename = StringField('Software name')
    softwareversion = StringField('Software version')
    submit = SubmitField('Submit')


class EditRaceJury(FlaskForm):
    jury_ref = SelectField('Jury', coerce=int, validators=[InputRequired()])
    function_ref = SelectField('Type', coerce=int, validators=[InputRequired(), FunctionAllowed])
    # phonenbr = StringField('Phone number')
    # email = StringField('E-mail', validators=[Email()])
    is_member = SelectField('Jury type', coerce=int, choices=[(1, 'Member'), (0, 'Jury')])
    submit = SubmitField('Add')


class EditCompetitorBase(FlaskForm):
    ru_lastname = StringField('Russian lastname', validators=[InputRequired()])
    ru_firstname = StringField('Russian name', validators=[InputRequired()])

    en_lastname = StringField('English lastname', validators=[InputRequired()])
    en_firstname = StringField('English name', validators=[InputRequired()])

    fis_code = StringField('FIS', validators=[InputRequired()])

    gender_ref = SelectField('Gender', coerce=int, validators=[InputRequired()])
    birth = DateField('Birthday date', format='%d.%m.%Y')
    nation_code_ref = SelectField('Nation', coerce=int, validators=[InputRequired()])
    national_code = StringField('National code')

    NSA = StringField('NSA')
    category_ref = SelectField('Category', coerce=int, validators=[InputRequired()])

    # points = StringField('Points')# Не понятно
    # fis_points = StringField('Points')
    is_ajax = HiddenField('is_ajax')
    submit = SubmitField('Submit')



class EditRaceCompetitor(FlaskForm):
    competitor_ref = SelectField('Competitor', coerce=int, validators=[InputRequired()])

    age_class = StringField('Age class')
    transponder_1 = StringField('Transponder 1')
    transponder_2 = StringField('Transponder 2')
    bib = IntegerField('Bib')

    submit = SubmitField('Add')

class EditRaceCompetitorTeamForm(EditRaceCompetitor):
    team_ref = HiddenField('Team', validators=[InputRequired()])

class EditJuryBase(FlaskForm):
    ru_lastname = StringField('Russian lastname', validators=[InputRequired()])
    ru_firstname = StringField('Russian name', validators=[InputRequired()])

    en_lastname = StringField('English lastname', validators=[InputRequired()])
    en_firstname = StringField('English name', validators=[InputRequired()])

    nation_ref = SelectField('Nation', coerce=int, validators=[InputRequired()])
    phonenbr = StringField('Phone number', validators=[InputRequired()])
    email = StringField('E-mail', validators=[InputRequired(), Email()])

    submit = SubmitField('Submit')


class EditCourseBase(FlaskForm):
    course_coursetter_ref = SelectField('Coursetter', coerce=int, validators=[InputRequired()])
    ru_name = StringField('Russian name', validators=[InputRequired()])
    en_name = StringField('English name', validators=[InputRequired()])
    homologation =IntegerField('Homologation (0 - No homologation)')
    length = IntegerField('Length')
    gates = IntegerField('Gates')
    tuminggates = IntegerField('Tuminggates')
    startelev = IntegerField('Startelev')
    finishelev = IntegerField('Finishelev')
    submit = SubmitField('Submit')


class EditCourseForerunnerBase(FlaskForm):
    order = IntegerField('Order')
    forerunner_ref = SelectField('Forerunner', coerce=int, validators=[InputRequired()])
    # course_ref = SelectField('Course', coerce=int, validators=[InputRequired()])
    submit = SubmitField('Submit')


class EditForerunnerBase(FlaskForm):
    ru_lastname = StringField('Russian lastname', validators=[InputRequired()])
    ru_firstname = StringField('Russian name', validators=[InputRequired()])

    en_lastname = StringField('English lastname', validators=[InputRequired()])
    en_firstname = StringField('English name', validators=[InputRequired()])

    nation_ref = SelectField('Nation', coerce=int, validators=[InputRequired()])

    submit = SubmitField('Submit')


class EditCoursetterBase(FlaskForm):
    ru_lastname = StringField('Russian lastname', validators=[InputRequired()])
    ru_firstname = StringField('Russian name', validators=[InputRequired()])

    en_lastname = StringField('English lastname', validators=[InputRequired()])
    en_firstname = StringField('English name', validators=[InputRequired()])

    nation_ref = SelectField('Nation', coerce=int, validators=[InputRequired()])
    submit = SubmitField('Submit')

class EditTeamForm(FlaskForm):

    fis_code = StringField('fis code', validators=[InputRequired()])
    en_teamname = StringField('English name', validators=[InputRequired()])
    ru_teamname = StringField('Russian name', validators=[InputRequired()])
    nation_ref = SelectField('Nation', coerce=int)

    submit = SubmitField('Submit')


class EditRaceTeamForm(FlaskForm):
    team_ref = SelectField('Team', coerce=int, validators=[InputRequired()])
    bib = IntegerField('Bib', validators=[InputRequired()])
    # classified = BooleanField('Classified', validators=[InputRequired()])
    submit = SubmitField('Submit')

class EditRunInfoForm(FlaskForm):
    # course_ref = SelectField('Course', coerce=int, validators=[InputRequired()])
    # discipline_ref = SelectField('Discipline', coerce=int)
    number = IntegerField('Number', validators=[InputRequired()])
    submit = SubmitField('Submit')

class EditCoutseRunForm(FlaskForm):
    # course_ref = SelectField('Course', coerce=int, validators=[InputRequired()])
    run_ref = SelectField('Run', coerce=int)
    # number = IntegerField('Number', validators=[InputRequired()])
    submit = SubmitField('Submit')


class EditRunInfoDisciplineForm(EditRunInfoForm):
    discipline_ref = SelectField('Discipline', coerce=int)

    __order = ('csrf_token', 'discipline_ref', 'number', 'submit')

    def __iter__(self):
        fields = list(super(EditRunInfoDisciplineForm, self).__iter__())
        get_field = lambda field_id: next((fld for fld in fields if fld.id == field_id))
        return (get_field(field_id) for field_id in self.__order)

class EditRunInfoParallelForm(EditRunInfoForm):
    runtype_ref = SelectField('Run type', coerce=int)

    __order = ('csrf_token', 'runtype_ref', 'number', 'submit')

    def __iter__(self):
        fields = list(super(EditRunInfoParallelForm, self).__iter__())
        get_field = lambda field_id: next((fld for fld in fields if fld.id == field_id))
        return (get_field(field_id) for field_id in self.__order)


class EditCourseDeviceForm(FlaskForm):
    # course_ref = SelectField('Course', coerce=int, validators=[InputRequired()])
    order = IntegerField('Order', validators=[InputRequired()])
    course_device_type_ref = SelectField('Device type', coerce=int, validators=[InputRequired()])
    device_ref = SelectField('Device', coerce=int, validators=[InputRequired()])
    distance = IntegerField('Distance', validators=[InputRequired()])
    submit = SubmitField('Submit')


class EditDeviceForm(FlaskForm):
    src_dev = StringField('src dev', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    type_ref = SelectField('Type', coerce=int,  validators=[InputRequired()])
    submit = SubmitField('Submit')



class EditDeviceTypeForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    submit = SubmitField('Submit')