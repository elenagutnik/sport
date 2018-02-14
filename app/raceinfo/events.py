from .. import socketio
from .models import *
from . import raceinfo
from .. import db
from ..decorators import admin_required
from . import jsonencoder
import json
import operator

from sqlalchemy import cast, TIME, DATE, asc
import time
from operator import attrgetter
from flask_login import current_user
from datetime import datetime
from flask import request, abort, render_template

@raceinfo.route('/d')
def device_1get():
    db.create_all()
    return ''
#
# @raceinfo.route('/input/data', methods=['POST', 'GET'])
# def load_data():
#     # try:
#
#     data = json.loads(request.args['data'])
#     # Девайс с которого пришли данные
#     device = Device.query.filter_by(src_dev=data['src_dev']).one()
#     # Трассы на которых стоит этот девайс
#     course_devices = db.session.query(CourseDevice.course_id).filter_by(device_id=device.id)
#     courses = db.session.query(Course.id).filter(Course.id.in_(course_devices))
#     # Заезд с пришли данные
#
#     run = RunInfo.query.filter(RunInfo.course_id.in_(courses), RunInfo.starttime < datetime.now(), RunInfo.endtime == None ).one()
#
#     #
#     # Сам девайс с которого пришли данные
#     course_device = db.session.query(CourseDevice, CourseDeviceType).join(CourseDeviceType).\
#         filter(CourseDevice.device_id == device.id,
#                CourseDevice.course_id == run.course_id).one()
#
#     competitor = RaceCompetitor.query.filter_by(bib=data['bib']).one()
#
#     results = ResultDetail.query.filter(ResultDetail.course_device_id==course_device[0].id).all()
#
#     result = ResultDetail(
#         course_device_id=course_device[0].id,
#         race_competitor_id=competitor.id,
#         run_id=run.id,
#         absolut_time=data['time']
#     )
#     if course_device[1].name == "Start":
#         result.time = 0
#         result.sectortime = 0
#         result.sectordiff = 0
#         result.sectorrank = 1
#
#         result.is_start = True
#     else:
#         tmp=0
#         start_device = db.session.query(CourseDevice.id).filter(CourseDevice.course_id == run.course_id,
#                                                                 CourseDevice.course_device_type_id == 1)
#         start_result = ResultDetail.query.filter(ResultDetail.race_competitor_id == competitor.id,
#                                                          ResultDetail.course_device_id == start_device,
#                                                          ResultDetail.run_id==run.id).one()
#
#         previous_course_device = CourseDevice.query.filter_by(order=course_device[0].order - 1, course_id=run.course_id).one()
#
#         previous_device_results = db.session.query(ResultDetail).filter(ResultDetail.course_device_id==previous_course_device.id,
#             ResultDetail.race_competitor_id == competitor.id,  ResultDetail.run_id==run.id).one()
#
#         result.time = data['time'] - start_result.absolut_time
#         result.sectortime = data['time'] - previous_device_results.absolut_time
#         result.speed = (course_device[0].distance - previous_course_device.distance) / result.sectortime
#
#         if len(results) == 0:
#             result.diff = 0
#             result.rank = 1
#             # пересчитать
#             result.sectordiff = 0
#         else:
#             best_result = min(results, key=attrgetter("time"))
#
#             result.diff = result.time - best_result.time
#             best_result = min(results, key=attrgetter("sectortime"))
#
#             result.sectordiff = result.sectortime - best_result.sectortime
#     db.session.add(result)
#
#
#     final_results = db.session.query(ResultDetail, RaceCompetitor, Competitor, CourseDevice, CourseDeviceType).join(RaceCompetitor).join(Competitor).join(CourseDevice).join(CourseDeviceType).filter(ResultDetail.course_device_id == course_device[0].id, ResultDetail.run_id==run.id).all()
#
#     tmp = json.dumps(final_results, cls=jsonencoder.AlchemyEncoder)
#     socketio.emit("newData", tmp)
#     input_data = DataIn(
#         src_sys=data['src_sys'],
#         src_dev=data['src_dev'],
#         bib=data['bib'],
#         event_code=data['eventcode'],
#         time=data['time'],
#         reserved=data['reserved']
#     )
#
#     db.session.add(input_data)
#     db.session.add(result)
#     db.session.commit()
#
#     return '', 200
#     # except:
#     #     abort(500)

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
    resultDetail.timerun = data['absolut_time']
    resultDetail.result_id = result.id
    resultDetail.gate = data['gate']
    resultDetail.reason = data['reason']

    db.session.add(resultDetail)
    db.session.commit()

    return 'huy', 200

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

# @raceinfo.route('/input/data', methods=['POST', 'GET'])
# def load_data_vol2():
#     #
#     CachedObject = TempCashe.query.filter(TempCashe.key=='Current_competitor').one()
#     CachedCompetitor = json.loads(CachedObject.data)
#     #
#     ere =request
#     data = request.json
#     # Девайс с которого пришли данные
#     device = Device.query.filter_by(src_dev=data['src_dev']).one()
#     # Трассы на которых стоит этот девайс
#     course_devices = db.session.query(CourseDevice.course_id).filter_by(device_id=device.id)
#     courses = db.session.query(Course.id).filter(Course.id.in_(course_devices))
#     # Заезд с пришли данные
#
#     run = RunInfo.query.filter(RunInfo.course_id.in_(courses), RunInfo.starttime < datetime.now(), RunInfo.endtime == None ).one()
#
#
#
#     # Сам девайс с которого пришли данные
#     course_device = db.session.query(CourseDevice, CourseDeviceType).join(CourseDeviceType).\
#         filter(CourseDevice.device_id==device.id,
#                CourseDevice.course_id==run.course_id).one()
#
#     # competitor = RaceCompetitor.query.filter_by(id=CachedCompetitor['Current_competitor_id']).one()
#
#     results = ResultDetail.query.filter(ResultDetail.course_device_id == course_device[0].id).all()
#
#     result = ResultDetail(
#         course_device_id=course_device[0].id,
#         # race_competitor_id=competitor.id,
#         run_id=run.id,
#         absolut_time=data['time']
#
#     )
#     if course_device[1].name == "Start":
#         competitor_id = db.session.query(RunOrder.race_competitor_id).filter(RunOrder.run_id == run.id,
#                                                                              RunOrder.order == CachedCompetitor['order']+1).one()
#         result.race_competitor_id = competitor_id.race_competitor_id
#         result.time = 0
#         result.sectortime = 0
#         result.sectordiff = 0
#         result.sectorrank = 1
#         CachedObject.data = json.dumps(dict(run=run.id, order=CachedCompetitor['order']+1, competitor_id=competitor_id.race_competitor_id))
#         db.session.add(CachedObject)
#         db.session.commit()
#         result.is_start = True
#     else:
#         result.race_competitor_id = CachedCompetitor['competitor_id']
#         tmp=0
#         start_device = db.session.query(CourseDevice.id).filter(CourseDevice.course_id == run.course_id,
#                                                                 CourseDevice.course_device_type_id == 1)
#         start_result = ResultDetail.query.filter(ResultDetail.race_competitor_id == result.race_competitor_id,
#                                                  ResultDetail.course_device_id == start_device,
#                                                  ResultDetail.run_id == run.id).one()
#
#         previous_course_device = CourseDevice.query.filter_by(order=course_device[0].order - 1, course_id=run.course_id).one()
#
#         previous_device_results = db.session.query(ResultDetail).filter(ResultDetail.course_device_id == previous_course_device.id,
#             ResultDetail.race_competitor_id == result.race_competitor_id,  ResultDetail.run_id == run.id).one()
#         # time
#         result.time = data['time'] - start_result.absolut_time
#         result.sectortime = data['time'] - previous_device_results.absolut_time
#         result.speed = ((course_device[0].distance - previous_course_device.distance)/1000) / (result.sectortime/3600000)
#         # temp_time= datetime.fromtimestamp(result.absolut_time / 1e3)
#         # result.time = data['time'] - start_result.absolut_time
#         # result.sectortime = data['time'] - previous_device_results.absolut_time
#         # result.speed = (course_device[0].distance - previous_course_device.distance) / result.sectortime
#         #
#
#         if len(results) == 0:
#             result.diff = 0
#             result.rank = 1
#             # пересчитать
#             result.sectordiff = 0
#         else:
#             best_result = min(results, key=attrgetter("time"))
#
#             result.diff = result.time - best_result.time
#             best_result = min(results, key=attrgetter("sectortime"))
#
#             result.sectordiff = result.sectortime - best_result.sectortime
#     db.session.add(result)
#
#     final_results = db.session.query(ResultDetail, RaceCompetitor, Competitor, CourseDevice, CourseDeviceType).join(RaceCompetitor).\
#         join(Competitor).\
#         join(CourseDevice).\
#         join(CourseDeviceType).\
#         filter(ResultDetail.course_device_id == course_device[0].id, ResultDetail.run_id==run.id).order_by(asc(RunOrder.order)).all()
#
#     tmp = json.dumps(final_results, cls=jsonencoder.AlchemyEncoder)
#     socketio.emit("newData", tmp)
#     input_data = DataIn(
#         src_sys=data['src_sys'],
#         src_dev=data['src_dev'],
#         bib=data['bib'],
#         event_code=data['eventcode'],
#         time=data['time'],
#         reserved=data['reserved']
#     )
#     db.session.add(input_data)
#     db.session.add(result)
#     db.session.commit()
#
#     # if course_device[1].name == "Finish":
#     # #     временный автоапрув
#     #     status = Status.query.filter_by(name='QLF').one()
#     #     try:
#     #         result = Result.query.filter_by(race_competitor_id=result.race_competitor_id).one()
#     #     except:
#     #         result = Result(race_competitor_id=result.race_competitor_id)
#     #         db.session.add(result)
#     #         db.session.commit()
#     #
#     #     resultDetail = ResultApproved(
#     #         is_manual=False,
#     #         approve_user=current_user.id,
#     #         approve_time=datetime.now(),
#     #         race_competitor_id=result.race_competitor_id,
#     #         run_id=run.id,
#     #         status_id=status.id,
#     #         timerun=data['time'],
#     #         result_id=result.id
#     #     )
#     #     db.session.add(resultDetail)
#     #     db.session.commit()
#
#     return '', 200




@raceinfo.route('/current_data/get/<int:race_id>', methods=['POST', 'GET'])
def get_current_data(race_id):
    return json.dumps(db.session.query(RaceCompetitor, Competitor, ResultDetail, ResultApproved).join(Competitor)
                      .join(ResultDetail).join(ResultApproved)\
                      .filter(RaceCompetitor.race_id == race_id)\
                      .all(), cls=jsonencoder.AlchemyEncoder)
    return data


@raceinfo.route('/input/data', methods=['POST', 'GET'])
def load_data_vol2():

    data = json.loads(request.args['data'])
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

    results = ResultDetail.query.filter(ResultDetail.course_device_id == course_device[0].id).all()
    # Запущенный пользователь может быть только один, иначе ошибка

    try:
        resultApproved = ResultApproved.query.filter(ResultApproved.run_id == run.id,
                                                     ResultApproved.is_start == True,
                                                     ResultApproved.is_finish == None).one()
    except Exception as e:
        socketio.emit('errorHandler', json.dumps(dict([('ERROR', '000000'),('TIME', datetime.now().time().__str__()),('MESSAGE', 'Ошибка получения компетитора')])))
        input_data = DataIn(
            src_sys=data['src_sys'],
            src_dev=data['src_dev'],
            event_code=data['eventcode'],
            time=data['time'],
            reserved=data['reserved']
        )
        if 'bib' in data:
            input_data.bib = data['bib']
        db.session.add(input_data)

        db.session.commit()
        return ''
    competitor = RaceCompetitor.query.filter(RaceCompetitor.id == resultApproved.race_competitor_id).one()
#    competitor = RaceCompetitor.query.filter_by(resultApproved.race_competitor_id).one()
    result = ResultDetail(
        course_device_id=course_device[0].id,
        race_competitor_id=competitor.id,
        run_id=run.id,
        absolut_time=data['time'])

    if course_device[1].name == "Start":
        result.time = 0
        result.sectortime = 0
        result.sectordiff = 0
        result.sectorrank = 1
        result.is_start = True
    else:
        start_device = db.session.query(CourseDevice.id).filter(CourseDevice.course_id == run.course_id,
                                                                CourseDevice.course_device_type_id == 1)

#        start_result = ResultDetail.query.filter(ResultDetail.race_competitor_id == result.race_competitor_id,
#                                                 ResultDetail.course_device_id == start_device,
#                                                 ResultDetail.run_id == run.id).one()
        try:
           start_result = ResultDetail.query.filter(ResultDetail.race_competitor_id == result.race_competitor_id,
                                                    ResultDetail.course_device_id == start_device,
                                                    ResultDetail.run_id == run.id).one()
        except Exception as e:
           socketio.emit('errorHandler', json.dumps(dict([('ERROR', '0000x1'),('TIME', datetime.now().time().__str__()),('MESSAGE', 'Ошибка: дублирование данных')])))
           input_data = DataIn(
               src_sys=data['src_sys'],
               src_dev=data['src_dev'],
               event_code=data['eventcode'],
               time=data['time'],
               reserved=data['reserved']
           )
           if 'bib' in data:
               input_data.bib = data['bib']
           db.session.add(input_data)

           db.session.commit()
           return ''

        previous_course_device = CourseDevice.query.filter_by(order=course_device[0].order - 1, course_id=run.course_id).one()

        previous_device_results = db.session.query(ResultDetail).filter(ResultDetail.course_device_id == previous_course_device.id,
            ResultDetail.race_competitor_id == result.race_competitor_id,  ResultDetail.run_id == run.id).one()
        # time
        result.time = data['time'] - start_result.absolut_time
        result.sectortime = data['time'] - previous_device_results.absolut_time
        result.speed = ((course_device[0].distance - previous_course_device.distance)/1000) / (result.sectortime/3600000)

        if len(results) == 0:
            result.diff = 0
            result.rank = 1
            # пересчитать
            result.sectordiff = 0
        else:
            best_result = min(results, key=attrgetter("time"))

            result.diff = result.time - best_result.time
            best_result = min(results, key=attrgetter("sectortime"))

            result.sectordiff = result.sectortime - best_result.sectortime

    db.session.add(result)
    db.session.commit()

    # result_details = ResultDetail.query.filter(
    #     ResultDetail.run_id == run.id,
    #     ResultDetail.course_device_id == course_device[0].id
    # ).order_by(asc(ResultDetail.diff)).all()
    # for i in range(0, len(result_details)):
    #     result_details[i].rank = i+1
    # result_details.sort(key=operator.attrgetter('sectortime'))
    # for i in range(0, len(result_details)):
    #     result_details[i].sectorrank = i+1



    # result_details = ResultDetail.query.filter(
    #     ResultDetail.run_id == run.id,
    #     ResultDetail.course_device_id == course_device[0].id
    # ).order_by(asc(ResultDetail.diff)).all()


    result_details = db.session.query(ResultDetail, RaceCompetitor, Competitor, CourseDevice, CourseDeviceType,RunOrder).\
        join(RaceCompetitor).\
        join(Competitor).\
        join(CourseDevice).\
        join(CourseDeviceType).\
        join(RunOrder, RunOrder.race_competitor_id == RaceCompetitor.id).\
        filter(ResultDetail.course_device_id == course_device[0].id, ResultDetail.run_id == run.id,RunOrder.run_id == run.id).order_by(asc(ResultDetail.diff)).all()
    for i in range(0, len(result_details)):
        result_details[i][0].rank = i+1
    # result_details.sort(key=operator.attrgetter('sectortime'))
    result_details.sort(key=lambda item: item[0].sectortime)

    for i in range(0, len(result_details)):
        result_details[i][0].sectorrank = i+1
    result_details.sort(key=lambda item: item[5].order)
    # final_results = db.session.query(ResultDetail, RaceCompetitor, Competitor, CourseDevice, CourseDeviceType,RunOrder).\
    #    join(RaceCompetitor).\
    #    join(Competitor).\
    #    join(CourseDevice).\
    #    join(CourseDeviceType).\
    #    join(RunOrder, RunOrder.race_competitor_id == RaceCompetitor.id).\
    #    filter(ResultDetail.course_device_id == course_device[0].id, ResultDetail.run_id == run.id,RunOrder.run_id == run.id).order_by(asc(RunOrder.order)).all()

    # final_results = db.session.query(ResultDetail, RaceCompetitor, Competitor, CourseDevice, CourseDeviceType, RunOrder).join(RaceCompetitor).\
    #    join(Competitor).\
    #    join(CourseDevice).\
    #    join(CourseDeviceType).\
    #    filter(ResultDetail.course_device_id == course_device[0].id, ResultDetail.run_id==run.id).order_by(asc(RunOrder.order)).all()
    tmp = json.dumps(result_details, cls=jsonencoder.AlchemyEncoder)
    socketio.emit("newData", tmp)
    input_data = DataIn(
        src_sys=data['src_sys'],
        src_dev=data['src_dev'],
        event_code=data['eventcode'],
        time=data['time'],
        reserved=data['reserved']
    )
    if 'bib' in data:
        input_data.bib = data['bib']
    db.session.add(input_data)
    db.session.commit()

    return '', 200



@raceinfo.route('/promise', methods=['POST', 'GET'])
def get_current_datdda():
    return render_template("testPromises.html")
