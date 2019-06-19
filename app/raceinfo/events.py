from .. import socketio
from ..decorators import admin_required
from .models import *
from . import jsonencoder, raceinfo
import json
from distutils.util import strtobool
from functools import wraps
from sqlalchemy import cast, DATE, func, asc, and_
from flask_login import login_required
from .DataViewer import ConvertRunResults, ConvertCompetitorStart, ConvertCompetitorsRankList, ConvertCompetitorFinish, \
    TreeView, ConvertErrorData, DataInView
from datetime import datetime, timedelta
from flask import request, render_template
from .Scoreboard import Scoreboard

from .Race import RaceGetter
from .runList import runList_view


# from .. import semaphore, lock

def exectutiontime(message):
    def real_dec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = datetime.now()
            result = func(*args, **kwargs)
            end = datetime.now()
            # print(message, 'elapsed time:', (end-timedelta(hours=start.hour, minutes=start.minute,seconds=start.second,microseconds=start.microsecond)).time())
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

@raceinfo.route('/emulation/<int:race_id>/<string:is_parallel>')
def emulation(race_id,is_parallel):
    race = Race.query.get(race_id)

    devices = db.session.query(CourseDevice,Device).join(Device).filter(Course.race_id == race_id,
                                        CourseDevice.course_id == Course.id).order_by(CourseDevice.order).all()
    if strtobool(is_parallel):
        devices_dict = {}
        for item in devices:
            if item[0].course_id not in devices_dict.keys():
                devices_dict[item[0].course_id] = []
            devices_dict[item[0].course_id].append(item)
        return render_template('timer_parallel.html',
                                   race=json.dumps(race, cls=jsonencoder.AlchemyEncoder),
                                   devices=json.dumps(devices_dict, cls=jsonencoder.AlchemyEncoder))
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
@raceinfo.route('/jury_page/tmp')
@admin_required
def jury_page_tmp():
    return render_template('new_format_tester.html')
@raceinfo.route('/run/get/', methods=['POST', 'GET'])
def run_get():
    try:
        race_id = request.args['race_id']
        data = json.dumps(RunInfo.query.filter(RunInfo.race_id == race_id).order_by(RunInfo.number.asc(), RunInfo.is_second.asc()).all(), cls=jsonencoder.AlchemyEncoder)
        return data
    except:
        db.session.flush()
        db.session.commit()
        return json.dumps(RunInfo.query.
                          filter(cast(RunInfo.starttime, DATE) == datetime.now().date()).
                          all(),
                          cls=jsonencoder.AlchemyEncoder)

# /approve/edit/run/18/competitor/9?
# @raceinfo.route('/approve/edit/run/<int:run_id>/competitor/<int:competitor_id>', methods=['POST', 'GET'])
@socketio.on('CompetitorManualApprove')
def manual_approve(data):
    raceHandler = RaceGetter.getRaceByRunid(data['run_id'])
    result = raceHandler.competitor_manualapprove(data['competitor_id'],
                                         data['status_id'],
                                         data['finish_time'],
                                         data['start_time'],
                                         data['gate'],
                                         data['reason'])
    if result:
        tree_view, manual_list, dql_list = raceHandler.recalculate_run_results()
        socketio.emit("NewDataManual", json.dumps({
            data['run_id']: {
                db.session.query(RunOrder.course_id).filter(RunOrder.run_id == data['run_id'],
                                                            RunOrder.race_competitor_id == data['competitor_id']).scalar():
                    [
                        {
                            'is_manual': True,
                            'race_competitor_id': data['competitor_id'],
                            'manual_order': raceHandler.runOrder.manual_order
                        },
                        ConvertRunResults(tree_view, manual_list, dql_list)
                ]
            }
        }))


@socketio.on('GetResults')
def socket_get_results(data):
    # data = json.loads(json_data)
    print('GetResults', json.dumps(data))
    if 'race_id' in data.keys():
        run_list = RunInfo.query.filter(RunInfo.race_id == data['race_id'], RunInfo.starttime != None, RunInfo.run_type_id!=3).all()
        result_list = {}
        for run in run_list:
            results, manual, dql_list = TreeView(run.id)
            result_list[run.id] = [ConvertRunResults(results, manual, dql_list), json.loads(DataInView(run.id))]
            #result_list[run.id] = [ConvertRunResults(results, manual, dql_list), DataInView(run.id)]
        socketio.emit('Results', json.dumps(result_list))
    else:
        if 'run_id' in data.keys():
            run = RunInfo.query.get(data['run_id'])
            results, manual, dql_list = TreeView(data['run_id'])
            socketio.emit('Results', json.dumps({
                run.id: [
                    ConvertRunResults(results, manual, dql_list),
                    DataInView(run.id)
                ]
            }))
    return

@socketio.on('ScoreboardSendStartlist')
def scoreboard_send_start_list(data):
    raceHandler = RaceGetter.getRaceByRunid(data['run_id'])
    scoreboard = Scoreboard(raceHandler)
    scoreboard.start_list()
    scoreboard.send()

@socketio.on('GetRaceStatus')
def get_race_status(data):
    raceHandler = RaceGetter.getRaceByid(data['race_id'])
    print('RaceStatus')
    tmp = json.dumps(raceHandler.checkRace())
    print(tmp)
    # socketio.emit('RaceStatus', json.dumps(raceHandler.checkRace()))
    socketio.emit('RaceStatus', raceHandler.checkRace())


@socketio.on('GetRaceInfo')
def get_race_info(data):
    print(data)
    if 'race_id' in data.keys():
        run_list = db.session.query(RunInfo, RunType, Discipline).\
            join(RunType, RunInfo.run_type_id == RunType.id). \
            join(Discipline, RunInfo.discipline_id == Discipline.id, isouter=True). \
            filter(RunInfo.race_id == data['race_id'], RunInfo.run_type_id != 3).all()

        race_info = {}
        for run in run_list:
            race_info[run[0].id] = {
                'starttime': (None if run[0].starttime is None else str(run[0].starttime)),
                'endtime': (None if run[0].endtime is None else str(run[0].endtime)),
                'number': run[0].number,
                'type': run[1].name,
                'is_second': run[0].is_second,
                'discipline': (None if run[2] is None
          else run[2].en_name),
                'discipline_fiscode': (None if run[2] is None
                               else run[2].fiscode),
                'courses': {},
                'start_list': runList_view(db.session.query(Competitor, RaceCompetitor, RunOrder).join(RaceCompetitor).\
                    join(RunOrder).filter(RunOrder.run_id == run[0].id).\
                    order_by(RunOrder.is_participate.asc(), RunOrder.order.asc()).all())
            }
            courses = db.session.query(Course).filter(Course.id == RunCourses.course_id,
                                                      RunCourses.run_id == run[0].id).all()
            for course in courses:
                race_info[run[0].id]['courses'][course.id] = {
                    'name': course.en_name,
                    'devices': []
                }
                devices = db.session.query(CourseDevice, CourseDeviceType).\
                    join(CourseDeviceType, CourseDevice.course_device_type_id == CourseDeviceType.id).\
                    filter(CourseDevice.course_id == course.id).all()
                for device in devices:
                    race_info[run[0].id]['courses'][course.id]['devices'].append({
                        'id': device[0].id,
                        'order': device[0].order,
                        'distance': device[0].distance,
                        'type': device[1].name,
                    })
        socketio.emit('RaceInfo', json.dumps({'run_list': race_info}))
        print(json.dumps({'run_list': race_info}))
        forerunners_runs = RunInfo.query.filter(RunInfo.race_id == data['race_id'], RunInfo.starttime != None,
                                                RunInfo.run_type_id == 3).first()
        if forerunners_runs is not None:
            run_list = db.session.query(Forerunner, CourseForerunner, RaceCompetitor, RunOrder). \
                join(CourseForerunner, CourseForerunner.forerunner_id == Forerunner.id).filter(
                RunOrder.run_id == forerunners_runs.id). \
                join(RaceCompetitor, RaceCompetitor.forerunner_id == CourseForerunner.id). \
                join(RunOrder).filter(RunOrder.run_id == forerunners_runs.id). \
                order_by(RunOrder.order).all()
            results, manual, dql_list = TreeView(forerunners_runs.id)

            courses = db.session.query(Course).filter(Course.id == RunCourses.course_id,
                                                      RunCourses.run_id == forerunners_runs.id).all()
            result = \
                {
                    forerunners_runs.id:
                    [
                        {
                            'starttime': (None if forerunners_runs.starttime is None else str(forerunners_runs.starttime)),
                            'endtime': (None if forerunners_runs.endtime is None else str(forerunners_runs.endtime)),
                            'number': forerunners_runs.number,
                            'courses': {},
                            'start_list': runList_view([[item[0], item[2], item[3]] for item in run_list])
                        },
                        ConvertRunResults(results, manual, dql_list)
                    ]
                }
            for course in courses:
                result[forerunners_runs.id][0]['courses'][course.id] = {
                    'name': course.en_name,
                    'devices': []
                }
                devices = db.session.query(CourseDevice, CourseDeviceType). \
                    join(CourseDeviceType, CourseDevice.course_device_type_id == CourseDeviceType.id). \
                    filter(CourseDevice.course_id == course.id).all()
                for device in devices:
                    result[forerunners_runs.id][0]['courses'][course.id]['devices'].append({
                        'id': device[0].id,
                        'order': device[0].order,
                        'distance': device[0].distance,
                        'type': device[1].name,
                    })

            socketio.emit('ForerunnersResults', json.dumps(result))

@raceinfo.route('/raceinfo/<int:race_id>', methods=['GET', 'POST'])
def get_race_info2(race_id):

    run_list = db.session.query(RunInfo, RunType, Discipline).\
        join(RunType, RunInfo.run_type_id == RunType.id). \
        join(Discipline, RunInfo.discipline_id == Discipline.id, isouter=True). \
        filter(RunInfo.race_id == race_id, RunInfo.run_type_id != 3).all()

    race_info = {}
    for run in run_list:
        race_info[run[0].id] = {
            'starttime': (None if run[0].starttime is None else str(run[0].starttime)),
            'endtime': (None if run[0].endtime is None else str(run[0].endtime)),
            'number': run[0].number,
            'type': run[1].name,
            'is_second': run[0].is_second,
            'discipline': (None if run[2] is None
      else run[2].en_name),
            'discipline_fiscode': (None if run[2] is None
                           else run[2].fiscode),
            'courses': {},
            'start_list': runList_view(db.session.query(Competitor, RaceCompetitor, RunOrder).join(RaceCompetitor).\
                join(RunOrder).filter(RunOrder.run_id == run[0].id).
                                       order_by(RunOrder.is_participate.desc(), RunOrder.order.asc()).all())
        }
        courses = db.session.query(Course).filter(Course.id == RunCourses.course_id,
                                                  RunCourses.run_id == run[0].id).all()
        for course in courses:
            race_info[run[0].id]['courses'][course.id] = {
                'name': course.en_name,
                'devices': []
            }
            devices = db.session.query(CourseDevice, CourseDeviceType).\
                join(CourseDeviceType, CourseDevice.course_device_type_id == CourseDeviceType.id).\
                filter(CourseDevice.course_id == course.id).all()
            for device in devices:
                race_info[run[0].id]['courses'][course.id]['devices'].append({
                    'id': device[0].id,
                    'order': device[0].order,
                    'distance': device[0].distance,
                    'type': device[1].name,
                })
    return json.dumps({'run_list': race_info})


@raceinfo.route('/run/competitor/clear', methods=['GET', 'POST'])
@login_required
@admin_required
def competitor_clear():
    raceHandler = RaceGetter.getRaceByRunid(run_id=request.args.get('run_id'))
    raceHandler.competitor_clear(competitor_id=request.args.get('competitor_id'))
    raceHandler.recalculate_run_results()
    socketio.emit('removeResult', json.dumps(
        {
            'removed_competitor': request.args.get('competitor_id'),
            'manual_order': raceHandler.runOrder.manual_order
         }))
    return 'OK'


@raceinfo.route('/run/competitor/start', methods=['GET', 'POST'])
@login_required
@admin_required
def competitor_start():
    raceHandler = RaceGetter.getRaceByRunid(run_id=request.args.get('run_id'))
    raceHandler.competitor_manualstart(competitor_id=request.args.get('competitor_id'))
    return '', 200


@raceinfo.route('/input/data', methods=['POST', 'GET'])
@exectutiontime('Full time')
def load_data_vol3():
    """
        NewDataStart (Информация о старте спортсмена (race_competitor_id, absolut_time, run_id))
        NewDataPoint (Текущий спортсмен + список пересчитанных рангов (sectorrank, rank) на текущем устройсве)
        NewDataFinish (Полный набор данных для всего заезда)
    """
    # semaphore.acquire()

    try:
        data = request.json
        data['TIME'] = int(datetime.strptime(data['TIME'], '%d.%m.%Y %H:%M:%S.%f').timestamp()*1000)
        raceHandler = RaceGetter.getRace(data)
        if raceHandler is None:
            raise Exception("Race is not found")
        else:
            raceHandler.setDeviceDataInDB(data)
            raceHandler.competitor_get_current()
            if raceHandler.is_start():
                print('NewDataStart', data, raceHandler.__class__.__name__, raceHandler.courseDeviceType.name)
                if raceHandler.competitor is None:
                    raceHandler.competitor_autostart()
                raceHandler.resultApprove.is_start = True
                raceHandler.set_start_result_detail()
                socketio.emit("NewDataStart", json.dumps({raceHandler.run.id: {
                    raceHandler.courseDevice.course_id: ConvertCompetitorStart(raceHandler.result,
                                                                               raceHandler.courseDevice,
                                                                               raceHandler.data_in)}
                }))

                scoreboard = Scoreboard(raceHandler)
                scoreboard.started_competitor()
                scoreboard.send()

                db.session.add(raceHandler.result)
                db.session.commit()

                raceHandler.resultApprove.start_time = raceHandler.result.absolut_time
                return ''
            else:
                if raceHandler.is_competitor():
                    raceHandler.set_result_detail()

                    raceHandler.calculate_personal_sector_params()
                    if raceHandler.is_finish_():
                        raceHandler.competitor_finish()
                        db.session.add(raceHandler.result)
                        db.session.commit()
                        tree_view, manual_list, dql_list = raceHandler.recalculate_run_results()
                        print('NewDataFinish', data, raceHandler.__class__.__name__, raceHandler.courseDeviceType.name)
                        socketio.emit("NewDataFinish", json.dumps({
                            raceHandler.run.id: [
                                {
                                    raceHandler.courseDevice.course_id: ConvertCompetitorFinish(raceHandler.result, raceHandler.courseDevice, raceHandler.resultApprove,
                                                                               raceHandler.data_in)
                                },
                                ConvertRunResults(tree_view, manual_list, dql_list)
                            ]
                        }))

                        scoreboard = Scoreboard(raceHandler)
                        if raceHandler.result.rank == 1:
                            scoreboard.new_best_time()
                            scoreboard.send()
                        scoreboard.finished_competitor()
                        scoreboard.send()
                        scoreboard.finished_list()
                        scoreboard.send()

                    else:
                        print('NewDataPoint', data, raceHandler.__class__.__name__, raceHandler.courseDeviceType.name)
                        result_details = raceHandler.get_sector_results()
                        raceHandler.calculate_common_sector_params(result_details)
                        socketio.emit("NewDataPoint", json.dumps({
                            raceHandler.run.id: [
                                {
                                    raceHandler.courseDevice.course_id: ConvertCompetitorStart(raceHandler.result,
                                                                                               raceHandler.courseDevice,
                                                                               raceHandler.data_in)
                                },
                                    ConvertCompetitorsRankList(result_details, raceHandler.courseDevice)
                            ]

                        }))

                        db.session.add(raceHandler.result)
                        db.session.commit()
                        scoreboard = Scoreboard(raceHandler)
                        scoreboard.crossed_device()
                        scoreboard.send()
    except:
        data_in = DataIn(
            src_sys=data['SRC_SYS'],
            src_dev=data['SRC_DEV'],
            event_code=data['EVENT_CODE'],
            time=data['TIME'],
        )
        print(data)
        db.session.add(data_in)
        db.session.commit()
        socketio.emit("ErrorData", ConvertErrorData(data_in))
    # finally:
    #     semaphore.release()
    #     print('released')
    return '', 200

@socketio.on('DataInChangeCompetitors')
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
        raceHandler = RaceGetter.getRaceByRunid(run_id)
        if raceHandler is None:
            socketio.emit('change/data_in/error', 'Ошибка получения гонки')
        else:
            raceHandler.recalculate_run_results(run_id)
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

