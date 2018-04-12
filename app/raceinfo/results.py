from . import raceinfo, jsonencoder
from .models import Race, ResultDetail, RunInfo
from .. import db
from sqlalchemy import func
import json


@raceinfo.route('/race/<int:race_id>/results')
def race_results(race_id):
    race = Race.query.filter(Race.id == race_id).one()
    if race.result_function == 1:
        return Sum_of_runs(race)
    elif race.result_function == 2:
        return The_best_one(race)
    elif race.result_function == 3:
        return The_sum_of_two_best_runs(race)
    elif race.result_function == 4:
        return The_sum_of_three_best_runs()
    return ''

def Sum_of_runs(race):
    result_list = db.session.query(ResultDetail.race_competitor_id, func.count(ResultDetail.id), func.sum(ResultDetail.time).label('total')).join(RunInfo). \
        filter(ResultDetail.time != None, RunInfo.race_id == race.id).\
        group_by(ResultDetail.race_competitor_id).order_by(func.count(ResultDetail.id).desc(),func.sum(ResultDetail.time).asc()).all()
    return ''

def The_best_one(race):
    result_list = db.session.query(ResultDetail.race_competitor_id, func.count(ResultDetail.id), func.min(ResultDetail.time).label('total')).join(RunInfo). \
        filter(ResultDetail.time != None, RunInfo.race_id == race.id).\
        group_by(ResultDetail.race_competitor_id).order_by(func.count(ResultDetail.id).desc(),func.sum(ResultDetail.time).asc()).all()
    return ''

def The_sum_of_two_best_runs(race):
    result_list = db.session.query(ResultDetail.race_competitor_id, func.count(ResultDetail.id), func.min(ResultDetail.time).label('total')).join(RunInfo). \
        filter(ResultDetail.time != None, RunInfo.race_id == race.id).\
        group_by(ResultDetail.race_competitor_id).having(func.count(ResultDetail.id)<=2).order_by(func.count(ResultDetail.id).desc(),func.sum(ResultDetail.time).asc()).all()
    return ''

def The_sum_of_three_best_runs():
    pass


@raceinfo.route('ralts')
def race_resul32ts():
    return str('bla')