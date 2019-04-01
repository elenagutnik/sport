from flask import request, render_template

from datetime import datetime, timedelta
from flask_login import login_required
from . import shorttrack
from ..decorators import admin_required
from sqlalchemy import func

from .Race import EventDefiner, PhotofinishEvent, timeConverter, RaceManager
# For emulator
import json
from .models import *
from sqlalchemy.ext.declarative import DeclarativeMeta

from .deviceDataHandler import dataHandler
from .. import socketio

# замена Celery
from .. import lock
# ----->

from functools import wraps

def exectutiontime(message):
    def real_dec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = datetime.now()
            result = func(*args, **kwargs)
            end = datetime.now()
            print(message, 'elapsed time:', (end-timedelta(hours=start.hour, minutes=start.minute,seconds=start.second,microseconds=start.microsecond)).time())
            return result
        return wrapper
    return real_dec



from flask_socketio import join_room, leave_room, send, emit, rooms

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    if isinstance(data, datetime):
                        fields[field] = data.isoformat()
                    else:
                        fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)



@shorttrack.route('/emulation/test/<int:race_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def emulator_test(race_id):
    return render_template('shorttrack/test_page.html', race_id=race_id)


@shorttrack.route('/emulation/<int:race_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def emulator(race_id):
    try:
        current = RunInfo.query.filter(RunInfo.endtime == None,
                                       RunInfo.starttime < datetime.now(),
                                       RunInfo.race_id == race_id).one()
    except:
        emulator_clear(race_id)
        return 'Нет активных заездов'
    try:
        last_run = db.session.query(RunGroup).filter(RunGroup.is_start == None,
                                                     RunGroup.is_finish == None,
                                                     RunGroup.run_id == current.id).\
            order_by(RunGroup.number.asc()).limit(1).first()
    except:
        emulator_clear(race_id)
        return 'Нет группы для старта'

    competitors = db.session.query(Competitor, RunOrder).\
        join(RunOrder, RunOrder.competitor_id == Competitor.id).\
        filter(RunOrder.group_id == last_run.id).all()

    competitors_list = []

    for item in competitors:
        competitors_list.append({
            'order': item[1].order,
            'id': item[0].id,
            'transponder_1': item[0].transponder_1,
            'transponder_2': item[0].transponder_2
        })

    jury_list = db.session.query(Jury, JuryType).join(JuryType, JuryType.id == Jury.type_id). \
        filter(Jury.race_id == race_id).all()

    device = db.session.query(Device).filter(Device.race_id == race_id).one()
    circle_count = db.session.query(func.count(VirtualDevice.id)).filter(VirtualDevice.race_id == race_id).scalar()-1
    return render_template('timer_shorttrack.html',
                           competitors=json.dumps(competitors_list),
                           device=json.dumps(device, cls=AlchemyEncoder),
                           circle_count=circle_count, race_id=race_id, run_id=current.id, jury=jury_list)

@shorttrack.route('/emulation/<int:race_id>/clear', methods=['GET', 'POST'])
@login_required
@admin_required
def emulator_clear(race_id):

    db.session.query(ResultDetail).delete()
    db.session.query(ResultApproved).delete()
    db.session.query(RunInfo).filter(RunInfo.race_id == race_id).update({"endtime": None,
                                                                       "starttime": None})
    db.session.query(RunGroup).update({"is_finish": None, "is_start": None})
    db.session.query(JuryResult).delete()
    db.session.commit()
    return 'Подчищено!'

@shorttrack.route('/jury_page/<int:race_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def jury_page(race_id):
    jury_list = db.session.query(Jury, JuryType).join(JuryType, JuryType.id == Jury.type_id).\
        filter(Jury.race_id == race_id).all()

    Competitors_list = db.session.query(Competitor, RunOrder).\
        join(RunOrder, RunOrder.competitor_id == Competitor.id).\
        filter(Competitor.race_id == race_id).\
        order_by(RunOrder.group_id.asc(), RunOrder.order.asc()).all()

    runsList = db.session.query(RunInfo).filter(RunInfo.race_id == race_id).order_by(RunInfo.number.asc()).all()

    resultList = db.session.query(ResultDetail, VirtualDevice).\
        join(VirtualDevice, VirtualDevice.id == ResultDetail.virtual_device_id).\
        filter(ResultDetail.run_id.in_([item.id for item in runsList]),
               ResultDetail.is_first == True).order_by(VirtualDevice.order.asc()).all()
    treeViewResult = {}
    for item in resultList:
        if item[0].run_id not in treeViewResult.keys():
            treeViewResult[item[0].run_id] = {}
        if item[0].competitor_id not in treeViewResult[item[0].run_id].keys():
            treeViewResult[item[0].run_id][item[0].competitor_id] = []
        treeViewResult[item[0].run_id][item[0].competitor_id].append(
            {
                'time': timeConverter(item[0].time),
                'diff': timeConverter(item[0].diff),
                'rank': item[0].grouprank,
                'device_order': item[1].order
            }
        )
    treeView = {}
    for item in Competitors_list:
        if item[1].run_id not in treeView.keys():
            treeView[item[1].run_id] = {}
        if item[1].group_id not in treeView[item[1].run_id].keys():
            treeView[item[1].run_id][item[1].group_id] = []
        treeView[item[1].run_id][item[1].group_id].append(item[0])

    run_groups = RunGroup.query.filter(RunGroup.run_id.in_([item.id for item in runsList])).order_by(RunGroup.number.asc()).all()
    virtual_devices = VirtualDevice.query.filter(VirtualDevice.race_id == race_id).all()
    run_info = {}
    for item in runsList:
        run_info[item.number] = {
            'id': item.id,
            'starttime': item.starttime,
            'endtime': item.endtime,
            'name': item.name,
            'groups': []
        }
        for group in run_groups:
            if group.run_id == run_info[item.number]['id']:
                run_info[item.number]['groups'].append(group)

    return render_template('shorttrack/jury_page.html',
                           competitors=treeView,
                           runs=runsList, race_id=race_id,
                           jury=jury_list, run_info=run_info, result_list=treeViewResult, virtual_devices=virtual_devices)

@shorttrack.route('/competitorslist', methods=['GET', 'POST'])
@login_required
@admin_required
def competitors_get_by_group():
    db_competitorsList=db.session.query(Competitor, RunOrder).join(RunOrder, RunOrder.competitor_id == Competitor.id).\
        filter(RunOrder.group_id == request.args.get('group_id')).all()
    result = []
    for item in db_competitorsList:
        result.append({
            'id': item[0].id,
            'ru_lastname': item[0].ru_lastname,
            'ru_firstname': item[0].ru_firstname,
        })
    return json.dumps(result)



@shorttrack.route('/input/data', methods=['POST', 'GET'])
@exectutiontime('Full time')
def load_data():
    print('input time', datetime.now().isoformat())
    data = request.json
    print(data)

    lock.acquire()
    try:
        # dataHandler.delay(data=data)
        racehandler = EventDefiner(data)
        racehandler.HandleData()
        if racehandler.isDataForSend:
            socketio.emit(racehandler.EVENT_NAME, json.dumps(racehandler.resultView()))
            print(racehandler.EVENT_NAME, json.dumps(racehandler.resultView()))
    finally:
        lock.release()
    return '', 200



@shorttrack.route('/race/<int:id>/run/<int:run_id>/photofinish', methods=['GET', 'POST'])
def race_photofinish_data(id, run_id):
    data = db.session.query(RunInfo, Race).join(Race, Race.id == RunInfo.race_id).filter(RunInfo.id == run_id).first()
    photofinishHandler = PhotofinishEvent(data[0], data[1], Competitor.query.get(request.form.get('competitor_id')), datetime.strptime(request.form.get('time'), '%M:%S.%f').time())
    photofinishHandler.HandleData()
    return json.dumps(photofinishHandler.resultView())
    # photoFinishData = PhotoFinishData(
    #     competitor_id=request.form.get('competitor_id'),
    #     run_id=run_id,
    #     time=datetime.strptime(request.form.get('time'), '%M:%S.%f').time()
    # )
    # db.session.add(photoFinishData)
    # db.session.commit()
    # return 'Good'

@socketio.on('join')
def on_join(data):
    print(data['room'])
    join_room(data['room'])
    print(rooms())

@socketio.on('CompetitorApprove')
def onCompetitorApprove(data):
    raceHandler = RaceManager(group_id=data['group_id'])
    return json.dumps(
        raceHandler.competitorApprove(data['competitor_id'], data['status_id'])
    )

@socketio.on('FalseStart')
def onFalseStart(data):
    raceHandler = RaceManager(group_id=data['group_id'])
    return json.dumps(
        raceHandler.falseStart()
    )

        # @socketio.on('disconnect')
# def test_disconnect():
#     pass