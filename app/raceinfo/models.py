from datetime import datetime
from flask import current_app
from .. import db
from sqlalchemy import func, or_, and_
from .errors import BibRepeat
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
    is_combination = db.Column(db.Boolean)
    is_parallel = db.Column(db.Boolean)
    is_qualification = db.Column(db.Boolean)

    def __repr__(self):
        return self.fiscode

    @staticmethod
    def insert():
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
            'CAR': "Carving",
            'QLF': "Qualification (Parallel)"
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
    level = db.Column(db.Integer)# level 0-4

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
    race_id = db.Column(db.Integer, db.ForeignKey('race.id', ondelete='CASCADE'))
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
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'))


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
    race_id = db.Column(db.Integer, db.ForeignKey('race.id', ondelete='CASCADE'))
    jury_function_id = db.Column(db.Integer, db.ForeignKey('jury_type.id'))
    phonenbr = db.Column(db.String)
    email = db.Column(db.String)
    is_member = db.Column(db.Boolean)

class JuryType(db.Model):
    __tablename__ = 'jury_type'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    description = db.Column(db.String)
    is_member_allowed = db.Column(db.Boolean)
    @staticmethod
    def insert():
        Types = {
            'TechnicalDelegate': False,
            'ChiefRace': True,
            'Referee': True,
            'Assistantreferee': True,
            'ChiefCourse': True,
            'Startreferee': True,
            'Finishreferee': True,
            'ChiefTiming': True,
        }
        for c in Types.keys():
            type = JuryType.query.filter_by(type=c).first()
            if type is None:
                type = JuryType(type=c)
                type.is_member_allowed = Types[c]
            db.session.add(type)
        db.session.commit()



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

    @staticmethod
    def add(fiscode=None,
            en_firstname=None, en_lastname=None,
            ru_firstname=None, ru_lastname=None,
            gender_id=None, birth=None,
            nation_code_id=None, NSA=None,
            category_id=None, national_code=None):
        competitor = Competitor.query.filter(
            or_(
                Competitor.fiscode == str(fiscode),
                and_(
                    Competitor.en_firstname == en_firstname,
                    Competitor.en_lastname == en_lastname),
                    Competitor.birth == birth
                )
        ).first()
        if competitor is None:
            competitor = Competitor(
                fiscode=fiscode,
                en_firstname=en_firstname,
                en_lastname=en_lastname,
                ru_firstname=ru_firstname,
                ru_lastname=ru_lastname,
                gender_id=gender_id,
                birth=birth,
                nation_code_id=nation_code_id,
                NSA=NSA,
                category_id=category_id,
                national_code=national_code
            )
            db.session.add(competitor)
            db.session.commit()
            return competitor
        else:
             return competitor





class RaceCompetitor(db.Model):
    __tablename__ = 'race_competitor'
    id = db.Column(db.Integer, primary_key=True)
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id'))
    forerunner_id = db.Column(db.Integer, db.ForeignKey('course_forerunner.id'))
    race_id = db.Column(db.Integer, db.ForeignKey('race.id', ondelete='CASCADE'))
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
    # я об этом пожалею
    run_id =db.Column(db.Integer, db.ForeignKey('run_info.id', ondelete='CASCADE'))
    # переделать в связь с run_info, team_id
    gate = db.Column(db.String)
    reason = db.Column(db.String)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id',ondelete='CASCADE' ))
    fis_points = db.Column(db.Float)

    club = db.Column(db.String)
    diff = db.Column(db.BigInteger)

    @staticmethod
    def add(competitor_id=None, race_id=None,
            bib=None, club=None, transponder_1=None, transponder_2=None, age_class=None, team_id=None):
        race_competitor = RaceCompetitor.query.filter(RaceCompetitor.competitor_id == competitor_id,
                                                      RaceCompetitor.race_id == race_id).first()
        current_bib = RaceCompetitor.query.filter(RaceCompetitor.bib==bib, RaceCompetitor.race_id==race_id).first()
        if current_bib is not None:
            competitor = Competitor.query.get(current_bib.competitor_id)
            raise BibRepeat((competitor.en_lastname+' '+competitor.en_firstname), bib)
        if race_competitor is None:
            race_competitor = RaceCompetitor(
                competitor_id=competitor_id,
                race_id=race_id,
                bib=bib,
                club=club,
                transponder_1=transponder_1,
                transponder_2=transponder_2,
                age_class=age_class,
                team_id=team_id
            )
        else:
            race_competitor.bib = bib
            race_competitor.club = club
            race_competitor.transponder_1 = transponder_1
            race_competitor.transponder_2 = transponder_2
        db.session.add(race_competitor)
        db.session.commit()
        return race_competitor

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
            'Combination': ""
        }
        for f in function.keys():
            result_function = RunOrderFunction.query.filter_by(name=f).first()
            if result_function is None:
                result_function = RunOrderFunction(name=f)
                result_function.descrioption = function[f]
            db.session.add(result_function)
        db.session.commit()

    @staticmethod
    def get(competitor_id,run_id):
        return RunOrder.query.filter(RunOrder.race_competitor_id == competitor_id,
                              RunOrder.run_id == run_id).one()

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
    racedate = db.Column(db.DateTime)# probably must be 3 fields: day, month, year
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
        return self.eventname

class Weather(db.Model):
    __tablename__ = 'weather'
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('race.id', ondelete='CASCADE'))
    time = db.Column(db.Time)
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


class RunType(db.Model):
    __tablename__ = 'run_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    is_parralel = db.Column(db.Boolean)
    is_forerunner = db.Column(db.Boolean)
    is_test = db.Column(db.Boolean)
    is_qualification = db.Column(db.Boolean)
    # normal = 1
    # test = 2
    # forerunner = 3
    # qualification = 4
    @staticmethod
    def insert():
        types = ['normal', 'test', 'forerunner', 'qualification', 'final']

        for t in types:
            type = RunType.query.filter_by(name=t).first()
            if type is None:
                type = RunType(name=t)
            db.session.add(type)
        db.session.commit()

class RunInfo(db.Model):
    __tablename__ = 'run_info'
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('race.id', ondelete='CASCADE'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    number = db.Column(db.Integer)
    starttime = db.Column(db.DateTime)
    endtime = db.Column(db.DateTime)
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.id'))
    run_type_id = db.Column(db.Integer, db.ForeignKey('run_type.id'))
    is_second = db.Column(db.Boolean)

class RunCourses(db.Model):
    __tablename__ = 'run_courses'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'))
    run_id = db.Column(db.Integer, db.ForeignKey('run_info.id', ondelete='CASCADE'))

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
    race_id = db.Column(db.Integer, db.ForeignKey('race.id', ondelete='CASCADE'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    run_id = db.Column(db.Integer, db.ForeignKey('run_info.id'))
    bib = db.Column(db.Integer)
    classified = db.Column(db.Boolean)
    en_teamname = db.Column(db.String)
    ru_teamname = db.Column(db.String)
    parent_race_id = db.Column(db.Integer, db.ForeignKey('race.id'))

class CourseDevice(db.Model):
    __tablename__ = 'course_device'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'))
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

    race_id = db.Column(db.Integer, db.ForeignKey('race.id', ondelete='CASCADE'))
    run_id = db.Column(db.Integer, db.ForeignKey('run_info.id', ondelete='CASCADE'))
    cource_device_id = db.Column(db.Integer, db.ForeignKey('course_device.id'))
    src_sys = db.Column(db.String)
    src_dev = db.Column(db.String)
    bib = db.Column(db.Integer)
    event_code = db.Column(db.String)
    time = db.Column(db.BigInteger)
    reserved = db.Column(db.String)

    @staticmethod
    def set(SRC_SYS,SRC_DEV, TIME, EVENT_CODE, bib=None, run_id=None, cource_device_id=None):
        dataIn = DataIn(
            src_sys=SRC_SYS,
            src_dev=SRC_DEV,
            event_code=EVENT_CODE,
            time=TIME,
            run_id=run_id,
            cource_device_id=cource_device_id,
            bib=bib
        )
        db.session.add(dataIn)
        db.session.commit()
        return dataIn

class ResultDetail(db.Model):
    __tablename__ = 'result_detail'
    id = db.Column(db.Integer, primary_key=True)
    course_device_id = db.Column(db.Integer, db.ForeignKey('course_device.id'))
    race_competitor_id = db.Column(db.Integer, db.ForeignKey('race_competitor.id', ondelete='CASCADE'))
    run_id = db.Column(db.Integer, db.ForeignKey('run_info.id', ondelete='CASCADE'))

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

    def resetResult(self):
        self.data_in_id = None
        self.diff = None
        self.time = None
        self.rank = None
        self.speed = None
        self.sectortime = None
        self.sectordiff = None
        self.sectorrank = None
        self.absolut_time = None

    @staticmethod
    def remove(competitor_id,run_id):
        ResultDetail.query.filter(
            ResultDetail.race_competitor_id == competitor_id,
            ResultDetail.run_id == run_id
        ).delete()

class ResultApproved(db.Model):
    __tablename__ = 'result_approved'
    id = db.Column(db.Integer, primary_key=True)
    race_competitor_id = db.Column(db.Integer, db.ForeignKey('race_competitor.id', ondelete='CASCADE'))
    result_id = db.Column(db.Integer, db.ForeignKey('result.id'))
    run_id = db.Column(db.Integer, db.ForeignKey('run_info.id', ondelete='CASCADE'))
    approve_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    approve_time = db.Column(db.DateTime)
    time = db.Column(db.BigInteger)
    adder_time = db.Column(db.BigInteger, default=0)
    adder_diff = db.Column(db.BigInteger, default=0)
    diff = db.Column(db.BigInteger)
    start_time = db.Column(db.BigInteger)
    finish_time = db.Column(db.BigInteger)
    rank = db.Column(db.Integer)
    is_manual = db.Column(db.Boolean)
    gate = db.Column(db.String)
    reason = db.Column(db.String)
    is_start = db.Column(db.Boolean)
    is_finish = db.Column(db.Boolean)


    def set_competitor_adder(self, run_number):
        adder = db.session.query(func.sum(ResultApproved.time).label('time'),
                                 func.sum(ResultApproved.diff).label('diff')).\
            filter(ResultApproved.race_competitor_id == self.race_competitor_id,
                   ResultApproved.run_id == RunInfo.id,
                   RunInfo.number < run_number).first()
        if adder.time is not None:
            self.adder_time = adder.time
            self.adder_diff = adder.diff

    @staticmethod
    def get(competitor_id, run_id):
        return ResultApproved.query.filter_by(
            race_competitor_id=competitor_id,
            run_id=run_id).one()

    @staticmethod
    def remove(competitor_id, run_id):
        ResultApproved.query.filter(
            ResultApproved.race_competitor_id == competitor_id,
            ResultApproved.run_id == run_id
        ).delete()



class Result(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer, primary_key=True)
    race_competitor_id = db.Column(db.Integer, db.ForeignKey('race_competitor.id', ondelete='CASCADE'))
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
    run_id = db.Column(db.Integer, db.ForeignKey('run_info.id', ondelete='CASCADE'))
    race_competitor_id = db.Column(db.Integer, db.ForeignKey('race_competitor.id', ondelete='CASCADE'))
    order = db.Column(db.Integer)
    #
    is_participate = db.Column(db.Boolean)
    manual_order = db.Column(db.Integer)

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    @staticmethod
    def get(competitor_id, run_id):
        return RunOrder.query.filter(RunOrder.race_competitor_id == competitor_id,
                                     RunOrder.run_id == run_id).one()

class FisPoints(db.Model):
    __tablename__ = 'fis_points'
    id = db.Column(db.Integer, primary_key=True)
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id'))
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.id'))
    fispoint = db.Column(db.Float)
    date_update = db.Column(db.DateTime)
    date_expired = db.Column(db.DateTime)

    @property
    def point(self):
        return self.fispoint

    @point.setter
    def point(self, fispoint):
        if str(fispoint) == '999.99':
            self.fispoint = fispoint * -1
        else:
            self.fispoint = fispoint

class RaceCompetitorFisPoints(db.Model):
    __tablename__ = 'race_com_fis_points'
    id = db.Column(db.Integer, primary_key=True)
    race_competitor_id = db.Column(db.Integer, db.ForeignKey('race_competitor.id', ondelete='CASCADE'))
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.id'))
    fispoint = db.Column(db.Float)

    @property
    def point(self):
        return self.fispoint

    @point.setter
    def point(self, fispoint):
        if str(fispoint) == '999.99':
            self.fispoint = fispoint * -1
        else:
            self.fispoint = fispoint
class System(db.Model):
    __tablename__ = 'system_table'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String, unique=True)
    value = db.Column(db.String)
