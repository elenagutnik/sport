from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user
from . import raceinfo
from ..decorators import admin_required
from .forms import *
import json
from .models import *
from . import jsonencoder
from .runList import race_order_buld, rebuild_startlist
from sqlalchemy import cast, DATE
from sqlalchemy import func


@raceinfo.route('/race/<int:id>/run/<int:run_id>/del', methods=['GET', 'POST'])
@admin_required
def race_course_run_del(id,run_id):
    run_info = RunInfo.query.get_or_404(run_id)
    db.session.delete(run_info)
    flash('The run has been deleted.')
    return redirect(url_for('.race_run', id=id,_external=True))



@raceinfo.route('/race/<int:id>/run/add', methods=['GET', 'POST'])
@admin_required
def race_run_add(id):
    is_combination = db.session.query(Discipline.is_combination.label('is_combination')).\
        filter(Discipline.id == Race.discipline_id, Race.id == id).one()

    if is_combination.is_combination == True:
        form = EditRunInfoDisciplineForm()
        form.discipline_ref.choices = [(item.id, item.fiscode + '.' + item.en_name) for item in
                               Discipline.query.filter(Discipline.is_combination == None).all()]
    else:
        form = EditRunInfoForm()

    if current_user.lang == 'ru':
        form.course_ref.choices = [(item.id, item.ru_name ) for item in
                                   Course.query.filter_by(race_id=id).all()]
    else:

        form.course_ref.choices = [(item.id, item.ru_name ) for item in
                                   Course.query.filter_by(race_id=id).all()]
    if form.validate_on_submit():
        run_info = RunInfo(
            race_id=id,
            course_id=form.course_ref.data,
            number=form.number.data,
        )
        if is_combination.is_combination == True:
            run_info.discipline_id = form.discipline_ref.data
        db.session.add(run_info)
        db.session.commit()
        flash('The run has been added.')
        return redirect(url_for('.race_run', id=id, _external=True))
    return render_template('raceinfo/static-tab/form_page.html', title='Add run', form=form)

@raceinfo.route('/race/<int:id>/run/<int:run_id>/edit', methods=['GET', 'POST'])
@admin_required
def race_run_edit(id, run_id):
    is_combination = db.session.query(Discipline.is_combination.label('is_combination')).\
        filter(Discipline.id == Race.discipline_id, Race.id == id).one()

    if is_combination.is_combination == True:
        form = EditRunInfoDisciplineForm()
        form.discipline_ref.choices = [(item.id, item.fiscode + '.' + item.en_name) for item in
                               Discipline.query.filter(Discipline.is_combination == None).all()]
    else:
        form = EditRunInfoForm()
    run_info = RunInfo.query.filter_by(id=run_id).one()

    if current_user.lang == 'ru':
        form.course_ref.choices = [(item.id, item.ru_name) for item in
                                   Course.query.filter_by(race_id=id).all()]
    else:
        form.course_ref.choices = [(item.id, item.ru_name) for item in
                                   Course.query.filter_by(race_id=id).all()]
    if form.validate_on_submit():
        run_info.race_id = id
        run_info.course_id = form.course_ref.data
        run_info.number = form.number.data
        db.session.add(run_info)
        db.session.commit()
        if is_combination.is_combination == True:
            run_info.discipline_id = form.discipline_ref.data
        else:
            run_info.discipline_id = None
        flash('The run has been updated.')
        return redirect(url_for('.race_run', id=id, _external=True))

    form.course_ref.data = run_info.course_id
    if is_combination.is_combination == True:
        form.discipline_ref.data = run_info.discipline_id
    form.number.data = run_info.number
    return render_template('raceinfo/static-tab/form_page.html', title='Edit run', form=form)



@raceinfo.route('/race/<int:id>/run/<int:run_id>/start', methods=['GET', 'POST'])
@admin_required
def race_course_run_start(id, run_id):
    try:
        rebuild_startlist(run_id)
        is_combination = db.session.query(Discipline.is_combination).filter(Discipline.id == Race.discipline_id,
                                                           Race.id == id).one()

        run_info = RunInfo.query.get_or_404(run_id)
        if is_combination.is_combination is True and run_info.discipline_id is None:
            return 'fail', 200
        run_info.starttime = datetime.now()
        db.session.add(run_info)
        db.session.commit()
    except:
        return 'fail', 200
    return json.dumps({'start_time': str(run_info.starttime)})
#
@raceinfo.route('/race/<int:id>/run/<int:run_id>/stop', methods=['GET', 'POST'])
@admin_required
def race_course_run_stop(id,run_id):
    run_info = RunInfo.query.get_or_404(run_id)
    run_info.endtime = datetime.now()
    db.session.add(run_info)

    race_order_buld(id, run_id, run_info.number)

    return json.dumps({'stop_time': str(run_info.endtime)})



@raceinfo.route('/race/<int:id>/run/forerunner/build', methods=['GET', 'POST'])
@admin_required
def forerunner_run_create(id):
    nextRun = db.session.query(RunInfo).filter(RunInfo.starttime == None, RunInfo.race_id==id).order_by(RunInfo.number.asc()).first()

    run = RunInfo(
        course_id=nextRun.course_id,
        race_id=id,
        run_type=RunType.forerunner,
        starttime=datetime.now()
    )
    db.session.add(run)
    db.session.commit()
    CourseForerunner_list = CourseForerunner.query.filter(CourseForerunner.course_id == run.course_id).all()
    for item in CourseForerunner_list:
        tmp = RaceCompetitor(
            forerunner_id=item.forerunner_id,
            race_id=id,
            run_id=run.id
        )
        db.session.add(tmp)
        db.session.commit()
        run_order = RunOrder(
            race_competitor_id=tmp.id,
            run_id=run.id,
            order=item.order
        )
        db.session.add(run_order)
    db.session.commit()
    return ''


@raceinfo.route('/race/<int:id>/run/<int:run_id>/forerunners/del', methods=['GET', 'POST'])
@admin_required
def forerunner_run_delete(id, run_id):
    db.session.delete(RunInfo.query.get(run_id))
    return '0'


