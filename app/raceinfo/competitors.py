import pyexcel
from .. import db
from . import jsonencoder, raceinfo
from flask import request, render_template, redirect,url_for, flash
from .models import Competitor, RaceCompetitor, Gender, Category, Nation, Race, FisPoints

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
    for item in sheet.to_array()[1:]:
        print(item)
        try:
            gender = next(g for g in genders if g.fiscode == item[5])
            category = next(c for c in categorys if c.name == item[10])
            nation = next(n for n in nations if n.name == item[7])
            competitor = Competitor.query.filter_by(fiscode=str(item[0])).first()
            if competitor is None:
                competitor = Competitor(
                    fiscode=item[0],
                    ru_firstname=item[3],
                    en_firstname=item[1],
                    ru_lastname=item[4],
                    en_lastname=item[2],
                    gender_id=gender.id,
                    # справочник
                    birth=item[6],
                    nation_code_id=nation.id,
                    # справочник
                    # national_code=item[0],
                    NSA=item[0],
                    category_id=category.id,
                    # справочник
                )
            db.session.add(competitor)
            db.session.commit()
            race_competitor = RaceCompetitor.query.filter_by(competitor_id=competitor.id).first()
            if race_competitor is None:
                race_competitor = RaceCompetitor(
                    competitor_id=competitor.id,
                    race_id=race_id,
                    age_class=item[11],
                    chip=item[13],
                    bib=item[12],
                    fis_points=item[14]
                )
            else:
                race_competitor.chip = item[13]
                race_competitor.bib = item[12]
                race_competitor.age_class = item[11]
                race_competitor.fis_points = item[14]
            db.session.add(race_competitor)
            fis_point = FisPoints.query.filter(FisPoints.competitor_id==competitor.id, FisPoints.discipline_id==race.discipline_id).first()
            if fis_point is None:
                fis_point = FisPoints(
                    competitor_id=competitor.id,
                    discipline_id=race.discipline_id,
                    fispoint=item[14]
                )
                db.session.add(fis_point)
            else:
                fis_point.fispoint = item[14]
        except BaseException as e:
            flash('Ошибка добавления компетитора %s %s' % (item[1], item[2]))
    db.session.commit()
    return redirect(url_for('.edit_race_competitor', id=race_id))

@raceinfo.route('/upload', methods=['GET'])
def upload_form():
    return render_template('raceinfo/upload_table_form.html')