from .. import socketio
from ..decorators import admin_required
from .models import *
from . import jsonencoder, raceinfo
import json
from distutils.util import strtobool
from functools import wraps
from sqlalchemy import cast, DATE, func, asc, and_
from flask_login import current_user, login_required
from .DataViewer import ConvertRunResults, ConvertCompetitorStart, ConvertCompetitorsRankList, ConvertCompetitorFinish, \
    TreeView, TreeView2
from datetime import datetime, timedelta
from flask import request, render_template
from .Scoreboard import Scoreboard

from .Race import RaceGetter

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
    RunType.insert()
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

# /approve/edit/run/18/competitor/9?
# @raceinfo.route('/approve/edit/run/<int:run_id>/competitor/<int:competitor_id>', methods=['POST', 'GET'])
@socketio.on('CompetitorManualApprove')
def manual_approve(data):
    raceHandler = RaceGetter.getRaceByRunid(data['run_id'])
    raceHandler.competitor_manualapprove(data['competitor_id'],
                                         data['status_id'],
                                         data['finish_time'],
                                         data['start_time'],
                                         data['gate'],
                                         data['reason'])


@socketio.on('GetResults')
def socket_get_results(data):
    # data = json.loads(json_data)
    if 'run_id' in data.keys():
        run = RunInfo.query.get(data['run_id'])
        results, manual = TreeView(data['run_id'])
        socketio.emit('Results', json.dumps({
            run.id: ConvertRunResults(results, manual)

        }))
    if 'race_id' in data.keys():
        run_list = RunInfo.query.filter(RunInfo.race_id == data['race_id'], RunInfo.starttime != None).all()
        result_list = {}
        for run in run_list:
            results, manual = TreeView(run.id)
            result_list[run.id] = ConvertRunResults(results, manual)
        socketio.emit('Results', json.dumps(result_list))
    else:
        return

@socketio.on('ScoreboardSendStartlist')
def scoreboard_send_start_list(data):
    raceHandler = RaceGetter.getRaceByRunid(data['run_id'])
    scoreboard = Scoreboard(raceHandler)
    scoreboard.start_list()
    scoreboard.send()

@socketio.on('GetRaceInfo')
def get_race_info(data):
    if 'race_id' in data.keys():
        run_list = db.session.query(RunInfo, RunType, Discipline).\
            join(RunType, RunInfo.run_type_id == RunType.id). \
            join(Discipline, RunInfo.discipline_id == Discipline.id, isouter=True). \
            filter(RunInfo.race_id == data['race_id']).all()

        race_info = {}
        for run in run_list:
            race_info[run[0].id] = {
                'starttime': str(run[0].starttime),
                'endtime': str(run[0].endtime),
                'number': run[0].number,
                'type': run[1].name,
                'discipline': (None if run[2] is None
          else run[2].en_name),
                'discipline_fiscode': (None if run[2] is None
                               else run[2].fiscode),
                'courses': {}
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


@raceinfo.route('/run/competitor/clear', methods=['GET', 'POST'])
@login_required
@admin_required
def competitor_clear():
    raceHandler = RaceGetter.getRaceByRunid(run_id=request.args.get('run_id'))
    raceHandler.competitor_clear(competitor_id=request.args.get('competitor_id'))
    raceHandler.recalculate_run_results()
    socketio.emit('removeResult', json.dumps(dict(removed_competitor=request.args.get('competitor_id'))))
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
        d
    """
    data = request.json
    data['TIME'] = int(datetime.strptime(data['TIME'], '%d.%m.%Y %H:%M:%S.%f').timestamp()*1000)

    raceHandler = RaceGetter.getRace(data)
    raceHandler.setDeviceDataInDB(data)
    raceHandler.competitor_get_current()
    if raceHandler.is_start():
        if raceHandler.competitor is None:
            raceHandler.competitor_autostart()
        raceHandler.resultApprove.is_start = True
        raceHandler.set_start_result_detail()

        socketio.emit("NewDataStart", json.dumps({raceHandler.run.id: {
            raceHandler.courseDevice.course_id: ConvertCompetitorStart(raceHandler.result, raceHandler.courseDevice)}
        }))
        print(str(raceHandler.get_competitor_info()))
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
                tree_view, manual_list = raceHandler.recalculate_run_results()

                socketio.emit("NewDataFinish", json.dumps({
                    raceHandler.run.id: [
                        {
                            raceHandler.courseDevice.course_id: ConvertCompetitorFinish(raceHandler.result, raceHandler.courseDevice, raceHandler.resultApprove)
                        },
                        ConvertRunResults(tree_view, manual_list)
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
                result_details = db.session.query(ResultDetail). \
                    filter(
                    ResultDetail.course_device_id == raceHandler.courseDevice.id,
                    ResultDetail.run_id == raceHandler.run.id).all()
                raceHandler.calculate_common_sector_params(result_details)

                socketio.emit("NewDataPoint", json.dumps({
                    raceHandler.run.id: [
                        {
                            raceHandler.courseDevice.course_id: ConvertCompetitorStart(raceHandler.result, raceHandler.courseDevice)},
                            ConvertCompetitorsRankList(result_details, raceHandler.courseDevice)
                    ]

                }))
                db.session.add(raceHandler.result)
                db.session.commit()
                scoreboard = Scoreboard(raceHandler)
                scoreboard.crossed_device()
                scoreboard.send()

    return '', 200