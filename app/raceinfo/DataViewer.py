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
            'time': formatTime(current_result.time),
            'diff': formatTime(current_result.diff),
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


def formatTime(time):
    return (datetime.datetime.fromtimestamp(time/1000)).strftime('%M:%S.%f')[:-3]
