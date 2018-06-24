from flask import make_response, render_template, request
import pdfkit
from .models import *
import tempfile
import datetime

import io
from . import raceinfo
from .results import get_results

import xlwt
import json
from math import floor
path = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"

@raceinfo.route('/race/<int:race_id>/reports')
def reports_page(race_id):
    race = RaceInformation.get_main_race_info(race_id)
    return render_template('reports/report_page.html', race=race[0])

@raceinfo.route('/race/<int:race_id>/reports/xls')
def generate_excel(race_id):
    wb = ExcelGenerator('results')

    wb.set_header(
        db.session.query(RunInfo).distinct(RunInfo.id). \
            filter(RunInfo.race_id == race_id). \
            count()
    )

    wb.set_data(json.loads(get_results(race_id)))

    response = make_response(wb.get_xls_file())
    response.headers['Content-Type'] = 'application/vnd.ms-excel'
    response.headers['Content-Disposition'] = 'inline; filename=xls_report.xls'
    return response


@raceinfo.route('/race/<int:race_id>/reports/orderlist')
def generate_orderlist_report(race_id):
    # try:
    # Prepare data

    ffactor =request.args.get('fields[ffactor]')

    race = RaceInformation.get_main_race_info(race_id)
    course = RaceInformation.get_course_info(race_id)

    # Create report

    report = OrderListReport(race)
    report.set_header()
    report.set_content(race=race,
                       jury=RaceInformation.get_jury_info(race_id),
                       course=course,
                       coursesetter=RaceInformation.get_coursesetter_info(course.course_coursetter_id),
                       competitors=RaceInformation.get_competitor_info(race_id),
                       forerunners=RaceInformation.get_forunners_info(course.id),
                       number_of_NOCs=RaceInformation.get_number_of_NOCs(race_id), F=ffactor
                       )
    report.set_footer()

    response = make_response(report.get_file())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=orderlist_report.pdf'
    return response
    # except:
    #     return render_template('custom_error.html', title='Ошибка формирования отчета')

@raceinfo.route('/race/<int:race_id>/reports/orderlist/<int:run_number>')
def generate_orderlist_report_for_run(race_id, run_number):
    # try:
    # Prepare data
    race = RaceInformation.get_main_race_info(race_id)
    course = RaceInformation.get_course_info(race_id)
    ffactor =request.args.get('fields[ffactor]')

    # Create report

    report = OrderListReport(race, run_number)
    report.set_header()
    report.set_content(race=race,
                       jury=RaceInformation.get_jury_info(race_id),
                       course=course,
                       coursesetter=RaceInformation.get_coursesetter_info(course.course_coursetter_id),
                       competitors=RaceInformation.get_competitor_info_for_run(race_id, run_number),
                       forerunners=RaceInformation.get_forunners_info(course.id),
                       number_of_NOCs=RaceInformation.get_number_of_NOCs(race_id),
                       runs=RaceInformation.get_runs_starttime(race_id), F=ffactor
                       )
    report.set_footer()

    response = make_response(report.get_file())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=orderlist_report.pdf'
    return response
    # except:
    #     return render_template('custom_error.html', title='Ошибка формирования отчета')

@raceinfo.route('/race/<int:race_id>/reports/results')
def generate_results_report(race_id):
    # Prepare data
    # try:
    ffactor =request.args.get('fields[ffactor]')
    penalty = request.args.get('fields[penalty]')
    reasondesc = request.args.get('fields[reasondesc]')

    race = RaceInformation.get_main_race_info(race_id)
    course = RaceInformation.get_course_info(race_id)


    qlf_list, disqlf_list = RaceInformation.get_results(RaceInformation.get_competitor_info(race_id),
                                                        RaceInformation.get_approved_competitor_info(race_id))
    # Create report

    run_numbers = db.session.query(RunInfo).distinct(RunInfo.id). \
        filter(RunInfo.race_id == race_id). \
        count()
    report = RaceResultReport(race)

    report.set_header()

    report.set_content(jury=RaceInformation.get_jury_info(race_id),
                       course=course,
                       coursesetter=RaceInformation.get_coursesetter_info(course.course_coursetter_id),
                       forerunners=RaceInformation.get_forunners_info(course.id),
                       qlf_list=qlf_list,
                       disqlf_list=disqlf_list,
                       weather=RaceInformation.get_weather_info(race_id), F=ffactor, penalty=penalty, reasondesc=reasondesc
                       )

    report.set_footer()

    response = make_response(report.get_file())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=results_report.pdf'
    return response
    # except:
    #     return render_template('custom_error.html', title='Ошибка формирования отчета')

@raceinfo.route('/race/<int:race_id>/reports/results/first')
def generate_results_report_first(race_id):
    # Prepare data
    # try:
    ffactor =request.args.get('fields[ffactor]')
    penalty = request.args.get('fields[penalty]')
    reasondesc = request.args.get('fields[reasondesc]')

    race = RaceInformation.get_main_race_info(race_id)
    course = RaceInformation.get_course_info(race_id)


    qlf_list, disqlf_list = RaceInformation.get_first_run_results(RaceInformation.get_competitor_info(race_id),
                                                        RaceInformation.get_first_run_approves(race_id))
    # Create report

    run_numbers = db.session.query(RunInfo).distinct(RunInfo.id). \
        filter(RunInfo.race_id == race_id). \
        count()
    report = RaceResultReport(race, is_first_run=True)

    report.set_header()

    report.set_content(jury=RaceInformation.get_jury_info(race_id),
                       course=course,
                       coursesetter=RaceInformation.get_coursesetter_info(course.course_coursetter_id),
                       forerunners=RaceInformation.get_forunners_info(course.id),
                       qlf_list=qlf_list,
                       disqlf_list=disqlf_list,
                       weather=RaceInformation.get_weather_info(race_id), F=ffactor, penalty=penalty, reasondesc=reasondesc
                       )



    report.set_footer()

    response = make_response(report.get_file())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=results_report.pdf'
    return response
    # except:
    #     return render_template('custom_error.html', title='Ошибка формирования отчета')

@raceinfo.route('/race/<int:race_id>/reports/results/unofficial')
def generate_unofficial_results_report(race_id):
    # Prepare data
    # try:
    ffactor =request.args.get('fields[ffactor]')
    penalty = request.args.get('fields[penalty]')
    reasondesc = request.args.get('fields[reasondesc]')

    race = RaceInformation.get_main_race_info(race_id)
    course = RaceInformation.get_course_info(race_id)


    qlf_list, disqlf_list = RaceInformation.get_results(RaceInformation.get_competitor_info(race_id),
                                                        RaceInformation.get_approved_competitor_info(race_id))
    # Create report
    run_numbers = db.session.query(RunInfo).distinct(RunInfo.id). \
        filter(RunInfo.race_id == race_id). \
        count()
    report = RaceResultReport(race, is_first_run=False, is_official=False)

    report.set_header()

    report.set_content(jury=RaceInformation.get_jury_info(race_id),
                       course=course,
                       coursesetter=RaceInformation.get_coursesetter_info(course.course_coursetter_id),
                       forerunners=RaceInformation.get_forunners_info(course.id),
                       qlf_list=qlf_list,
                       disqlf_list=disqlf_list,
                       weather=RaceInformation.get_weather_info(race_id), F=ffactor, penalty=penalty, reasondesc=reasondesc
                       )


    report.set_footer()

    response = make_response(report.get_file())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=results_report.pdf'
    return response
    # except:
    #     return render_template('custom_error.html', title='Ошибка формирования отчета')
    #
    #
    #



class Report:
    options = {}
    content = None
    run_number = None
    title = None

    def __init__(self, race):
        self.options = {
            'page-size': 'A4',
            'dpi': 400,
            '--margin-top': '30'
        }
        self.race = race

    def set_header(self):
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as header:
            self.options['--header-html'] = header.name
            header.write(
                render_template('reports/header.html', race=self.race,
                                title=self.title,
                                run_title=self.run_number,
                                date=self.race[0].racedate.strftime('%a %d %b %Y'),
                                time=self.race[0].racedate.strftime('%H:%M')).encode('utf-8')
            )
        return
    def set_footer(self):
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as footer:
            self.options['--footer-html'] = footer.name
            footer.write(
                render_template('reports/footer.html', race=self.race,
                                date=self.race[0].racedate.strftime('%a %d %b %Y'),
                                codex=self.race[0].codex,
                                place=self.race[0].place,
                                country_code=self.race[4].name,
                                generation_time=datetime.datetime.now()
                                ).encode('utf-8')
            )
        return

    def get_file(self):
        # return pdfkit.from_string(self.content, False, self.options, configuration=pdfkit.configuration(wkhtmltopdf=path))
        return pdfkit.from_string(self.content, False, self.options)

class OrderListReport(Report):
    def __init__(self, race, run_number=0):
        super().__init__(race)
        self.run_number = run_number
        self.title = "START LIST"

    def set_content(self, race, jury, course, coursesetter, competitors, forerunners, number_of_NOCs, F, runs=None):
        self.content = render_template('reports/startlist.html',
                                       title=self.title,
                                      race=race,
                                      jury=jury,
                                      course=course,
                                      course_setter=coursesetter,
                                      competitors=competitors,
                                      forerunners=forerunners,
                                      number_of_NOCs=number_of_NOCs,
                                      run_number=self.run_number,
                                      runs=runs, F=F)


class RaceResultReport(Report):

    is_first_run = None

    def __init__(self, race, is_first_run=False, is_official=True):
        super().__init__(race)
        if is_official:
            self.title = "OFFICIAL RESULTS"
        else:
            self.title = "UNOFFICIAL RESULTS"
        self.is_first_run = is_first_run

    def set_content(self, jury, course, coursesetter, forerunners, qlf_list, disqlf_list, weather, F, penalty, reasondesc):
        if self.race[3].is_combination:
            course = db.session.query(Course,RunInfo,Discipline.en_name.label('discipline')).\
                join(RunInfo, RunInfo.course_id==Course.id).\
                join(Discipline, Discipline.id==RunInfo.discipline_id, isouter=True).filter(Course.race_id==self.race[0].id).order_by(RunInfo.number).all()
            self.content = render_template('reports/combination.html',
                                           title=self.title,
                                           qlf_competitors=qlf_list,
                                           disqlf_competitors=disqlf_list,
                                           course=course,
                                           course_setter=coursesetter,
                                           jury=jury,
                                           weather=weather,
                                           forerunners=forerunners, F=F, penalty=penalty,
                                           reasondesc=reasondesc, is_first_run=self.is_first_run)
        else:
            self.content = render_template('reports/results.html',
                                           title=self.title,
                                           qlf_competitors=qlf_list,
                                           disqlf_competitors=disqlf_list,
                                           course=course,
                                           course_setter=coursesetter,
                                           jury=jury,
                                           weather=weather,
                                           forerunners=forerunners, F=F, penalty=penalty,
                                           reasondesc=reasondesc, is_first_run=self.is_first_run)

class ExcelGenerator:
    cursor = []
    wb = None
    ws = None
    def __init__(self, sheet_name):
        self.cursor = [0, 0]
        self.wb = xlwt.Workbook()
        self.ws = self.wb.add_sheet(sheet_name)
    def set_header(self, run_count):
        header = [{'name': 'Bib',
                   'rows_count': 0,
                   'cell_count': 1,
                   }, {'name': 'Name',
                       'rows_count': 0,
                       'cell_count': 1,
                       },
                          {'name': 'Surname',
                           'rows_count': 0,
                           'cell_count': 1,
                           },
                              {'name': 'Rank',
                               'rows_count': 0,
                               'cell_count': 1,
                               }, {'name': 'Time',
                                   'rows_count': 0,
                                   'cell_count': 1,
                                   }, {'name': 'Diff',
                                       'rows_count': 0,
                                       'cell_count': 1,
                                       }, {'name': 'Status',
                                           'rows_count': 0,
                                           'cell_count': 1,
                                           }]

        for index, item in enumerate(header):
            self.ws.write_merge(0, 0+item['cell_count'], index + item['rows_count'], index + item['rows_count'], item['name'])
        self.cursor[1]=7
        for item in range(run_count):
            self.ws.write_merge(0, 0, self.cursor[1], self.cursor[1]+4,
                                'Run '+ str(item+1))
            self.ws.write(1, self.cursor[1], 'Rank')
            self.ws.write(1, self.cursor[1]+1, 'Time')
            self.ws.write(1, self.cursor[1]+2, 'Status')
            self.ws.write(1, self.cursor[1]+3, 'Gate')
            self.ws.write(1, self.cursor[1]+4, 'reason')
            self.cursor[1] += 5
        self.cursor[0] = 3
        self.cursor[1] = 1
    def set_data(self, data):
        for item in data:
            self.ws.write(self.cursor[0], 0, item['bib'])
            self.ws.write(self.cursor[0], 1, item['en_firstname'])
            self.ws.write(self.cursor[0], 2, item['ru_firstname'])
            self.ws.write(self.cursor[0], 3, item['global_rank'])
            self.ws.write(self.cursor[0], 4, time_convertor(item['result_time']))
            self.ws.write(self.cursor[0], 5, time_convertor(item['diff']))
            self.ws.write(self.cursor[0], 6, item['status'])
            self.cursor[1] = 7
            for result_item in item['results']:

                self.ws.write(self.cursor[0], self.cursor[1], result_item['rank'])
                self.cursor[1] += 1
                self.ws.write(self.cursor[0], self.cursor[1], time_convertor(result_item['time']))
                self.cursor[1] += 1
                self.ws.write(self.cursor[0], self.cursor[1], result_item['status'])
                self.cursor[1] += 1
                if result_item['status_id'] != 1:
                    self.ws.write(self.cursor[0], self.cursor[1], result_item['gate'])
                    self.cursor[1] += 1
                    self.ws.write(self.cursor[0], self.cursor[1], result_item['reason'])
                    self.cursor[1] += 1
            self.cursor[0] += 1


    def save(self, path):
        self.wb.save(path)


    def get_xls_file(self):
        output = io.BytesIO()
        self.wb.save(output)
        return output.getvalue()

class RaceInformation:
    @staticmethod
    def get_main_race_info(race_id):
        return db.session.query(Race, Gender, Category, Discipline, Nation). \
            join(Gender). \
            join(Category). \
            join(Discipline). \
            join(Nation, Race.nation_id == Nation.id). \
            filter(Race.id == race_id).one()

    @staticmethod
    def get_forunners_info(course_id):
        return db.session.query(Forerunner.en_firstname.label('en_firstname'),
                                Forerunner.en_lastname.label('en_lastname'),
                                CourseForerunner.order.label('order'),
                                Nation.name.label('name')). \
            filter(Forerunner.nation_id == Nation.id,
                   CourseForerunner.forerunner_id == Forerunner.id,
                   CourseForerunner.course_id == course_id). \
            all()

    @staticmethod
    def get_jury_info(race_id):
        return db.session.query(Jury.en_lastname.label('en_lastname'),
                                Jury.en_firstname.label('en_firstname'),
                                JuryType.type.label('type'),
                                Nation.name).filter(RaceJury.race_id == race_id,
                                                    JuryType.id == RaceJury.jury_function_id,
                                                    RaceJury.jury_id == Jury.id,
                                                    Jury.nation_id == Nation.id).all()

    @staticmethod
    def get_course_info(race_id):
        return Course.query.filter(Course.race_id == race_id).first()

    @staticmethod
    def get_coursesetter_info(course_coursetter_id):
        return db.session.query(Coursetter.en_lastname.label('en_lastname'),
                                Coursetter.en_firstname.label('en_firstname'),
                                Nation.name.label('name')) \
            .filter(Coursetter.id == course_coursetter_id,
                    Coursetter.nation_id == Nation.id).one()

    @staticmethod
    def get_competitor_info(race_id):
        return db.session.query(Competitor, RaceCompetitor, Nation). \
            join(RaceCompetitor). \
            join(Nation, Nation.id == Competitor.nation_code_id). \
            filter(RaceCompetitor.race_id == race_id). \
            order_by(RaceCompetitor.bib). \
            all()

    @staticmethod
    def get_competitor_info_for_run(race_id, run_number):
        run = RunInfo.query.filter(RunInfo.race_id==race_id, RunInfo.number==run_number).first()
        return db.session.query(Competitor, RaceCompetitor, Nation, RunOrder). \
            join(RaceCompetitor). \
            join(Nation, Nation.id == Competitor.nation_code_id). \
            join(RunOrder, RunOrder.race_competitor_id == RaceCompetitor.id). \
            filter(RaceCompetitor.race_id == race_id, RunOrder.run_id==run.id). \
            order_by(RunOrder.order). \
            all()

    @staticmethod
    def get_number_of_NOCs(race_id):
        return db.session.query(Nation).distinct(Nation.name). \
               filter(RaceCompetitor.race_id == race_id,
               RaceCompetitor.competitor_id == Competitor.id,
               Competitor.nation_code_id == Nation.id).count()

    @staticmethod
    def get_results(race_competitors, competitors_approve):
        qlf_list = []
        disqlf_list = {}
        for item in race_competitors:
            if item[1].status_id == 1:
                qlf_item = {
                    'rank': item[1].rank,
                    'bib': item[1].bib,
                    'fiscode': item[0].fiscode,
                    'en_firstname': item[0].en_firstname,
                    'en_lastname': item[0].en_lastname,
                    'birth': item[0].birth,
                    'club': item[1].club,
                    'nation': item[2].name,
                    # 'total': (datetime.datetime.fromtimestamp(item[1].time).strftime("%m:%S.%f"))[:-3],
                    # 'diff': (datetime.datetime.fromtimestamp(item[1].diff).strftime("%m:%S.%f"))[:-3]
                    'total': time_convertor(item[1].time),
                    'diff': time_convertor(item[1].diff)
                }
                for approve in competitors_approve:
                    if item[1].id == approve.competitor_id:
                        qlf_item['time' + str(approve.run_number)] = time_convertor(approve.time)
                        qlf_item['rank' + str(approve.run_number)] = approve.rank
                qlf_list.append(qlf_item)
            else:
                if item[1].status_id not in disqlf_list:
                    disqlf_list[item[1].status_id] = {
                        'competitors': []
                    }
                    status_name = Status.query.filter(Status.id == item[1].status_id).first()
                    if status_name is not None:
                        disqlf_list[item[1].status_id]['status'] = status_name.description
                disqlf_list[item[1].status_id]['competitors'].append({
                    'bib': item[1].bib,
                    'fiscode': item[0].fiscode,
                    'en_firstname': item[0].en_firstname,
                    'en_lastname': item[0].en_lastname,
                    'birth': item[0].birth,
                    'club': item[1].club,
                    'nation': item[2].name,
                    'status': item[1].status_id,
                    'gate': item[1].gate,
                    'reason': item[1].reason
                })
        return sorted(qlf_list, key=lambda item: item['rank']), disqlf_list

    @staticmethod
    def get_first_run_results(race_competitors, competitors_approve):
        qlf_list = []
        disqlf_list = {}
        for item in competitors_approve:
            if item.status_id == 1:
                competitor = next((competitor for competitor in race_competitors if
                                   competitor[1].id == item.competitor_id), None)
                qlf_item = {
                    'bib': competitor[1].bib,
                    'fiscode': competitor[0].fiscode,
                    'en_firstname': competitor[0].en_firstname,
                    'en_lastname': competitor[0].en_lastname,
                    'birth': competitor[0].birth,
                    'club': competitor[1].club,
                    'nation': competitor[2].name,
                    'statuc_id': item.status_id,
                    'time': time_convertor(item.time),
                    'rank': item.rank,
                    'diff': time_convertor(item.diff)
                }
                qlf_list.append(qlf_item)
        return sorted(qlf_list, key=lambda item: item['rank']), disqlf_list

    @staticmethod
    def get_approved_competitor_info(race_id):
        return db.session.query(ResultApproved.race_competitor_id.label('competitor_id'),
                                ResultApproved.time.label('time'),
                                ResultApproved.rank.label('rank'),
                                ResultApproved.gate.label('gate'),
                                ResultApproved.diff.label('diff'),
                                ResultApproved.reason.label('reason'),
                                RunInfo.number.label('run_number')).\
            filter(ResultApproved.run_id == RunInfo.id,
                   RunInfo.race_id == race_id,
                   RunInfo.number.in_([1, 2])).all()
    @staticmethod
    def get_first_run_approves(race_id):
        return db.session.query(ResultApproved.race_competitor_id.label('competitor_id'),
                                ResultApproved.time.label('time'),
                                ResultApproved.rank.label('rank'),
                                ResultApproved.gate.label('gate'),
                                ResultApproved.diff.label('diff'),
                                ResultApproved.status_id.label('status_id'),
                                ResultApproved.reason.label('reason'),
                                RunInfo.number.label('run_number')).\
            filter(ResultApproved.run_id == RunInfo.id,
                   RunInfo.race_id == race_id,
                   RunInfo.number == 1).all()
    @staticmethod
    def get_weather_info(race_id):
        return Weather.query.filter(Weather.race_id == race_id).all()

    @staticmethod
    def get_runs_starttime(race_id):
        return [(item.number, item.starttime.strftime('%H:%M')) for item in
                RunInfo.query.filter(RunInfo.race_id == race_id,
                                     RunInfo.number.in_([1, 2])).all()]

def time_convertor(timestamp):

    if timestamp == None or timestamp == "None":
        return None
    sss = int(timestamp) % 1000
    str_sss = str(sss)

    if sss < 100:
        str_sss = "0"+str(str_sss)
    if sss < 10:
        str_sss = "0"+str(str_sss)
    ss=floor(int(timestamp)/1000)%60
    if ss < 10:
        ss = "0" + str(ss)
    mm=floor(int(timestamp)/60000)
    if mm < 10:
        mm = "0"+str(mm)

    return (mm+":"+str(ss)+"."+str(str_sss))[:-1]




