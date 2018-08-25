from .. import db
from sqlalchemy.ext.declarative import declarative_base


db.Model_RW = db.make_declarative_base()

class Gender(db.Model_RW):
    __bind_key__ = 'shorttrack'
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

class Nation(db.Model_RW):
    __bind_key__ = 'shorttrack'
    __tablename__ = 'nation'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(3))
    ru_description = db.Column(db.String(50))
    en_description = db.Column(db.String(50))
    def __repr__(self):
        return self.name


class Competitor(db.Model_RW):
    __bind_key__ = 'shorttrack'
    __tablename__ = 'competitor'

    id = db.Column(db.Integer, primary_key=True)
    best_season_time = db.Column(db.Time)
    bib = db.Column(db.String)

    ru_firstname = db.Column(db.String)
    en_firstname = db.Column(db.String)
    ru_lastname = db.Column(db.String)
    en_lastname = db.Column(db.String)
    gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'))

    birth = db.Column(db.Date)
    nation_id = db.Column(db.Integer, db.ForeignKey('nation.id'))

    club = db.Column(db.String)
    transponder_1 = db.Column(db.String)
    transponder_2 = db.Column(db.String)

class Race(db.Model_RW):
    __tablename__ = 'race'
    __bind_key__ = 'shorttrack'
    id = db.Column(db.Integer, primary_key=True)
    eventname = db.Column(db.String)
    place = db.Column(db.String)
    racedate = db.Column(db.DateTime)

    description = db.Column(db.String)

