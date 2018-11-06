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
    points = db.Column(db.Float)
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
    distance = db.Column(db.Integer)
    description = db.Column(db.String)
    competitors_in_group = db.Column(db.Integer)

class RunInfo(db.Model):
    __tablename__ = 'run_info'
    __bind_key__ = 'shorttrack'
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('race.id', ondelete='CASCADE'))
    number = db.Column(db.Integer)
    name = db.Column(db.String)
    starttime = db.Column(db.DateTime)
    endtime = db.Column(db.DateTime)


class RunGroup(db.Model):
    __tablename__ = 'run_group'
    __bind_key__ = 'shorttrack'
    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.Integer, db.ForeignKey('run_info.id', ondelete='CASCADE'))
    number = db.Column(db.Integer)
    is_start = db.Column(db.Boolean)
    is_finish = db.Column(db.Boolean)

class RunOrder(db.Model):
    __bind_key__ = 'shorttrack'
    __tablename__ = 'run_order'
    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.Integer, db.ForeignKey('run_info.id', ondelete='CASCADE'))
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id', ondelete='CASCADE'))
    order = db.Column(db.Integer)
    group_id = db.Column(db.Integer, db.ForeignKey('run_group.id', ondelete='CASCADE'))

class ResultDetail(db.Model):
    __tablename__ = 'result_detail'
    __bind_key__ = 'shorttrack'

    id = db.Column(db.Integer, primary_key=True)
    virtual_device_id = db.Column(db.Integer, db.ForeignKey('virtual_devices.id', ondelete='CASCADE' ))
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id', ondelete='CASCADE'))
    run_id = db.Column(db.Integer, db.ForeignKey('run_info.id', ondelete='CASCADE'))
    group_id = db.Column(db.Integer, db.ForeignKey('run_group.id', ondelete='CASCADE'))
    data_in_id = db.Column(db.Integer, db.ForeignKey('data_in.id'))
    diff = db.Column(db.Time)
    time = db.Column(db.Time)
    rank = db.Column(db.Integer)
    speed = db.Column(db.Float)
    sectortime = db.Column(db.BigInteger)
    sectordiff = db.Column(db.BigInteger)
    grouprank = db.Column(db.Integer)

    is_first = db.Column(db.Boolean)


class ResultApproved(db.Model):
    __tablename__ = 'result_approved'
    __bind_key__ = 'shorttrack'
    id = db.Column(db.Integer, primary_key=True)
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id', ondelete='CASCADE'))
    run_id = db.Column(db.Integer, db.ForeignKey('run_info.id', ondelete='CASCADE'))
    group_id = db.Column(db.Integer, db.ForeignKey('run_group.id', ondelete='CASCADE'))
    status = db.Column(db.Integer, db.ForeignKey('status.id', ondelete='CASCADE'))
    diff = db.Column(db.Time)
    time = db.Column(db.Time)
    rank = db.Column(db.Integer)
    is_photoinish = db.Column(db.Boolean)

class Device(db.Model):
    __bind_key__ = 'shorttrack'
    __tablename__ = 'course_device'
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('race.id', ondelete='CASCADE'))
    order = db.Column(db.Integer)
    src_dev = db.Column(db.String)
    name = db.Column(db.String)

class VirtualDevice(db.Model):
    __bind_key__ = 'shorttrack'
    __tablename__ = 'virtual_devices'
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('race.id', ondelete='CASCADE'))
    order = db.Column(db.Integer)
    distance = db.Column(db.Integer)
    is_finish = db.Column(db.Boolean)

class DataIn(db.Model):
    __bind_key__ = 'shorttrack'
    __tablename__ = 'data_in'
    id = db.Column(db.Integer, primary_key=True)
    transponder = db.Column(db.String)
    src_dev = db.Column(db.String)
    time = db.Column(db.Time)

class JuryType(db.Model):
    __bind_key__ = 'shorttrack'
    __tablename__ = 'jury_type'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    description = db.Column(db.String)
    @staticmethod
    def insert():
        Types = [
            'Referee', 'Assistant Referee', 'Assistant Referee Video',
             'Starter', 'Competitors Steward', 'Heat Box Steward',
             'Photo Finish Judge', 'Lap Scorer', 'Lap Recorder',
             'Announcer', 'Track steward', 'Technical Delegate',
             'Chief Finish Line Judge', 'Finish Line Judge',
             'Chief Timekeeper', 'Timekeeper'
         ]
        for t in Types:
            type = JuryType.query.filter_by(type=t).first()
            if type is None:
                type = JuryType(type=t)
            db.session.add(type)
        db.session.commit()


class Jury(db.Model):
    __bind_key__ = 'shorttrack'
    __tablename__ = 'jury'
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('race.id', ondelete='CASCADE'))
    type_id = db.Column(db.Integer, db.ForeignKey('jury_type.id'))
    ru_lastname = db.Column(db.String)
    ru_firstname = db.Column(db.String)
    en_lastname = db.Column(db.String)
    en_firstname = db.Column(db.String)

    event_code = db.Column(db.String)


class Status(db.Model):
    __tablename__ = 'status'
    __bind_key__ = 'shorttrack'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    @staticmethod
    def insert():
        status = ['QLF', 'QLF-1', 'QLF-2', 'DQL', 'DQL-1', 'DQL-2']
        for d in status:
            stts = Status.query.filter_by(name=d).first()
            if stts is None:
                stts = Status(name=d, description=d)
            db.session.add(stts)
        db.session.commit()


class PhotoFinishData(db.Model):
    __bind_key__ = 'shorttrack'
    __tablename__ = 'photo_finishdata'
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('race.id', ondelete='CASCADE'))
    run_id = db.Column(db.Integer, db.ForeignKey('run_info.id', ondelete='CASCADE'))
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id', ondelete='CASCADE'))
    time = db.Column(db.Time)

class JuryResult(db.Model):
    __bind_key__ = 'shorttrack'
    __tablename__ = 'jury_result'
    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.Integer, db.ForeignKey('run_info.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('run_group.id'))
    jury_id = db.Column(db.Integer, db.ForeignKey('jury.id'))
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id',  ondelete='CASCADE'))
    time = db.Column(db.Time)
    rank = db.Column(db.Integer)



