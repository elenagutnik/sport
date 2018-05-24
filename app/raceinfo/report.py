from flask import make_response, render_template
import pdfkit
from .models import *
import tempfile

import json
from . import raceinfo


@raceinfo.route('/race/report')
def Report():
    return render_template('reports/startlist.html')

@raceinfo.route('/race/<int:race_id>/report/ishtml/<isHTML>')
def Report_show(race_id,isHTML):

    # Race
    race = db.session.query(Race, Gender, Category, Discipline, Nation).\
        join(Gender). \
        join(Category). \
        join(Discipline). \
        join(Nation, Race.nation_id==Nation.id).\
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
                                        Nation.name.label('name'))\
        .filter(Coursetter.id == course.course_coursetter_id,
                Coursetter.nation_id == Nation.id).one()

    # Competitors
    competitors = db.session.query(Competitor, RaceCompetitor, Nation).\
        join(RaceCompetitor).\
        join(Nation, Nation.id == Competitor.nation_code_id).\
        filter(RaceCompetitor.race_id == race_id).\
        order_by(RaceCompetitor.bib).\
        all()

    number_of_NOCs = db.session.query(Nation).distinct(Nation.name).\
        filter(RaceCompetitor.race_id==race_id,
               RaceCompetitor.competitor_id==Competitor.id,
               Competitor.nation_code_id==Nation.id).\
        count()
    forerunners = db.session.query(Forerunner.en_firstname.label('en_firstname'),
                                   Forerunner.en_lastname.label('en_lastname'),
                                   CourseForerunner.order.label('order'),
                                   Nation.name.label('name')).\
        filter(Forerunner.nation_id == Nation.id,
               CourseForerunner.forerunner_id == Forerunner.id,
               CourseForerunner.course_id == course.id).\
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
        '--header-spacing': '30',
        '--margin-top': '40'
    }
    add_pdf_header(options, race)
    if isHTML=='true':
        return html_render
    else:

        pdf = pdfkit.from_string(html_render, False, options)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=report.pdf'
        return response

def add_pdf_header(options, race):
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as header:
        options['--header-html'] = header.name
        header.write(
            render_template('reports/header.html', race=race).encode('utf-8')
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
    qlf_list = []
    disqlf_list = []
    for item in race_competitors:
        if item[0].status_id == 1:
            qlf_item={
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
        else: #Did not start
            disqlf_list.append({
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
    qlf_list=sorted(qlf_list, key= lambda item: item['rank'])
    return render_template('reports/results.html',
                           qlf_competitors=qlf_list,
                           disqlf_competitors=qlf_list,
                           course=course,
                           course_setter=course_setter, jury=jury)

