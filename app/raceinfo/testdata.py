from . import raceinfo
from .models import *
from datetime import datetime, timedelta
import random
from ..models import Role
@raceinfo.route('/test_data/', methods=['GET', 'POST'])
def insert_test_data():
    # db.create_all()
    # Discipline.insert_discipline()
    # Gender.insert_genders()
    # Status.insert()
    # Jury_function.insert_functions()
    # CourseDeviceType.insert_types()
    # nation =Nation( name='Rus',ru_description='Rus',en_description='Rus' )
    # db.session.add(nation)
    # category =Category(
    #     name='te',
    #     description = 'test',
    #     level =2
    # )
    # db.session.add(category)
    # db.session.commit()
    # strings=['name', 'surname']
    # for i in range(1,30):
    #     year = random.randint(1950, 2000)
    #     month = random.randint(1, 12)
    #     day = random.randint(1, 28)
    #     birth_date = datetime(year, month, day)
    #     competitor = Competitor(
    #         fiscode = i,
    #         ru_firstname = strings[0]+str(i),
    #         en_firstname = strings[0]+str(i),
    #         ru_lastname = strings[1]+str(i),
    #         en_lastname = strings[1]+str(i),
    #         gender_id = random.randint(1,2),
    #
    #         birth = birth_date,
    #         nation_code_id = 1,
    #
    #         national_code =1,
    #         NSA = i,
    #         category_id = 1,
    #
    #         points = 1,
    #         fis_points =1
    #     )
    #     db.session.add(competitor)
    # strings=['name', 'surname']
    # for i in range(1,5):
    #     coursetter = Coursetter(
    #         ru_firstname = strings[0]+str(i),
    #         en_firstname = strings[0]+str(i),
    #         ru_lastname = strings[1]+str(i),
    #         en_lastname = strings[1]+str(i),
    #         nation_id = 1,
    #     )
    #     db.session.add(coursetter)
    #     forerunner = Forerunner(
    #         ru_firstname=strings[0] + str(i),
    #         en_firstname=strings[0] + str(i),
    #         ru_lastname=strings[1] + str(i),
    #         en_lastname=strings[1] + str(i),
    #         nation_id=1,
    #     )
    #
    #     db.session.add(forerunner)
    return '', 200
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




   # result_details = db.session.query(ResultDetail, RaceCompetitor, Competitor, CourseDevice, CourseDeviceType,RunOrder).\
    #     join(RaceCompetitor).\
    #     join(Competitor).\
    #     join(CourseDevice).\
    #     join(CourseDeviceType).\
    #     join(RunOrder, RunOrder.race_competitor_id == RaceCompetitor.id).\
    #     filter(ResultDetail.course_device_id == course_device[0].id, ResultDetail.run_id == run.id,RunOrder.run_id == run.id).order_by(asc(ResultDetail.diff)).all()