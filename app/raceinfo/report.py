from flask import make_response, render_template
import pdfkit
from .models import *

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
    jury = db.session.query(RaceJury, Jury, JuryType, Nation).\
        join(Jury, RaceJury.jury_id==Jury.id).\
        join(JuryType, JuryType.id==RaceJury.jury_function_id). \
        join(Nation, Jury.nation_id == Nation.id). \
        filter(RaceJury.race_id == race_id).all()

    # Course
    course = Course.query.filter(Course.race_id == race_id).first()
    course_setter = db.session.query(Coursetter, Nation).\
        join(Nation, Coursetter.nation_id == Nation.id).\
        filter(Coursetter.id == course.course_coursetter_id).\
        one()

    # Competitors
    competitors = db.session.query(Competitor, RaceCompetitor, Nation).\
        join(RaceCompetitor).\
        join(Nation, Nation.id == Competitor.nation_code_id).\
        filter(RaceCompetitor.race_id == race_id).\
        order_by(RaceCompetitor.bib).\
        all()


    html_render = render_template('reports/startlist.html',
                                  race=race,
                                  jury=jury,
                                  course=course,
                                  course_setter=course_setter,
                                  competitors=competitors)

    options = {
        'page-size': 'A4',
        'dpi': 400,
    }
    if isHTML=='true':
        return html_render
    else:
        pdf = pdfkit.from_string(html_render, False, options)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=report.pdf'
        return response
    # string_pdf=io.StringIO(pdf)
    # return send_file(pdf,mimetype='application/pdf',as_attachment=False)


