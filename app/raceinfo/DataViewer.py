from.models import Race,RaceCompetitor, ResultApproved, ResultDetail,RunInfo
from .. import db
import datetime
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

    def get_commpetitor_result(self, current_result):
        db_results = db.session.query(ResultApproved.time.label('time'),
                                      ResultApproved.diff.label('diff')).\
            order_by(RunInfo.number.desc()).\
            filter(RunInfo.number < self.run.number, ResultApproved.run_id == RunInfo.id,
                   ResultApproved.race_competitor_id == current_result.race_competitor_id).\
            first()
        return {
            'time': formatTime(db_results.time + current_result.time),
            'diff': formatTime(db_results.diff + current_result.diff),
            'rank': current_result.rank,
            'race_competitor_id': current_result.race_competitor_id
        }

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
    dt = datetime.datetime(2018, 1, 1)
    dt.timestamp()
    return (datetime.datetime.fromtimestamp(dt.timestamp()+time/1000)).strftime(format)[:-3]
    # return time

def ConvertRunResults(tree_view):
    for device_number in tree_view:
        for competitor_id in tree_view[device_number]:
            result_item = {
                'sectorrank': tree_view[device_number][competitor_id][0].sectorrank,
                'sectortime': timeConverter(tree_view[device_number][competitor_id][0].sectortime),
                'sectordiff': timeConverter(tree_view[device_number][competitor_id][0].sectordiff),
                'rank': tree_view[device_number][competitor_id][0].rank,
                'time': timeConverter(tree_view[device_number][competitor_id][0].time),
                'diff': timeConverter(tree_view[device_number][competitor_id][0].diff),
                'speed': tree_view[device_number][competitor_id][0].speed,
                'absoluttime': timeConverter(tree_view[device_number][competitor_id][0].absolut_time, '%H:%M:%S.%f'),
            }
            tree_view[device_number][competitor_id] = result_item
    return tree_view


def ConvertCompetitorStart(resultDetail, courseDevice):
    return {
        resultDetail.race_competitor_id:
            {
                'sectortime': timeConverter(resultDetail.sectortime),
                'sectordiff': timeConverter(resultDetail.sectordiff),
                'time': timeConverter(resultDetail.time),
                'diff': timeConverter(resultDetail.diff),
                'rank': resultDetail.rank,
                'sectorrank': resultDetail.sectorrank,
                'speed': resultDetail.speed,
                'absoluttime': timeConverter(resultDetail.absolut_time, '%H:%M:%S.%f'),
                'course_device_id': courseDevice.id
            }
    }

def ConvertCompetitorsRankList(result_details):
    rank_list = {}
    for item in result_details:
        rank_list[item.race_competitor_id] = {
            'sectorrank': item.sectorrank,
            'rank': item.rank,
        }
    return rank_list