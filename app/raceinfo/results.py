from . import raceinfo, jsonencoder
from .models import Race, Discipline, RunInfo, RaceCompetitor, ResultApproved, Competitor, Status
from .. import db
from sqlalchemy import func
from .DataViewer import timeConverter
import json



@raceinfo.route('/race/<int:race_id>/results')
def race_results(race_id):
    RaceCompetitor.query.\
       filter(RaceCompetitor.race_id == race_id).\
       update(
        {
            'rank': None,
            'reason': None,
            'status_id': None,
            'diff': None,
            'time': None,
            'gate': None
        })
    db.session.commit()

    race = db.session.query(Race, Discipline).join(Discipline, Discipline.id == Race.discipline_id).filter(Race.id == race_id).one()

    Competitors_list = db.session.query(RaceCompetitor, Competitor).join(Competitor).filter(RaceCompetitor.race_id == race_id).all()
    QLF_list=[]
    if race[1].is_combination:
        QLF_list = Sum_of_runs_Combination(race[0],
                               db.session.query(func.count(RunInfo.id)).filter(RunInfo.race_id == race_id).scalar())
    elif race[0].result_function == 1:
        QLF_list = Sum_of_runs(race[0], db.session.query(func.count(RunInfo.id)).filter(RunInfo.race_id == race_id).scalar())
    elif race[0].result_function == 2:
        QLF_list = The_best_one(race[0])
    elif race[0].result_function == 3:
        QLF_list = The_sum_of_two_best_runs(race[0])
    elif race[0].result_function == 4:
        QLF_list = The_sum_of_three_best_runs(race[0])

    QLF_competitors = [item[0] for item in QLF_list]

    DNQ_list = db.session.query(ResultApproved.status_id.label('status_id'),
                                ResultApproved.reason.label('reason'),
                                ResultApproved.gate.label('gate'),
                                ResultApproved.race_competitor_id.label('race_competitor_id')).\
        filter(ResultApproved.race_competitor_id.notin_(QLF_competitors),
               ResultApproved.run_id == RunInfo.id, RunInfo.race_id == race_id, ResultApproved.status_id != 1).all()
    set_results_to_DB(QLF_list, DNQ_list, Competitors_list)

    return get_results(race_id, Competitors_list)

def Sum_of_runs_Combination(race, run_count):
    QLF_list = db.session.query(ResultApproved.race_competitor_id, func.count(ResultApproved.id), func.sum(ResultApproved.time).label('total')).\
        join(RunInfo). \
        filter(ResultApproved.time != None, RunInfo.race_id == race.id, ResultApproved.status_id == 1).\
        group_by(ResultApproved.race_competitor_id).having(func.count(ResultApproved.id) == run_count).order_by(func.count(ResultApproved.id).asc(), func.sum(ResultApproved.time).asc()).all()
    return QLF_list

def Sum_of_runs(race, run_count):
    QLF_list = db.session.query(ResultApproved.race_competitor_id, func.count(ResultApproved.id), func.min(ResultApproved.time).label('total')).\
        join(RunInfo). \
        filter(ResultApproved.time != None, RunInfo.race_id == race.id, ResultApproved.status_id == 1).\
        group_by(ResultApproved.race_competitor_id).having(func.count(ResultApproved.id) == run_count).order_by(func.count(ResultApproved.id).asc(), func.max(ResultApproved.time).asc()).all()
    return QLF_list

# Никак

def The_best_one(race):
    QLF_list = db.session.query(ResultApproved.race_competitor_id, func.count(ResultApproved.id), func.min(ResultApproved.time).label('total')).\
        join(RunInfo). \
        filter(ResultApproved.time != None, RunInfo.race_id == race.id, ResultApproved.status_id==1).\
        group_by(ResultApproved.race_competitor_id).order_by(func.min(ResultApproved.time).asc()).all()
    return QLF_list

# Никак

def The_sum_of_two_best_runs(race):
    result_list = db.session.query(ResultApproved.race_competitor_id, ResultApproved.time).\
        join(RunInfo). \
        filter(ResultApproved.time != None, RunInfo.race_id == race.id, ResultApproved.status_id==1).\
        order_by(ResultApproved.race_competitor_id.asc(), ResultApproved.time.asc()).all()
    total_result =[]
    succes_runs = 0
    points = 0
    previous_competitor = result_list[0][0]
    for item in result_list:
        if previous_competitor == item[0]:
            if succes_runs != 2:
                points += item[1]
                succes_runs += 1
            else:
                continue
        else:
            if succes_runs == 2:
                total_result.append([previous_competitor, succes_runs, points])
            previous_competitor = item[0]
            points = item[1]
            succes_runs = 1
    if succes_runs == 2:
        total_result.append([previous_competitor, succes_runs, points])
    total_result = sorted(total_result, key=lambda item: item[2])
    return total_result

# Если спортсмен не QLF, то не участвует в формированиие в последующем заезде, остальные
# сортирутся по rank в обратном порядке
#
def The_sum_of_three_best_runs(race):
    result_list = db.session.query(ResultApproved.race_competitor_id, ResultApproved.time).\
        join(RunInfo). \
        filter(ResultApproved.time != None, RunInfo.race_id == race.id, ResultApproved.status_id==1).\
        order_by(ResultApproved.race_competitor_id.asc(), ResultApproved.time.asc()).all()
    total_result = []
    succes_runs = 0
    points = 0
    previous_competitor = result_list[0][0]
    for item in result_list:
        if previous_competitor == item[0]:
            if succes_runs != 3:
                points += item[1]
                succes_runs += 1
            else:
                continue
        else:
            if succes_runs == 3:
                total_result.append([previous_competitor, succes_runs, points])
            previous_competitor = item[0]
            points = item[1]
            succes_runs = 1
    if succes_runs == 3:
        total_result.append([previous_competitor, succes_runs, points])
    return total_result


# def set_results_to_DB(result_list, competitor_list, lose_competitors, key=None):
#     best_competitor = next((item for item in competitor_list if result_list[0][0] == item[0].id), None)
#
#     for index, result in enumerate(result_list):
#         competitor_item = next((item for item in competitor_list if result[0] == item[0].id), None)
#         if key(result):
#             competitor_item[0].rank = index+1
#             competitor_item[0].time = result[2]
#             competitor_item[0].diff = result[2] - best_competitor[0].time
#             competitor_item[0].status_id = 1
#
def set_results_to_DB(QLF_list, DNQ_list, Competitors_list):

    best_competitor = next((item for item in Competitors_list if QLF_list[0][0] == item[0].id), None)

    for index, result in enumerate(QLF_list):
        competitor_item = next((item for item in Competitors_list if result[0] == item[0].id), None)
        competitor_item[0].rank = index+1
        competitor_item[0].time = result[2]
        competitor_item[0].diff = result[2] - best_competitor[0].time
        competitor_item[0].status_id = 1
    for result in DNQ_list:
        competitor_item = next((item for item in Competitors_list if result.race_competitor_id == item[0].id), None)
        competitor_item[0].status_id = result.status_id
        competitor_item[0].reason = result.reason
        competitor_item[0].gate = result.gate

@raceinfo.route('/race/<int:race_id>/results/get')
def get_results(race_id, competitorList = None):
    if competitorList is None:
        competitorList = db.session.query(RaceCompetitor, Competitor).join(Competitor).filter(
            RaceCompetitor.race_id == race_id).all()
    resultApproves = db.session.query(ResultApproved, RunInfo).join(RunInfo).filter(RunInfo.race_id == race_id).all()
    result = []
    statuses = Status.query.all()
    for item in competitorList:
        result_item =dict([
            ('global_rank', item[0].rank),
            ('race_competitor_id', item[0].id),
            ('diff', timeConverter(item[0].diff)),
            ('status_id', item[0].status_id),
            ('bib', item[0].bib),
            ('ru_firstname', item[1].ru_firstname),
            ('en_firstname', item[1].en_firstname),
            ('ru_lastname', item[1].ru_lastname),
            ('en_lastname', item[1].en_lastname)
        ])
        result_item['status']=next((item.name for item in statuses if item.id == result_item['status_id']), None)
        if item[0].time is not None:
            result_item['result_time'] = timeConverter(item[0].time)
        else:
            result_item['result_time'] = None
        approve__result_item = []
        for approve in resultApproves:
            if item[0].id == approve[0].race_competitor_id:
                approve__result_item.append(
                    dict([
                        ('run_id', approve[0].run_id),
                        ('reason', approve[0].reason),
                        ('rank', approve[0].rank),
                        ('gate', approve[0].gate),
                        ('status_id', approve[0].status_id),
                        ('time', timeConverter(approve[0].time)),
                        ('status', next((item.name for item in statuses if item.id == approve[0].status_id), None))
                    ])
                )

        result_item['results'] = approve__result_item
        result.append(result_item)
    result = sorted(result, key=lambda item: (item['global_rank'] is None, item['global_rank']))
    return json.dumps(
        {
            'success': True,
            'data': result
        }
    )

