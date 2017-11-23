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

class Discipline(db.Model):
    __tablename__ = 'discipline'
    id = db.Column(db.Integer, primary_key=True)
    fiscode = db.Column(db.String)
    ru_name = db.Column(db.String)
    en_name = db.Column(db.String)
    def __repr__(self):
        return self.fiscode

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

class Competitor(db.Model):
    __tablename__ = 'competitor'
    id = db.Column(db.Integer, primary_key=True)
    fiscode = db.Column(db.String)
    ru_name = db.Column(db.String)
    en_name = db.Column(db.String)
    ru_fname = db.Column(db.String)
    en_fname = db.Column(db.String)
    #gender = db.Column(db.String(1))
    birth = db.Column(db.Date)



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

class Mark(db.Model):
    __tablename__ = 'mark'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4))
    description = db.Column(db.String(100))
