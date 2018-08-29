from .. import db_shorttrack as db



class Gender(db.Model):
    __tablename__ = 'gender'
    __bind_key__ = 'shorttrack'


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

class Nation(db.Model):
    __tablename__ = 'nation'
    __bind_key__ = 'shorttrack'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(3))
    ru_description = db.Column(db.String(50))
    en_description = db.Column(db.String(50))
    def __repr__(self):
        return self.name


class Competitor(db.Model):
    __tablename__ = 'competitor'
    __bind_key__ = 'shorttrack'

    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('race.id', ondelete='CASCADE'))
    nation_id = db.Column(db.Integer, db.ForeignKey('nation.id'))
    gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'))
    best_season_time = db.Column(db.Time)
    bib = db.Column(db.String)

    ru_firstname = db.Column(db.String)
    en_firstname = db.Column(db.String)
    ru_lastname = db.Column(db.String)
    en_lastname = db.Column(db.String)

    birth = db.Column(db.Date)

    club = db.Column(db.String)
    transponder_1 = db.Column(db.String)
    transponder_2 = db.Column(db.String)

class Race(db.Model):
    __bind_key__ = 'shorttrack'
    __tablename__ = 'race'
    id = db.Column(db.Integer, primary_key=True)
    eventname = db.Column(db.String)
    place = db.Column(db.String)
    racedate = db.Column(db.DateTime)

    description = db.Column(db.String)

class RunInfo(db.Model):
    __tablename__ = 'run_info'
    __bind_key__ = 'shorttrack'
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('race.id', ondelete='CASCADE'))
    number = db.Column(db.Integer)
    starttime = db.Column(db.DateTime)
    endtime = db.Column(db.DateTime)

class RunOrder(db.Model):
    __bind_key__ = 'shorttrack'
    __tablename__ = 'run_order'
    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.Integer, db.ForeignKey('run_info.id', ondelete='CASCADE'))
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id', ondelete='CASCADE'))
    order = db.Column(db.Integer)

class ResultDetail(db.Model):
    __tablename__ = 'result_detail'
    __bind_key__ = 'shorttrack'
    id = db.Column(db.Integer, primary_key=True)
    # course_device_id = db.Column(db.Integer, db.ForeignKey('course_device.id'))
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id', ondelete='CASCADE'))
    run_id = db.Column(db.Integer, db.ForeignKey('run_info.id', ondelete='CASCADE'))

    data_in_id = db.Column(db.Integer, db.ForeignKey('data_in.id'))

    diff = db.Column(db.BigInteger)
    time = db.Column(db.BigInteger)
    rank = db.Column(db.Integer)
    speed = db.Column(db.Float)
    sectortime = db.Column(db.BigInteger)
    sectordiff = db.Column(db.BigInteger)
    sectorrank = db.Column(db.Integer)


class ResultApproved(db.Model):
    __tablename__ = 'result_approved'
    __bind_key__ = 'shorttrack'
    id = db.Column(db.Integer, primary_key=True)
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id', ondelete='CASCADE'))
    run_id = db.Column(db.Integer, db.ForeignKey('run_info.id', ondelete='CASCADE'))
    # status = db.Column(db.Integer, db.ForeignKey('status.id', ondelete='CASCADE'))
    diff = db.Column(db.BigInteger)
    time = db.Column(db.BigInteger)
    rank = db.Column(db.Integer)
class Device(db.Model):
    __bind_key__ = 'shorttrack'
    __tablename__ = 'course_device'
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('race.id', ondelete='CASCADE'))
    order = db.Column(db.Integer)
    src_dev = db.Column(db.String)
    name = db.Column(db.String)

class DataIn(db.Model):
    __bind_key__ = 'shorttrack'
    __tablename__ = 'data_in'
    id = db.Column(db.Integer, primary_key=True)