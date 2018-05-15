from datetime import datetime
from flask import current_app
from .. import db

class Gender(db.Model):
    __tablename__ = 'gender'
    id = db.Column(db.Integer, primary_key=True)
    fiscode = db.Column(db.String)
    ru_name = db.Column(db.String)
    en_name = db.Column(db.String)
    def __repr__(self):
        return self.fiscode

    @staticmethod
    def insert_genders():
        genders = ['Male', "Female"]
        for d in genders:
            gender = Gender.query.filter_by(fiscode=d).first()
            if gender is None:
                gender = Gender(fiscode=d)
            gender.en_name = d
            gender.ru_name = d
            gender.fiscode = d
            db.session.add(gender)
        db.session.commit()


class Discipline(db.Model):
    __tablename__ = 'discipline'
    id = db.Column(db.Integer, primary_key=True)
    fiscode = db.Column(db.String)
    ru_name = db.Column(db.String)
    en_name = db.Column(db.String)
    def __repr__(self):
        return self.fiscode

    @staticmethod
    def insert_discipline():
        disciplines = {
            'DH': "Downhill",
            'SL': "Slalom",
            'GS': "Giant Slalom",
            'SG': "Super G",
            'SC': "Super Combined",
            'TE': "Team",
            'KOS': "KO Slalom",
            'KOG': "KO Giant Slalom",
            'PGS': "Parallel Giant Slalom",
            'PSL': "Parallel Slalom",
            'CE': "City Event",
            'IND': "Indoor",
            'P': "Parallel",
            'CAR': "Carving"
        }
        for d in disciplines.keys():
            discipline = Discipline.query.filter_by(fiscode=d).first()
            if discipline is None:
                discipline = Discipline(fiscode=d)
            discipline.en_name = disciplines[d]
            discipline.ru_name = disciplines[d]
            db.session.add(discipline)
        db.session.commit()


class TDRole(db.Model):
    __tablename__ = 'tdrole'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    tds = db.relationship('TD', backref='tdrole_ref', lazy='dynamic')
    def __repr__(self):
        return self.name

class TD(db.Model):
    __tablename__ = 'td'
    id = db.Column(db.Integer, primary_key=True)
    tdnumber = db.Column(db.String)
    ru_firstname = db.Column(db.String)
    en_firstname = db.Column(db.String)
    ru_lastname = db.Column(db.String)
    en_lastname = db.Column(db.String)
    ru_nation = db.Column(db.String)
    en_nation = db.Column(db.String)
    tdrole_id = db.Column(db.Integer, db.ForeignKey('tdrole.id'))
    def __repr__(self):
        return '<TD %r>' % self.ru_lastname

class Category(db.Model):
    # FIS category of Event
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(3))
    description = db.Column(db.String(150))
    level = db.Column(db.Integer) # level 0-4

    @staticmethod
    def insert():
        Categorys = {
            'OWG': "Olimpic Winter Games",
            'WSC': "FIS World Ski Championships",
            'WC': "FIS World Cup",
        }
        for c in Categorys.keys():
            category = Category.query.filter_by(name=c).first()
            if category is None:
                category = Category(name=c)
                category.description = Categorys[c]
            db.session.add(category)
        db.session.commit()
    def __repr__(self):
        return self.name

class Nation(db.Model):
    # FIS abbreviation for nations
    __tablename__ = 'nation'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(3))
    ru_description = db.Column(db.String(50))
    en_description = db.Column(db.String(50))
    def __repr__(self):
        return self.name

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('race.id'))
    course_coursetter_id = db.Column(db.Integer, db.ForeignKey('coursetter.id'))
    run = db.Column(db.Integer)
    ru_name = db.Column(db.String)
    en_name = db.Column(db.String)
    homologation = db.Column(db.Integer)
    length = db.Column(db.Integer)
    gates = db.Column(db.Integer)
    tuminggates = db.Column(db.Integer)
    startelev = db.Column(db.Integer)
    finishelev = db.Column(db.Integer)


class CourseForerunner(db.Model):
    __tablename__ = 'course_forerunner'
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    forerunner_id = db.Column(db.Integer, db.ForeignKey('forerunner.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))


class Forerunner(db.Model):
    __tablename__ = 'forerunner'
    id = db.Column(db.Integer, primary_key=True)
    ru_lastname = db.Column(db.String)
    ru_firstname = db.Column(db.String)
    en_lastname = db.Column(db.String)
    en_firstname = db.Column(db.String)
    nation_id = db.Column(db.Integer, db.ForeignKey('nation.id'))


class Coursetter(db.Model):
    __tablename__ = 'coursetter'
    id = db.Column(db.Integer, primary_key=True)
    ru_lastname = db.Column(db.String)
    ru_firstname = db.Column(db.String)
    en_lastname = db.Column(db.String)
    en_firstname = db.Column(db.String)
    nation_id = db.Column(db.Integer, db.ForeignKey('nation.id'))


class Jury(db.Model):
    __tablename__ = 'jury'
    id = db.Column(db.Integer, primary_key=True)
    ru_lastname = db.Column(db.String)
    ru_firstname = db.Column(db.String)
    en_lastname = db.Column(db.String)
    en_firstname = db.Column(db.String)
    nation_id = db.Column(db.Integer, db.ForeignKey('nation.id'))
    phonenbr = db.Column(db.String)
    email = db.Column(db.String)

class RaceJury(db.Model):
    __tablename__ = 'race_jury'
    id = db.Column(db.Integer, primary_key=True)
    jury_id = db.Column(db.Integer, db.ForeignKey('jury.id'))
    race_id = db.Column(db.Integer, db.ForeignKey('race.id'))
    jury_function_id = db.Column(db.Integer, db.ForeignKey('jury_function.id'))
    phonenbr = db.Column(db.String)
    email = db.Column(db.String)


class Competitor(db.Model):
    __tablename__ = 'competitor'
    id = db.Column(db.Integer, primary_key=True)
    fiscode = db.Column(db.String)
    ru_firstname = db.Column(db.String)
    en_firstname = db.Column(db.String)
    ru_lastname = db.Column(db.String)
    en_lastname = db.Column(db.String)
    gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'))#справочник
    birth = db.Column(db.Date)
    nation_code_id = db.Column(db.Integer, db.ForeignKey('nation.id'))#справочник
    national_code = db.Column(db.String)
    NSA = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))#справочник
    points = db.Column(db.Float)


class RaceCompetitor(db.Model):
    __tablename__ = 'race_competitor'
    id = db.Column(db.Integer, primary_key=True)
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id'))
    race_id = db.Column(db.Integer, db.ForeignKey('race.id'))
    age_class = db.Column(db.String)
    transponder_1 = db.Column(db.String)
    transponder_2 = db.Column(db.String)
    bib = db.Column(db.Integer)
    classified = db.Column(db.Boolean)
    # results
    rank = db.Column(db.Integer)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    time = db.Column(db.BigInteger)
    order = db.Column(db.Integer)
    run_id =db.Column(db.Integer, db.ForeignKey('run_info.id'))
    # переделать в связь с run_info, team_id
    gate = db.Column(db.String)
    reason = db.Column(db.String)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    fis_points = db.Column(db.Float)

    club = db.Column(db.String)

class ResultFunction(db.Model):
    __tablename__ = 'result_function'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    descrioption = db.Column(db.String)

    @staticmethod
    def insert():
        function = {
            'Sum of runs': "Сумма попыток - итоговый результат - суммируются результаты всех попыток каждого спортсмена",
            'The best one': "Лучшая из попыток - итоговая таблица результатов формируется из лучшего времени каждого спортсмена",
            'The sum of two best runs': "Выбирается сумма двух лучших попыток спортсмена и заносится в итоговый список",
            'The sum of three best runs': "Выбирается сумм трех лучших попыток спортсмена и заносится в итоговый список"
        }
        for f in function.keys():
            result_function = ResultFunction.query.filter_by(name=f).first()
            if result_function is None:
                result_function = ResultFunction(name=f)
                result_function.descrioption = function[f]
            db.session.add(result_function)
        db.session.commit()

class RunOrderFunction(db.Model):
    __tablename__ = 'run_order_function'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    descrioption = db.Column(db.String)

    @staticmethod
    def insert():
        function = {
            'Drop Off': "Спортсмен не получивший QLF в текущем ране, не участвует в слудующем",
            'All competitors': "Спортсмены участвуют во всех заездах, не зависимо от статуса",
        }
        for f in function.keys():
            result_function = RunOrderFunction.query.filter_by(name=f).first()
            if result_function is None:
                result_function = RunOrderFunction(name=f)
                result_function.descrioption = function[f]
            db.session.add(result_function)
        db.session.commit()

class Race(db.Model):
    __tablename__ = 'race'
    id = db.Column(db.Integer, primary_key=True)
    # Raceheader
    sector = db.Column(db.String(2), default='AL')
    gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'))
    season = db.Column(db.Integer)
    codex = db.Column(db.Integer)
    nation_id = db.Column(db.Integer, db.ForeignKey('nation.id'))
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    result_function = db.Column(db.Integer, db.ForeignKey('result_function.id'))

    run_order_function = db.Column(db.Integer, db.ForeignKey('run_order_function.id'))

    type_of_content = db.Column(db.String)
    training = db.Column(db.String)
    speedcodex = db.Column(db.Integer)
    eventname = db.Column(db.String)
    #td

    td_delegate_tdnumber = db.Column(db.String)
    td_delegate_ru_firstname = db.Column(db.String)
    td_delegate_en_firstname = db.Column(db.String)
    td_delegate_ru_lastname = db.Column(db.String)
    td_delegate_en_lastname = db.Column(db.String)
    td_delegate_nation_id = db.Column(db.Integer, db.ForeignKey('nation.id'))

    td_assistant_tdnumber = db.Column(db.String)
    td_assistant_ru_firstname = db.Column(db.String)
    td_assistant_en_firstname = db.Column(db.String)
    td_assistant_ru_lastname = db.Column(db.String)
    td_assistant_en_lastname = db.Column(db.String)
    td_assistant_nation_id = db.Column(db.Integer, db.ForeignKey('nation.id'))

    place = db.Column(db.String)
    racedate = db.Column(db.Date) # probably must be 3 fields: day, month, year
    tempunit = db.Column(db.String(1))
    longunit = db.Column(db.String(2))
    speedunit = db.Column(db.String(3))
    windunit = db.Column(db.String(3))
    # AL_race
    # - Jury

    # - AL_raceinfo
    usedfislist = db.Column(db.String)
    appliedpenalty = db.Column(db.String)
    calculatedpenalty = db.Column(db.Integer)
    fvalue = db.Column(db.Integer)
    # - - Course
    # - - Weather
    timingby = db.Column(db.String)
    dataprocessingby = db.Column(db.String)
    softwarecompany = db.Column(db.String)
    softwarename = db.Column(db.String)
    softwareversion = db.Column(db.String)



    # - AL_classified
    # - AL_notclassified


    isTeam = db.Column(db.Boolean)

    def __repr__(self):
        return self.name

class Weather(db.Model):
    __tablename__ = 'weather'
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('race.id'))
    time = db.Column(db.DateTime)
    place = db.Column(db.String)
    weather = db.Column(db.String)
    snow = db.Column(db.String)
    temperatureair = db.Column(db.Numeric)
    temperaturesnow = db.Column(db.Numeric)
    humiditystart = db.Column(db.Integer)
    windspeed = db.Column(db.Numeric)

class Report_type(db.Model):
    __tablename__ = 'report_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    function = db.Column(db.String)

class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4))
    description = db.Column(db.String(100))
    filter_order = db.Column(db.Integer)
    @staticmethod
    def insert():
        status = {
            'QLF': "Qualified",
            'DNS': "Did not start ",
            'DNS1': "Did not start run 1",
            'DNS2': "Did not start run 2",
            'DSQ': "Disqualified",
            'DSQ1': "Disqualified run 1",
            'DSQ2': "Disqualified run 2",
            'DNF': "Did not finish ",
            'DNF1': "Did not finish run 1",
            'DNF2': "Did not finish run 2",
            'DNQ': "Did not qualify",
            'DNQ1': "Did not qualify run 1",
            'DPO': "Doping offense ",
            'NPS': "Not permitted to start ",
            'DQB': "Disqualification for unsportsmanlike behavior",
            'DQO': "Disqualified for over quota"
        }
        for d in status.keys():
            stts = Status.query.filter_by(name=d).first()
            if stts is None:
                stts = Status(name=d)
                stts.description = status[d]
            db.session.add(stts)
        db.session.commit()

class Mark(db.Model):
    __tablename__ = 'mark'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4))
    description = db.Column(db.String(100))

class Jury_function(db.Model):
    __tablename__ = 'jury_function'
    id = db.Column(db.Integer, primary_key=True)
    ru_function = db.Column(db.String)
    en_function = db.Column(db.String)
    attribute_values = db.Column(db.String)

    @staticmethod
    def insert_functions():
        functions = [
            'ChiefRace',
            'Referee',
            'Assistantreferee',
            'ChiefCourse',
            'Startreferee',
            'Finishreferee',
            'ChiefTiming'
        ]
        for d in functions:
            discipline = Jury_function.query.filter_by(attribute_values=d).first()
            if discipline is None:
                discipline = Jury_function(attribute_values=d)
            discipline.ru_function = d
            discipline.en_function = d
            db.session.add(discipline)
        db.session.commit()

class RunInfo(db.Model):
    __tablename__ = 'run_info'
    id = db.Column(db.Integer, primary_key=True)

    race_id = db.Column(db.Integer, db.ForeignKey('race.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    number = db.Column(db.Integer)
    starttime = db.Column(db.DateTime)
    endtime = db.Column(db.DateTime)

class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    fis_code = db.Column(db.String)
    en_teamname = db.Column(db.String)
    ru_teamname = db.Column(db.String)
    nation_id = db.Column(db.Integer, db.ForeignKey('nation.id'))

class RaceTeam(db.Model):
    __tablename__ = 'race_team'
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('race.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    run_id = db.Column(db.Integer, db.ForeignKey('run_info.id'))
    bib = db.Column(db.Integer)
    classified = db.Column(db.Boolean)
    en_teamname = db.Column(db.String)
    ru_teamname = db.Column(db.String)

class CourseDevice(db.Model):
    __tablename__ = 'course_device'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    order = db.Column(db.Integer)
    distance = db.Column(db.Integer)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    course_device_type_id = db.Column(db.Integer, db.ForeignKey('course_device_type.id'))

class Device(db.Model):
    __tablename__ = 'device'
    id = db.Column(db.Integer, primary_key=True)
    src_dev = db.Column(db.String)
    name = db.Column(db.String)
    type_id = db.Column(db.Integer, db.ForeignKey('device_type.id'))

class DeviceType(db.Model):
    __tablename__ = 'device_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class CourseDeviceType(db.Model):
    __tablename__ = 'course_device_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    @staticmethod
    def insert_types():
        course_device_types = ['Start', 'Finish', 'Point']
        for d in course_device_types:
            device_type = CourseDeviceType.query.filter_by(name=d).first()
            if device_type is None:
                device_type = CourseDeviceType(name=d)
            db.session.add(device_type)
        db.session.commit()


class DataIn(db.Model):
    __tablename__ = 'data_in'
    id = db.Column(db.Integer, primary_key=True)
    dt = db.Column(db.DateTime)

    race_id = db.Column(db.Integer, db.ForeignKey('race.id'))
    run_id = db.Column(db.Integer, db.ForeignKey('run_info.id'))
    cource_device_id = db.Column(db.Integer, db.ForeignKey('course_device.id'))
    src_sys = db.Column(db.String)
    src_dev = db.Column(db.String)
    bib = db.Column(db.Integer)
    event_code = db.Column(db.String)
    time = db.Column(db.BigInteger)
    reserved = db.Column(db.String)

class ResultDetail(db.Model):
    __tablename__ = 'result_detail'
    id = db.Column(db.Integer, primary_key=True)
    course_device_id = db.Column(db.Integer, db.ForeignKey('course_device.id'))
    race_competitor_id = db.Column(db.Integer, db.ForeignKey('race_competitor.id'))
    run_id = db.Column(db.Integer, db.ForeignKey('run_info.id'))

    data_in_id = db.Column(db.Integer, db.ForeignKey('data_in.id'))

    diff = db.Column(db.BigInteger)
    time = db.Column(db.BigInteger)
    rank = db.Column(db.Integer)
    speed = db.Column(db.Float)
    sectortime = db.Column(db.BigInteger)
    sectordiff = db.Column(db.BigInteger)
    sectorrank = db.Column(db.Integer)

    absolut_time = db.Column(db.BigInteger)
    is_start = db.Column(db.Boolean)

class ResultApproved(db.Model):
    __tablename__ = 'result_approved'
    id = db.Column(db.Integer, primary_key=True)
    race_competitor_id = db.Column(db.Integer, db.ForeignKey('race_competitor.id'))
    result_id = db.Column(db.Integer, db.ForeignKey('result.id'))
    run_id = db.Column(db.Integer, db.ForeignKey('run_info.id'))
    approve_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    approve_time = db.Column(db.DateTime)
    time = db.Column(db.BigInteger)
    diff = db.Column(db.BigInteger)
    start_time = db.Column(db.BigInteger)
    finish_time = db.Column(db.BigInteger)
    rank = db.Column(db.Integer)
    is_manual = db.Column(db.Boolean)
    gate = db.Column(db.String)
    reason = db.Column(db.String)
    is_start = db.Column(db.Boolean)
    is_finish = db.Column(db.Boolean)

class Result(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer, primary_key=True)
    race_competitor_id = db.Column(db.Integer, db.ForeignKey('race_competitor.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    approve_time = db.Column(db.DateTime)
    timerun1 = db.Column(db.BigInteger)
    timerun2 = db.Column(db.BigInteger)
    timerun3 = db.Column(db.BigInteger)
    diff = db.Column(db.BigInteger)
    racepoints = db.Column(db.BigInteger)
    level = db.Column(db.Integer)
    approve_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_manuale = db.Column(db.Boolean)

class RunOrder(db.Model):
    __tablename__ = 'run_order'
    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.Integer, db.ForeignKey('run_info.id'))
    race_competitor_id = db.Column(db.Integer, db.ForeignKey('race_competitor.id'))
    order = db.Column(db.Integer)
    #
    manual_order = db.Column(db.Integer)
    # course_id = db.Column(db.Integer, db.ForeignKey('race_competitor.id'))

class TempCashe(db.Model):
    # Вресенный класс,  для кэширования объектов, объекты хранятся в формате JSON
    __tablename__ = 'CASHE'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String)
    data = db.Column(db.String)

class FisPoints(db.Model):
    __tablename__ = 'fis_points'
    id = db.Column(db.Integer, primary_key=True)
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id'))
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.id'))
    fispoint = db.Column(db.Float)
    date_update = db.Column(db.DateTime)
    date_expired = db.Column(db.DateTime)

