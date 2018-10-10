import pyexcel
import psycopg2
from .. import db
from . import raceinfo
from datetime import datetime
from flask import request, render_template, redirect, url_for, flash
from .models import Competitor, RaceCompetitor, Gender, Category, Nation, Race, FisPoints, RaceCompetitorFisPoints

@raceinfo.route('/race/<int:race_id>/competitors/upload', methods=['POST'])
def load_competitors(race_id):
    filename = request.files['list'].filename
    extension = filename.split(".")[-1]
    content = request.files['list'].read()
    sheet = pyexcel.get_sheet(file_type=extension, file_content=content)
    genders = Gender.query.all()
    categorys = Category.query.all()
    nations = Nation.query.all()
    race = Race.query.filter_by(id=race_id).one()

    gender = None
    category = None
    nation = None

    for item in sheet.to_array()[1:]:
        try:
            competitor = None
            if gender is None or gender.fiscode != item[6]:
                gender = next(g for g in genders if g.fiscode == item[6])
            if category is None or category.name != item[13]:
                category = next(c for c in categorys if c.name == item[12])
            if nation is None or nation.name != item[8]:
                nation = next(n for n in nations if n.name == item[8])

            if item[0] != '':
                competitor = Competitor.query.filter_by(fiscode=str(item[0])).first()
            if competitor is None:
                competitor = Competitor(
                    fiscode=item[0],
                    en_firstname=item[2],
                    en_lastname=item[3],
                    ru_firstname=item[4],
                    ru_lastname=item[5],
                    gender_id=gender.id,
                    birth=item[7],
                    nation_code_id=nation.id,
                    NSA=item[0],
                    category_id=category.id
                )
                db.session.add(competitor)
                db.session.commit()
            race_competitor = RaceCompetitor.query.filter(RaceCompetitor.competitor_id == competitor.id,
                                                          RaceCompetitor.race_id == race_id).first()
            if item[1]=='':
                bib = None
            else:
                bib = item[1]
            if race_competitor is None:
                race_competitor = RaceCompetitor(
                    competitor_id=competitor.id,
                    race_id=race_id,
                    bib=bib,
                    club=item[9],
                    transponder_1=item[10],
                    transponder_2=item[11],
                    age_class=calculate_age_class(competitor.birth, race.racedate)
                )
            else:
                race_competitor.bib = bib
                race_competitor.club = item[9]
                race_competitor.transponder_1 = item[10]
                race_competitor.transponder_2 = item[11]
            db.session.add(race_competitor)
            db.session.commit()

            for index in range(13, 25):
                if type(item[index]) is float or type(item[index]) is int:
                    discipline_id = ((sheet.to_array()[0][index]).split('-'))[0]
                    fis_point = FisPoints.query.filter(FisPoints.competitor_id == competitor.id,
                                                       FisPoints.discipline_id == discipline_id).first()
                    race_competitor_fispoints = RaceCompetitorFisPoints.query.filter(RaceCompetitorFisPoints.race_competitor_id==race_competitor.id,
                                                         RaceCompetitorFisPoints.discipline_id == discipline_id).first()
                    if fis_point is None:
                        fis_point = FisPoints(
                            competitor_id=competitor.id,
                            discipline_id=discipline_id,
                            point=item[index]
                        )
                    else:
                        fis_point.fispoint = item[index]

                    if race_competitor_fispoints is None:
                        race_competitor_fispoints = RaceCompetitorFisPoints(
                            race_competitor_id=race_competitor.id,
                            discipline_id=discipline_id,
                            point=item[index]
                        )
                    else:
                        race_competitor_fispoints.point = item[index]
                    db.session.add(fis_point)
                    db.session.add(race_competitor_fispoints)
                    db.session.commit()
        except BaseException as e:
            print(e)
            flash('Ошибка добавления компетитора %s %s' % (item[2], item[3]))
    return redirect(url_for('.edit_race_competitor', id=race_id, _external=True))

def calculate_age_class(birth, race_date):
    middle = datetime(int(datetime.now().year), 7, 1).date()
    competitor_age = race_date.year - birth.year
    if race_date.date() < middle:
        age_classes = {'U14': [13, 14], 'U16': [15, 16], 'U18': [17, 18], 'U21': [19, 21]}
    else:
        age_classes = {'U14': [12, 13], 'U16': [14, 15], 'U18': [16, 17], 'U21': [18, 20]}
    for age_class in age_classes:
        if competitor_age >= age_classes[age_class][0] and competitor_age <= age_classes[age_class][1]:
            return age_class




@raceinfo.route('/upload', methods=['GET'])
def upload_form():
    return render_template('raceinfo/upload_table_form.html')