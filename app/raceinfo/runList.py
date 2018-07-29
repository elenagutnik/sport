from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required
from . import raceinfo
from ..decorators import admin_required
import itertools
import json
from sqlalchemy import and_
from . import jsonencoder
from .models import *

@raceinfo.route('/startlist/run/<int:run_id>/get/', methods=['POST', 'GET'])
def startlist_get(run_id):
    data = json.dumps(db.session.query(Competitor, RaceCompetitor, RunOrder).join(RaceCompetitor).
                      join(RunOrder).filter(RunOrder.run_id == run_id).
                      order_by(RunOrder.order).all(),
                      cls=jsonencoder.AlchemyEncoder)
    return data


def race_order_buld(race_id, current_run_id, current_run_number):
    race = db.session.query(Race).filter(Race.id == race_id).first()
    discipline = Discipline.query.filter(Discipline.id == race.discipline_id).first()
    if discipline.is_parallel:
        run = db.session.query(RunInfo).filter(RunInfo.run_type_id == 4,
                                               RunInfo.number == 2, RunInfo.race_id == race_id).first()
        if run is not None:
            parallel_qualification_second_run_list(race_id, current_run_id, run)
        else:
            run = RunInfo.query.filter(RunInfo.race_id == race_id,
                                       RunType.id == 6,
                                       RunInfo.starttime is None).\
                order_by(RunInfo.number.asc()).limit(1).first()
            if run.is_second:
                pass
            else:
                buld_final_list(current_run_id, run)
    else:
        if race.run_order_function == 1:
            next_run_list_drop_out(race_id, current_run_id, current_run_number)
        elif race.run_order_function == 2:
            next_run_list_classical(race_id, current_run_id, current_run_number)
        elif race.run_order_function == 3:
            next_run_list_combination(race_id, current_run_id, current_run_number)
    return

@raceinfo.route('/race/<int:race_id>/order_list/build', methods=['GET', 'POST'])
@login_required
@admin_required
def race_order_list(race_id):
    race = Race.query.filter_by(id=race_id).one()

    discipline = Discipline.query.filter(Discipline.id == race.discipline_id).first()

    if discipline.is_parallel:
        try:
            run = RunInfo.query.filter_by(race_id=race_id, number=1, run_type_id=4).one()
        except:
            flash('Отсутсвует заезд, невозможно сформировать стартовый список')
            return redirect(url_for('.race', id=race_id, _external=True))

        RunOrder.query.filter(RunOrder.run_id == run.id).delete()
        parallel_start_list(run)
    else:
        try:
            run = RunInfo.query.filter_by(race_id=race_id, number=1).one()
        except:
            flash('Отсутсвует заезд, невозможно сформировать стартовый список')
            return redirect(url_for('.race', id=race_id, _external=True))

        RunOrder.query.filter(RunOrder.run_id == run.id).delete()
        try:
            course = RunCourses.query.filter(RunCourses.run_id==run.id).one()
        except:
            flash('Не указана трасса для заезда, невозможно сформировать стартовый список')
            return redirect(url_for('.race', id=race_id, _external=True))
        if discipline.is_combination == None:
            race_competitors = db.session.query(RaceCompetitor, RaceCompetitorFisPoints).\
                join(RaceCompetitorFisPoints, RaceCompetitorFisPoints.race_competitor_id == RaceCompetitor.id).\
                filter(RaceCompetitor.race_id == race_id, RaceCompetitorFisPoints.discipline_id == race.discipline_id).\
                order_by(RaceCompetitorFisPoints.fispoint.desc()).all()

        else:
            if run.discipline_id is None:
                flash("Ошибка формирования стартового листа: Не указана дисциплина для заезда", "error")
                return render_template('raceinfo/static-tab/order_list.html', race=race, run=run, competitors=[])

            sub_query = db.session.query(RaceCompetitorFisPoints).filter(
                RaceCompetitorFisPoints.discipline_id == run.discipline_id).subquery()

            race_competitors = db.session.query(RaceCompetitor, sub_query) \
                .outerjoin(sub_query, and_(sub_query.c.race_competitor_id == RaceCompetitor.id))\
                .filter(RaceCompetitor.race_id == race_id)\
                .all()

            race_competitors = sorted(race_competitors, key=lambda item: (item[4] is None, item[4]))

        for index, item in enumerate(race_competitors):
            run_order = RunOrder(
                race_competitor_id=item[0].id,
                run_id=run.id,
                order=index+1,
                course_id=course.course_id
            )
            db.session.add(run_order)
        db.session.commit()

    orders_list = db.session.query(Competitor, RaceCompetitor, RunOrder, RaceCompetitorFisPoints).\
        join(RaceCompetitor).\
        join(RunOrder).\
        join(RaceCompetitorFisPoints, and_(RaceCompetitorFisPoints.race_competitor_id == RaceCompetitor.id,
                                           RaceCompetitorFisPoints.discipline_id == run.discipline_id), isouter=True).\
        filter(RunOrder.run_id == run.id).order_by(RunOrder.order.asc()).all()
    return render_template('raceinfo/static-tab/order_list.html', race=race, run=run, competitors=orders_list)

@raceinfo.route('/race/order_list/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def race_order_list_edit():
    data = json.loads(request.args['data'])
    new_order = data['order_list']
    for order in new_order:
        runOrder = RunOrder.query.filter(RunOrder.run_id == data['run_id'],
                              RunOrder.id == order[0]).first()
        runOrder.order = order[1]
        runOrder.is_participate = order[2]
        db.session.add(runOrder)
    db.session.commit()
    return '', 200


def next_run_list_classical(race_id, current_run_id, current_run_number):
    try:
        news_run = db.session.query(RunInfo.id).filter(RunInfo.race_id == race_id,
                                                       RunInfo.number == current_run_number+ 1).one()
        RunOrder.query.filter(RunOrder.run_id == news_run.id).delete()

        sub_query = db.session.query(ResultApproved.race_competitor_id, Status.filter_order).join(Status).filter(
            ResultApproved.run_id == current_run_id).subquery()
        course = RunCourses.query.filter(RunCourses.run_id == news_run.id).first()

        race_competitors = db.session.query(RaceCompetitor, sub_query) \
            .outerjoin(sub_query, and_(sub_query.c.race_competitor_id == RaceCompetitor.id)) \
            .order_by(sub_query.c.filter_order.asc()) \
            .all()

        for i in range(len(race_competitors)):
            run_order = RunOrder(
                race_competitor_id=race_competitors[i][0].id,
                run_id=news_run.id,
                order=i + 1,
                course_id=course.course_id
            )
            db.session.add(run_order)
        db.session.commit()
        return
    except:
        return

@login_required
@admin_required
def next_run_list_drop_out(race_id, current_run_id, current_run_number):
    try:
        news_run = db.session.query(RunInfo.id).filter(RunInfo.race_id == race_id,
                                                       RunInfo.number == current_run_number + 1).one()
        RunOrder.query.filter(RunOrder.run_id == news_run.id).delete()

        course = RunCourses.query.filter(RunCourses.run_id==news_run.id).first()

        race_competitors = db.session.query(RaceCompetitor, ResultApproved).\
            join(ResultApproved).\
            filter(ResultApproved.run_id==current_run_id,
                   ResultApproved.status_id==1).\
            order_by(ResultApproved.time.desc()).\
            all()

        for i in range(len(race_competitors)):
            run_order = RunOrder(
                race_competitor_id=race_competitors[i][0].id,
                run_id=news_run.id,
                order=i + 1,
                course_id=course.course_id
            )
            db.session.add(run_order)
        db.session.commit()
        return
    except:
        return


def next_run_list_combination(race_id, current_run_id, current_run_number):
    try:
        news_run = db.session.query(RunInfo).filter(RunInfo.race_id == race_id,
                                                       RunInfo.number == current_run_number + 1).one()
        if news_run.discipline_id is None:
            return "Error: отсутсвиует дисциплина для заезда"

        RunOrder.query.filter(RunOrder.run_id == news_run.id).delete()

        course = RunCourses.query.filter(RunCourses.run_id == news_run.id).first()

        race_competitors = db.session.query(RaceCompetitor, ResultApproved, RaceCompetitorFisPoints.fispoint.label('fispoint')).\
            join(ResultApproved).\
            join(RaceCompetitorFisPoints, and_(RaceCompetitorFisPoints.race_competitor_id == RaceCompetitor.id,
                                               RaceCompetitorFisPoints.discipline_id == news_run.discipline_id), isouter=True).\
            filter(ResultApproved.run_id == current_run_id,
                   ResultApproved.status_id == 1).\
            all()
        race_competitors = sorted(race_competitors, key=lambda item: (item[2] is None, item[2]))
        for index, item in enumerate(race_competitors):
            run_order = RunOrder(
                race_competitor_id=item[0].id,
                run_id=news_run.id,
                order=index + 1,
                course_id=course.course_id
            )
            db.session.add(run_order)
        db.session.commit()
        return
    except:
        return

def parallel_start_list(run):
    # try:

        if run is not None:
            run_courses = db.session.query(RunCourses).filter(RunInfo.id==RunCourses.run_id,
                                                             RunInfo.id==run.id,
                                                             RunInfo.race_id==run.race_id).limit(2).all()
            if len(run_courses)!=2:
                flash('Ошибка формирования стартового списка: недостаточное количество трасс')
                return
            competitors_list_even = RaceCompetitor.query.filter(RaceCompetitor.race_id == run.race_id,
                                                                (RaceCompetitor.bib % 2) == 0).order_by(
                RaceCompetitor.bib.desc()).all()
            competitors_list_odd = RaceCompetitor.query.filter(RaceCompetitor.race_id == run.race_id,
                                                               (RaceCompetitor.bib % 2) != 0).order_by(
                RaceCompetitor.bib.asc()).all()
            for index, (odd_item, even_item) in enumerate(itertools.zip_longest(competitors_list_odd, competitors_list_even)):
                if odd_item is not None:
                    first_course_order = RunOrder(
                        race_competitor_id=odd_item.id,
                        run_id=run_courses[0].run_id,
                        order=index + 1,
                        course_id=run_courses[0].course_id
                    )
                    db.session.add(first_course_order)
                if even_item is not None:
                    second_course_order = RunOrder(
                        race_competitor_id=even_item.id,
                        run_id=run_courses[0].run_id,
                        order=index + 1,
                        course_id=run_courses[1].course_id
                    )
                    db.session.add(second_course_order)
            db.session.commit()
        return
    # except:
    #     return
def parallel_qualification_second_run_list(race_id, current_run_id, run):
    run_courses = db.session.query(RunCourses).filter(RunInfo.id==RunCourses.run_id,
                                                     RunInfo.id==run.id,
                                                     RunInfo.race_id==race_id).limit(2).all()
    if len(run_courses) != 2:
        return False
    first_course_order_list = db.session.query(RunOrder, ResultApproved).\
        join(ResultApproved,
             and_(ResultApproved.run_id == current_run_id,
                  ResultApproved.race_competitor_id == RunOrder.race_competitor_id,
                  ResultApproved.status_id == 1), isouter=True).\
        filter(RunInfo.id == RunOrder.run_id, RunInfo.id == current_run_id,
               RunOrder.course_id == run_courses[0].course_id).order_by(RunOrder.order.asc()).all()

    second_course_order_list = db.session.query(RunOrder, ResultApproved).\
        join(ResultApproved,
             and_(ResultApproved.run_id == current_run_id,
                  ResultApproved.race_competitor_id == RunOrder.race_competitor_id,
                  ResultApproved.status_id == 1), isouter=True).\
        filter(RunInfo.id == RunOrder.run_id, RunInfo.id == current_run_id,
               RunOrder.course_id == run_courses[1].course_id).order_by(RunOrder.order.asc()).all()
    run__list = []
    for first_item, second_item in itertools.zip_longest(first_course_order_list, second_course_order_list):
        temp_item = []
        if first_item is not None and first_item[1] is not None:
            temp_item.append(
                RunOrder(
                    race_competitor_id=first_item[0].race_competitor_id,
                    run_id=run.id,
                    course_id=run_courses[1].course_id)
            )

        if second_item is not None and second_item[1] is not None:
            temp_item.append(
                RunOrder(
                    race_competitor_id=second_item[0].race_competitor_id,
                    run_id=run.id,
                    course_id=run_courses[0].course_id)
            )
        if len(temp_item) != 0:
            run__list.append(temp_item)

    for index, items in enumerate(run__list):
        for item in items:
            item.order = index+1
            db.session.add(item)
    db.session.commit()
    return True

@raceinfo.route('/race/<int:race_id>/run/<int:run_id>/order_list/revers', methods=['GET', 'POST'])
def revers_first_15(race_id,run_id):
    run = RunInfo.query.filter(RunInfo.id == run_id).first()
    if run is not None and run.number != 1:
        order_list = sorted(RunOrder.query.filter(RunOrder.run_id == run.id).order_by(RunOrder.order.asc()).limit(15).all(), key=lambda item: item.order)
        for index, item in enumerate(reversed(order_list)):
            item.order = index + 1
            db.session.add(item)
        db.session.commit()
        return json.dumps(order_list, cls=jsonencoder.AlchemyEncoder)
    return json.dumps(dict([('error', "Недопустимый заезд")]))


def rebuild_startlist(run_id):
    # run_courses = RunCourses.query.filter(RunCourses.run_id==run_id).all()
    # RunOrder.query.filter(RunOrder.run_id == run_id, RunOrder.is_participate == False).delete()
    # for course in run_courses:
    #     start_list = RunOrder.query.filter(RunOrder.run_id == course.run_id).order_by(RunOrder.order.asc()).all()
    #     for index, item in enumerate(start_list):
    #         item.order = index+1
    pass

def buld_final_list(current_run_id, run):
    start_list = RunOrder.query.filter(RunOrder.run_id == current_run_id).all()
