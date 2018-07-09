from .. import socketio, db, migrate

from ..decorators import admin_required
from .models import *
from . import jsonencoder, raceinfo
import json

from functools import wraps
from sqlalchemy import cast, DATE, func, asc,  or_, and_

from flask_login import current_user, login_required
from .DataViewer import ConvertRunResults, ConvertCompetitorStart, ConvertCompetitorsRankList, ConvertCompetitorFinish, TreeView

from datetime import datetime, timedelta
from flask import request, render_template

from .Scoreboard import Scoreboard

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


@raceinfo.route('/migrate')
def device_1get():
    return ''

@raceinfo.route('/emulation/<int:race_id>/clear')
def emulation_clear_results(race_id):
    db.engine.execute('delete from result_detail; ')
    db.engine.execute('delete from data_in;')
    db.engine.execute('delete from result_approved;')
    db.engine.execute('delete from result;')
    db.engine.execute('delete from run_order;')
    db.engine.execute('update run_info set endtime=NULL;')
    db.engine.execute('update run_info set starttime=NULL;')
    db.engine.execute('update run_order set manual_order=NULL;')
    return "cleared"

@raceinfo.route('/emulation/<int:race_id>')
def emulation(race_id):
    race = Race.query.get(race_id)

    devices = db.session.query(CourseDevice,Device).join(Device).filter(Course.race_id == race_id,
                                        CourseDevice.course_id == Course.id).order_by(CourseDevice.order).all()
    return render_template('timer.html',
                           race=json.dumps(race, cls=jsonencoder.AlchemyEncoder),
                           devices=json.dumps(devices, cls=jsonencoder.AlchemyEncoder))

@raceinfo.route('/receiver')
def receiver():
    return render_template('receiver.html')

@raceinfo.route('/receiver_jury')
@admin_required
def receiver_jury():
    return render_template('receiver_jury.html')

@raceinfo.route('/jury_page')
@admin_required
def jury_page():
    return render_template('jury_page.html')

@raceinfo.route('/run/get/', methods=['POST', 'GET'])
def run_get():
    try:
        race_id = request.args['race_id']
        data = json.dumps(RunInfo.query.filter(RunInfo.race_id == race_id).all(), cls=jsonencoder.AlchemyEncoder)
        return data
    except:
        db.session.flush()
        db.session.commit()
        return json.dumps(RunInfo.query.
                          filter(cast(RunInfo.starttime, DATE) == datetime.now().date()).
                          all(),
                          cls=jsonencoder.AlchemyEncoder)

@raceinfo.route('/device/get/course/<int:course_id>')
def device_get(course_id):
    return json.dumps(db.session.query(CourseDevice, CourseDeviceType).join(CourseDeviceType).filter(CourseDevice.course_id == course_id).order_by(CourseDevice.order).all(), cls=jsonencoder.AlchemyEncoder)

def setDeviceDataInDB(data, run_id, cource_device_id):
    input_data = DataIn(

        src_sys=data['SRC_SYS'],
        src_dev=data['SRC_DEV'],
        event_code=data['EVENT_CODE'],
        time=data['TIME'],
        run_id=run_id,
        cource_device_id=cource_device_id
    )
    if 'BIB' in data:
        input_data.bib = data['BIB']
    db.session.add(input_data)
    db.session.commit()
    return input_data


def get_previous_run_result_or_null(run, race_competitor_id):
    race = Race.query.get(run.race_id)
    if race.result_function==1 and run.number != 1:
        previous_run_result = db.session.query(ResultApproved.time.label('time'),
                                           ResultApproved.diff.label('diff')). \
        order_by(RunInfo.number.desc()). \
        filter(RunInfo.number < run.number, ResultApproved.run_id == RunInfo.id,
               ResultApproved.race_competitor_id ==race_competitor_id). \
            first()
        previous_run_result = previous_run_result._asdict()
    else:
        previous_run_result = {'time': 0, 'diff': 0}
    return previous_run_result


@raceinfo.route('/run/competitor/start', methods=['GET', 'POST'])
@login_required
@admin_required
def competitor_start():
    result_approves = ResultApproved(
        race_competitor_id=request.args.get('competitor_id'),
        run_id=request.args.get('run_id'))
    db.session.add(result_approves)
    db.session.commit()
    competitor_order = db.session.query(func.count('*')).select_from(RunOrder).\
                           filter(RunOrder.run_id == request.args.get('run_id'),
                                  RunOrder.manual_order != None, RunOrder.manual_order != 0).\
                           scalar()+1
    current_competitor = RunOrder.query.filter(RunOrder.race_competitor_id == request.args.get('competitor_id'),
                                               RunOrder.run_id == request.args.get('run_id')).one()

    current_competitor.manual_order = competitor_order
    db.session.add(current_competitor)
    db.session.commit()
    return '', 200

def competitor_start_run(run):
    race = Race.query.get(run.race_id)


    race_competitors = db.session.query(RaceCompetitor, RunOrder). \
        join(RunOrder). \
        filter(RunOrder.run_id == run.id).order_by(asc(RunOrder.order)).all()
    order = sum(item[1].manual_order is not None and item[1].manual_order != 0 for item in race_competitors)


    сompetitor = next(item for item in race_competitors if item[1].manual_order is None)
    сompetitor[1].manual_order = order + 1

    if race.result_function == 1 and run.number > 1:
        adder = db.session.query(func.sum(ResultApproved.time).label('time'),
                                 func.sum(ResultApproved.diff).label('diff')).\
            filter(ResultApproved.race_competitor_id == сompetitor[0].id,
                   ResultApproved.run_id == RunInfo.id,
                   RunInfo.number < run.number).first()

        result_approves = ResultApproved(run_id=run.id,
                                         is_start=True,
                                         race_competitor_id=сompetitor[0].id,
                                         adder_time=adder.time,
                                         adder_diff=adder.diff
                                         )
    else:
        result_approves = ResultApproved(run_id=run.id,
                                         is_start=True,
                                         race_competitor_id=сompetitor[0].id)
    db.session.add(сompetitor[1])
    db.session.add(result_approves)
    db.session.commit()
    return сompetitor

def get_current_competitor(course_device_id, run_id):
    competitor_order = db.session.query(func.count('*')).select_from(ResultDetail).\
                           filter(ResultDetail.run_id == run_id,
                            ResultDetail.course_device_id == course_device_id). \
                            scalar() + 1
    print('текущий девайс', competitor_order-1)

    competitor = db.session.query(RaceCompetitor, RunOrder).\
           join(RunOrder). \
        filter(RunOrder.manual_order == competitor_order, RunOrder.run_id == run_id).first()
    return competitor

def competitor_finish(competitor_id, run, finish_time):
    # try:
    result_approves = ResultApproved.query.filter_by(
        race_competitor_id=competitor_id,
        run_id=run.id).one()
    result_approves.finish_time = finish_time
    result_approves.time = result_approves.finish_time - result_approves.start_time
    result_approves.status_id = 1
    result_approves.is_finish = True

    db.session.add(result_approves)
    db.session.commit()
    return result_approves
    # except Exception as err:
    #     return None

@raceinfo.route('/run/competitor/remove', methods=['GET', 'POST'])
@login_required
@admin_required
def competitor_remove():
    ResultApproved.query.filter(
        ResultApproved.race_competitor_id == request.args.get('competitor_id'),
        ResultApproved.run_id == request.args.get('run_id')
    ).delete()
    return '', 200

@raceinfo.route('/run/competitor/clear', methods=['GET', 'POST'])
@login_required
@admin_required
def competitor_clear():
    competitor_order = RunOrder.query.filter(RunOrder.race_competitor_id == request.args.get('competitor_id'),
                                             RunOrder.run_id == request.args.get('run_id')).one()

    if competitor_order.manual_order is not None:
        others_competitors_orders = RunOrder.query.filter(RunOrder.manual_order > competitor_order.manual_order,
                                                 RunOrder.run_id == request.args.get('run_id')).all()
        if len(others_competitors_orders) > 0:
            for item in others_competitors_orders:
                item.manual_order -= 1
                db.session.add(item)
        competitor_order.manual_order = 0

        db.session.add(competitor_order)

        ResultDetail.query.filter(
           ResultDetail.race_competitor_id == request.args.get('competitor_id'),
           ResultDetail.run_id == request.args.get('run_id')
        ).delete()
    ResultApproved.query.filter(
       ResultApproved.race_competitor_id == request.args.get('competitor_id'),
       ResultApproved.run_id == request.args.get('run_id')
    ).delete()
    db.session.commit()
    recalculate_run_results(request.args.get('run_id'))
    socketio.emit('removeResult', json.dumps(dict(removed_competitor=request.args.get('competitor_id'))))
    return 'OK'

@raceinfo.route('/approve/run/<int:run_id>/competitor/<int:competitor_id>')
@admin_required
def approve_automate(run_id, competitor_id):
   status = Status.query.filter_by(name='QLF').one()
   try:
       resultDetail = ResultApproved.query.filtel(ResultApproved.race_competitor_id == competitor_id, ResultApproved.run_id==run_id).one()
       resultDetail.is_manual = False
       resultDetail.approve_user = current_user.id
       resultDetail.approve_time = datetime.now()
       resultDetail.race_competitor_id = competitor_id
       resultDetail.run_id = run_id
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



       return 'ok', 200
@socketio.on('ManualApprove')
def approve_manual(data):
    try:
       resultApproved = ResultApproved.query.filter_by(race_competitor_id=data['competitor_id'], run_id=data['run_id']).one()
    except:
        resultApproved = ResultApproved(
           race_competitor_id=data['competitor_id'],
           run_id=data['run_id'],
           is_start=False
        )
    resultApproved.is_manual = True
    resultApproved.approve_user = current_user.id
    resultApproved.approve_time = datetime.now()
    resultApproved.status_id = data['status_id']
    # try:
    if resultApproved.status_id == '1':

        run = RunInfo.query.get(data['run_id'])
        race = Race.query.get(run.race_id)
        if race.result_function == 1 and run.number > 1:
            adder = db.session.query(func.sum(ResultApproved.time).label('time'),
                                     func.sum(ResultApproved.diff).label('diff')). \
                filter(ResultApproved.race_competitor_id == data['competitor_id'],
                       ResultApproved.run_id == RunInfo.id,
                       RunInfo.number < run.number).first()

            resultApproved.adder_time = adder.time
            resultApproved.adder_diff = adder.diff

        if resultApproved.is_start == False:
            competitorOrder = RunOrder.query.filter(RunOrder.race_competitor_id == data['competitor_id'],
                                                    RunOrder.run_id == data['run_id']).\
                first()
            competitorOrder.manual_order = 0
            db.session.add(competitorOrder)
            db.session.commit()
        if data['finish_time'] != '':
            finish_device = db.session.query(ResultDetail, CourseDevice, CourseDeviceType).\
                join(CourseDevice).\
                join(CourseDeviceType).\
                filter(ResultDetail.race_competitor_id == data['competitor_id'],
                                             ResultDetail.run_id == data['run_id'], CourseDeviceType == 3).\
                first()
            if finish_device is not None:
                finish_device[0].data_in_id = None
                finish_device[0].absolute_time = data['finish_time']
                db.session.add(finish_device)
            resultApproved.finish_time = data['finish_time']
        if data['start_time'] != '':
            start_device = db.session.query(ResultDetail, CourseDevice, CourseDeviceType).\
                join(CourseDevice).\
                join(CourseDeviceType).\
                filter(ResultDetail.race_competitor_id == data['competitor_id'],
                                             ResultDetail.run_id == data['run_id'], CourseDeviceType == 1).\
                first()
            if start_device is not None:
                start_device[0].data_in_id = None
                start_device[0].absolute_time = data['start_time']
                db.session.add(start_device)
            resultApproved.start_time = data['start_time']

        resultApproved.time = int(resultApproved.finish_time) - int(resultApproved.start_time)
    else:
        resultApproved.gate = data['gate']
        resultApproved.reason = data['reason']
    db.session.add(resultApproved)
    db.session.commit()
    # except:
    #     pass

    if resultApproved.is_start == True:
        results_list = db.session.query(CourseDevice, ResultDetail).\
            join(ResultDetail, and_(CourseDevice.id == ResultDetail.course_device_id,
                                    ResultDetail.run_id == data['run_id'],
                                    ResultDetail.race_competitor_id == data['competitor_id']), isouter=True).\
            filter(CourseDevice.course_id == RunInfo.course_id, RunInfo.id == data['run_id']).\
            all()
        for item in results_list:
            if item[1] is None:
                resultDetail = ResultDetail(
                                run_id=data['run_id'],
                                race_competitor_id=data['competitor_id'],
                                course_device_id=item[0].id
                            )
                db.session.add(resultDetail)
            else:
                item[0].reset()
        db.session.commit()
    results = recalculate_run_results(resultApproved.run_id)

    socketio.emit("NewDataManual", json.dumps({
        data['run_id']: {
            db.session.query(RunInfo.course_id).filter(RunInfo.id == data['run_id']).scalar(): [
                {
                    'is_manual': True,
                    'race_competitor_id': data['competitor_id']
                 },
                results
            ]
        }
    }))
def calculate_finish_params(current_competitor_finish, finished_competitors):
    try:
        start_result = db.session.query(ResultDetail).filter(ResultDetail.run_id == current_competitor_finish.run_id,
                                                             ResultDetail.race_competitor_id == current_competitor_finish.race_competitor_id,
                                                             ResultDetail.is_start == True).one()
        current_competitor_finish.time = current_competitor_finish.absolut_time - start_result.absolut_time
        сompetitors_list = sorted([current_competitor_finish] + finished_competitors, key=lambda item: item.time)

        for index, item in enumerate(сompetitors_list):
            item.diff = item.time - сompetitors_list[0].time
            item.rank = index + 1
    except:
        socketio.emit('recount/error', dict(competitor_id=current_competitor_finish.id,
                                            error='Count finished params: diff, rank'))
def calculate_personal_sector_params(current_competitor, device, course_id):
    # try:
        previous_course_device = CourseDevice.query.filter_by(order=device.order-1, course_id=course_id).one()
        previous_device_results = db.session.query(ResultDetail).filter(
            ResultDetail.course_device_id == previous_course_device.id,
            ResultDetail.race_competitor_id == current_competitor.race_competitor_id,
            ResultDetail.run_id == current_competitor.run_id).one()
        current_competitor.sectortime = current_competitor.absolut_time - previous_device_results.absolut_time
        current_competitor.time = previous_device_results.time + current_competitor.sectortime
        current_competitor.speed = ((device.distance - previous_course_device.distance) / 1000) / (current_competitor.sectortime / 3600000)
    # except:
    #     socketio.emit('recount/error', dict(competitor_id=current_competitor.id,
    #                                         error='Count personal params: speed, sectortime'))

def calculate_common_sector_params(current_competitor, competitors_list):
    # try:
        if len(competitors_list) != 0:
            min_сompetitor_sectortime = min(competitors_list, key=lambda item: item.sectortime)
            min_сompetitor_time = min(competitors_list, key=lambda item: item.time)

            current_competitor.diff = current_competitor.time - min_сompetitor_time.time
            current_competitor.sectordiff = current_competitor.sectortime - min_сompetitor_sectortime.sectortime

            сompetitors_list_ordered_sectortime = sorted([current_competitor] + competitors_list,
                                                         key=lambda item: item.sectortime)
            сompetitors_list_ordered_time = sorted([current_competitor] + competitors_list,
                                                   key=lambda item: item.time)

            for index, (sectortime_item,  time_item) in enumerate(zip(сompetitors_list_ordered_sectortime,
                                                                      сompetitors_list_ordered_time)):
                sectortime_item.sectorrank = index+1
                time_item.rank = index + 1

        else:
            current_competitor.sectordiff = 0
            current_competitor.sectorrank = 1
            current_competitor.diff = 0
            current_competitor.rank = 1
    # except:
    #     socketio.emit('recount/error', dict(competitor_id=current_competitor.id,
    #                                         error='Count common params: sectorrank, sectordiff'))

def recalculate_run_results(run_id):
    tree_view, manual_list = TreeView(run_id)
    if len(tree_view) > 0:
        for key, item in tree_view.items():
            if key == 1:
                continue
            else:
                recalculate_sector_results(item, tree_view[key-1])
        recalculate_finished_results(run_id)
    return ConvertRunResults(tree_view, manual_list)

def recalculate_sector_results(current_results=None, previous_results=None):
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



def recalculate_finished_results(run_id):
    finish_results = ResultApproved.query.filter(ResultApproved.run_id == run_id).all()
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

@socketio.on('GetResults')
def socket_get_results(data):
    # data = json.loads(json_data)
    if 'run_id' in data.keys():
        run = RunInfo.query.get(data['run_id'])
        results, manual = TreeView(data['run_id'])
        socketio.emit('Results', json.dumps({
            run.id: {
                run.course_id: ConvertRunResults(results, manual)
            }
        }))
    if 'race_id' in data.keys():
        run_list = RunInfo.query.filter(RunInfo.race_id == data['race_id'], RunInfo.starttime != None).all()
        result_list = []
        for run in run_list:
            results, manual = TreeView(run.id)
            result_list.append({
                run.id: {
                    run.course_id: ConvertRunResults(results, manual)
                }
            })
        socketio.emit('Results', json.dumps(result_list))
    else:
        return



@socketio.on('change/data_in/competitors')
def edit_competitor(json_data):
    error_list = []
    data = json.loads(json_data)
    tree_view = {}
    # Причведение данных к удобночитаемому формату
    for item in data:
        if item['run_id'] not in tree_view.keys():
            tree_view[item['run_id']] = {}

        if item['race_competitor_id'] not in tree_view[item['run_id']].keys():
            tree_view[item['run_id']][item['race_competitor_id']] = []
        tree_view[item['run_id']][item['race_competitor_id']].append({'result_detail_id': item['result_detail_id'],
                                                                      'data_in_id': item['data_in_id']})
    for run_id, competitors_list in tree_view.items():
        devices = get_start_finish_device(run_id)
        for competitor_id, data_list in competitors_list.items():
            if competitor_id == '-1':
                for item in data_list:
                    resultCleared = ResultDetail.query.filter(ResultDetail.id == item['result_detail_id']).one()
                    if resultCleared.course_device_id in list(devices.keys()):
                        clear_approve(devices, resultCleared)
                    resultCleared.reset()
                    db.session.add(resultCleared)
            elif competitor_id == '-2':
                 for item in data_list:
                    ResultDetail.query.filter(ResultDetail.id == item['result_detail_id']).delete()
            else:
                for item in data_list:
                    result_approved = ResultApproved.query.filter(ResultApproved.run_id == run_id,
                                                                      ResultApproved.race_competitor_id == competitor_id).first()
                    if result_approved is None:
                        error = {'error': "Competitor doesn't start", 'competitor': competitor_id}
                        error_list.append(error)
                        break
                    else:
                        dataIn = DataIn.query.filter(DataIn.id == item['data_in_id']).one()
                        isDataSet = ResultDetail.query.filter(ResultDetail.data_in_id == dataIn.id).count()
                        if isDataSet > 0:
                            error = {'error': "Double data", 'data_in_od': item['data_in_id']}
                            error_list.append(error)

                        competitor_result_detail = ResultDetail.query.filter(ResultDetail.run_id == run_id,
                                                                             ResultDetail.course_device_id == dataIn.cource_device_id,
                                                                             ResultDetail.race_competitor_id == competitor_id).first()
                        if competitor_result_detail is not None:
                            competitor_result_detail.data_in_id = dataIn.id
                            competitor_result_detail.absolut_time = dataIn.time
                        else:
                            competitor_result_detail = ResultDetail(
                                course_device_id=dataIn.cource_device_id,
                                run_id=run_id,
                                data_in_id=dataIn.id,
                                race_competitor_id=competitor_id,
                                absolut_time=dataIn.time
                            )
                        if competitor_result_detail.course_device_id in list(devices.keys()):
                            resultApproved = ResultApproved.query.filter(ResultApproved.run_id == run_id,
                                                                         ResultApproved.race_competitor_id == competitor_id).first()
                            if devices[competitor_result_detail.course_device_id] == 1:
                                resultApproved.start_time = dataIn.time
                            else:
                                resultApproved.finish_time = dataIn.time
                            resultApproved.diff = None
                            resultApproved.rank = None
                            resultApproved.time = None
                            resultApproved.status_id = None
                        db.session.add(competitor_result_detail)
                        db.session.commit()
        recalculate_run_results(run_id)
        socketio.emit('change/data_in/error', json.dumps(error_list))
    socket_get_results(json.dumps(list(tree_view.keys())))

def clear_approve(devices, resultDetail, resultApproved=None):
    if resultApproved is None:
        resultApproved = ResultApproved.query.filter(ResultApproved.run_id == resultDetail.run_id,
                                              ResultApproved.race_competitor_id == resultDetail.race_competitor_id).one()
    resultApproved.status_id = None
    resultApproved.time = None
    resultApproved.start_time = None
    resultDetail.rank = None
    resultDetail.diff = None
    if devices[resultDetail.course_device_id] == 1:
        resultApproved.start_time = None
    else:
        resultApproved.finish_time = None
    db.session.add(resultApproved)

def switch_approve(new_approve, old_approve, devices, device_id):
    if devices[device_id] == 1:
        new_approve.start_time = old_approve.start_time
    else:
        new_approve.finish_time = old_approve.finish_time
    new_approve.status_id = None

def get_start_finish_device(run_id):
    data = db.session.query(CourseDevice.id.label('device_id'), CourseDevice.course_device_type_id.label('type_id')).filter(CourseDevice.course_device_type_id != 3,
                                             CourseDevice.course_id == RunInfo.course_id,
                                             RunInfo.id == run_id).all()
    dict_view = {}
    for item in data:
        dict_view[item[0]] = item[1]
    return dict_view


@raceinfo.route('/current_data/get/<int:race_id>', methods=['POST', 'GET'])
def crutch_result_list(race_id):
    data = db.session.query(ResultDetail, RaceCompetitor, Competitor, CourseDevice, ResultApproved, CourseDeviceType)\
        .join(RaceCompetitor).join(Competitor).join(CourseDevice).join(ResultApproved).join(CourseDeviceType)\
        .filter(RaceCompetitor.race_id == race_id)\
        .order_by(asc(ResultApproved.start_time)).all()

    manual_data = db.session.query(ResultApproved, RaceCompetitor, Competitor)\
        .join(RaceCompetitor).join(Competitor)\
        .filter(RaceCompetitor.race_id == race_id, ResultApproved.is_manual==True)\
        .all()
    for _item in manual_data:
        if not any(item[1].id == _item[1].id for item in data):
            result = [None, _item[1], _item[2], None, _item[0], None]
            data.append(result)

    data = sorted(data, key=lambda item: (item[4].start_time is None, item[4].start_time))
    return json.dumps(data, cls=jsonencoder.AlchemyEncoder)


@raceinfo.route('/input/data', methods=['POST', 'GET'])
@exectutiontime('Full time')
def load_data_vol2():
    """
        NewDataStart (Информация о старте спортсмена (race_competitor_id, absolut_time, run_id))
        NewDataPoint (Текущий спортсмен + список пересчитанных рангов (sectorrank, rank) на текущем устройсве)
        NewDataFinish (Полный набор данных для всего заезда)
    """
    data = request.json
    data['TIME'] = int(datetime.strptime(data['TIME'], '%d.%m.%Y %H:%M:%S.%f').timestamp()*1000)
    # data = json.loads(request.args['data'])
    # Перевести на кэш {
    # Девайс с которого пришли данные
    device = Device.query.filter_by(src_dev=data['SRC_DEV']).one()
    # Трассы на которых стоит этот девайс
    course_devices = db.session.query(CourseDevice.course_id).filter_by(device_id=device.id)
    courses = db.session.query(Course.id).filter(Course.id.in_(course_devices))
    # Заезд с пришли данные
    # try:
    run = RunInfo.query.filter(RunInfo.course_id.in_(courses), RunInfo.starttime < datetime.now(), RunInfo.endtime == None).one()

    # Сам девайс с которого пришли данные
    course_device = db.session.query(CourseDevice, CourseDeviceType).join(CourseDeviceType).\
        filter(CourseDevice.device_id == device.id,
               CourseDevice.course_id == run.course_id).one()

    device_data = setDeviceDataInDB(data, run.id, course_device[0].id)

    competitor = get_current_competitor(course_device[0].id, run.id)


    if course_device[1].name == "Start":
        if competitor is None:
            competitor = competitor_start_run(run)

        start_data = get_previous_run_result_or_null(run, competitor[0].id)
        result = ResultDetail(
            course_device_id=course_device[0].id,
            run_id=run.id,
            time=start_data['time'],
            diff=start_data['diff'],
            data_in_id=device_data.id,
            race_competitor_id=competitor[0].id,
            absolut_time=data['TIME'],
            sectortime=0,
            sectordiff=0,
            is_start=True
        )
        socketio.emit("NewDataStart", json.dumps({run.id: {
            course_device[0].course_id: ConvertCompetitorStart(result, course_device[0])}
        }))

        # scoreboard = Scoreboard(result, run)
        # scoreboard.started_competitor()
        # scoreboard.send()

        db.session.add(result)
        db.session.commit()

        approvedResult = ResultApproved.query.filter(ResultApproved.race_competitor_id == result.race_competitor_id,
                                                     ResultApproved.run_id == result.run_id).one()
        approvedResult.is_start = True
        approvedResult.start_time = result.absolut_time
        return ''
    else:
        if competitor is not None:

            result = ResultDetail(
                course_device_id=course_device[0].id,
                run_id=run.id,
                data_in_id=device_data.id,
                race_competitor_id=competitor[0].id,
                absolut_time=data['TIME'])

            calculate_personal_sector_params(result, course_device[0], run.course_id)
            if course_device[1].name == "Finish":
                approve=competitor_finish(competitor[0].id, run, result.absolut_time)
                db.session.add(result)
                db.session.commit()
                results = recalculate_run_results(run.id)

                socketio.emit("NewDataFinish", json.dumps({
                    run.id: {
                        course_device[0].course_id: [ConvertCompetitorFinish(result, course_device[0], approve), results]
                    }
                }))

                # scoreboard = Scoreboard(result, run)
                # if result.rank == 1:
                #     scoreboard.new_best_time()
                #     scoreboard.send()
                # scoreboard.finished_competitor()
                # scoreboard.send()
                # scoreboard.finished_list()
                # scoreboard.send()

            else:
                result_details = db.session.query(ResultDetail). \
                    filter(
                    ResultDetail.course_device_id == course_device[0].id,
                    ResultDetail.run_id == run.id).all()
                calculate_common_sector_params(result, result_details)
                socketio.emit("NewDataPoint", json.dumps({
                    run.id: {
                        course_device[0].course_id: [
                            ConvertCompetitorStart(result, course_device[0]),
                            ConvertCompetitorsRankList(result_details, course_device[0])
                        ]
                    }
                }))
                db.session.add(result)
                db.session.commit()
                # scoreboard = Scoreboard(result, run)
                # scoreboard.crossed_device()
                # scoreboard.send()

        else:
            socketio.emit('errorData', json.dumps({'ERROR': 'UNKNOWED COMPETITOR', 'DATA': device_data}, cls=jsonencoder.AlchemyEncoder))

    return '', 200
@raceinfo.route('/temp/jury_page')
def test_newFormat_page():
    return render_template('new_format_tester.html')


