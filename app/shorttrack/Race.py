from .models import *
from . import shorttrack
from .. import db_shorttrack as db
from datetime import timedelta, datetime, time, date
from sqlalchemy import or_, func, distinct
import json
import pyexcel

from  flask import request, flash, redirect,url_for

TIME_DELTA = timedelta(seconds=4)

def EventDefiner(event_data):
    race_info = db.session.query(RunInfo,
                                 Race,
                                 ).filter(
        Race.id == RunInfo.race_id,
        RunInfo.starttime < datetime.now(),
        RunInfo.endtime == None
    ).one()
    if event_data['EVENT_CODE'] == 'C0':
        return StartEvent(race_info[0], race_info[1], event_data)
    elif event_data['EVENT_CODE'] == 'C1':
        return ShrortTrack(race_info[0], race_info[1], event_data)
    else:
        return JuryEvent(race_info[0], race_info[1], event_data)

class ShrortTrack:
    EVENT_NAME = 'STNewDataPoint'

    def __init__(self, runInfo, race, device_data):
        self.runInfo = runInfo
        self.runGroup = RunGroup.query.filter(RunGroup.run_id == self.runInfo.id,
                                              RunGroup.is_start == True,
                                              RunGroup.is_finish == None).first()
        self.race = race
        self.device = Device.query.filter(Device.race_id == self.race.id, Device.src_dev == device_data['SRC_DEV']).first()
        self.competitor = db.session.query(Competitor).filter(
            Competitor.race_id == self.race.id,
            or_(Competitor.transponder_1 == device_data['TRANSPONDER'],
                Competitor.transponder_2 == device_data['TRANSPONDER'])).first()
        self.device_data = device_data
        self.isDataForSend = True
        self.dataIn = None
        self.virtualDevice = None

        self.resultDetail = None
        self.resultDetailList = None

    def setDataIn(self):
        self.dataIn = DataIn(
            transponder=self.device_data['TRANSPONDER'],
            src_dev=self.device_data['SRC_DEV'],
            time=self.device_data['TIME']
        )
        db.session.add(self.device)
        db.session.commit()

    def setResultDetail(self, device_id):
        self.resultDetail = ResultDetail()
        self.resultDetail.time = self.dataIn.time
        self.resultDetail.competitor_id = self.competitor.id
        self.resultDetail.virtual_device_id = device_id
        self.resultDetail.run_id = self.runInfo.id
        self.resultDetail.time = self.device_data['TIME']
        self.resultDetail.group_id = self.runGroup.id
        db.session.add(self.resultDetail)
        db.session.commit()

    def getCirclesCount(self):
        self.crossedCirclesCount = db.session.query(func.count(distinct(ResultDetail.virtual_device_id))).\
            filter(ResultDetail.run_id == self.runInfo.id, ResultDetail.competitor_id == self.competitor.id).\
            scalar()


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
            runCompetitorsList = db.session.query(ResultDetail).\
            filter(ResultDetail.virtual_device_id == self.virtualDevice.id,
                   ResultDetail.run_id == self.runInfo.id,
                   ResultDetail.is_first == True).\
            order_by(ResultDetail.time.asc()).all()
            for index, item in enumerate(runCompetitorsList):
                item.rank = index + 1
                db.session.add(item)
            db.session.commit()
            besttTime = datetime.combine(date.min, groupCompetitorsList[0].time) - datetime.min
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

    def HandleData(self):
        self.getCirclesCount()
        self.setDataIn()
        if self.crossedCirclesCount > 1:
            previousResults = self.getPreviousDeviceData(self.crossedCirclesCount)
            if len(previousResults) < 2:

                if (datetime.combine(date(1,1,1), previousResults[0].time) + TIME_DELTA).time() < (datetime.strptime(self.device_data['TIME'], '%M:%S.%f')).time():
                    self.getDevice(self.crossedCirclesCount)
                    self.setResultDetail(self.virtualDevice.id)
                    self.FirstLeg()
                    self.calculateRanks()
                else:
                    self.isDataForSend = False
                    self.setResultDetail(previousResults[0].virtual_device_id)
            else:

                self.getDevice(self.crossedCirclesCount)
                self.setResultDetail(self.virtualDevice.id)
                self.FirstLeg()
                self.calculateRanks()
        else:
            if (datetime.min + TIME_DELTA).time() < (datetime.strptime(self.device_data['TIME'], '%M:%S.%f')).time():

                self.getDevice(1)
                self.setResultDetail(self.virtualDevice.id)
                self.FirstLeg()
                self.calculateRanks()
            else:
                self.isDataForSend = False

    def resultView(self):
        return {
            'competitor_id': self.competitor.id,
            'time': timeConverter(self.resultDetail.time),
            'diff': timeConverter(self.resultDetail.diff),
            'rank': self.resultDetail.grouprank,
            'run_id': self.runInfo.id,
            'device_order': self.virtualDevice.order
        }

class JuryEvent:
    EVENT_NAME = 'STJuryData'

    def __init__(self, runInfo, race, device_data):
        self.jury = Jury.query.filter(Jury.event_code == device_data['EVENT_CODE']).first()
        self.runInfo = runInfo
        self.runGroup = RunGroup.query.filter(RunGroup.run_id == self.runInfo.id,
                                              RunGroup.is_start == True,
                                              RunGroup.is_finish == None).first()
        self.race = race
        self.jury = Jury.query.filter(Jury.race_id == self.race.id,
                                      Jury.event_code == device_data['EVENT_CODE']).first()
        self.juryResult = None
        self.device_data = device_data

        self.isDataForSend = True

    def HandleData(self):
        self.juryResult = JuryResult(
            run_id=self.runInfo.id,
            jury_id=self.jury.id,
            group_id=self.runGroup.id,
            time=(datetime.strptime(self.device_data['TIME'], '%M:%S.%f')).time(),
            rank=db.session.query(func.count(JuryResult.id)).filter(JuryResult.jury_id == self.jury.id,
                                                                 JuryResult.group_id == self.runGroup.id
                                                                 ).scalar() + 1
        )
        db.session.add(self.juryResult)
        db.session.commit()

    def resultView(self):
        return {
            'jury_id': self.jury.id,
            'time': timeConverter(self.juryResult.time),
            'rank': self.juryResult.rank,
            'run_id': self.runInfo.id,
            'group_id': self.runGroup.id
        }

class StartEvent:
    EVENT_NAME = 'STNewStartData'

    def __init__(self, runInfo, race, device_data):
        self.jury = Jury.query.filter(Jury.event_code == device_data['EVENT_CODE']).first()
        self.runInfo = runInfo
        self.race = race
        self.device_data = device_data
        self.virtualDevice = VirtualDevice.query.filter(VirtualDevice.race_id==self.race.id,
                                                        VirtualDevice.order==0).first()

        self.runGroup = None
        self.isDataForSend = True
        self.resultViewData = []

    def HandleData(self):
        activeGroup = db.session.query(RunGroup).filter(RunGroup.run_id == self.runInfo.id,
                                                         RunGroup.is_start == True,
                                                         RunGroup.is_finish == None).first()
        if activeGroup is not None:
            activeGroup.is_finish = True
        nextGroupToStart = db.session.query(RunGroup).filter(RunGroup.run_id == self.runInfo.id,
                                                             RunGroup.is_start == None,
                                                             RunGroup.is_finish == None).\
            order_by(RunGroup.number.asc()).limit(1).first()
        if nextGroupToStart is not None:
            nextGroupToStart.is_start = True
            self.runGroup = nextGroupToStart
            self.createStartDeviceResults(self.race.id, self.runInfo.id, nextGroupToStart.id)

    def createStartDeviceResults(self, race_id, run_id, group_id):
        virtualStartDevice = VirtualDevice.query.filter(VirtualDevice.race_id == race_id,
                                                        VirtualDevice.order == 0).first()
        runCompetitorsList = db.session.query(Competitor, RunOrder).\
            join(RunOrder, RunOrder.competitor_id == Competitor.id).filter(RunOrder.group_id == group_id).all()
        for item in runCompetitorsList:
            resultDetailFirst = ResultDetail(
                competitor_id=item[0].id,
                time=time(0, 0),
                diff=time(0, 0),
                run_id=run_id,
                virtual_device_id=virtualStartDevice.id,
                is_first=True
            )

            resultDetail = ResultDetail(
                competitor_id=item[0].id,
                time=time(0, 0),
                diff=time(0, 0),
                run_id=run_id,
                virtual_device_id=virtualStartDevice.id
            )
            db.session.add(resultDetail)
            db.session.add(resultDetailFirst)
            self.resultViewData.append(self.convertDBdata(resultDetailFirst))
        db.session.commit()
    def convertDBdata(self, data):
        return {
            'competitor_id': data.competitor_id,
            'time': timeConverter(data.time),
            'diff': timeConverter(data.diff),
            'rank': 0,
            'run_id': self.runInfo.id,
            'device_order': self.virtualDevice.order
        }
    def resultView(self):
        return self.resultViewData

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
        number=runNumber+1
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
#
# @shorttrack.route('/race/<int:id>/run/<int:run_id>/group/start', methods=['GET', 'POST'])
# def race_group_run_start(id, run_id):
#     activeGroup = db.session.query(RunGroup).filter(RunGroup.run_id == run_id,
#                                                      RunGroup.is_start == True,
#                                                      RunGroup.is_finish == None).first()
#     if activeGroup is not None:
#         activeGroup.is_finish = True
#     nextGroupToStart = db.session.query(RunGroup).filter(RunGroup.run_id == run_id,
#                                                          RunGroup.is_start == None,
#                                                          RunGroup.is_finish == None).\
#         order_by(RunGroup.number.asc()).limit(1).first()
#     if nextGroupToStart is not None:
#         nextGroupToStart.is_start = True
#         createStartDeviceResults(id, run_id, nextGroupToStart.id)
#         return ''
#     else:
#         return 'ERROR'

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

    statusList = Status.query.all()

    db.session.query(RunOrder).filter(RunOrder.run_id == run_id).delete()
    for item in sheet.to_array()[1:]:
        status = next((itm for itm in runList if itm.number == item[6]), None)
        if status != None:
            resultApproved = ResultApproved.query.filter(ResultApproved.competitor_id == item[0],
                                                         ResultApproved.run_id == run_id).first()
            if resultApproved is None:
                resultApproved = ResultApproved(
                    competitor_id=item[0],
                    run_id=run_id,
                    status_id=status.id
                )
            else:
                resultApproved.run_id = status.id
            db.session.add(resultApproved)

        if item[7] != '':
            group = next((itm for itm in runList if itm.number == item[7]), None)
            if group is None:
                group = RunGroup(
                    number=item[7],
                    run_id=run_id
                )
                db.session.add(group)
                db.session.commit()
                runList.append(group)

            runOrder = RunOrder(
                group_id=group.id,
                order=item[8],
                competitor_id=item[0],
                run_id=run_id
            )
            db.session.add(runOrder)
    db.session.commit()
    return redirect(url_for('.race_run_orderlist',race_id=id, run_id=run_id, _external=True))



@shorttrack.route('/race/<int:id>/run/<int:run_id>/photofinish', methods=['GET', 'POST'])
def race_photofinish_data(id, run_id):
    photoFinishData = PhotoFinishData(
        competitor_id=request.form.get('competitor_id'),
        run_id=run_id,
        time=datetime.strptime(request.form.get('time'), '%M:%S.%f').time()
    )
    db.session.add(photoFinishData)
    db.session.commit()
    return 'Good'