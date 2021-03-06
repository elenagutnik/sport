from .. import socketio, db, migrate

from ..decorators import admin_required
from .models import *
from . import jsonencoder, raceinfo
import json

from functools import wraps
from sqlalchemy import cast, DATE, func, asc,  or_

from flask_login import current_user, login_required
from flask_migrate import upgrade as _upgrade

from datetime import datetime, timedelta
from flask import request, render_template

from .Scoreboard import Scoreboard

def exectutiontime(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        print('Elapsed time:', (end-timedelta(hours=start.hour,minutes=start.minute,seconds=start.second,microseconds=start.microsecond)).time())
        return result
    return wrapper

@raceinfo.route('/migrate')
def device_1get():
    RunOrderFunction.insert()
    return ''

@raceinfo.route('/emulation/<int:race_id>/clear')
def emulation_clear_results(race_id):
    db.engine.execute('delete from result_detail; ')
    db.engine.execute('delete from data_in;')
    db.engine.execute('delete from result_approved;')
    db.engine.execute('delete from result;')
    # db.engine.execute('delete from "CASHE";')
    db.engine.execute('delete from run_order;')
    db.engine.execute('update run_info set endtime=NULL;')
    #db.engine.execute('INSERT INTO "CASHE" (id, key, data) VALUES (1,\'Current_competitor\', \'{"run": 1, "order": 0}\')')
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

@raceinfo.route('/input/data', methods=['POST', 'GET'])
@exectutiontime
def load_data_vol2():
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
    result = None
    # try:
    run = RunInfo.query.filter(RunInfo.course_id.in_(courses), RunInfo.starttime < datetime.now(), RunInfo.endtime == None ).one()

    # Сам девайс с которого пришли данные
    course_device = db.session.query(CourseDevice, CourseDeviceType).join(CourseDeviceType).\
        filter(CourseDevice.device_id == device.id,
               CourseDevice.course_id == run.course_id).one()

    device_data = setDeviceDataInDB(data, run.id, course_device[0].id)

    competitor = get_current_competitor(course_device[0].id, run.id)

    finished_data = None

    if course_device[1].name == "Start":
        if competitor is None:
            competitor = competitor_start_run(run.id)
        result = ResultDetail(
            course_device_id=course_device[0].id,
            run_id=run.id,
            data_in_id=device_data.id,
            race_competitor_id=competitor[0].id,
            absolut_time=data['TIME'])

        board = Scoreboard(bib=competitor[0].bib,
                           firstname=competitor[1].en_firstname,
                           lastname=competitor[1].en_lastname,
                           country_code=competitor[3].name,
                           time='0')

        Scoreboard.send(board.started_competitor())

        db.session.add(result)
        db.session.commit()
        result.sectortime = 0
        result.sectordiff = 0
        result.is_start = True
        approvedResult = ResultApproved.query.filter(ResultApproved.race_competitor_id == result.race_competitor_id,
                                                     ResultApproved.run_id == result.run_id).one()
        approvedResult.is_start = True
        approvedResult.start_time = result.absolut_time
        result_details = db.session.query(ResultDetail). \
            filter(
            ResultDetail.course_device_id == course_device[0].id,
            ResultDetail.run_id == run.id).all()
        # result_details = crutch_result_list(course_device_id=course_device[0].id, run_id=run.id)
    else:
        if competitor is not None:

            board = Scoreboard(bib=competitor[0].bib,
                               firstname=competitor[1].en_firstname,
                               lastname=competitor[1].en_lastname,
                               country_code=competitor[3].name
                               )

            result = ResultDetail(
                course_device_id=course_device[0].id,
                run_id=run.id,
                data_in_id=device_data.id,
                race_competitor_id=competitor[0].id,
                absolut_time=data['TIME'])
            if course_device[1].name == "Finish":
                result_details = db.session.query(ResultDetail). \
                    filter(ResultDetail.run_id == run.id).all()
                db.session.add(result)
                db.session.commit()
                competitor_aprove = competitor_finish(competitor[0].id, run.id, result.absolut_time)

                board.time = competitor_aprove.time
                Scoreboard.send(board.finished_competitor())

                recalculate_run_results(run.id)
                finished_data = ResultApproved.query.filter(ResultApproved.run_id==run.id).all()


            else:

                result_details = db.session.query(ResultDetail). \
                    filter(
                    ResultDetail.course_device_id == course_device[0].id,
                    ResultDetail.run_id == run.id).all()
                db.session.add(result)
                db.session.commit()
                calculate_personal_sector_params(result, course_device[0], run.course_id)

                board.time = result.time
                Scoreboard.send(board.crossed_device())

                calculate_common_sector_params(result, result_details)

        else:
            socketio.emit('errorData', json.dumps({'ERROR': 'UNKNOWED COMPETITOR', 'DATA': device_data}, cls=jsonencoder.AlchemyEncoder))

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
        list_of_object=result_details,finished_data=finished_data), cls=jsonencoder.AlchemyEncoder))
    # except:
    #     ddata = DataIn(
    #         src_sys=data['SRC_SYS'],
    #         src_dev=data['SRC_DEV'],
    #         event_code=data['EVENT_CODE'],
    #         time=data['TIME'],
    #
    #     )
    #     if course_device is not None:
    #         ddata.cource_device_id = course_device[0].id
    #     if run is not None:
    #         ddata.run_id = run.id
    #     db.session.add(ddata)
    #     db.session.commit()
    #     socketio.emit("errorData", json.dumps(ddata, cls=jsonencoder.AlchemyEncoder))
    #     return '', 200
    return '', 200

# @raceinfo.route('/current_data/get/<int:race_id>', methods=['POST', 'GET'])
# def get_current_data(race_id):
#     tmp =db.session.query(ResultDetail,RaceCompetitor, Competitor, CourseDevice, ResultApproved, CourseDeviceType).join(RaceCompetitor)\
#                       .join(Competitor).join(CourseDevice).join(ResultApproved).join(CourseDeviceType)\
#                       .filter(RaceCompetitor.race_id == race_id)\
#                       .order_by(asc(ResultDetail.absolut_time))\
#                       .all()
#     dd= json.dumps(db.session.query(ResultDetail,RaceCompetitor, Competitor, CourseDevice, ResultApproved, CourseDeviceType).join(RaceCompetitor)
#                       .join(Competitor).join(CourseDevice).join(ResultApproved).join(CourseDeviceType)\
#                       .filter(RaceCompetitor.race_id == race_id)\
#                       .order_by(asc(ResultDetail.absolut_time))
#                       .all(), cls=jsonencoder.AlchemyEncoder)
#     return json.dumps(db.session.query(ResultDetail,RaceCompetitor, Competitor, CourseDevice, ResultApproved, CourseDeviceType).join(RaceCompetitor)
#                       .join(Competitor).join(CourseDevice).join(ResultApproved).join(CourseDeviceType)\
#                       .filter(RaceCompetitor.race_id == race_id)\
#                       .order_by(asc(ResultDetail.absolut_time))
#                       .all(), cls=jsonencoder.AlchemyEncoder)

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

def competitor_start_run(run_id):
    race_competitors = db.session.query(RaceCompetitor, Competitor, RunOrder, Nation). \
        join(Competitor). \
        join(RunOrder). \
        join(Nation, Competitor.nation_code_id == Nation.id). \
        filter(RunOrder.run_id == run_id).order_by(asc(RunOrder.order)).all()
    order = sum(item[2].manual_order is not None and item[2].manual_order != 0 for item in race_competitors)


    сompetitor = next(item for item in race_competitors if item[2].manual_order is None)
    сompetitor[2].manual_order = order + 1
    result_approves = ResultApproved(run_id=run_id,
                                     is_start=True,
                                     race_competitor_id=сompetitor[0].id)
    db.session.add(сompetitor[2])
    db.session.add(result_approves)
    db.session.commit()
    return сompetitor

def get_current_competitor(course_device_id, run_id):
    competitor_order = db.session.query(func.count('*')).select_from(ResultDetail).\
                           filter(ResultDetail.run_id == run_id,
                            ResultDetail.course_device_id == course_device_id). \
                            scalar() + 1
    print('текущий девайс', competitor_order-1)

    competitor = db.session.query(RaceCompetitor, Competitor, RunOrder, Nation).\
           join(Competitor).\
           join(RunOrder). \
           join(Nation, Competitor.nation_code_id == Nation.id). \
        filter(RunOrder.manual_order == competitor_order, RunOrder.run_id == run_id).first()
    return competitor

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


        return result_approves
    except Exception as err:
        return None

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
        competitor_order.manual_order = None

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
       resultApproved = ResultApproved.query.filter_by(race_competitor_id=competitor_id, run_id=run_id).one()
    except:
        resultApproved = ResultApproved(
           race_competitor_id=competitor_id,
           run_id=run_id,
           is_start=False
        )
    resultApproved.is_manual = True
    resultApproved.approve_user = current_user.id
    resultApproved.approve_time = datetime.now()
    resultApproved.status_id = data['status_id']
    resultApproved.is_finish = True
    try:

        if resultApproved.is_start == False:
            competitorOrder = RunOrder.query.filter(RunOrder.race_competitor_id == competitor_id, RunOrder.run_id==run_id).first()
            competitorOrder.manual_order = 0
            db.session.add(competitorOrder)
            db.session.commit()
        if data['finish_time'] != '':
            finish_device = db.session.query(ResultDetail, CourseDevice, CourseDeviceType).join(CourseDevice).join(CourseDeviceType).filter(ResultDetail.race_competitor_id == competitor_id,
                                             ResultDetail.run_id == run_id, CourseDeviceType==3).first()
            if finish_device is not None:
                finish_device[0].data_in_id = None
                finish_device[0].absolute_time = data['finish_time']
                db.session.add(finish_device)
            resultApproved.finish_time = data['finish_time']
        if data['start_time'] != '':
            start_device = db.session.query(ResultDetail, CourseDevice, CourseDeviceType).join(CourseDevice).join(CourseDeviceType).filter(ResultDetail.race_competitor_id == competitor_id,
                                             ResultDetail.run_id == run_id, CourseDeviceType==1).first()
            if start_device is not None:
                start_device[0].data_in_id = None
                start_device[0].absolute_time = data['start_time']
                db.session.add(start_device)
            resultApproved.start_time = data['start_time']
        try:
            resultApproved.time = int(resultApproved.finish_time) - int(resultApproved.start_time)
        except:
            resultApproved.time = None
        db.session.commit()
    except:
        pass
    resultApproved.gate = data['gate']
    resultApproved.reason = data['reason']

    db.session.add(resultApproved)
    db.session.commit()

    if resultApproved.is_start == True:
        for item in db.session.query(CourseDevice.id).filter(CourseDevice.course_id == RunInfo.course_id, RunInfo.id == run_id).all():
            resultDetail = ResultDetail.query.filter(ResultDetail.run_id == run_id,
                                                     ResultDetail.race_competitor_id == competitor_id,
                                                     ResultDetail.course_device_id == item).first()
            if resultDetail is None:
                resultDetail = ResultDetail(
                    run_id=run_id,
                    race_competitor_id=competitor_id,
                    course_device_id=item
                )
                db.session.add(resultDetail)
            else:
                resultDetail.sectorrank = None
                resultDetail.sectordiff = None

        db.session.commit()
    recalculate_run_results(resultApproved.run_id)
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
def recalculate_run_results(run_id):
    tree_view = {}
    data = db.session.query(ResultDetail, ResultApproved, CourseDevice).\
           join(CourseDevice, CourseDevice.id == ResultDetail.course_device_id).\
           join(ResultApproved, ResultApproved.race_competitor_id == ResultDetail.race_competitor_id, isouter=True).\
           filter(ResultDetail.run_id == run_id, ResultApproved.run_id==run_id,  or_(ResultApproved.status_id == None, ResultApproved.status_id == 1)).\
        order_by(asc(CourseDevice.order)).\
        all()
    if len(data)>0:
        for item in data:
            if item[2].order not in tree_view.keys():
                tree_view[item[2].order] = []
            tree_view[item[2].order].append(item)

        for key, item in tree_view.items():
            if key == 1:
                continue
            else:
                recalculate_sector_results(item, tree_view[key-1])
        keys_list = list(tree_view.keys())
        # recalculate_finished_results_old(tree_view[keys_list[0]], tree_view[keys_list[-1]])
        recalculate_finished_resaults(run_id)
        return json.dumps(tree_view, cls=jsonencoder.AlchemyEncoder)
    recalculate_finished_resaults(run_id)
    return ''

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
    try:
        min_element = next(item for item in сompetitors_list if item[1].status_id == 1)
        for index, item in enumerate(сompetitors_list):
            try:
                item[0].sectordiff = item[0].sectortime - min_element[0].sectortime
                item[0].sectorrank = index + 1
            except:
                item[0].sectordiff = None
                item[0].sectorrank = None
    except:
        for index, item in enumerate(сompetitors_list):
            item[0].sectordiff = None
            item[0].sectorrank = None

def recalculate_finished_results_old(start_results, finish_results):
    for finish_result in finish_results:
        for start_item in start_results:
            if finish_result[0].race_competitor_id == start_item[0].race_competitor_id:
                try:
                    finish_result[0].time = finish_result[0].absolut_time - start_item[0].absolut_time
                    break
                except:
                    finish_result[0].time = None
    сompetitors_list = sorted(finish_results, key=lambda item: (item[0].time is None, item[1].status_id is None, item[1].status_id, item[0].time))

    for index, item in enumerate(сompetitors_list):
        if item[1].status_id == 1:
            item[0].diff = item[0].time - сompetitors_list[0][0].time
            item[0].rank = index + 1
        else:
            item[0].diff = None
            item[0].rank = None


def recalculate_finished_resaults(run_id):
    finish_results = ResultApproved.query.filter(ResultApproved.run_id == run_id).all()
    сompetitors_list = sorted(finish_results, key=lambda item: (item.time is None, item.status_id is None,item.status_id, item.time))

    for index, item in enumerate(сompetitors_list):
        try:
            if item.status_id == 1:
                item.time = item.finish_time - item.start_time
                item.diff = item.time - сompetitors_list[0].time
                item.rank = index + 1
            else:
                item.diff = None
                item.rank = None
        except:
            item.diff = None
            item.rank = None

# @socketio.on('get/results')
# def socket_get_results(data):
#     socketio.emit('get/results/response', json.dumps(db.session.query(DataIn, ResultDetail, RaceCompetitor, Competitor, CourseDevice).
#                                                     join(ResultDetail, isouter=True).
#                                                     join(RaceCompetitor, isouter=True).
#                                                     join(Competitor, isouter=True).
#                                                     join(CourseDevice, DataIn.cource_device_id==CourseDevice.id , isouter=True).
#                                                     filter(DataIn.run_id == data['run_id']).
#                                                     order_by(asc(DataIn.id)).
#                                                     all(),
#                   cls=jsonencoder.AlchemyEncoder))
@socketio.on('get/results')
def socket_get_results(data):
    socketio.emit('get/results/response', json.dumps(db.session.query(DataIn, ResultDetail, RaceCompetitor, Competitor, CourseDevice).
                                                    join(ResultDetail, isouter=True).
                                                    join(RaceCompetitor, isouter=True).
                                                    join(Competitor, isouter=True).
                                                    join(CourseDevice, DataIn.cource_device_id==CourseDevice.id, isouter=True).
                                                    filter(DataIn.run_id.in_(json.loads(data))).
                                                    order_by(asc(DataIn.time)).
                                                    all(),
                  cls=jsonencoder.AlchemyEncoder))

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
                    result_set_None(resultCleared)
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
        resultApproved = ResultApproved.query.filter(ResultApproved.run_id == resultDetail.run_id,
                                              ResultApproved.race_competitor_id == resultDetail.race_competitor_id).one()
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

# @raceinfo.route('/get_results/<int:run_id>/<int:course_device_id>')
# def crutch_result_list(run_id, course_device_id):
#     resultDetail = db.session.query(ResultDetail)\
#         .filter(ResultDetail.run_id==run_id, ResultDetail.course_device_id==course_device_id)\
#         .all()
#     resultApproved= db.session.query(ResultApproved).filter(ResultApproved.run_id==run_id).order_by(ResultApproved.id).all()
#     for approve in resultApproved:
#         any(item== approve for item in resultDetail)
#     # return json.dumps(, cls=jsonencoder.AlchemyEncoder)


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
    # StartDevice = db.session.query(CourseDevice, CourseDeviceType).join(CourseDeviceType).filter().first()
    # FinishDevice = db.session.query(CourseDevice, CourseDeviceType).join(CourseDeviceType).filter().first()
    for _item in manual_data:
        if not any(item[1].id == _item[1].id for item in data):
            result = [None, _item[1], _item[2], None, _item[0], None]
            data.append(result)

    data = sorted(data, key=lambda item: (item[4].start_time is None, item[4].start_time))
    return json.dumps(data, cls=jsonencoder.AlchemyEncoder)



def reset_DSQ_competitors(competitor_id, run_id):
    result_details = db.session.query(ResultDetail, ResultApproved).\
        filter(ResultDetail.run_id == run_id, ResultDetail.race_competitor_id == competitor_id).\
        all()
    result_approwed = ResultApproved.query.filter(ResultApproved.run_id == run_id,
                                                  ResultApproved.race_competitor_id == competitor_id).first()
    result_approwed.rank = None
    result_approwed.diff = None
    result_approwed.time = None
    db.session.add(result_approwed)

    for item in result_details:
        item.sectordiff = None
        item.absolut_time = None
        item.sectorrank = None
        item.sectortime = None
        item.speed = None

        db.session.add(item)
    db.session.commit()
    return ''

def reestablish_DSQ_competitors(competitor_id, run_id):
    result_details = db.session.query(ResultDetail, DataIn).\
        join(DataIn, ResultDetail.data_in_id==DataIn.id).\
        filter(ResultDetail.run_id==run_id, ResultDetail.race_competitor_id==competitor_id).\
        all()
    result_approwed = ResultApproved.query.filter(ResultApproved.run_id == run_id,
                                                  ResultApproved.race_competitor_id == competitor_id).first()
    result_approwed.time = ResultApproved.finish_time-ResultApproved.start_time
    db.session.add(result_approwed)
    for item in result_details:
        item[0].absolut_time = item[1].time
        db.session.add(item)
    db.session.commit()
    return ''
