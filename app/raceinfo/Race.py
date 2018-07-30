from .models import *
from .DataViewer import TreeView
from sqlalchemy import cast, DATE, func, asc, and_, sql

from datetime import datetime

class BaseRace:
    def __init__(self, race=None, runInfo=None, runType=None, discipline=None, courseDevice=None, courseDeviceType=None):
        self.race = race
        self.run = runInfo
        self.runType = runType
        self.discipline = discipline
        self.courseDevice = courseDevice
        self.courseDeviceType = courseDeviceType
        self.competitor = None
        self.data_in = None
        self.result = None
        self.resultApprove = None

    def setDeviceDataInDB(self, data):
        self.data_in=DataIn(
            src_sys=data['SRC_SYS'],
            src_dev=data['SRC_DEV'],
            event_code=data['EVENT_CODE'],
            time=data['TIME'],
        )
        if 'BIB' in data:
            self.data_in.bib = data['BIB']
        if self.run is not None:
            self.data_in.run_id = self.run.id
        if self.courseDevice is not None:
            self.data_in.cource_device_id = self.courseDevice.id
        db.session.add(self.data_in)
        db.session.commit()


    def competitor_autostart(self):
        race_competitors = db.session.query(RaceCompetitor, RunOrder). \
            join(RunOrder). \
            filter(RunOrder.run_id == self.run.id, RunOrder.course_id == self.courseDevice.course_id).order_by(RunOrder.order.asc()).all()
        order = sum(item[1].manual_order is not None and item[1].manual_order != 0 for item in race_competitors)

        сompetitor = next(item for item in race_competitors if item[1].manual_order is None)
        сompetitor[1].manual_order = order + 1

        competitor_Approve = ResultApproved(run_id=self.run.id,
                                         is_start=True,
                                         race_competitor_id=сompetitor[0].id)
        db.session.add(сompetitor[1])
        db.session.add(competitor_Approve)
        db.session.commit()
        self.resultApprove = competitor_Approve
        self.competitor = сompetitor[0]

    def competitor_manualstart(self, competitor_id):
        competitor_Approve = ResultApproved(
            race_competitor_id=competitor_id,
            run_id=self.run.id)
        db.session.add(competitor_Approve)
        db.session.commit()
        competitor_order = db.session.query(func.count('*')).select_from(RunOrder). \
                               filter(RunOrder.run_id == self.run.id,
                                      RunOrder.manual_order != None, RunOrder.manual_order != 0). \
                               scalar() + 1
        current_competitor = RunOrder.query.filter(RunOrder.race_competitor_id == competitor_id,
                                                   RunOrder.run_id == self.run.id).one()

        current_competitor.manual_order = competitor_order
        db.session.add(current_competitor)
        db.session.commit()
        self.resultApprove = competitor_Approve


    def competitor_get_current(self):
        competitor_order = db.session.query(func.count('*')).select_from(ResultDetail). \
                               filter(ResultDetail.run_id == self.run.id,
                                      ResultDetail.course_device_id == self.courseDevice.id). \
                               scalar() + 1

        competitor = db.session.query(RaceCompetitor, ResultApproved). \
            join(ResultApproved, and_(RaceCompetitor.id == ResultApproved.race_competitor_id,
                                      ResultApproved.run_id == self.run.id)). \
            filter(RunOrder.race_competitor_id == RaceCompetitor.id,
                   RunOrder.manual_order == competitor_order,
                   RunOrder.run_id == self.run.id, RunOrder.course_id == self.courseDevice.course_id
                   ).first()
        if competitor is not None:
            self.competitor = competitor[0]
            self.resultApprove = competitor[1]

    def competitor_finish(self):
        competitor_Approve = ResultApproved.get(self.competitor.id, self.run.id)
        competitor_Approve.finish_time = self.result.absolut_time
        competitor_Approve.time = competitor_Approve.finish_time - competitor_Approve.start_time
        competitor_Approve.status_id = 1
        competitor_Approve.is_finish = True
        db.session.add(competitor_Approve)
        db.session.commit()
        return competitor_Approve

    def competitor_clear(self, competitor_id):
        competitor_order = RunOrder.get(competitor_id, self.run.id)

        if competitor_order.manual_order is not None:
            next_passed_competitors_list = RunOrder.query.filter(RunOrder.manual_order > competitor_order.manual_order,
                                                     RunOrder.run_id == self.run.id).all()
            if len(next_passed_competitors_list) > 0:
                for item in next_passed_competitors_list:
                    item.manual_order -= 1
                    db.session.add(item)
            competitor_order.manual_order = 0

            db.session.add(competitor_order)
            ResultDetail.remove(competitor_id, self.run.id)

        ResultApproved.remove(competitor_id, self.run.id)
        db.session.commit()
        # recalculate_run_results(request.args.get('run_id'))
        # socketio.emit('removeResult', json.dumps(dict(removed_competitor=request.args.get('competitor_id'))))

    def competitor_autoapprove(self, competitor_id):
        status = Status.query.filter_by(name='QLF').one()
        try:
           resultDetail = ResultApproved.get(competitor_id, self.run.id)
           resultDetail.is_manual = False
           resultDetail.approve_time = datetime.now()
           resultDetail.race_competitor_id = competitor_id
           resultDetail.run_id = self.run.id
           resultDetail.status_id = status.id
           db.session.add(resultDetail)
           db.session.commit()
        except:
           try:
               Result.query.filter_by(race_competitor_id=competitor_id).one()
           except:
               result = Result(race_competitor_id=competitor_id)
               db.session.add(result)
               db.session.commit()

    def competitor_manualapprove(self, competitor_id, status_id, finish_time, start_time, gate, reason):
        try:
            resultApproved = ResultApproved.get(competitor_id, self.run.id)
        except:
            resultApproved = ResultApproved(
                race_competitor_id=competitor_id,
                run_id=self.run.id,
                is_start=False
            )
        resultApproved.is_manual = True
        resultApproved.approve_time = datetime.now()
        resultApproved.status_id = status_id
        try:
            if resultApproved.status_id == '1':
                if self.race.result_function == 1 and self.run.number > 1:
                    resultApproved.set_competitor_adder(self.run.number)

                if resultApproved.is_start == False:
                    competitorOrder = RunOrder.query.filter(RunOrder.race_competitor_id ==competitor_id,
                                                            RunOrder.run_id == self.run.id). \
                        first()
                    competitorOrder.manual_order = 0
                    db.session.add(competitorOrder)
                    db.session.commit()
                if finish_time != '':
                    finish_device = db.session.query(ResultDetail, CourseDevice, CourseDeviceType). \
                        join(CourseDevice). \
                        join(CourseDeviceType). \
                        filter(ResultDetail.race_competitor_id == competitor_id,
                               ResultDetail.run_id == self.run.id, CourseDeviceType == 3). \
                        first()
                    if finish_device is not None:
                        finish_device[0].data_in_id = None
                        finish_device[0].absolute_time = finish_time
                        db.session.add(finish_device)
                    resultApproved.finish_time = finish_time
                if start_time != '':
                    start_device = db.session.query(ResultDetail, CourseDevice, CourseDeviceType). \
                        join(CourseDevice). \
                        join(CourseDeviceType). \
                        filter(ResultDetail.race_competitor_id == competitor_id,
                               ResultDetail.run_id == self.run.id, CourseDeviceType == 1). \
                        first()
                    if start_device is not None:
                        start_device[0].data_in_id = None
                        start_device[0].absolute_time = start_time
                        db.session.add(start_device)
                    resultApproved.start_time = start_time

                resultApproved.time = int(resultApproved.finish_time) - int(resultApproved.start_time)
            else:
                resultApproved.gate = gate
                resultApproved.reason = reason
            db.session.add(resultApproved)
        except:
            return False

        if resultApproved.is_start == True:
            results_list = db.session.query(CourseDevice, ResultDetail). \
                join(ResultDetail, and_(CourseDevice.id == ResultDetail.course_device_id,
                                        ResultDetail.run_id == self.run.id,
                                        ResultDetail.race_competitor_id == competitor_id), isouter=True). \
                filter(CourseDevice.course_id == RunInfo.course_id, RunInfo.id == self.run.id). \
                all()
            for item in results_list:
                if item[1] is None:
                    resultDetail = ResultDetail(
                        run_id=self.run.id,
                        race_competitor_id=competitor_id,
                        course_device_id=item[0].id
                    )
                    db.session.add(resultDetail)
                else:
                    item[0].reset()
        db.session.commit()
        return True

    def set_result_detail(self):
        self.result = ResultDetail(
            course_device_id=self.courseDevice.id,
            run_id=self.run.id,
            time=self.resultApprove.adder_time,
            diff=self.resultApprove.adder_diff,
            data_in_id=self.data_in.id,
            race_competitor_id=self.competitor.id,
            absolut_time=self.data_in.time,
            sectortime=0,
            sectordiff=0,
            is_start=True
        )
    def set_start_result_detail(self):
        self.set_result_detail()
        self.result.time = self.resultApprove.adder_time
        self.result.diff = self.resultApprove.adder_diff

    def calculate_personal_sector_params(self):
        previous_course_device = CourseDevice.query.filter_by(order=self.courseDevice.order-1, course_id=self.courseDevice.course_id).one()
        previous_device_results = db.session.query(ResultDetail).filter(
            ResultDetail.course_device_id == previous_course_device.id,
            ResultDetail.race_competitor_id == self.result.race_competitor_id,
            ResultDetail.run_id == self.result.run_id).one()
        self.result.sectortime = self.result.absolut_time - previous_device_results.absolut_time
        self.result.time = previous_device_results.time + self.result.sectortime
        self.result.speed = ((self.courseDevice.distance - previous_course_device.distance) / 1000) / (self.result.sectortime / 3600000)

    def calculate_common_sector_params(self, competitors_list):
        if len(competitors_list) != 0:
            min_сompetitor_sectortime = min(competitors_list, key=lambda item: item.sectortime)
            min_сompetitor_time = min(competitors_list, key=lambda item: item.time)

            self.result.diff = self.result.time - min_сompetitor_time.time
            self.result.sectordiff = self.result.sectortime - min_сompetitor_sectortime.sectortime

            сompetitors_list_ordered_sectortime = sorted([self.result] + competitors_list,
                                                         key=lambda item: item.sectortime)
            сompetitors_list_ordered_time = sorted([self.result] + competitors_list,
                                                   key=lambda item: item.time)

            for index, (sectortime_item,  time_item) in enumerate(zip(сompetitors_list_ordered_sectortime,
                                                                      сompetitors_list_ordered_time)):
                sectortime_item.sectorrank = index+1
                time_item.rank = index + 1
        else:
            self.result.sectordiff = 0
            self.result.sectorrank = 1
            self.result.diff = 0
            self.result.rank = 1

    def recalculate_run_results(self):
        tree_view, manual_list = TreeView(self.run.id)
        if len(tree_view) > 0:
            courses = list(tree_view.keys())
            for key, item in tree_view[courses[0]].items():
                if key == 1:
                    continue
                else:
                    self.recalculate_sector_results(item, tree_view[courses[0]][key - 1])
            self.recalculate_finished_results()
        return tree_view, manual_list

    def recalculate_sector_results(self, current_results=None, previous_results=None):
        #  пересчитать  параметры speed, sectortime, time
        for competitor_id, current_result_item in current_results.items():
            try:
                current_result_item[1].sectortime = current_result_item[1].absolut_time - previous_results[competitor_id][1].absolut_time
                current_result_item[1].time = current_result_item[1].sectortime + previous_results[competitor_id][1].time
                current_result_item[1].speed = ((current_result_item[2].distance - previous_results[competitor_id][2].distance) / 1000) / (
                    current_result_item[1].sectortime / 3600000)
            except:
                current_result_item[1].sectortime = None
                current_result_item[1].speed = None
                current_result_item[1].time = None

        сompetitors_list_ordered_sectortime = sorted(list(current_results.values()),
                                                     key=lambda item: (item[1].sectortime is None, item[1].sectortime))
        сompetitors_list_ordered_time = sorted(list(current_results.values()),
                                                     key=lambda item: (item[1].time is None, item[1].time))

        sectortime_min_item = next(item for item in сompetitors_list_ordered_sectortime if item[0].status_id == 1)
        time_min_item = next(item for item in сompetitors_list_ordered_time if item[0].status_id == 1)

        for index, (sectortime_item, time_item) in enumerate(zip(сompetitors_list_ordered_sectortime, сompetitors_list_ordered_time)):
            try:
                sectortime_item[1].sectordiff = sectortime_item[1].sectortime - sectortime_min_item[1].sectortime
                sectortime_item[1].sectorrank = index + 1
                time_item[1].diff = time_item[1].time - time_min_item[1].time
                time_item[1].rank = index + 1
            except:
                sectortime_item[1].sectordiff = None
                sectortime_item[1].sectorrank = None
                time_item[1].diff = None
                time_item[1].rank = None

    def recalculate_finished_results(self):
        finish_results = ResultApproved.query.filter(ResultApproved.run_id == self.run.id, ResultApproved.is_finish==True).all()
        сompetitors_list = sorted(finish_results, key=lambda item: (item.time is None,
                                                                    item.status_id is None, item.status_id,
                                                                    item.finish_time - item.start_time+item.adder_time))
        ResultApproved_min_time = min(сompetitors_list, key=lambda item:(item.time))
        for index, item in enumerate(сompetitors_list):
            try:
                if item.status_id == 1:
                    item.time = item.finish_time - item.start_time
                    item.diff = item.time - ResultApproved_min_time.time
                    item.rank = index + 1
                else:
                    item.diff = None
                    item.rank = None
            except:
                item.diff = None
                item.rank = None


    def is_start(self):
        if self.courseDeviceType.name == 'Start':
            return True
        else:
            return False

    def is_point(self):
        if self.courseDeviceType.name == 'Point':
            return True
        else:
            return False
    def is_finish_(self):
        if self.courseDeviceType.name == 'Finish':
            return True
        else:
            return False
    def is_competitor(self):
        if self.competitor is None:
            return False
        else:
            return True
    def get_competitor_info(self):
        return db.session.query(RaceCompetitor.bib.label('bib'),
                                Competitor.en_firstname.label('firstname'),
                                Competitor.en_lastname.label('lastname'),
                         Nation.name.label('country_code')). \
            filter(RaceCompetitor.competitor_id == Competitor.id,
                   Competitor.nation_code_id == Nation.id,
                   RaceCompetitor.id == self.competitor.id).first()

    def start_list_info(self):
        return db.session.query(RunOrder.order.label('order'),
                                RaceCompetitor.bib.label('bib'),
                                Competitor.en_firstname.label('firstname'),
                                Competitor.en_lastname.label('lastname')).\
            filter(RunOrder.race_competitor_id == RaceCompetitor.id,
                   RaceCompetitor.competitor_id == Competitor.id,
                   RunOrder.run_id == self.run.id).all()

    def finish_list_info(self):
        return db.session.query(ResultApproved.rank.label('rank'),
                                RaceCompetitor.bib.label('bib'),
                                Competitor.en_firstname.label('firstname'),
                                Competitor.en_lastname.label('lastname'),
                                ResultApproved.diff.label('diff')). \
            filter(ResultApproved.race_competitor_id == RaceCompetitor.id,
                   RaceCompetitor.competitor_id == Competitor.id,
                   ResultApproved.run_id == self.run.id,
                   ResultApproved.is_finish == True).all()

class ClassicRace(BaseRace):
    def __init__(self, race=None, runInfo=None, runType=None, discipline=None, courseDevice=None, courseDeviceType=None):
        super().__init__(race, runInfo, runType, discipline, courseDevice, courseDeviceType)
        pass

class Combination(ClassicRace):
    def __init__(self, race=None, runInfo=None, runType=None, discipline=None, courseDevice=None, courseDeviceType=None):
        super().__init__( race, runInfo, runType, discipline, courseDevice, courseDeviceType)
        pass

class SummationTimeRace(ClassicRace):
    def __init__(self, race=None, runInfo=None, runType=None, discipline=None, courseDevice=None, courseDeviceType=None):
        super().__init__(race, runInfo, runType, discipline, courseDevice, courseDeviceType)
        pass

    def competitor_autostart(self):
        super().competitor_autostart()
        self.resultApprove.set_competitor_adder(self.run.number)

    def competitor_manualstart(self, competitor_id):
        super().competitor_manualstart(competitor_id)
        self.resultApprove.set_competitor_adder(self.run.number)

class ParallelRace(BaseRace):
    def __init__(self, race=None, runInfo=None, runType=None, discipline=None, courseDevice=None, courseDeviceType=None):
        super().__init__(race, runInfo, runType, discipline, courseDevice, courseDeviceType)
        pass

class QualificationRace(BaseRace):
    def __init__(self, race=None, runInfo=None, runType=None, discipline=None, courseDevice=None, courseDeviceType=None):
        super().__init__(race, runInfo, runType, discipline, courseDevice, courseDeviceType)

    def competitor_autostart(self):
        super().competitor_autostart()
        self.resultApprove.set_competitor_adder(self.run.number)

    def competitor_manualstart(self, competitor_id):
        super().competitor_manualstart(competitor_id)
        self.resultApprove.set_competitor_adder(self.run.number)

    def recalculate_run_results(self):
        tree_view, manual = TreeView(self.run.id)
        if len(tree_view) > 0:
            courses = list(tree_view.keys())
            if len(courses) == 1:
                super().recalculate_run_results()
            else:
                for (key, item), (key2, item_2) in zip(list(tree_view[courses[0]].items()), list(tree_view[courses[1]].items())):
                    if key == 1:
                        continue
                    else:
                        self.recalculate_sector_results({**item, **item_2}, {**tree_view[courses[0]][key-1], **tree_view[courses[1]][key2-1]})
                self.recalculate_finished_results()
        return tree_view, manual

class ForerunnerRace(BaseRace):
    def __init__(self, race=None, runInfo=None, runType=None, discipline=None, courseDevice=None, courseDeviceType=None):
        super().__init__(race, runInfo, runType, discipline, courseDevice, courseDeviceType)
        pass
    def get_competitor_info(self):
        return db.session.query(CourseForerunner.order.label('bib'),
                                Forerunner.en_firstname.label('firstname'),
                                Forerunner.en_lastname.label('lastname'),
                                Nation.name.label('country_code')).\
            filter(RaceCompetitor.forerunner_id == CourseForerunner.id,
                   CourseForerunner.forerunner_id == Forerunner.id,
                   Forerunner.nation_id == Nation.id,
                   RaceCompetitor.id == self.competitor.id).first()
    def start_list_info(self):
        return db.session.query(sql.label('order', RunOrder.order),
                                CourseForerunner.order.label('bib'),
                                Forerunner.en_firstname.label('firstname'),
                                Forerunner.en_lastname.label('lastname'),
                                Nation.name.label('country_code')).\
            filter(RunOrder.race_competitor_id == RaceCompetitor.id,
                   RaceCompetitor.forerunner_id == CourseForerunner.id,
                   RunOrder.run_id == self.run.id).all()

    def finish_list_info(self):
        return db.session.query(ResultApproved.rank.label('rank'),
                                RaceCompetitor.bib.label('bib'),
                                Forerunner.en_firstname.label('firstname'),
                                Forerunner.en_lastname.label('lastname'),
                                ResultApproved.diff.label('diff')).\
            filter(ResultApproved.race_competitor_id == RaceCompetitor.id,
                   RaceCompetitor.competitor_id == CourseForerunner.id,
                   CourseForerunner.forerunner_id == Forerunner.id,
                   ResultApproved.run_id == self.run.id,
                   ResultApproved.is_finish == True).all()
class RaceGetter:

    @staticmethod
    def getRace(device_data=None, run_id=None):
        """
        :param device_data:
        :return: BaseRace object
        """

        print(device_data)
        race_info = db.session.query(RunInfo,
                                     CourseDeviceType,
                                     CourseDevice,
                                     Course,
                                     RunType,
                                     Race,
                                     Discipline,
                                     ).filter(
            Device.src_dev == device_data['SRC_DEV'],
            Device.id == CourseDevice.device_id,
            CourseDevice.course_device_type_id == CourseDeviceType.id,
            CourseDevice.course_id == RunCourses.course_id,
            Course.id==RunCourses.course_id,
            RunCourses.run_id == RunInfo.id,
            RunInfo.starttime < datetime.now(),
            RunInfo.endtime == None,
            RunInfo.run_type_id == RunType.id,
            RunInfo.race_id == Race.id,
            Race.discipline_id == Discipline.id
        ).one()


        if race_info[4].is_forerunner:
            print('ForerunnerRace')
            return ForerunnerRace(race=race_info[5],
                                  runInfo=race_info[0],
                                  runType=race_info[4],
                                  discipline=race_info[6],
                                  courseDevice=race_info[2],
                                  courseDeviceType=race_info[1])
        elif race_info[6].is_parallel:
            if race_info[4].is_qualification:
                print('QualificationRace')
                return QualificationRace(race=race_info[5],
                                         runInfo=race_info[0],
                                         runType=race_info[4],
                                         discipline=race_info[6],
                                         courseDevice=race_info[2],
                                         courseDeviceType=race_info[1])
            else:
                print('ParallelRace')
                return ParallelRace(race=race_info[5],
                                         runInfo=race_info[0],
                                         runType=race_info[4],
                                         discipline=race_info[6],
                                         courseDevice=race_info[2],
                                         courseDeviceType=race_info[1])
        elif race_info[6].is_combination:
            print('Combination')
            return Combination(race=race_info[5],
                                     runInfo=race_info[0],
                                     runType=race_info[4],
                                     discipline=race_info[6],
                                     courseDevice=race_info[2],
                                     courseDeviceType=race_info[1])
        elif race_info[5].result_function == 1:
            print('SummationTimeRace')
            return SummationTimeRace(race=race_info[5],
                                     runInfo=race_info[0],
                                     runType=race_info[4],
                                     discipline=race_info[6],
                                     courseDevice=race_info[2],
                                     courseDeviceType=race_info[1])
        else:
            print('ClassicRace')
            return ClassicRace(race=race_info[5],
                                     runInfo=race_info[0],
                                     runType=race_info[4],
                                     discipline=race_info[6],
                                     courseDevice=race_info[2],
                                     courseDeviceType=race_info[1])

    @staticmethod
    def getRaceByRunid(run_id=None):
        """
        :param device_data:
        :return: BaseRace object
        """
        race_info = db.session.query(RunInfo,
                                     Course,
                                     RunType,
                                     Race,
                                     Discipline,
                                     ).filter(
            Course.id == RunCourses.course_id,
            RunCourses.run_id == RunInfo.id,
            RunInfo.run_type_id == RunType.id,
            RunInfo.race_id == Race.id,
            Race.discipline_id == Discipline.id,
            RunInfo.id == run_id
        ).one()

        if race_info[0].run_type_id == 3:
            print('ForerunnerRace')
            return ForerunnerRace(race=race_info[3],
                                  runInfo=race_info[0],
                                  runType=race_info[2],
                                  discipline=race_info[4])

        elif race_info[4].is_parallel:
            if race_info[2].is_qualification:
                print('QualificationRace')
                return QualificationRace(race=race_info[3],
                                         runInfo=race_info[0],
                                         runType=race_info[2],
                                         discipline=race_info[4])
            else:
                print('ParallelRace')
                return ParallelRace(race=race_info[3],
                                    runInfo=race_info[0],
                                    runType=race_info[2],
                                    discipline=race_info[4])
        elif race_info[4].is_combination:
            print('Combination')
            return Combination(race=race_info[3],
                               runInfo=race_info[0],
                               runType=race_info[2],
                               discipline=race_info[4])
        elif race_info[3].result_function == 1:
            print('SummationTimeRace')
            return SummationTimeRace(race=race_info[3],
                                     runInfo=race_info[0],
                                     runType=race_info[2],
                                     discipline=race_info[4])
        else:
            print('ClassicRace')
            return ClassicRace(race=race_info[3],
                               runInfo=race_info[0],
                               runType=race_info[2],
                               discipline=race_info[4])