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
    ResultFunction.insert()
    Discipline.insert_discipline()
    Gender.insert_genders()
    Status.insert()
    Jury_function.insert_functions()
    CourseDeviceType.insert_types()
    return ''

@raceinfo.route('/emulation')
def emulation():
    db.engine.execute('delete from result_detail; ')
    db.engine.execute('delete from data_in;')
    db.engine.execute('delete from result_approved;')
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

@raceinfo.route('/jury_page')
@admin_required
def jury_page():
    return render_template('jury_page.html')

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
    print('Competitor RUN INFO:')
    print('Current device:', course_device[0].id, 'order:', course_device[0].order, 'type:', course_device[1].name)
    device_data = setDeviceDataInDB(data, run.id, course_device[0].id)

    result = ResultDetail(
        course_device_id=course_device[0].id,
        race_competitor_id=competitor[0].id,
        run_id=run.id,
        data_in_id=device_data.id,
        absolut_time=data['time'])
    print('Current data: competitor', result.race_competitor_id, 'absolut_time:', result.absolut_time)
    result_details = db.session.query(ResultDetail). \
        filter(
        ResultDetail.course_device_id == course_device[0].id,
        ResultDetail.run_id == run.id).all()
    print('Competitors crossed this  device:', len(result_details))
    for index, item in enumerate(result_details):
        print(index,'.', item.race_competitor_id)
    if course_device[1].name == "Start":
        result.sectortime = 0
        result.sectordiff = 0
        result.is_start = True
    else:
    # socketio.emit('get/results/response',
    #               json.dumps([device_data, None, competitor], cls=jsonencoder.AlchemyEncoder))
    # return ''
    #     calculate_sector_params(result, course_device[0], run.course_id, result_details)
        calculate_personal_sector_params(result, course_device[0], run.course_id)
        calculate_common_sector_params(result, result_details)

        if course_device[1].name == "Finish":
            finished_competitors = db.session.query(ResultDetail).filter(
                ResultDetail.course_device_id == course_device[0].id,
                ResultDetail.run_id == run.id).all()
            competitor_finish(competitor[0].id, run.id)
            calculate_finish_params(result, finished_competitors)


    db.session.add(result)
    db.session.commit()

    socketio.emit('get/results/response', json.dumps([device_data, result, competitor], cls=jsonencoder.AlchemyEncoder))
    socketio.emit("newData", json.dumps(
        dict(current_object=[
        result,
        competitor[0],
        competitor[1],
        course_device[0],
        ResultApproved.query.filter(ResultApproved.race_competitor_id == competitor[0].id, ResultApproved.run_id == run.id).one(),
        course_device[1]
    ],
        list_of_object=result_details), cls=jsonencoder.AlchemyEncoder))

    return '', 200

@raceinfo.route('/current_data/get/<int:race_id>', methods=['POST', 'GET'])
def get_current_data(race_id):
    return json.dumps(db.session.query(ResultDetail,RaceCompetitor, Competitor, CourseDevice, ResultApproved, CourseDeviceType).join(RaceCompetitor)
                      .join(Competitor).join(CourseDevice).join(ResultApproved).join(CourseDeviceType)\
                      .filter(RaceCompetitor.race_id == race_id)\
                      .all(), cls=jsonencoder.AlchemyEncoder)

def setDeviceDataInDB(data, run_id, cource_device_id):
    input_data = DataIn(
        src_sys=data['src_sys'],
        src_dev=data['src_dev'],
        event_code=data['eventcode'],
        time=data['time'],
        reserved=data['reserved'],
        run_id = run_id,
        cource_device_id=cource_device_id
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
       resultDetail = ResultApproved.query.filtel(ResultApproved.race_competitor_id==competitor_id, ResultApproved.run_id==run_id).one()
       resultDetail.is_manual = True
       resultDetail.is_manual = False
       resultDetail.approve_user = current_user.id
       resultDetail.approve_time = datetime.now()
       resultDetail.race_competitor_id = competitor_id
       resultDetail.run_id = run_id
       resultDetail.status_id = status.id

   except:
       try:
           result = Result.query.filter_by(race_competitor_id=competitor_id).one()
       except:
           result = Result(race_competitor_id=competitor_id)
           db.session.add(result)
           db.session.commit()

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
   try:
       resultDetail = ResultApproved.query.filter_by(race_competitor_id=competitor_id, run_id=run_id).one()
   except:
       resultDetail = ResultApproved(
           race_competitor_id=competitor_id,
           run_id=run_id
       )
   resultDetail.is_manual = True
   resultDetail.approve_user = current_user.id
   resultDetail.approve_time = datetime.now()
   resultDetail.status_id = data['status_id']
   if data['absolut_time'] != '':
       resultDetail.timerun = data['absolut_time']
   resultDetail.result_id = result.id
   resultDetail.gate = data['gate']
   resultDetail.reason = data['reason']

   db.session.add(resultDetail)
   db.session.commit()
   return 'Ok', 200


def calculate_finish_params(current_competitor_finish, finished_competitors):
    start_result = db.session.query(ResultDetail).filter(ResultDetail.run_id == current_competitor_finish.run_id,
                                          ResultDetail.race_competitor_id == current_competitor_finish.race_competitor_id,
                                          ResultDetail.is_start == True).one()
    current_competitor_finish.time = current_competitor_finish.absolut_time - start_result.absolut_time

    сompetitors_list = sorted([current_competitor_finish] + finished_competitors, key=lambda item: item.time)

    for index, item in enumerate(сompetitors_list):
        item.diff = item.time - сompetitors_list[0].time
        item.rank = index + 1

# def calculate_sector_params(current_competitor, device, course_id, device_competitors_list):
#     print("function: calculate_sector_params")
#     previous_course_device = CourseDevice.query.filter_by(order=device.order-1, course_id=course_id).one()
#
#     print("current device order:%s" % device.order)
#     print("previous device order:%s" % previous_course_device.order)
#
#     previous_device_results = db.session.query(ResultDetail).filter(ResultDetail.course_device_id == previous_course_device.id,
#                                                                     ResultDetail.race_competitor_id == current_competitor.race_competitor_id,
#                                                                     ResultDetail.run_id == current_competitor.run_id).one()
#     print("previous device result:%s" % previous_device_results.id, previous_device_results.absolut_time, previous_device_results.sectortime, previous_device_results.sectordiff, previous_device_results.sectorrank )
#     current_competitor.sectortime = current_competitor.absolut_time - previous_device_results.absolut_time
#
#     current_competitor.speed = ((device.distance - previous_course_device.distance) / 1000) / (current_competitor.sectortime / 3600000)
#     if len(device_competitors_list) != 0:
#         min_сompetitor = min(device_competitors_list, key=lambda item: item.sectortime)
#         if min_сompetitor.sectortime < current_competitor.sectortime:
#             сompetitors_list = sorted([current_competitor] + device_competitors_list, key=lambda item: item.sectortime)
#             for index, item in enumerate(сompetitors_list):
#                 item.sectordiff = item.sectortime - сompetitors_list[0].sectortime
#                 item.sectorrank = index + 1
#                 print('competitor id:', item.race_competitor_id, 'sector diff:', item.sectordiff,'sector rank:', item.sectorrank)
#         else:
#             current_competitor.sectordiff = current_competitor.sectortime - min_сompetitor.sectortime
#             current_competitor.sectorrank = 1
#             сompetitors_list = sorted([current_competitor] + device_competitors_list, key=lambda item: item.sectortime)
#             for index, item in enumerate(сompetitors_list):
#                 # item.sectordiff = item.sectortime - сompetitors_list[0].sectortime
#                 item.sectorrank = index + 2
#                 print('competitor id:', item.race_competitor_id, 'sector diff:', item.sectordiff, 'sector rank:', item.sectorrank)
#     else:
#         current_competitor.sectordiff = 0
#         current_competitor.sectorrank = 1


def calculate_personal_sector_params(current_competitor, device, course_id):
    previous_course_device = CourseDevice.query.filter_by(order=device.order-1, course_id=course_id).one()

    previous_device_results = db.session.query(ResultDetail).filter(ResultDetail.course_device_id == previous_course_device.id,
                                                                    ResultDetail.race_competitor_id == current_competitor.race_competitor_id,
                                                                    ResultDetail.run_id == current_competitor.run_id).one()
    current_competitor.sectortime = current_competitor.absolut_time - previous_device_results.absolut_time

    current_competitor.speed = ((device.distance - previous_course_device.distance) / 1000) / (current_competitor.sectortime / 3600000)

# Функция принемает текущий результат и список  объекты ResultDetail
# результатов БЕЗ текущего
def calculate_common_sector_params(current_competitor, competitors_list):
    if len(competitors_list) != 0:
            min_сompetitor = min(competitors_list, key=lambda item: item.sectortime)
            if min_сompetitor.sectortime < current_competitor.sectortime:
                сompetitors_list = sorted([current_competitor] + current_competitor, key=lambda item: item.sectortime)
                for index, item in enumerate(сompetitors_list):
                    item.sectordiff = item.sectortime - сompetitors_list[0].sectortime
                    item.sectorrank = index + 1
            else:
                current_competitor.sectordiff = current_competitor.sectortime - min_сompetitor.sectortime
                current_competitor.sectorrank = 1
                сompetitors_list = sorted([current_competitor] + competitors_list, key=lambda item: item.sectortime)
                for index, item in enumerate(сompetitors_list):
                    # item.sectordiff = item.sectortime - сompetitors_list[0].sectortime
                    item.sectorrank = index + 2
    else:
        current_competitor.sectordiff = 0
        current_competitor.sectorrank = 1


@socketio.on('get/results')
def socket_get_results(data):
    socketio.emit('get/results/response', json.dumps(db.session.query(DataIn, ResultDetail, RaceCompetitor).
                                                    join(ResultDetail, isouter=True).
                                                    join(RaceCompetitor, isouter=True).
                                                    filter(DataIn.run_id == data['run_id']).
                                                    all(),
                  cls=jsonencoder.AlchemyEncoder))


@socketio.on('change/data_in/competitors')
def edit_cometitor(json_data):
    data = json.loads(json_data)
    for item in data:
        if item['ResultDetail'] is not None:
            resultDetail = ResultDetail.query.filter(ResultDetail.id == item['ResultDetail']).one()

            resultDetail.race_competitor_id = item['RaceCompetitor']
        else:
            dataIn = DataIn.query.filter(DataIn.id == item['DataIn']).one()
            resultDetail = ResultDetail(
                course_device_id=dataIn.cource_device_id,
                race_competitor_id=item['RaceCompetitor'],
                run_id=dataIn.run_id,
                data_in_id=dataIn.id,
                absolut_time=dataIn.time
            )
            db.session.add(resultDetail)
            db.session.commit()

        device = CourseDevice.query.filter(Device.id == resultDetail.course_device_id).one()
        competitors_list = ResultDetail.query.filter(ResultDetail.race_competitor_id != resultDetail.race_competitor_id,
                                                     ResultDetail.course_device_id == resultDetail.course_device_id).all()
        calculate_personal_sector_params(resultDetail, device.id, device.course_id)
        calculate_common_sector_params(resultDetail, competitors_list)
        if device.course_device_type_id == 3:
            calculate_finish_params(resultDetail, competitors_list)

    socket_get_results({'run_id': dataIn.run_id})
