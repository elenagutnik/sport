from flask_login import login_required
from . import shorttrack
from ..decorators import admin_required

from .models import *
from .forms import *
from .. import db_shorttrack as db
import pyexcel
from .RunList import RunList, ExcelGenerator

from flask import request, render_template, redirect,url_for, flash, make_response
from .models import Competitor, Gender, Nation, Race


@shorttrack.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    db.create_all(bind='__all__')
    JuryType.insert()
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
            description=form.description.data,
            distance=form.distance.data,
            competitors_in_group=form.competitors_in_group.data
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
        race.distance = form.distance.data
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


@shorttrack.route('/race/<int:race_id>/competitors/', methods=['GET', 'POST'])
@login_required
@admin_required
def race_competitors_edit(race_id):
    race = Race.query.get_or_404(race_id)
    items = Competitor.query.filter(Competitor.race_id==race_id).all()
    return render_template('shorttrack/static-tab/competitors_race.html', race=race, competitors=items)

@shorttrack.route('/race/<int:race_id>/competitors/upload', methods=['POST'])
@login_required
@admin_required
def load_competitors(race_id):
    filename = request.files['list'].filename
    extension = filename.split(".")[-1]
    content = request.files['list'].read()
    sheet = pyexcel.get_sheet(file_type=extension, file_content=content)
    genders = Gender.query.all()
    nations = Nation.query.all()

    Competitor.query.filter(Competitor.race_id == race_id).delete()
    gender = None
    nation = None

    for item in sheet.to_array()[1:]:
        # try:
            if gender is None or gender.fiscode != item[5]:
                gender = next(g for g in genders if g.fiscode == item[5])
            if nation is None or nation.name != item[7]:
                nation = next(n for n in nations if n.name == item[7])

            competitor = Competitor(
                race_id=race_id,
                en_firstname=item[1],
                en_lastname=item[2],
                ru_firstname=item[3],
                ru_lastname=item[4],
                gender_id=gender.id,
                birth=item[6],
                nation_id=nation.id,
                club=item[8],
                transponder_1=item[9],
                transponder_2=item[10],
                points=item[11],

            )
            if len(item[12]) != 0:
                competitor.best_season_time=item[12]
            db.session.add(competitor)
            db.session.commit()
            if item[0] == '':
                competitor.bib = None
            else:
                competitor.bib = item[0]
            db.session.add(competitor)
            db.session.commit()

        # except BaseException as e:
        #     print(e)
        #     flash('Ошибка добавления компетитора %s %s' % (item[1], item[2]))
    return redirect(url_for('.race_competitors_edit', race_id=race_id, _external=True))


@shorttrack.route('/race/<int:race_id>/devices/', methods=['GET', 'POST'])
@login_required
@admin_required
def race_device(race_id):
    items = Device.query.filter(Device.race_id == race_id).all()
    return render_template('shorttrack/static-tab/devices_list.html', items=items, race_id=race_id)

@shorttrack.route('/race/<int:race_id>/run/', methods=['GET', 'POST'])
@login_required
@admin_required
def race_runs(race_id):
    items = RunInfo.query.filter(RunInfo.race_id == race_id).order_by(RunInfo.number.asc()).all()
    return render_template('shorttrack/static-tab/run_list.html', items=items, race_id=race_id)

@shorttrack.route('/race/<int:race_id>/devices/add', methods=['GET', 'POST'])
@login_required
@admin_required
def race_device_add(race_id):
    form = DeviceBaseForm()
    if form.validate_on_submit():
        device = Device(
            race_id=race_id,
            src_dev=form.src_dev.data,
            name=form.name.data
        )
        db.session.add(device)
        db.session.commit()
        flash('The device has been updated.')
        return redirect(url_for('.race_device', race_id=race_id, _external=True))
    return render_template('shorttrack/form_page.html', form=form, title='Add device')


@shorttrack.route('/race/<int:race_id>/devices/<int:device_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def race_device_edit(race_id, device_id):
    form = DeviceBaseForm()
    device = Device.query.get(device_id)
    if form.validate_on_submit():
        device.name = form.name.data
        device.src_dev = form.src_dev.data
        flash('The device has been updated.')
        return redirect(url_for('.race_device', race_id=race_id, _external=True))
    form.name.data = device.name
    form.src_dev.data = device.src_dev
    return render_template('shorttrack/form_page.html', form=form, title='Edit device')


@shorttrack.route('/race/<int:race_id>/devices/<int:device_id>/del', methods=['GET', 'POST'])
@login_required
@admin_required
def race_device_del(race_id, device_id):
    Device.query.filter(Device.id == device_id).delete()
    flash('The device has been updated.')
    return redirect(url_for('.race_device', race_id=race_id, _external=True))


@shorttrack.route('/race/<int:race_id>/run/<int:run_id>/orderlist', methods=['GET', 'POST'])
@login_required
@admin_required
def race_run_orderlist(race_id, run_id):
    сompetitors_list = db.session.query(Competitor, RunOrder). \
        join(RunOrder, RunOrder.competitor_id == Competitor.id, isouter=True). \
        filter(RunOrder.run_id == run_id, ). \
        order_by(RunOrder.group_id.asc(), RunOrder.order.asc()).all()

    treeView = {}
    for item in сompetitors_list:
        print(item[1].run_id, item[1].group_id)
        if item[1].group_id not in treeView.keys():
            treeView[item[1].group_id] = []
        treeView[item[1].group_id].append(item)

    return render_template('shorttrack/static-tab/runorder_list.html', race_id=race_id, item_list=treeView)


@shorttrack.route('/race/<int:race_id>/runlist/build', methods=['GET', 'POST'])
@login_required
@admin_required
def race_runlist_build(race_id):
    list = RunList(race_id)
    list.builder_1st_run()
    return redirect(url_for('.race_run_orderlist', race_id=race_id, run_id=list.run.id, _external=True))


@shorttrack.route('/race/<int:race_id>/run/<int:run_id>/results', methods=['GET', 'POST'])
@login_required
@admin_required
def xcl_run_results(race_id, run_id):
    required_run = RunInfo.query.filter(RunInfo.id == run_id).first()
    if required_run.endtime == None:
        flash('Невозможно сформировать результаты. Заезд не завершен ')
        return redirect(url_for('.race_runs', race_id=race_id, _external=True))
    else:
        wb = ExcelGenerator('results')
        wb.set_header()
        wb.set_data(race_id, run_id)
        response = make_response(wb.get_xls_file())
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers['Content-Disposition'] = 'inline; filename=xls_report.xls'

        return response


@shorttrack.route('/race/<int:race_id>/jury/', methods=['GET', 'POST'])
@login_required
@admin_required
def race_jury_list(race_id):
    jury_list = db.session.query(Jury, JuryType).join(JuryType).filter(Jury.race_id == race_id).all()
    return render_template('shorttrack/static-tab/jury_list.html',race_id=race_id, list=jury_list)


@shorttrack.route('/race/<int:race_id>/jury/add', methods=['GET', 'POST'])
@login_required
@admin_required
def race_jury_add(race_id):
    form = JuryBaseForm()
    form.jury_type_ref.choices = [(item.id, item.type) for item in
                               JuryType.query.all()]
    if form.validate_on_submit():
        jury = Jury(
            race_id=race_id,
            type_id=form.jury_type_ref.data,
            event_code=form.event_code.data,
            ru_lastname=form.ru_lastname.data,
            ru_firstname=form.ru_firstname.data,
            en_lastname=form.en_lastname.data,
            en_firstname=form.en_firstname.data
        )
        db.session.add(jury)
        db.session.commit()
        flash('The jury has been updated.')
        return redirect(url_for('.race_jury_list', race_id=race_id, _external=True))
    return render_template('shorttrack/form_page.html', form=form, title='Add jury')
