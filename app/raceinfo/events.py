from .. import socketio, db
from ..decorators import admin_required
from .models import *
from . import jsonencoder, raceinfo
import json

from functools import wraps
from sqlalchemy import cast, DATE, func, asc

from flask_login import current_user, login_required
from datetime import datetime, timedelta
from flask import request, render_template

def exectutiontime(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        print('Elapsed time:', (end-timedelta(hours=start.hour,minutes=start.minute,seconds=start.second,microseconds=start.microsecond)).time())
        return result
    return wrapper

@raceinfo.route('/d')
def device_1get():
    db.create_all()
    return ''

@raceinfo.route('/emulation')
def emulation():
    db.engine.execute('delete from data_in;')
    db.engine.execute('delete from result_approved;')
    db.engine.execute('delete from result_detail; ')
    db.engine.execute('delete from result;')
    db.engine.execute('delete from "CASHE";')
    db.engine.execute('update run_info set endtime=NULL;')
    db.engine.execute('INSERT INTO "CASHE" (id, key, data) VALUES (1,\'Current_competitor\', \'{"run": 1, "order": 0}\')')
    db.engine.execute('update run_info set starttime=NULL where number!=1;')
    db.engine.execute('update run_order set manual_order=NULL;')

    return render_template('timer.html')

@raceinfo.route('/receiver')
def receiver():
    return render_template('receiver.html')

@raceinfo.route('/receiver_jury')
@admin_required
def receiver_jury():
    return render_template('receiver_jury.html')

@raceinfo.route('/run/get/', methods=['POST', 'GET'])
def run_get():
    if 'race_id' in request.args:
        race_id = request.args['race_id']
        data = json.dumps(RunInfo.query.filter(RunInfo.race_id == race_id).all(), cls=jsonencoder.AlchemyEncoder)
        return data
    return json.dumps(RunInfo.query.filter(cast(RunInfo.starttime, DATE) == datetime.now().date()).all(), cls=jsonencoder.AlchemyEncoder)

@raceinfo.route('/startlist/run/<int:run_id>/get/', methods=['POST', 'GET'])
def startlist_get(run_id):
    data = json.dumps(db.session.query(Competitor,RaceCompetitor,RunOrder).join(RaceCompetitor).join(RunOrder).filter(RunOrder.run_id==run_id).order_by(RunOrder.order).all(), cls=jsonencoder.AlchemyEncoder)
    return data

@raceinfo.route('/device/get/course/<int:course_id>')
def device_get(course_id):
    return json.dumps(db.session.query(CourseDevice, CourseDeviceType).join(CourseDeviceType).filter(CourseDevice.course_id == course_id).all(), cls=jsonencoder.AlchemyEncoder)

@raceinfo.route('/input/data', methods=['POST', 'GET'])
@exectutiontime
def load_data_vol2():
    data = json.loads(request.args['data'])
    # Перевести на кэш {
    # Девайс с которого пришли данные
    device = Device.query.filter_by(src_dev=data['src_dev']).one()
    # Трассы на которых стоит этот девайс
    course_devices = db.session.query(CourseDevice.course_id).filter_by(device_id=device.id)
    courses = db.session.query(Course.id).filter(Course.id.in_(course_devices))
    # Заезд с пришли данные

    run = RunInfo.query.filter(RunInfo.course_id.in_(courses), RunInfo.starttime < datetime.now(), RunInfo.endtime == None ).one()

    # Сам девайс с которого пришли данные
    course_device = db.session.query(CourseDevice, CourseDeviceType).join(CourseDeviceType).\
        filter(CourseDevice.device_id == device.id,
               CourseDevice.course_id == run.course_id).one()

    competitor = get_current_competitor(course_device[0].id, run.id)
    print('Old race competitor id:', competitor[0].id)

    device_data = setDeviceDataInDB(data, run.id)

    result = ResultDetail(
        course_device_id=course_device[0].id,
        race_competitor_id=competitor[0].id,
        run_id=run.id,
        data_in_id=device_data.id,
        absolut_time=data['time'])

    if course_device[1].name == "Start":
        result.time = 0
        result.sectortime = 0
        result.is_start = True
    else:
        start_device = db.session.query(CourseDevice.id).filter(CourseDevice.course_id == run.course_id,
                                                                CourseDevice.course_device_type_id == 1)

        try:
           start_result = ResultDetail.query.filter(ResultDetail.race_competitor_id == result.race_competitor_id,
                                                    ResultDetail.course_device_id == start_device,
                                                    ResultDetail.run_id == run.id).one()
        except Exception as e:
            socketio.emit('errorHandler', json.dumps(dict([('ERROR', '0000x1'),
                                                           ('TIME', datetime.now().time().__str__()),
                                                           ('MESSAGE', 'Ошибка: дублирование данных'),
                                                           ('DATA', json.dumps(device_data, cls=jsonencoder.AlchemyEncoder)),
                                                           ('COMPETITOR', json.dumps(competitor, cls=jsonencoder.AlchemyEncoder))
                                                           ])))
            socketio.emit('get/results/response',
                          json.dumps([device_data, None, competitor], cls=jsonencoder.AlchemyEncoder))
            return ''
        try:
            previous_course_device = CourseDevice.query.filter_by(order=course_device[0].order - 1, course_id=run.course_id).one()

            previous_device_results = db.session.query(ResultDetail).filter(ResultDetail.course_device_id == previous_course_device.id,
                ResultDetail.race_competitor_id == result.race_competitor_id,  ResultDetail.run_id == run.id).one()
            result.time = data['time'] - start_result.absolut_time
            result.sectortime = data['time'] - previous_device_results.absolut_time
            result.speed = ((course_device[0].distance - previous_course_device.distance)/1000) / (result.sectortime/3600000)
        except:
            pass
        if course_device[1].name == "Finish":
            competitor_finish(competitor[0].id, run.id)

    db.session.add(result)
    db.session.commit()
    result_details = db.session.query(ResultDetail).\
        filter(
            ResultDetail.course_device_id == course_device[0].id,
            ResultDetail.run_id == run.id).all()

    if len(result_details) == 1:
        result.diff = 0
        result.sectordiff = 0
        result.sectorrank = 1
        result.rank = 1
    else:
        min_time_result = min(result_details, key=lambda item: item.time)
        min_sectortime_result = min(result_details, key=lambda item: item.sectortime)

        for item in result_details:
            item.diff = item.time - min_time_result.time
            item.sectordiff = item.sectortime - min_sectortime_result.sectortime

        result_details.sort(key=lambda item: item.diff)
        for index, item in enumerate(result_details):
            item.rank = index+1

        result_details.sort(key=lambda item: item.sectordiff)
        for index, item in enumerate(result_details):
            item.sectorrank = index + 1
    socketio.emit('get/results/response', json.dumps([device_data, result, competitor], cls=jsonencoder.AlchemyEncoder))
    socketio.emit("newData", json.dumps(
        dict(current_object=[
        result_details.pop(result_details.index(result)),
        competitor[0],
        competitor[1],
        course_device[0],
        course_device[1]
    ],
        list_of_object=result_details), cls=jsonencoder.AlchemyEncoder))

    return '', 200

@raceinfo.route('/current_data/get/<int:race_id>', methods=['POST', 'GET'])
def get_current_data(race_id):
    return json.dumps(db.session.query(ResultDetail,RaceCompetitor, Competitor, CourseDevice,ResultApproved).join(RaceCompetitor)
                      .join(Competitor).join(CourseDevice).join(ResultApproved)\
                      .filter(RaceCompetitor.race_id == race_id)\
                      .all(), cls=jsonencoder.AlchemyEncoder)


def setDeviceDataInDB(data, run_id):
    input_data = DataIn(
        src_sys=data['src_sys'],
        src_dev=data['src_dev'],
        event_code=data['eventcode'],
        time=data['time'],
        reserved=data['reserved'],
        run_id = run_id
    )
    if 'bib' in data:
        input_data.bib = data['bib']
    db.session.add(input_data)
    db.session.commit()
    return input_data


@raceinfo.route('/run/competitor/start', methods=['GET', 'POST'])
@login_required
@admin_required
def competitor_start():
    result_approves = ResultApproved(
        race_competitor_id=request.args.get('competitor_id'),
        run_id=request.args.get('run_id'),
        is_start=True)
    db.session.add(result_approves)
    db.session.commit()
    competitor_order = db.session.query(func.count('*')).select_from(RunOrder).\
                           filter(RunOrder.run_id == request.args.get('run_id'),
                                  RunOrder.manual_order != None).\
                           scalar()+1
    current_competitor = RunOrder.query.filter(RunOrder.race_competitor_id == request.args.get('competitor_id'),
                                               RunOrder.run_id == request.args.get('run_id')).one()

    current_competitor.manual_order = competitor_order
    db.session.add(current_competitor)
    db.session.commit()
    print('competitor_order', competitor_order)
    return '', 200


def get_current_competitor(course_device_id, run_id):
    competitor_order = db.session.query(func.count('*')).select_from(ResultDetail). \
                           filter(ResultDetail.run_id == run_id,
                                  ResultDetail.course_device_id == course_device_id). \
                           scalar() + 1
    print('function: get_current_competitor')
    print('competitor_order', competitor_order)
    try:
        race_competitor = db.session.query(RaceCompetitor, Competitor, RunOrder).\
            join(Competitor).\
            join(RunOrder).\
            filter(RunOrder.manual_order == competitor_order, RunOrder.run_id == run_id).one()
    except:
        race_competitor = db.session.query(RaceCompetitor, Competitor, RunOrder). \
            join(Competitor). \
            join(RunOrder). \
            filter(RunOrder.manual_order == None, RunOrder.run_id == run_id).order_by(asc(RunOrder.order)).limit(1).one()
        race_competitor[2].manual_order = competitor_order
        result_approves = ResultApproved(
            race_competitor_id=race_competitor[0].id,
            run_id=run_id,
            is_start=True)
        db.session.add(result_approves)
        db.session.add(race_competitor[2])
        db.session.commit()
    print('New race competitor id:', race_competitor[0].id)
    return race_competitor


# Not required, rewrite to automatic
# @raceinfo.route('/run/competitor/finish', methods=['GET', 'POST'])
# @login_required
# @admin_required
def competitor_finish(competitor_id, run_id):
    try:
        result_approves = ResultApproved.query.filter_by(
            race_competitor_id=competitor_id,
            run_id=run_id).one()
        # Если что ипсправить
        result_approves.status_id = 1
        result_approves.is_finish = True
        db.session.add(result_approves)
        db.session.commit()
        return
    except Exception as err:
        return
# Без разницы какую функцию использовать в случае, если
# компетитор упал, мы писали функцию для отмены старта, ее и можно использовать,
# если не нравится написал функцию competitor_remove по URL /run/competitor/remove
# но если судья сразу не отменит спортсмена есть вероятность
# потерять акктуальные данные следующего спортсмена
# Жюри придется их доставать из "ямы" сырых данных :-)

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
   ResultApproved.query.filter(
       ResultApproved.race_competitor_id == request.args.get('competitor_id'),
       ResultApproved.run_id == request.args.get('run_id')
   ).delete()
   ResultDetail.query.filter(
       ResultDetail.race_competitor_id == request.args.get('competitor_id'),
       ResultDetail.run_id == request.args.get('run_id')
   ).delete()

   socketio.emit('removeResult', json.dumps(dict(removed_competitor=request.args.get('competitor_id'))))

   return '', 200

@raceinfo.route('/approve/run/<int:run_id>/competitor/<int:competitor_id>')
@admin_required
def approve_automate(run_id, competitor_id):
   status = Status.query.filter_by(name='QLF').one()
   try:
       ResultApproved.query.filtel(ResultApproved.race_competitor_id==competitor_id, ResultApproved.run_id==run_id).one()
       return 'record allredy exist', 200
   except:
       try:
           result = Result.query.filter_by(race_competitor_id=competitor_id).one()
       except:
           result = Result(race_competitor_id=competitor_id)
           db.session.add(result)
           db.session.commit()

       resultDetail = ResultApproved.query.filter_by(race_competitor_id=competitor_id, run_id=run_id).one()
       resultDetail.is_manual = True
       resultDetail.is_manual = False
       resultDetail.approve_user = current_user.id
       resultDetail.approve_time = datetime.now()
       resultDetail.race_competitor_id = competitor_id
       resultDetail.run_id = run_id
       resultDetail.status_id = status.id
       resultDetail.result_id = result.id

       db.session.add(resultDetail)
       db.session.commit()

       return 'ok', 200


@raceinfo.route('/approve/edit/run/<int:run_id>/competitor/<int:competitor_id>')
def approve_manual(run_id, competitor_id):
    data = json.loads(request.args['data'])
    try:
        result = Result.query.filter_by(race_competitor_id=competitor_id).one()
    except:
        result = Result(race_competitor_id=competitor_id)
        db.session.add(result)
        db.session.commit()

    resultDetail = ResultApproved.query.filter_by(race_competitor_id=competitor_id, run_id=run_id).one()
    resultDetail.is_manual = True,
    resultDetail.approve_user = current_user.id
    resultDetail.approve_time = datetime.now()
    resultDetail.status_id = data['status_id']
    if data['absolur_time'] != '':
        resultDetail.timerun = data['absolut_time']
    resultDetail.result_id = result.id
    resultDetail.gate = data['gate']
    resultDetail.reason = data['reason']

    db.session.add(resultDetail)
    db.session.commit()

    return 'Ok', 200

def result_detail_recount(result_details):
    min_time_result = min(result_details, key=lambda item: item.time)
    min_sectortime_result = min(result_details, key=lambda item: item.sectortime)

    for item in result_details:
        item.diff = item.time - min_time_result.time
        item.sectordiff = item.sectortime - min_sectortime_result.sectortime

    result_details.sort(key=lambda item: item.diff)
    for index, item in enumerate(result_details):
        item.rank = index + 1

    result_details.sort(key=lambda item: item.sectordiff)
    for index, item in enumerate(result_details):
        item.sectorrank = index + 1

            # }

    # Запущенный пользователь может быть только один, иначе ошибка
    #
    # try:
    #     resultApproved = ResultApproved.query.filter(ResultApproved.run_id == run.id,
    #                                                  ResultApproved.is_start == True,
    #                                                  ResultApproved.is_finish == None).one()
    # except Exception as e:
    #     device_data = setDeviceDataInDB(data)
    #     socketio.emit('errorHandler', json.dumps(dict([('ERROR', '000000'),
    #                                                    ('TIME', datetime.now().time().__str__()),
    #                                                    ('MESSAGE', 'Ошибка получения компетитора'),
    #                                                    ('DATA', json.dumps(device_data, cls=jsonencoder.AlchemyEncoder))
    #                                                    ])))
    #     return ''
    #  Получение компетитора
    # competitor = db.session.query(RaceCompetitor, Competitor).join(Competitor).filter(RaceCompetitor.id == resultApproved.race_competitor_id).one()

@socketio.on('get/results')
def socket_get_results(data):
    socketio.emit('get/results/response', json.dumps(db.session.query(DataIn, ResultDetail, RaceCompetitor).
                                                     join(ResultDetail, isouter=True).
                                                     join(RaceCompetitor, isouter=True).
                                                     filter(DataIn.run_id == data['run_id']).order_by(asc(DataIn.id)).
                                                     all(),
                                                     cls=jsonencoder.AlchemyEncoder))