from .. import socketio, db
from ..decorators import admin_required
from .models import *
from . import jsonencoder, raceinfo
import json

from functools import wraps
from sqlalchemy import cast, DATE, func, asc, null,

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
    return json.dumps(db.session.query(CourseDevice, CourseDeviceType).join(CourseDeviceType).filter(CourseDevice.course_id == course_id).order_by(CourseDevice.order).all(), cls=jsonencoder.AlchemyEncoder)

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
    db.session.add(result)
    db.session.commit()

    for index, item in enumerate(result_details):
        print(index,'.', item.race_competitor_id)
    if course_device[1].name == "Start":
        result.sectortime = 0
        result.sectordiff = 0
        result.is_start = True
        approvedResult = ResultApproved.query.filter(ResultApproved.race_competitor_id == result.race_competitor_id,
                                                     ResultApproved.run_id == result.run_id).one()
        approvedResult.start_time = result.absolut_time
    elif course_device[1].name == "Finish":
        competitor_finish(competitor[0].id, run.id, result.absolut_time)
        recalculate_run_resaults(run.id)
        result_details = db.session.query(ResultDetail). \
            filter(ResultDetail.run_id == run.id).all()
    else:
        calculate_personal_sector_params(result, course_device[0], run.course_id)
        calculate_common_sector_params(result, result_details)

    socketio.emit('get/results/current', json.dumps([[device_data, result, competitor[0], competitor[1], course_device[0]]], cls=jsonencoder.AlchemyEncoder))
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
                      .order_by(asc(ResultDetail.absolut_time))
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

def competitor_finish(competitor_id, run_id, finish_time):
    try:
        result_approves = ResultApproved.query.filter_by(
            race_competitor_id=competitor_id,
            run_id=run_id).one()
        # Если что ипсправить
        result_approves.status_id = 1
        result_approves.is_finish = True
        result_approves.finish_time = finish_time
        result_approves.time = result_approves.finish_time - result_approves.start_time
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
    competitor_order = RunOrder.query.filter(RunOrder.race_competitor_id == request.args.get('competitor_id'),
                                             RunOrder.run_id == request.args.get('run_id')).one()
    others_competitors_orders = RunOrder.query.filter(RunOrder.manual_order > competitor_order.manual_order,
                                             RunOrder.run_id == request.args.get('run_id')).all()
    if len(others_competitors_orders) > 0:
        for item in others_competitors_orders:
            item.manual_order -= 1
            db.session.add(item)
    competitor_order.manual_order = None

    db.session.add(competitor_order)
    ResultApproved.query.filter(
       ResultApproved.race_competitor_id == request.args.get('competitor_id'),
       ResultApproved.run_id == request.args.get('run_id')
    ).delete()
    ResultDetail.query.filter(
       ResultDetail.race_competitor_id == request.args.get('competitor_id'),
       ResultDetail.run_id == request.args.get('run_id')
    ).delete()

    db.session.commit()
    socketio.emit('removeResult', json.dumps(dict(removed_competitor=request.args.get('competitor_id'))))

    recalculate_run_resaults(request.args.get('run_id'))
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
   resultDetail.gate = data['gate']
   resultDetail.reason = data['reason']

   db.session.add(resultDetail)
   db.session.commit()
   recalculate_run_resaults(resultDetail.run_id)
   return 'Ok', 200


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
    try:
        previous_course_device = CourseDevice.query.filter_by(order=device.order-1, course_id=course_id).one()
        previous_device_results = db.session.query(ResultDetail).filter(
            ResultDetail.course_device_id == previous_course_device.id,
            ResultDetail.race_competitor_id == current_competitor.race_competitor_id,
            ResultDetail.run_id == current_competitor.run_id).one()
        current_competitor.sectortime = current_competitor.absolut_time - previous_device_results.absolut_time
        current_competitor.speed = ((device.distance - previous_course_device.distance) / 1000) / (current_competitor.sectortime / 3600000)
    except:
        socketio.emit('recount/error', dict(competitor_id=current_competitor.id,
                                            error='Count personal params: speed, sectortime'))

# Функция принемает текущий результат и список  объекты ResultDetail
# результатов БЕЗ текущего
def calculate_common_sector_params(current_competitor, competitors_list):
    try:
        if len(competitors_list) != 0:
            min_сompetitor = min(competitors_list, key=lambda item: item.sectortime)
            if min_сompetitor.sectortime < current_competitor.sectortime:
                сompetitors_list = sorted([current_competitor] + competitors_list, key=lambda item: item.sectortime)
                for index, item in enumerate(сompetitors_list):
                    item.sectordiff = item.sectortime - сompetitors_list[0].sectortime
                    item.sectorrank = index + 1
            else:
                current_competitor.sectordiff = current_competitor.sectortime - min_сompetitor.sectortime
                current_competitor.sectorrank = 1
                сompetitors_list = sorted([current_competitor] + competitors_list, key=lambda item: item.sectortime)
                for index, item in enumerate(сompetitors_list):
                    # item.sectordiff = item.sectortime - сompetitors_list[0].sectortime
                    item.sectorrank = index + 1
        else:
            current_competitor.sectordiff = 0
            current_competitor.sectorrank = 1
    except:
        socketio.emit('recount/error', dict(competitor_id=current_competitor.id,
                                            error='Count common params: sectorrank, sectordiff'))


@raceinfo.route('/recalculate/<int:run_id>', methods=['GET'])
def recalculate_run_resaults(run_id):
    tree_view = {}
    data = db.session.query(ResultDetail, ResultApproved, CourseDevice).\
           join(CourseDevice, CourseDevice.id==ResultDetail.course_device_id).\
           join(ResultApproved, ResultApproved.race_competitor_id==ResultDetail.race_competitor_id, isouter=True).\
           filter(ResultDetail.run_id == run_id).order_by(asc(CourseDevice.order)).\
        all()
    for item in data:
        if item[2].order not in tree_view.keys():
            tree_view[item[2].order] = []
        tree_view[item[2].order].append(item)

    for key, item in tree_view.items():
        print(key, type(key))
        if key == 1:
            continue
        else:
            recalculate_sector_results(item, tree_view[key-1])
    keys_list=list(tree_view.keys())
    recalculate_finished_resaults_old(tree_view[keys_list[0]], tree_view[keys_list[-1]])
    recalculate_finished_resaults(run_id)
    return json.dumps(tree_view, cls=jsonencoder.AlchemyEncoder)

def recalculate_sector_results(current_results=None, previous_resaults=None):
    #  пересчитать  параметры speed, sectordiff
    for current_result in current_results:
        for previous_item in previous_resaults:
            if previous_item[0].race_competitor_id == current_result[0].race_competitor_id:
                try:
                    current_result[0].sectortime = current_result[0].absolut_time - previous_item[0].absolut_time
                    current_result[0].speed = ((current_result[2].distance - previous_item[2].distance) / 1000) / (
                        current_result[0].sectortime / 3600000)
                    break
                except:
                    current_result[0].sectortime = None
                    current_result[0].speed = None
    сompetitors_list = sorted(current_results, key=lambda item: (item[0].sectortime is None, item[0].sectortime))
    min_element = next(item for item in сompetitors_list if item[1].status_id == 1)

    for index, item in enumerate(сompetitors_list):
        try:
            item[0].sectordiff = item[0].sectortime - min_element[0].sectortime
            item[0].sectorrank = index + 1
        except:
            item[0].sectordiff = None
            item[0].sectorrank = None

def recalculate_finished_resaults_old(start_results, finish_results):
    for finish_result in finish_results:
        for start_item in start_results:
            if finish_result[0].race_competitor_id ==start_item[0].race_competitor_id:
                finish_result[0].time = finish_result[0].absolut_time - start_item[0].absolut_time
                break

    сompetitors_list = sorted(finish_results, key=lambda item: item[0].time)

    for index, item in enumerate(сompetitors_list):
        item[0].diff = item[0].time - сompetitors_list[0][0].time
        item[0].rank = index + 1

def recalculate_finished_resaults(run_id):
    finish_results = ResultApproved.query.filter(ResultApproved.run_id==run_id).all()
    сompetitors_list = sorted(finish_results, key= lambda item:( item.time is None, item.time))

    for index, item in enumerate(сompetitors_list):
        try:
            item.diff = item.time - сompetitors_list[0].time
            item.rank = index + 1
        except:
            item.diff = 0
            item.rank = 0


@socketio.on('get/results')
def socket_get_results(data):
    socketio.emit('get/results/response', json.dumps(db.session.query(DataIn, ResultDetail, RaceCompetitor, Competitor, CourseDevice).
                                                    join(ResultDetail, isouter=True).
                                                    join(RaceCompetitor, isouter=True).
                                                    join(Competitor, isouter=True).
                                                    join(CourseDevice, DataIn.cource_device_id==CourseDevice.id , isouter=True).
                                                    filter(DataIn.run_id == data['run_id']).
                                                    order_by(asc(DataIn.id)).
                                                    all(),
                  cls=jsonencoder.AlchemyEncoder))


# @socketio.on('change/data_in/competitors')
# def edit_competitor(json_data):
#     data = json.loads(json_data)
#     changed_results_list = []
#     for item in data:
#         # if item['']
#         # Получить все данные компетитора которому меняем набор данных
#         competitorResults = ResultDetail.query.filter(ResultDetail.run_id == item['run_id'],
#                                                       ResultDetail.race_competitor_id == item['race_competitor_id']).all()
#         dataIn = DataIn.query.filter(DataIn.id == item['data_in_id']).one()
#         if len(competitorResults):
#             existedData=next((item for item in competitorResults if item.course_device_id == dataIn.cource_device_id), None)
#             if existedData:
#                 db.session.delete(existedData)
#         if item['result_detail_id'] is not None:
#             print(item['result_detail_id'])
#             resultDetail = ResultDetail.query.filter(ResultDetail.id == item['result_detail_id']).one()
#             try:
#                 existenceData = ResultDetail.query.filter(ResultDetail.race_competitor_id==item['race_competitor_id'],
#                                          ResultDetail.course_device_id == resultDetail.course_device_id,
#                                          ResultDetail.run_id == resultDetail.run_id).delete()
#             except:
#                 pass
#
#             resultDetail.race_competitor_id = item['race_competitor_id']
#         else:
#             resultDetail = ResultDetail(
#                 course_device_id=dataIn.cource_device_id,
#                 race_competitor_id=item['race_competitor_id'],
#                 run_id=dataIn.run_id,
#                 data_in_id=dataIn.id,
#                 absolut_time=dataIn.time
#             )
#             db.session.add(resultDetail)
#             db.session.commit()
#             changed_results_list.append(resultDetail)
#     for resultDetail in changed_results_list:
#         device = CourseDevice.query.filter(CourseDevice.id == resultDetail.course_device_id).one()
#         competitors_list = ResultDetail.query.filter(ResultDetail.race_competitor_id != resultDetail.race_competitor_id,
#                                                      ResultDetail.course_device_id == resultDetail.course_device_id).all()
#         calculate_personal_sector_params(resultDetail, device, device.course_id)
#         calculate_common_sector_params(resultDetail, competitors_list)
#
#         if device.course_device_type_id == 3:
#             calculate_finish_params(resultDetail, competitors_list)
#
#     socket_get_results({'run_id': data[0]['run_id']})


@socketio.on('change/data_in/competitors')
def edit_competitor(json_data):
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
                    result_set_None(resultCleared)
                    db.session.add(resultCleared)

            else:
                for item in data_list:
                    try:
                        result_approved = ResultApproved.query.filter(ResultApproved.run_id == run_id,
                                                                      ResultApproved.race_competitor_id == competitor_id).one()
                    except:
                        resultApproved = ResultApproved(
                            run_id=run_id,
                            race_competitor_id=competitor_id,
                            is_start=True)
                        db.session.add(resultApproved)
                        db.session.commit()

                    if item['result_detail_id'] is not None:
                        new_result = ResultDetail.query.filter(ResultDetail.id == item['result_detail_id']).one()
                        try:
                            old_result = ResultDetail.query.filter(ResultDetail.race_competitor_id == competitor_id,
                                                               ResultDetail.run_id == new_result.run_id,
                                                               ResultDetail.course_device_id == new_result.course_device_id).one()

                            if old_result.course_device_id in list(devices.keys()):
                                old_approve= db.session.query(ResultApproved).filter(ResultApproved.run_id == run_id,
                                                                                     resultApproved.race_competitor_id==old_result.race_competitor_id).one()
                                new_approve= db.session.query(ResultApproved).filter(ResultApproved.run_id == run_id,
                                                                                     resultApproved.race_competitor_id==new_result.race_competitor_id).one()
                                switch_approve(new_approve, old_approve, devices, old_result.course_device_id)
                                clear_approve(devices, old_result)

                            result_set_None(old_result)
                            old_result.race_competitor_id = new_result.race_competitor_id
                        except:
                            pass
                        new_result.race_competitor_id = competitor_id
                    else:
                        dataIn = DataIn.query.filter(DataIn.id == item['data_in_id']).one()
                        resultDetail = ResultDetail(
                            course_device_id=dataIn.cource_device_id,
                            race_competitor_id=competitor_id,
                            run_id=dataIn.run_id,
                            data_in_id=dataIn.id,
                            absolut_time=dataIn.time
                        )
                        db.session.add(resultDetail)
                        db.session.commit()
        recalculate_run_resaults(run_id)
        socket_get_results({'run_id': run_id})

def result_set_None(result):
    result.speed = None
    result.sectortime = None
    result.absolut_time = None
    result.data_in_id = None
    result.diff = None
    result.time = None
    result.rank = None


def clear_approve(devices, resultDetail, resultApproved=None):
    if resultApproved is None:
        resultApproved = ResultApproved.query(ResultApproved.run_id == resultDetail.run_id,
                                              ResultApproved.race_competitor_id == resultDetail.race_competitor_id). \
            one()
    resultApproved.status_id = None
    resultApproved.time = None
    resultApproved.start_time = None
    resultDetail.rank = None
    resultDetail.diff = None
    if devices[resultDetail.course_device_id]==1:
        resultApproved.start_time = None
    else:
        resultApproved.finish_time = None
    db.session.add(resultApproved)

def switch_approve(new_approve, old_approve, devices, device_id):
    if devices[device_id]==1:
        new_approve.start_time = old_approve.start_time
    else:
        new_approve.finish_time = old_approve.finish_time
    new_approve.status_id=None

def get_start_finish_device(run_id):
    data = db.session.query(CourseDevice.id.label('device_id'), CourseDevice.course_device_type_id.label('type_id')).filter(CourseDevice.course_device_type_id != 3,
                                             CourseDevice.course_id == RunInfo.course_id,
                                             RunInfo.id == run_id).all()
    dict_view = {}
    for item in data:
        dict_view[item[0]] = item[1]
    return json.dumps(dict_view, cls=jsonencoder.AlchemyEncoder)