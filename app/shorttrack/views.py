from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from . import shorttrack
from ..decorators import admin_required
from flask_babel import gettext
import json
from .models import *
from .forms import *
from .. import db_shorttrack as db

@shorttrack.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    return render_template('shorttrack/index.html')

@shorttrack.route('/race/add/', methods=['GET', 'POST'])
@login_required
@admin_required
def race_add():
    form = RaceBaseForm()
    if request.method == 'POST' and form.validate_on_submit():
        race = Race(
            eventname=form.eventname.data,
            place=form.place.data,
            racedate=form.racedate.data,
            description=form.description.data
        )
        db.session.add(race)
        db.session.commit()
        return redirect(url_for('.race_list', _external=True))
    return render_template('shorttrack/form_page.html', title='Add race', form=form)

@shorttrack.route('/race/<int:race_id>/del/', methods=['GET', 'POST'])
@login_required
@admin_required
def race_del(race_id):
    db.session.delete(Race.query.get(race_id))
    flash('The race has deleted')
    return redirect(url_for('.race_list'))

@shorttrack.route('/race/<int:race_id>/base/edit/', methods=['GET', 'POST'])
@login_required
@admin_required
def race_edit_base(race_id):
    race = Race.query.get_or_404(race_id)
    form = RaceBaseForm()
    if form.validate_on_submit():
        race.eventname = form.eventname.data,
        race.place = form.place.data,
        race.racedate = form.racedate.data,
        race.description = form.description.data
        db.session.add(race)
        flash('The race has been updated.')
        return redirect(url_for('.race_list', _external=True))
    form.eventname.data = race.eventname
    form.place.data = race.place
    form.racedate.data = race.racedate
    form.description.data = race.description
    return render_template('shorttrack/form_page.html', title='Edit race', form=form)



@shorttrack.route('/race/', methods=['GET'])
@login_required
@admin_required
def race_list():
    race_list = Race.query.all()
    return render_template('shorttrack/static-tab/race_list.html', items=race_list)

@shorttrack.route('/race/<int:race_id>/edit/', methods=['GET', 'POST'])
@login_required
@admin_required
def race_edit(race_id):
    race = Race.query.get_or_404(race_id)
    form = RaceBaseForm()
    if form.validate_on_submit():
        race.eventname = form.eventname.data,
        race.place = form.place.data,
        race.racedate = form.racedate.data,
        race.description = form.description.data
        db.session.add(race)
        flash('The race has been updated.')
        return redirect(url_for('.race_list', _external=True))
    form.eventname.data = race.eventname
    form.place.data = race.place
    form.racedate.data = race.racedate
    form.description.data = race.description
    return render_template('shorttrack/race_view.html', race=race)
