from.models import Race,RaceCompetitor, ResultApproved, ResultDetail,RunOrder, CourseDevice, CourseDeviceType
from .. import db
from sqlalchemy import or_, and_, asc
import datetime, json


from .jsonencoder import AlchemyEncoder

class DataViewer:
    race = None
    def __init__(self, race, run):
        self.race = race
        self.run = run

class SummationResults(DataViewer):
    def __init__(self, race, run):
        super().__init__(race, run)

    def get_run_result(self):
        return

class SingleResults(DataViewer):
    def __init__(self, race, run):
        super().__init__(race, run)

    def get_run_result(self):
        return

    def get_commpetitor_result(self, current_result):
        return {
            'time': timeConverter(current_result.time),
            'diff': timeConverter(current_result.diff),
            'rank': current_result.rank,
            'race_competitor_id': current_result.race_competitor_id
        }

class DataViewFactory:
    @staticmethod
    def get_result(run):
        race = Race.query.get(run.race_id)

        if race.result_function == 1:
            return SummationResults(race, run)
        else:
            return SingleResults(race, run)


def timeConverter(time, format='%M:%S.%f'):
    try:
        dt = datetime.datetime(2018, 1, 1)
        dt.timestamp()
        return (datetime.datetime.fromtimestamp(dt.timestamp()+time/1000)).strftime(format)[:-3]
    except:
        return None
    # return time
def speedConverter(speed):
    try:
        return '%.3f' % round(speed, 3)
    except:
        return None
    # return time




def ConvertCompetitorStart(resultDetail, courseDevice, dataIn):
    return {
        resultDetail.race_competitor_id:
            {
                'sectortime': timeConverter(resultDetail.sectortime),
                'sectordiff': timeConverter(resultDetail.sectordiff),
                'time': timeConverter(resultDetail.time),
                'diff': timeConverter(resultDetail.diff),
                'rank': resultDetail.rank,
                'sectorrank': resultDetail.sectorrank,
                'speed': speedConverter(resultDetail.speed),
                'absoluttime': timeConverter(resultDetail.absolut_time, '%H:%M:%S.%f'),
                'course_device_id': courseDevice.id,
                'data_in_id': dataIn.id
            }
    }
def ConvertCompetitorFinish(resultDetail, courseDevice, resultApproved, dataIn):
    return {
        resultDetail.race_competitor_id:
            {
                'sectortime': timeConverter(resultDetail.sectortime),
                'sectordiff': timeConverter(resultDetail.sectordiff),
                'time': timeConverter(resultDetail.time),
                'diff': timeConverter(resultDetail.diff),
                'rank': resultDetail.rank,
                'sectorrank': resultDetail.sectorrank,
                'speed':  speedConverter(resultDetail.speed),
                'absoluttime': timeConverter(resultDetail.absolut_time, '%H:%M:%S.%f'),
                'course_device_id': courseDevice.id,
                'status_id': resultApproved.status_id,
                'data_in_id': dataIn.id
            }
    }

def ConvertCompetitorsRankList(result_details, courseDevice):
    rank_list = {}
    for item in result_details:
        rank_list[item.race_competitor_id] = {
            'sectorrank': item.sectorrank,
            'rank': item.rank,
        }
    return {courseDevice.id: rank_list}

# def TreeView(run_id):
#     tree_view = {}
#     manual_list = []
#     data = db.session.query(ResultApproved, ResultDetail, CourseDevice, CourseDeviceType). \
#         join(ResultDetail, and_(ResultApproved.race_competitor_id == ResultDetail.race_competitor_id, ResultDetail.run_id == run_id), isouter=True). \
#         join(CourseDevice, CourseDevice.id == ResultDetail.course_device_id, isouter=True). \
#         join(CourseDeviceType, CourseDevice.course_device_type_id == CourseDeviceType.id, isouter=True). \
#         filter(ResultApproved.run_id == run_id,  or_(ResultApproved.status_id == None, ResultApproved.status_id == 1)).\
#         order_by(asc(CourseDevice.order)).\
#         all()
#
#     if len(data) > 0:
#         for item in data:
#             try:
#                 if item[2].course_id not in tree_view.keys():
#                     tree_view[item[2].course_id] = {}
#                 if item[2].order not in tree_view[item[2].course_id].keys():
#                     tree_view[item[2].course_id][item[2].order] = {}
#                 if item[0].race_competitor_id not in tree_view[item[2].course_id][item[2].order].keys():
#                     tree_view[item[2].course_id][item[2].order][item[0].race_competitor_id] = item
#             except:
#                 if item[0].is_manual:
#                     manual_list.append(item)
#         return tree_view, manual_list, []
#     return {}, [], []

def TreeView(run_id):
    tree_view = {}
    manual_list = {}
    dql_list = {}
    data = db.session.query(ResultApproved, ResultDetail, CourseDevice, CourseDeviceType, RunOrder). \
        join(ResultDetail, and_(ResultApproved.race_competitor_id == ResultDetail.race_competitor_id, ResultDetail.run_id == run_id), isouter=True). \
        join(CourseDevice, CourseDevice.id == ResultDetail.course_device_id, isouter=True). \
        join(CourseDeviceType, CourseDevice.course_device_type_id == CourseDeviceType.id, isouter=True). \
        join(RunOrder, and_(RunOrder.race_competitor_id == ResultApproved.race_competitor_id, RunOrder.run_id == run_id), isouter=True). \
        filter(ResultApproved.run_id == run_id).\
        order_by(asc(CourseDevice.order)).\
        all()
    if len(data) > 0:
        for item in data:
            try:
                if item[0].is_manual and item[0].status_id !=1:
                    if item[4].course_id not in dql_list.keys():
                        dql_list[item[4].course_id] = []
                    dql_list[item[4].course_id].append(item)
                else:
                    if item[2].course_id not in tree_view.keys():
                        tree_view[item[2].course_id] = {}
                    if item[2].order not in tree_view[item[2].course_id].keys():
                        tree_view[item[2].course_id][item[2].order] = {}
                    if item[0].race_competitor_id not in tree_view[item[2].course_id][item[2].order].keys():
                        tree_view[item[2].course_id][item[2].order][item[0].race_competitor_id] = item
            except:
                if item[0].is_manual:
                    if item[4].course_id not in dql_list.keys():
                        manual_list[item[4].course_id] = []
                    manual_list[item[4].course_id].append(item)
        return tree_view, manual_list, dql_list
    return {}, [], []

def TreeView2(run_id):
    tree_view = {}
    manual_list = []

    data = db.session.query(ResultApproved, ResultDetail, CourseDevice, CourseDeviceType, RunOrder). \
        join(ResultDetail, and_(ResultApproved.race_competitor_id == ResultDetail.race_competitor_id, ResultDetail.run_id == run_id), isouter=True). \
        join(CourseDevice, CourseDevice.id == ResultDetail.course_device_id, isouter=True). \
        join(CourseDeviceType, CourseDevice.course_device_type_id == CourseDeviceType.id, isouter=True). \
        join(RunOrder, and_(ResultApproved.race_competitor_id == RunOrder.race_competitor_id, RunOrder.run_id == run_id), isouter=True). \
        filter(ResultApproved.run_id == run_id,  or_(ResultApproved.status_id == None, ResultApproved.status_id == 1)).\
        order_by(asc(CourseDevice.order)).\
        all()
    if len(data) > 0:
        for item in data:
            try:

                if item[2].course_id not in tree_view.keys():
                    tree_view[item[2].course_id] = {}
                if item[2].order not in tree_view[item[2].course_id].keys():
                    tree_view[item[2].course_id][item[2].order] = {}
                if item[0].race_competitor_id not in tree_view[item[2].course_id][item[2].order].keys():
                    tree_view[item[2].course_id][item[2].order][item[0].race_competitor_id] = item
            except:
                if item[0].is_manual:
                    manual_list.append(item)
        for item in manual_list:
            keys = list(tree_view[item[4].course_id].keys())
            tree_view[item[4].course_id][keys[0]][item[0].race_competitor_id] = item
            tree_view[item[4].course_id][keys[-1]][item[0].race_competitor_id] = item

        return tree_view
    return {}



def ConvertRunResults(tree_view, manual_list, dql_list):
    courses_id = list(tree_view.keys())
    for course_id in courses_id:
        keys = list(tree_view[course_id].keys())
        for device_number in keys[:-1]:
            for competitor_id in tree_view[course_id][device_number]:
                result_item = {
                    'sectorrank': tree_view[course_id][device_number][competitor_id][1].sectorrank,
                    'sectortime': timeConverter(tree_view[course_id][device_number][competitor_id][1].sectortime),
                    'sectordiff': timeConverter(tree_view[course_id][device_number][competitor_id][1].sectordiff),
                    'rank': tree_view[course_id][device_number][competitor_id][1].rank,
                    'time': timeConverter(tree_view[course_id][device_number][competitor_id][1].time),
                    'diff': timeConverter(tree_view[course_id][device_number][competitor_id][1].diff),
                    'speed': speedConverter(tree_view[course_id][device_number][competitor_id][1].speed),
                    'absoluttime': timeConverter(tree_view[course_id][device_number][competitor_id][1].absolut_time, '%H:%M:%S.%f'),
                }
                tree_view[course_id][device_number][competitor_id] = result_item

        for competitor_id in tree_view[course_id][keys[-1]]:
            if tree_view[course_id][keys[-1]][competitor_id][0].is_finish is True:
                result_item = {
                    'sectorrank': tree_view[course_id][keys[-1]][competitor_id][1].sectorrank,
                    'sectortime': timeConverter(tree_view[course_id][keys[-1]][competitor_id][1].sectortime),
                    'sectordiff': timeConverter(tree_view[course_id][keys[-1]][competitor_id][1].sectordiff),
                    'rank': tree_view[course_id][keys[-1]][competitor_id][0].rank,
                    'time': timeConverter(tree_view[course_id][keys[-1]][competitor_id][0].time+tree_view[course_id][keys[-1]][competitor_id][0].adder_time),
                    # 'diff': timeConverter(tree_view[course_id][keys[-1]][competitor_id][0].diff+tree_view[course_id][keys[-1]][competitor_id][0].adder_diff),
                    'speed': speedConverter(tree_view[course_id][keys[-1]][competitor_id][1].speed),
                    'absoluttime': timeConverter(tree_view[course_id][keys[-1]][competitor_id][1].absolut_time, '%H:%M:%S.%f'),
                    'status_id': tree_view[course_id][keys[-1]][competitor_id][0].status_id
                }
                try:
                    result_item['diff'] = timeConverter(tree_view[course_id][keys[-1]][competitor_id][0].diff+tree_view[course_id][keys[-1]][competitor_id][0].adder_diff)
                except:
                    result_item['diff'] = None
                tree_view[course_id][keys[-1]][competitor_id] = result_item
            else:
                tree_view[course_id][keys[-1]][competitor_id] = None
    for key in manual_list:
        keys_list = list(tree_view[key].keys())

        for item in manual_list[key]:

            tree_view[key][keys_list[0]][item[0].race_competitor_id] = {
                'absoluttime': timeConverter(item[0].start_time, '%H:%M:%S.%f'),
                'time': timeConverter(item[0].adder_time),
                'diff': timeConverter(item[0].adder_diff),
            }
            pass
            tree_view[key][keys_list[-1]][item[0].race_competitor_id] = {
                'time': timeConverter(item[0].time+item[0].adder_time),
                'diff': timeConverter(item[0].diff+item[0].adder_diff),
                'absoluttime': timeConverter(item[0].finish_time, '%H:%M:%S.%f'),
                'status_id': item[0].status_id,
                'rank': item[0].rank,
                'is_manual': item[0].is_manual
            }
    for key in dql_list:
        keys_list = list(tree_view[key].keys())
        for item in dql_list[key]:
            tree_view[key][keys_list[-1]][item[0].race_competitor_id] = {
            'status_id': item[0].status_id,
            'is_manual': item[0].is_manual,
            'reason': item[0].reason,
            'gate': item[0].gate
            }

    return tree_view


def ConvertErrorData(dataIn):
    return {
        'id': dataIn.id,
        'run_id': dataIn.run_id,
        'src_sys': dataIn.src_sys,
        'src_dev': dataIn.src_dev,
        'event_code': dataIn.event_code,
        'time': dataIn.time,
        'cource_device_id': dataIn.cource_device_id

    }