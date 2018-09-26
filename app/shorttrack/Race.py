from .models import *
from . import shorttrack
from .. import db_shorttrack as db
from datetime import timedelta, datetime, time, date
from sqlalchemy import or_, func, distinct
import json
import pyexcel

from  flask import request, flash, redirect,url_for

TIME_DELTA = timedelta(seconds=4)


class ShrortTrack:
    def __init__(self, device_data):
        print(device_data)
        race_info = db.session.query(RunInfo,
                                     RunGroup,
                                     Device,
                                     Race,
                                     Competitor
                                     ).filter(
            Device.src_dev == device_data['SRC_DEV'],
            Device.race_id == Race.id,
            Race.id == RunInfo.race_id,
            RunInfo.starttime < datetime.now(),
            RunInfo.endtime == None,
            RunInfo.id == RunGroup.run_id,
            RunGroup.is_start == True,
            RunGroup.is_finish == None,
            or_(Competitor.transponder_1 == device_data['TRANSPONDER'],
                Competitor.transponder_2 == device_data['TRANSPONDER'])
        ).one()

        self.runInfo = race_info[0]
        self.runGroup = race_info[1]
        self.device = race_info[2]
        self.race = race_info[3]
        self.competitor = race_info[4]
        self.isDataForSend=True
        self.dataIn = None
        self.virtualDevice = None

        self.resultDetail = None
        self.resultDetailList = None

    def setDataIn(self, device_data):
        self.dataIn = DataIn(
            transponder=device_data['TRANSPONDER'],
            src_dev=device_data['SRC_DEV'],
            time=device_data['TIME']
        )
        db.session.add(self.device)
        db.session.commit()

    def setResultDetail(self, device_data, device_id):
        self.resultDetail = ResultDetail()
        self.resultDetail.time = self.dataIn.time
        self.resultDetail.competitor_id = self.competitor.id
        self.resultDetail.virtual_device_id = device_id
        self.resultDetail.run_id = self.runInfo.id
        self.resultDetail.time = device_data['TIME']
        self.resultDetail.group_id = self.runGroup.id
        db.session.add(self.resultDetail)
        db.session.commit()

    def getCirclesCount(self, device_data):
        CrossedCirclesCount = db.session.query(func.count(distinct(ResultDetail.virtual_device_id))).\
            filter(ResultDetail.run_id == self.runInfo.id, ResultDetail.competitor_id == self.competitor.id).\
            scalar()
        if CrossedCirclesCount > 1:

            previousResults = self.getPreviousDeviceData(CrossedCirclesCount)

            if len(previousResults) < 2:

                if (datetime.combine(date(1,1,1), previousResults[0].time) + TIME_DELTA).time() < (datetime.strptime(device_data['TIME'], '%M:%S.%f')).time():
                    self.getDevice(CrossedCirclesCount)
                    self.setResultDetail(device_data, self.virtualDevice.id)
                    self.FirstLeg()
                    self.calculateRanks()
                else:
                    self.isDataForSend = False
                    self.setResultDetail(device_data, previousResults[0].virtual_device_id)
            else:

                self.getDevice(CrossedCirclesCount)
                self.setResultDetail(device_data, self.virtualDevice.id)
                self.FirstLeg()
                self.calculateRanks()
        else:
            if (datetime.min + TIME_DELTA).time() < (datetime.strptime(device_data['TIME'], '%M:%S.%f')).time():

                self.getDevice(1)
                self.setResultDetail(device_data, self.virtualDevice.id)
                self.FirstLeg()
                self.calculateRanks()
            else:
                self.isDataForSend = False

    def getPreviousDeviceData(self, CrossedCirclesCount):
        virtualDevice = VirtualDevice.query.filter(VirtualDevice.race_id == self.race.id,
                                   VirtualDevice.order == CrossedCirclesCount-1).first()
        return db.session.query(ResultDetail).filter(ResultDetail.virtual_device_id == virtualDevice.id,
                                                     ResultDetail.competitor_id == self.competitor.id).all()

    def FirstLeg(self):
        self.resultDetail.is_first = True

    def getDevice(self, CrossedCirclesCount):
        self.virtualDevice = VirtualDevice.query.filter(VirtualDevice.race_id == self.race.id,
                                          VirtualDevice.order == CrossedCirclesCount).first()

    def calculateRanks(self):
        groupCompetitorsList=db.session.query(ResultDetail).\
            filter(ResultDetail.virtual_device_id == self.virtualDevice.id,
                   ResultDetail.run_id == self.runInfo.id,
                   ResultDetail.is_first == True,
                   ResultDetail.group_id == self.runGroup.id).\
            order_by(ResultDetail.time.asc()).all()
        if self.runGroup.number != 1:
            runCompetitorsList=db.session.query(ResultDetail).\
            filter(ResultDetail.virtual_device_id == self.virtualDevice.id,
                   ResultDetail.run_id == self.runInfo.id,
                   ResultDetail.is_first == True).\
            order_by(ResultDetail.time.asc()).all()
            for index, item in enumerate(runCompetitorsList):
                item.rank = index + 1
                db.session.add(item)
            db.session.commit()
            besttTime=datetime.combine(date.min, groupCompetitorsList[0].time) - datetime.min
            for index, item in enumerate(groupCompetitorsList):
                item.diff = (datetime.combine(date.min, item.time) - besttTime).time()
                item.grouprank = index + 1
                db.session.add(item)
            db.session.commit()
            self.resultDetailList = groupCompetitorsList
        else:
            besttTime = datetime.combine(date.min,groupCompetitorsList[0].time) - datetime.min
            for index, item in enumerate(groupCompetitorsList):
                item.diff = (datetime.combine(date.min, item.time)-besttTime).time()
                item.rank = index+1
                item.grouprank = index + 1
                db.session.add(item)
            db.session.commit()
            self.resultDetailList = groupCompetitorsList
    def resultView(self):
        return {
            'competitor_id': self.competitor.id,
            'time': timeConverter(self.resultDetail.time),
            'diff': timeConverter(self.resultDetail.diff),
            'rank': self.resultDetail.grouprank,
            'run_id':self.runInfo.id,
            'device_order': self.virtualDevice.order
        }

def timeConverter(time, format='%M:%S.%f'):
    try:
        return time.strftime(format)[:-3]
    except:
        return None



@shorttrack.route('/race/<int:id>/run/add', methods=['GET', 'POST'])
def race_add_run(id):
    lastRun = RunInfo.query.filter(RunInfo.race_id == id).\
        order_by(RunInfo.number.desc()).\
        limit(1).first()
    if lastRun is None:
        runNumber = 0
    else:
        runNumber = lastRun.number

    newRun = RunInfo(
        name=request.form.get("new_run__name"),
        race_id=id,
        number=runNumber
    )
    db.session.add(newRun)
    db.session.commit()
    return json.dumps({
        'id': newRun.id,
        'number': newRun.number,
        'name': newRun.name
    })
@shorttrack.route('/race/<int:id>/run/<int:run_id>/del', methods=['GET', 'POST'])
def race_del_run(id, run_id):
    run_info = RunInfo.query.get_or_404(run_id)
    db.session.delete(run_info)
    flash('The run has been deleted.')
    return redirect(url_for('.race_runs', race_id=id,_external=True))




@shorttrack.route('/race/<int:id>/run/<int:run_id>/start', methods=['GET', 'POST'])
def race_course_run_start(id, run_id):
    run_info = RunInfo.query.get_or_404(run_id)
    run_info.starttime = datetime.now()
    db.session.add(run_info)
    db.session.commit()
    return run_info.starttime.isoformat()

@shorttrack.route('/race/<int:id>/run/<int:run_id>/group/start', methods=['GET', 'POST'])
def race_group_run_start(id, run_id):
    activeGroup = db.session.query(RunGroup).filter(RunGroup.run_id == run_id,
                                                     RunGroup.is_start == True,
                                                     RunGroup.is_finish == None).first()
    if activeGroup is not None:
        activeGroup.is_finish = True
    nextGroupToStart = db.session.query(RunGroup).filter(RunGroup.run_id == run_id,
                                                         RunGroup.is_start == None,
                                                         RunGroup.is_finish == None).\
        order_by(RunGroup.number.asc()).limit(1).first()
    if nextGroupToStart is not None:
        nextGroupToStart.is_start = True
        createStartDeviceResults(id, run_id, nextGroupToStart.id)
        return ''
    else:
        return 'ERROR'

@shorttrack.route('/race/<int:id>/run/<int:run_id>/stop', methods=['GET', 'POST'])
def race_course_run_stop(id, run_id):
    run_info = RunInfo.query.get_or_404(run_id)
    run_info.endtime = datetime.now()
    db.session.add(run_info)
    return run_info.endtime.isoformat()

@shorttrack.route('/race/<int:id>/run/<int:run_id>/startlist/upload', methods=[ 'POST'])
def race_run_startlist_upload(id, run_id):
    filename = request.files['list'].filename
    extension = filename.split(".")[-1]
    content = request.files['list'].read()
    sheet = pyexcel.get_sheet(file_type=extension, file_content=content)
    runList = RunGroup.query.filter(RunGroup.run_id == run_id).all()
    db.session.query(RunOrder).filter(RunOrder.run_id == run_id).delete()
    for item in sheet.to_array()[1:]:
        if item[6] != '':
            group = next((itm for itm in runList if itm.number == item[6]), None)
            if group is None:
                group = RunGroup(
                    number=item[6],
                    run_id=run_id
                )
                db.session.add(group)
                db.session.commit()
                runList.append(group)

            runOrder = RunOrder(
                group_id=group.id,
                order=item[7],
                competitor_id=item[0],
                run_id=run_id
            )
            db.session.add(runOrder)
    db.session.commit()
    return redirect(url_for('.race_run_orderlist',race_id=id, run_id=run_id, _external=True))


def createStartDeviceResults(race_id, run_id, group_id):
    virtualStartDevice = VirtualDevice.query.filter(VirtualDevice.race_id == race_id,
                                                    VirtualDevice.order == 0).first()
    runCompetitorsList= db.session.query(Competitor, RunOrder).\
        join(RunOrder, RunOrder.competitor_id == Competitor.id).filter(RunOrder.group_id == group_id).all()
    for item in runCompetitorsList:
        resultDetailFirst = ResultDetail(
            competitor_id=item[0].id,
            time=time(0, 0),
            run_id=run_id,
            virtual_device_id=virtualStartDevice.id,
            is_first=True
        )
        resultDetail = ResultDetail(
            competitor_id=item[0].id,
            time=time(0, 0),
            run_id=run_id,
            virtual_device_id=virtualStartDevice.id
        )
        db.session.add(resultDetail)
        db.session.add(resultDetailFirst)
    db.session.commit()

