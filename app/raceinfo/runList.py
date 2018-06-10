from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from . import raceinfo
from ..decorators import admin_required

import json
from sqlalchemy import and_
from . import jsonencoder
from .models import *

@raceinfo.route('/startlist/run/<int:run_id>/get/', methods=['POST', 'GET'])
def startlist_get(run_id):
    data = json.dumps(db.session.query(Competitor,RaceCompetitor,RunOrder).join(RaceCompetitor).join(RunOrder).filter(RunOrder.run_id==run_id).order_by(RunOrder.order).all(), cls=jsonencoder.AlchemyEncoder)
    return data


def race_order_buld(race_id, current_run_id, current_run_number):
    race_type = db.session.query(Race.run_order_function).filter(Race.id == race_id).scalar()
    if race_type == 1:
        next_run_list_drop_out(race_id, current_run_id, current_run_number)
    elif race_type ==2:
        next_run_list_classical(race_id, current_run_id, current_run_number)
    return

@raceinfo.route('/race/<int:run_id>/order_list/buld', methods=['GET', 'POST'])
@login_required
@admin_required
def race_order_list(run_id):
    race = Race.query.filter_by(id=run_id).one()
    try:
        run = RunInfo.query.filter_by(race_id=run_id, number=1).one()
    except:
        return redirect(url_for('.race', id=run_id, _external=True))

    RunOrder.query.filter(RunOrder.run_id==run.id).delete()

    race_competitors = db.session.query(RaceCompetitor, FisPoints).\
        join(FisPoints, FisPoints.competitor_id == RaceCompetitor.competitor_id).\
        filter(RaceCompetitor.race_id == run_id, FisPoints.discipline_id==race.discipline_id).\
        order_by(FisPoints.fispoint.desc()).all()

    for i in range(len(race_competitors)):
        run_order = RunOrder(
            race_competitor_id=race_competitors[i][0].id,
            run_id=run.id,
            order=i+1
        )
        db.session.add(run_order)
    db.session.commit()
    orders_list = db.session.query(Competitor, RaceCompetitor, RunOrder, FisPoints).join(RaceCompetitor).join(RunOrder). join(FisPoints, FisPoints.competitor_id == RaceCompetitor.competitor_id).filter(
        RunOrder.run_id == run.id).order_by(RunOrder.order.asc()).all()
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

        race_competitors = db.session.query(RaceCompetitor, sub_query) \
            .outerjoin(sub_query, and_(sub_query.c.race_competitor_id == RaceCompetitor.id)) \
            .order_by(sub_query.c.filter_order.asc()) \
            .all()

        for i in range(len(race_competitors)):
            run_order = RunOrder(
                race_competitor_id=race_competitors[i][0].id,
                run_id=news_run.id,
                order=i + 1
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

        sub_query = db.session.query(ResultApproved.race_competitor_id, Status.filter_order).\
            join(Status).\
            filter(ResultApproved.run_id == current_run_id,
                   Status.id == 1).\
            subquery()

        race_competitors = db.session.query(RaceCompetitor, sub_query) \
            .join(sub_query, and_(sub_query.c.race_competitor_id == RaceCompetitor.id)) \
            .order_by(RaceCompetitor.time.desc()) \
            .all()

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
                order=i + 1
            )
            db.session.add(run_order)
        db.session.commit()
        return
    except:
        return

@raceinfo.route('/race/<int:race_id>/run/<int:run_id>/order_list/revers', methods=['GET', 'POST'])
def revers_first_15(race_id,run_id):
    run = RunInfo.query.filter(RunInfo.id == run_id).first()
    if run is not None and run.number !=1:
        order_list = sorted(RunOrder.query.filter(RunOrder.run_id == run.id).order_by(RunOrder.order.asc()).limit(15).all(), key=lambda item: item.order)
        for index, item in enumerate(reversed(order_list)):
            item.order = index + 1
            db.session.add(item)
        db.session.commit()
        return json.dumps(order_list, cls=jsonencoder.AlchemyEncoder)
    return json.dumps(dict([('error', "Недопустимый заезд")]))
