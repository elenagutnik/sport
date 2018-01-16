from .. import socketio
from .models import *
from . import raceinfo
from .. import db

from . import jsonencoder
import json
from sqlalchemy import cast, TIME
import time
from operator import attrgetter


from flask import request, abort, render_template

@raceinfo.route('/input/data', methods=['POST', 'GET'])
def load_data():
    # try:

    data = json.loads(request.args['data'])
    # Девайс с которого пришли данные
    device = Device.query.filter_by(src_dev=data['src_dev']).one()
    # Трассы на которых стоит этот девайс
    course_devices = db.session.query(CourseDevice.course_id).filter_by(device_id=device.id)
    courses = db.session.query(Course.id).filter(Course.id.in_(course_devices))
    # Заезд с пришли данные
    run = RunInfo.query.filter(RunInfo.course_id.in_(courses), cast(RunInfo.starttime, TIME) < datetime.now().time()).one()
    # Сам девайс с которого пришли данные
    course_device = db.session.query(CourseDevice, CourseDeviceType).join(CourseDeviceType).\
        filter(CourseDevice.device_id==device.id,
               CourseDevice.course_id==run.course_id).one()

    competitor = RaceCompetitor.query.filter_by(bib=data['bib']).one()

    results = ResultDetail.query.filter(ResultDetail.course_device_id==course_device[0].id).all()

    result = ResultDetail(
        course_device_id=course_device[0].id,
        race_competitor_id=competitor.id,
        run_id=run.id,
        absolut_time=data['time']
    )
    if course_device[1].name == "Start":
        result.time = 0
        result.sectortime = 0
        result.sectordiff = 0
        result.sectorrank = 1

        result.is_start = True
    else:
        tmp=0
        start_device = db.session.query(CourseDevice.id).filter(CourseDevice.course_id == run.course_id,
                                                                CourseDevice.course_device_type_id == 1)
        start_result = ResultDetail.query.filter(ResultDetail.race_competitor_id == competitor.id,
                                                         ResultDetail.course_device_id == start_device).one()

        previous_course_device = CourseDevice.query.filter_by(order=course_device[0].order - 1, course_id=run.course_id).one()

        previous_device_results = db.session.query(ResultDetail).filter(ResultDetail.course_device_id==previous_course_device.id,
            ResultDetail.race_competitor_id == competitor.id).one()

        result.time = data['time'] - start_result.absolut_time
        result.sectortime = data['time'] - previous_device_results.absolut_time
        result.speed = (course_device[0].distance - previous_course_device.distance) / result.sectortime

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


    final_results = db.session.query(ResultDetail, RaceCompetitor, Competitor, CourseDevice, CourseDeviceType).join(RaceCompetitor).join(Competitor).join(CourseDevice).join(CourseDeviceType).filter(ResultDetail.course_device_id == course_device[0].id).all()

    tmp=json.dumps(final_results, cls=jsonencoder.AlchemyEncoder)
    socketio.emit("newData", tmp)
    input_data = DataIn(
        src_sys=data['src_sys'],
        src_dev=data['src_dev'],
        bib=data['bib'],
        event_code=data['eventcode'],
        time=data['time'],
        reserved=data['reserved']
    )

    db.session.add(input_data)
    db.session.add(result)
    db.session.commit()

    return '', 200
    # except:
    #     abort(500)



@raceinfo.route('/emulation')
def emulation():
    return render_template('timer.html')
@raceinfo.route('/receiver')
def receiver():
    return render_template('receiver.html')

@raceinfo.route('/receiver_jury')
def receiver_jury():
    return render_template('receiver_jury.html')

