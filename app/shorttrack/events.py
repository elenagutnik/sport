from flask import request, render_template

from datetime import datetime
from flask_login import login_required
from . import shorttrack
from ..decorators import admin_required
from sqlalchemy import func

from .Race import EventDefiner, PhotofinishEvent
# For emulator
import json
from .models import *
from sqlalchemy.ext.declarative import DeclarativeMeta

from .deviceDataHandler import dataHandler
from .. import socketio

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


@shorttrack.route('/emulation/<int:race_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def emulator(race_id):
    # try:
    current = RunInfo.query.filter(RunInfo.endtime == None,
                                   RunInfo.starttime < datetime.now(),
                                   RunInfo.race_id == race_id).first()
    last_run = db.session.query(RunGroup).filter(RunGroup.is_start == None,
                                                 RunGroup.is_finish == None,
                                                 RunGroup.run_id == current.id).\
        order_by(RunGroup.number.asc()).limit(1).first()
    competitors = db.session.query(Competitor, RunOrder).\
        join(RunOrder, RunOrder.competitor_id == Competitor.id).\
        filter(RunOrder.group_id == last_run.id).all()

    competitors_list = []
    for item in competitors:
        competitors_list.append({
            'order': item[1].order,
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
    # except:
    #     emulator_clear(race_id)
    #     return 'Наверное нету активных заездов'

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

    treeView={}
    for item in Competitors_list:
        if item[1].run_id not in treeView.keys():
            treeView[item[1].run_id] = {}
        if item[1].group_id not in treeView[item[1].run_id].keys():
            treeView[item[1].run_id][item[1].group_id] = []
        treeView[item[1].run_id][item[1].group_id].append(item[0])

    runsList = db.session.query(RunInfo).filter(RunInfo.race_id == race_id).order_by(RunInfo.number.asc()).all()
    run_groups = RunGroup.query.filter(RunGroup.run_id.in_([item.id for item in runsList])).order_by(RunGroup.number.asc()).all()
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
                           jury=jury_list, run_info=run_info)

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
def load_data():
    data = request.json
    dataHandler.delay(data=data)
    # racehandler = EventDefiner(data)
    # racehandler.HandleData()
    # print(racehandler.EVENT_NAME)
    # if racehandler.isDataForSend:
    #     socketio.emit(racehandler.EVENT_NAME, json.dumps(racehandler.resultView()))
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