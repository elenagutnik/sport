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
    discipline = Discipline.query.filter(Discipline.id == Race.discipline_id, Race.id == id).one()

    if discipline.is_combination == True:
        form = EditRunInfoDisciplineForm()
        form.discipline_ref.choices = [(item.id, item.fiscode + '.' + item.en_name) for item in
                               Discipline.query.filter(Discipline.is_combination == None).all()]

    # elif discipline.is_parallel:
    #     form = EditRunInfoParallelForm()
    #     form.runtype_ref.choices = [(item.id, item.name) for item in
    #                                 RunType.query.filter(RunType.is_parralel == True).all()]
    else:
        form = EditRunInfoForm()


    if form.validate_on_submit():
        run_info = RunInfo(
            race_id=id,
            number=form.number.data,
            run_type_id=1
        )
        if discipline.is_combination == True:
            run_info.discipline_id = form.discipline_ref.data
        elif discipline.is_parallel:
            # run_info.run_type_id = form.runtype_ref.data
            second_run = RunInfo(
                race_id=id,
                number=form.number.data,
                run_type_id=1,
                is_second=True
            )
            db.session.add(second_run)
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
    if form.validate_on_submit():
        run_info.race_id = id
        run_info.number = form.number.data
        db.session.add(run_info)
        db.session.commit()
        if is_combination.is_combination == True:
            run_info.discipline_id = form.discipline_ref.data
        else:
            run_info.discipline_id = None
        flash('The run has been updated.')
        return redirect(url_for('.race_run', id=id, _external=True))
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



@raceinfo.route('/race/<int:id>/run/forerunners/build', methods=['GET', 'POST'])
@admin_required
def forerunner_run_create(id):
    forerunner_runs = db.session.query(RunInfo).filter(RunInfo.run_type_id == 3, RunInfo.race_id == id).order_by(
        RunInfo.number.asc()).first()

    if forerunner_runs is not None:
        return 'Невозможно сформировать заезд. Заезд уже начат '

    try:
        next_run = db.session.query(RunInfo).filter(RunInfo.starttime == None, RunInfo.race_id == id).order_by(RunInfo.number.asc()).limit(1).one()
        run_courses_list = RunCourses.query.filter(RunCourses.run_id == next_run.id).all()
    except:
        return 'Невозможно сформировать заезд'
    run = RunInfo(
        race_id=id,
        run_type_id=db.session.query(RunType.id).filter(RunType.is_forerunner == True).scalar(),
        starttime=datetime.now()
    )
    db.session.add(run)
    db.session.commit()
    for item in run_courses_list:
        forerunner_course = RunCourses(
            run_id=run.id,
            course_id=item.course_id
        )
        db.session.add(forerunner_course)
    db.session.commit()
    CourseForerunner_list = CourseForerunner.query.filter(CourseForerunner.course_id.in_([item.course_id for item in run_courses_list])).all()
    for item in CourseForerunner_list:
        tmp = RaceCompetitor(
            forerunner_id=item.id,
            race_id=id,
            run_id=run.id
        )
        db.session.add(tmp)
        db.session.commit()
        run_order = RunOrder(
            race_competitor_id=tmp.id,
            run_id=run.id,
            order=item.order,
            course_id=item.course_id
        )
        db.session.add(run_order)
    db.session.commit()

    start_list = db.session.query(Forerunner.en_lastname.label('en_lastname'),
                                  Forerunner.en_firstname.label('en_firstname'),
                                  RaceCompetitor.id.label('id'),
                                  RunOrder.order.label('order'),
                                  RunOrder.course_id.label('course_id')).\
        filter(RunOrder.run_id == run.id,
               RunOrder.race_competitor_id == RaceCompetitor.id,
               RaceCompetitor.forerunner_id == CourseForerunner.id,
               CourseForerunner.forerunner_id == Forerunner.id).all()
    response_start_list = []
    for item in start_list:
        response_start_list.append({
            'id': item.id,
            'en_lastname': item.en_lastname,
            'en_firstname': item.en_firstname,
            'order': item.order,
            'course_id': item.course_id,

        })
    return json.dumps(response_start_list)


@raceinfo.route('/race/<int:id>/run/forerunners/del', methods=['GET', 'POST'])
@admin_required
def forerunner_run_delete(id):
    db.session.query(RunInfo).filter(RunInfo.race_id == id, RunInfo.run_type_id == 3).delete()
    db.session.commit()
    return '0'


