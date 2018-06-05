from flask import make_response, render_template
import pdfkit
from .models import *
import tempfile
import datetime
from flask import Response
import io
from . import raceinfo
from .results import get_results
from pathlib import Path

import xlwt
import json

path = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe";

@raceinfo.route('/race/<int:race_id>/report/ishtml/<isHTML>')
def Report_show(race_id,isHTML):
    try:
        # Race
        race = db.session.query(Race, Gender, Category, Discipline, Nation). \
            join(Gender). \
            join(Category). \
            join(Discipline). \
            join(Nation, Race.nation_id == Nation.id). \
            filter(Race.id == race_id).one()

        # Jury
        jury = db.session.query(Jury.en_lastname.label('en_lastname'),
                                Jury.en_firstname.label('en_firstname'),
                                JuryType.type.label('type'),
                                Nation.name).filter(RaceJury.race_id == race_id,
                                                    JuryType.id == RaceJury.jury_function_id,
                                                    RaceJury.jury_id == Jury.id,
                                                    Jury.nation_id == Nation.id).all()
        # Course
        course = Course.query.filter(Course.race_id == race_id).first()

        course_setter = db.session.query(Coursetter.en_lastname.label('en_lastname'),
                                         Coursetter.en_firstname.label('en_firstname'),
                                         Nation.name.label('name')) \
            .filter(Coursetter.id == course.course_coursetter_id,
                    Coursetter.nation_id == Nation.id).one()
        # Competitors
        competitors = db.session.query(Competitor, RaceCompetitor, Nation). \
            join(RaceCompetitor). \
            join(Nation, Nation.id == Competitor.nation_code_id). \
            filter(RaceCompetitor.race_id == race_id). \
            order_by(RaceCompetitor.bib). \
            all()

        number_of_NOCs = db.session.query(Nation).distinct(Nation.name). \
            filter(RaceCompetitor.race_id == race_id,
                   RaceCompetitor.competitor_id == Competitor.id,
                   Competitor.nation_code_id == Nation.id). \
            count()
        forerunners = db.session.query(Forerunner.en_firstname.label('en_firstname'),
                                       Forerunner.en_lastname.label('en_lastname'),
                                       CourseForerunner.order.label('order'),
                                       Nation.name.label('name')). \
            filter(Forerunner.nation_id == Nation.id,
                   CourseForerunner.forerunner_id == Forerunner.id,
                   CourseForerunner.course_id == course.id). \
            all()

        html_render = render_template('reports/startlist.html',
                                      race=race,
                                      jury=jury,
                                      course=course,
                                      course_setter=course_setter,
                                      competitors=competitors,
                                      forerunners=forerunners,
                                      number_of_NOCs=number_of_NOCs)

        options = {
            'page-size': 'A4',
            'dpi': 400,

            '--margin-top': '30',
            # '--margin-bottom':'-20mm',
            # '--footer-center':'[page]/[topage]'
        }
        add_pdf_header(options, race)
        add_pdf_footer(options, race)
        if isHTML == 'true':
            return html_render
        else:
            pdf = pdfkit.from_string(html_render, False, options, configuration=pdfkit.configuration(wkhtmltopdf=path))
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'inline; filename=report.pdf'
            return response
    except AttributeError:
        pass

def add_pdf_header(options, race):

    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as header:
        options['--header-html'] = header.name
        header.write(
            render_template('reports/header.html', race=race,
                            date=race[0].racedate.strftime('%a %d %b %Y'),
                            time=race[0].racedate.strftime('%H:%M')).encode('utf-8')
        )
    return

def add_pdf_footer(options, race):

    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as footer:
        options['--footer-html'] = footer.name
        footer.write(
            render_template('reports/footer.html', race=race,
                            date=race[0].racedate.strftime('%a %d %b %Y'),
                            codex=race[0].codex,
                            place=race[0].place,
                            country_code=race[4].name,
                            generation_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            ).encode('utf-8')
        )
    return

@raceinfo.route('/race/<int:race_id>/report/result')
def get_results__(race_id):
    race_competitors = db.session.query(RaceCompetitor, Competitor, Nation).\
        join(Competitor). \
        join(Nation, Competitor.nation_code_id==Nation.id). \
        filter(RaceCompetitor.race_id==race_id).\
        all()
    # Course

    jury = db.session.query(Jury.en_lastname.label('en_lastname'),
                            Jury.en_firstname.label('en_firstname'),
                            JuryType.type.label('type'),
                            Nation.name).filter(RaceJury.race_id == race_id,
                                                JuryType.id == RaceJury.jury_function_id,
                                                RaceJury.jury_id == Jury.id,
                                                Jury.nation_id == Nation.id).all()

    course = Course.query.filter(Course.race_id == race_id).first()

    course_setter = db.session.query(Coursetter.en_lastname.label('en_lastname'),
                                     Coursetter.en_firstname.label('en_firstname'),
                                     Nation.name.label('name')) \
        .filter(Coursetter.id == course.course_coursetter_id,
                Coursetter.nation_id == Nation.id).one()
    competitors_approve = db.session.query(ResultApproved.race_competitor_id.label('competitor_id'),
                                           ResultApproved.time.label('time'),
                                           ResultApproved.rank.label('rank'),
                                           ResultApproved.gate.label('gate'),
                                           ResultApproved.reason.label('reason'),
                                           RunInfo.number.label('run_number')). \
        filter(ResultApproved.run_id==RunInfo.id,
               RunInfo.number.in_([1, 2])).all()
    forerunners = db.session.query(Forerunner.en_firstname.label('en_firstname'),
                                   Forerunner.en_lastname.label('en_lastname'),
                                   CourseForerunner.order.label('order'),
                                   Nation.name.label('name')).\
        filter(Forerunner.nation_id == Nation.id,
               CourseForerunner.forerunner_id == Forerunner.id,
               CourseForerunner.course_id == course.id).\
        all()
    qlf_list = []
    disqlf_list = {}
    for item in race_competitors:
        if item[0].status_id == 1:
            qlf_item = {
                'rank': item[0].rank,
                'bib': item[0].bib,
                'fiscode': item[1].fiscode,
                'en_firstname':item[1].en_firstname,
                'en_lastname': item[1].en_lastname,
                'birth': item[1].birth,
                'club': item[0].club,
                'nation': item[2].name,
                'total': item[0].time,
                'diff': item[0].diff
            }
            for approve in competitors_approve:
                if item[0].id == approve.competitor_id:
                    qlf_item['time'+str(approve.run_number)] = approve.time
                    qlf_item['rank'+str(approve.run_number)] = approve.rank
            qlf_list.append(qlf_item)
        else:
            if item[0].status_id not in disqlf_list:
                disqlf_list[item[0].status_id]={
                    'name': (Status.query.filter(Status.id == item[0].status_id).one()).description,
                    'competitors': []
                }
            disqlf_list[item[0].status_id]['competitors'].append({
            'bib': item[0].bib,
            'fiscode': item[1].fiscode,
            'en_firstname': item[1].en_firstname,
            'en_lastname': item[1].en_lastname,
            'birth': item[1].birth,
            'club': item[0].club,
            'nation': item[2].name,
            'status': item[0].status_id,
            'gate': item[0].gate,
            'reason': item[0].reason
            })
    qlf_list = sorted(qlf_list, key= lambda item: item['rank'])

    weather = Weather.query.filter(Weather.race_id == race_id).all()
    return render_template('reports/results.html',
                           qlf_competitors=qlf_list,
                           disqlf_competitors=disqlf_list,
                           course=course,
                           course_setter=course_setter,
                           jury=jury,
                           weather=weather,
                           forerunners=forerunners)

def number_of_NOCs(race_id):
    return db.session.query(Nation).distinct(Nation.name). \
        filter(RaceCompetitor.race_id == race_id,
               RaceCompetitor.competitor_id == Competitor.id,
               Competitor.nation_code_id == Nation.id). \
        count()

@raceinfo.route('/race/<int:race_id>/reports')
def reports_page(race_id):
    startlist_report = None
    results_report = None

    number_of_NOCs = db.session.query(Nation).distinct(Nation.name). \
        filter(RaceCompetitor.race_id == race_id,
               RaceCompetitor.competitor_id == Competitor.id,
               Competitor.nation_code_id == Nation.id). \
        count()

    race_competitors = db.session.query(RaceCompetitor, Competitor, Nation).\
        join(Competitor). \
        join(Nation, Competitor.nation_code_id==Nation.id). \
        filter(RaceCompetitor.race_id==race_id).\
        all()

    race = bace_race_informaion(race_id)


    jury = jury_information(race_id)
    # Course
    course = Course.query.filter(Course.race_id == race_id).first()

    course_setter = couresetter_information(course.course_coursetter_id)
    # Competitors

    competitors = db.session.query(Competitor, RaceCompetitor, Nation). \
        join(RaceCompetitor). \
        join(Nation, Nation.id == Competitor.nation_code_id). \
        filter(RaceCompetitor.race_id == race_id). \
        order_by(RaceCompetitor.bib). \
        all()




    forerunners = forrunners_information(course.id)

    competitors_approve = db.session.query(ResultApproved.race_competitor_id.label('competitor_id'),
                                           ResultApproved.time.label('time'),
                                           ResultApproved.rank.label('rank'),
                                           ResultApproved.gate.label('gate'),
                                           ResultApproved.reason.label('reason'),
                                           RunInfo.number.label('run_number')). \
        filter(ResultApproved.run_id == RunInfo.id,
               RunInfo.race_id==race_id,
               RunInfo.number.in_([1, 2])).all()

    qlf_list, disqlf_list = prepare_results(race_competitors, competitors_approve)

    weather = Weather.query.filter(Weather.race_id == race_id).all()

    results_report = render_template('reports/results.html',
                           qlf_competitors=qlf_list,
                           disqlf_competitors=disqlf_list,
                           course=course,
                           course_setter=course_setter,
                           jury=jury,
                           weather=weather,
                           forerunners=forerunners)

    startlist_report = render_template('reports/startlist.html',
                                  race=race,
                                  jury=jury,
                                  course=course,
                                  course_setter=course_setter,
                                  competitors=competitors,
                                  forerunners=forerunners,
                                  number_of_NOCs=number_of_NOCs)

    options = {
        'page-size': 'A4',
        'dpi': 400,
        # '--header-spacing': '30',
        # '--footer-spacing': '30',
        '--margin-top': '30',
    }
    add_pdf_header(options, race)
    add_pdf_footer(options, race)

    pdfkit.from_string(startlist_report, pdf_path(race_id, 'startlist'), options, configuration=pdfkit.configuration(wkhtmltopdf=path))
    pdfkit.from_string(results_report, pdf_path(race_id, 'results'), options, configuration=pdfkit.configuration(wkhtmltopdf=path))

    return render_template('reports/report_page.html',
                           race=race[0],
                           startlist_pdf=pdf_path(race_id, 'startlist'),
                           results_pdf=pdf_path(race_id, 'results')
                           )

def pdf_path(race_id, report_type, format=None):
    if format is None:
        return str(Path(__file__).resolve().parents[1])+'/static/reports/race'+str(race_id)+report_type+'.pdf'
    else:
        return str(Path(__file__).resolve().parents[1]) + '/static/reports/race' + str(race_id) + report_type + '.'+str(format)
def prepare_results(race_competitors, competitors_approve):
    qlf_list = []
    disqlf_list = {}
    for item in race_competitors:
        if item[0].status_id == 1:
            qlf_item = {
                'rank': item[0].rank,
                'bib': item[0].bib,
                'fiscode': item[1].fiscode,
                'en_firstname': item[1].en_firstname,
                'en_lastname': item[1].en_lastname,
                'birth': item[1].birth,
                'club': item[0].club,
                'nation': item[2].name,
                'total': item[0].time,
                'diff': item[0].diff
            }
            for approve in competitors_approve:
                if item[0].id == approve.competitor_id:
                    qlf_item['time'+str(approve.run_number)] = approve.time
                    qlf_item['rank'+str(approve.run_number)] = approve.rank
            qlf_list.append(qlf_item)
        else:
            if item[0].status_id not in disqlf_list:
                disqlf_list[item[0].status_id] = {
                    'name': (Status.query.filter(Status.id == item[0].status_id).one()).description,
                    'competitors': []
                }
            disqlf_list[item[0].status_id]['competitors'].append({
                'bib': item[0].bib,
                'fiscode': item[1].fiscode,
                'en_firstname': item[1].en_firstname,
                'en_lastname': item[1].en_lastname,
                'birth': item[1].birth,
                'club': item[0].club,
                'nation': item[2].name,
                'status': item[0].status_id,
                'gate': item[0].gate,
                'reason': item[0].reason
            })
    return sorted(qlf_list, key=lambda item: item['rank']), disqlf_list

def bace_race_informaion(race_id):
    return db.session.query(Race, Gender, Category, Discipline, Nation).\
            join(Gender). \
            join(Category). \
            join(Discipline). \
            join(Nation, Race.nation_id==Nation.id).\
            filter(Race.id == race_id).one()

def jury_information(race_id):
    return db.session.query(Jury.en_lastname.label('en_lastname'),
                     Jury.en_firstname.label('en_firstname'),
                     JuryType.type.label('type'),
                     Nation.name).filter(RaceJury.race_id == race_id,
                                         JuryType.id == RaceJury.jury_function_id,
                                         RaceJury.jury_id == Jury.id,
                                         Jury.nation_id == Nation.id).all()

def couresetter_information(course_coursetter_id):
    return db.session.query(Coursetter.en_lastname.label('en_lastname'),
                                     Coursetter.en_firstname.label('en_firstname'),
                                     Nation.name.label('name')) \
        .filter(Coursetter.id == course_coursetter_id,
                Coursetter.nation_id == Nation.id).one()

def forrunners_information(course_id):
    return db.session.query(Forerunner.en_firstname.label('en_firstname'),
                     Forerunner.en_lastname.label('en_lastname'),
                     CourseForerunner.order.label('order'),
                     Nation.name.label('name')). \
        filter(Forerunner.nation_id == Nation.id,
               CourseForerunner.forerunner_id == Forerunner.id,
               CourseForerunner.course_id == course_id). \
        all()

@raceinfo.route('/race/<int:race_id>/xls')
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
    response.headers['Content-Disposition'] = 'inline; filename=report.xls'
    return response

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
                   'cell_count': 2,
                   }, {'name': 'Name',
                       'rows_count': 0,
                       'cell_count': 2,
                       }, {'name': 'Rank',
                           'rows_count': 0,
                           'cell_count': 2,
                           }, {'name': 'Time',
                               'rows_count': 0,
                               'cell_count': 2,
                               }, {'name': 'Diff',
                                   'rows_count': 0,
                                   'cell_count': 2,
                                   }, {'name': 'Status',
                                       'rows_count': 0,
                                       'cell_count': 2,
                                       }]

        for index, item in enumerate(header):
            self.ws.write_merge(0, 0+item['cell_count'], index + item['rows_count'], index + item['rows_count'], item['name'])
        self.cursor[1]=6
        for item in range(run_count):
            self.ws.write_merge(0, 0, self.cursor[1], self.cursor[1]+2,
                                'Run '+ str(item+1))
            self.ws.write(1, self.cursor[1], 'Rank')
            self.ws.write(1, self.cursor[1]+1, 'Time')
            self.ws.write(1, self.cursor[1]+2, 'Status')
            self.ws.write(2, self.cursor[1], 'Gate')
            self.ws.write_merge(2, 2, self.cursor[1]+1, self.cursor[1]+2, 'reason')
            self.cursor[1] += 3
        self.cursor[0] = 3
        self.cursor[1] = 1
    def set_data(self, data):
        for item in data:
            self.ws.write(self.cursor[0], 0, item['bib'])
            self.ws.write(self.cursor[0], 1, item['ru_firstname']+' '+item['en_firstname'])
            self.ws.write(self.cursor[0], 2, item['global_rank'])
            self.ws.write(self.cursor[0], 3, item['result_time'])
            self.ws.write(self.cursor[0], 4, item['diff'])
            self.ws.write(self.cursor[0], 5, item['status'])
            self.cursor[1] = 6
            for result_item in item['results']:
                if result_item['status_id']==1:
                    self.ws.write(self.cursor[0], self.cursor[1], result_item['rank'])
                    self.cursor[1] += 1
                    self.ws.write(self.cursor[0], self.cursor[1], result_item['time'])
                    self.cursor[1] += 1
                    self.ws.write(self.cursor[0], self.cursor[1], result_item['status'])
                    self.cursor[1] += 1
                else:
                    self.ws.write(self.cursor[0], self.cursor[1], result_item['gate'])
                    self.cursor[1] += 1
                    self.ws.write_merge(self.cursor[0],
                                        self.cursor[0],
                                        self.cursor[1],
                                        self.cursor[1]+1,
                                        result_item['reason'])
                    self.cursor[1] += 2
            self.cursor[0] += 1


    def save(self, path):
        self.wb.save(path)


    def get_xls_file(self):
        output = io.BytesIO()
        self.wb.save(output)
        return output.getvalue()
