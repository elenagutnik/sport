from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from . import raceinfo
from .. import db
from .models import *
from ..models import *
from ..decorators import admin_required
from .forms import *
from flask_babel import gettext

@raceinfo.route('/discipline/', methods=['GET', 'POST'])
@login_required
@admin_required
def discipline_list():
    disciplines = Discipline.query.all()
    return render_template('raceinfo/static-tab/discipline_list.html', disciplines=disciplines)

@raceinfo.route('/discipline/add/', methods=['GET', 'POST'])
@login_required
@admin_required
def discipline_add():
    form = EditDisciplineForm()
    if form.validate_on_submit():
        discipline = Discipline(fiscode = form.fiscode.data,
            ru_name = form.ru_name.data,
            en_name = form.en_name.data)
        db.session.add(discipline)
        flash('The discipline has been added.')
        return redirect(url_for('.discipline_list'))
    return render_template('raceinfo/static-tab/discipline_add.html', form=form)

@raceinfo.route('/discipline/<int:id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def discipline_edit(id):
    discipline = Discipline.query.get_or_404(id)
    form = EditDisciplineForm(discipline = discipline)
    if form.validate_on_submit():
        discipline.fiscode = form.fiscode.data
        discipline.ru_name = form.ru_name.data
        discipline.en_name = form.en_name.data
        db.session.add(discipline)
        flash('The discipline has been updated.')
        return redirect(url_for('.discipline_list'))
    form.fiscode.data = discipline.fiscode
    form.ru_name.data = discipline.ru_name
    form.en_name.data = discipline.en_name
    return render_template('raceinfo/static-tab/discipline_edit.html', form=form, discipline=discipline)

@raceinfo.route('/discipline/<int:id>/del/', methods=['GET', 'POST'])
@login_required
@admin_required
def discipline_del(id):
    discipline = Discipline.query.get_or_404(id)
    db.session.delete(discipline)
    flash('The discipline '+ discipline.ru_name +' has been deleted.')
    return redirect(url_for('.discipline_list'))

@raceinfo.route('/gender/', methods=['GET', 'POST'])
@login_required
@admin_required
def gender_list():
    genders = Gender.query.all()
    return render_template('raceinfo/static-tab/gender_list.html', genders=genders)

@raceinfo.route('/gender/add/', methods=['GET', 'POST'])
@login_required
@admin_required
def gender_add():
    form = EditGenderForm()
    if form.validate_on_submit():
        gender = Gender(fiscode = form.fiscode.data,
            ru_name = form.ru_name.data,
            en_name = form.en_name.data)
        db.session.add(gender)
        flash('The gender has been added.')
        return redirect(url_for('.gender_list'))
    return render_template('raceinfo/static-tab/gender_add.html', form=form)

@raceinfo.route('/gender/<int:id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def gender_edit(id):
    gender = Gender.query.get_or_404(id)
    form = EditGenderForm(gender = gender)
    if form.validate_on_submit():
        gender.fiscode = form.fiscode.data
        gender.ru_name = form.ru_name.data
        gender.en_name = form.en_name.data
        db.session.add(gender)
        flash('The gender has been updated.')
        return redirect(url_for('.gender_list'))
    form.fiscode.data = gender.fiscode
    form.ru_name.data = gender.ru_name
    form.en_name.data = gender.en_name
    return render_template('raceinfo/static-tab/gender_edit.html', form=form, gender=gender)

@raceinfo.route('/gender/<int:id>/del/', methods=['GET', 'POST'])
@login_required
@admin_required
def gender_del(id):
    gender = Gender.query.get_or_404(id)
    db.session.delete(gender)
    flash('The gender '+ gender.ru_name +' has been deleted.')
    return redirect(url_for('.gender_list'))

@raceinfo.route('/category/', methods=['GET', 'POST'])
@login_required
@admin_required
def category_list():
    items = Category.query.all()
    return render_template('raceinfo/static-tab/category_list.html', items=items)

@raceinfo.route('/category/add/', methods=['GET', 'POST'])
@login_required
@admin_required
def category_add():
    form = EditCategoryForm()
    if form.validate_on_submit():
        category = Category(
            name = form.name.data,
            description = form.description.data,
            level = form.level.data
            )
        db.session.add(category)
        flash('The category has been added.')
        return redirect(url_for('.category_list'))
    return render_template('raceinfo/static-tab/simpleform.html', form=form, title='Add category')

@raceinfo.route('/category/<int:id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def category_edit(id):
    category = Category.query.get_or_404(id)
    form = EditCategoryForm(category = category)
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        category.level = form.level.data
        db.session.add(category)
        flash('The category has been updated.')
        return redirect(url_for('.category_list'))
    form.name.data = category.name
    form.description.data = category.description
    form.level.data = category.level
    return render_template('raceinfo/static-tab/simpleform.html', form=category, category=category, title='Edit category')

@raceinfo.route('/category/<int:id>/del/', methods=['GET', 'POST'])
@login_required
@admin_required
def category_del(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    flash('The category '+ category.name +' has been deleted.')
    return redirect(url_for('.category_list'))

@raceinfo.route('/mark/', methods=['GET', 'POST'])
@login_required
@admin_required
def mark_list():
    items = Mark.query.all()
    return render_template('raceinfo/static-tab/mark_list.html', items=items)

@raceinfo.route('/mark/add/', methods=['GET', 'POST'])
@login_required
@admin_required
def mark_add():
    form = EditMarkForm()
    if form.validate_on_submit():
        mark = Mark(
            name = form.name.data,
            description = form.description.data
            )
        db.session.add(mark)
        flash('The mark has been added.')
        return redirect(url_for('.mark_list'))
    return render_template('raceinfo/static-tab/simpleform.html', form=form, title='Add Mark')

@raceinfo.route('/mark/<int:id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def mark_edit(id):
    mark = Mark.query.get_or_404(id)
    form = EditMarkForm(mark = mark)
    if form.validate_on_submit():
        mark.name = form.name.data
        mark.description = form.description.data
        db.session.add(mark)
        flash('The mark has been updated.')
        return redirect(url_for('.mark_list'))
    form.name.data = mark.name
    form.description.data = mark.description
    return render_template('raceinfo/static-tab/simpleform.html', form=form, mark=mark, title='Edit Mark')

@raceinfo.route('/mark/<int:id>/del/', methods=['GET', 'POST'])
@login_required
@admin_required
def mark_del(id):
    mark = Mark.query.get_or_404(id)
    db.session.delete(mark)
    flash('The mark '+ mark.ru_name +' has been deleted.')
    return redirect(url_for('.mark_list'))


@raceinfo.route('/nation/', methods=['GET', 'POST'])
@login_required
@admin_required
def nation_list():
    items = Nation.query.all()
    return render_template('raceinfo/static-tab/nation_list.html', items=items)

@raceinfo.route('/nation/add/', methods=['GET', 'POST'])
@login_required
@admin_required
def nation_add():
    form = EditNationForm()
    if form.validate_on_submit():
        nation = Nation(
            name = form.name.data,
            ru_description = form.ru_description.data,
            en_description = form.en_description.data
            )
        db.session.add(nation)
        flash('The nation has been added.')
        return redirect(url_for('.nation_list'))
    return render_template('raceinfo/static-tab/simpleform.html', form=form, title=gettext('Add Nation'))


@raceinfo.route('/nation/<int:id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def nation_edit(id):
    nation = Nation.query.get_or_404(id)
    form = EditNationForm(nation = nation)
    if form.validate_on_submit():
        nation.name = form.name.data
        nation.ru_description = form.ru_description.data
        nation.en_description = form.en_description.data
        db.session.add(nation)
        flash('The nation has been updated.')
        return redirect(url_for('.nation_list'))
    form.name.data = nation.name
    form.ru_description.data = nation.ru_description
    form.en_description.data = nation.en_description
    return render_template('raceinfo/static-tab/simpleform.html', form=form, obj=nation, title=gettext('Edit Nation'))

@raceinfo.route('/nation/<int:id>/del/', methods=['GET', 'POST'])
@login_required
@admin_required
def nation_del(id):
    nation = Nation.query.get_or_404(id)
    db.session.delete(nation)
    flash('The nation '+ nation.ru_name +' has been deleted.')
    return redirect(url_for('.nation_list'))


@raceinfo.route('/status/', methods=['GET', 'POST'])
@login_required
@admin_required
def status_list():
    items = Status.query.all()
    return render_template('raceinfo/static-tab/status_list.html', items=items)

@raceinfo.route('/status/add/', methods=['GET', 'POST'])
@login_required
@admin_required
def status_add():
    form = EditStatusForm()
    if form.validate_on_submit():
        status = Status(
            name = form.name.data,
            description = form.description.data
            )
        db.session.add(status)
        flash('The status has been added.')
        return redirect(url_for('.status_list'))
    return render_template('raceinfo/static-tab/status_add.html', form=form)

@raceinfo.route('/status/<int:id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def status_edit(id):
    status = Status.query.get_or_404(id)
    form = EditStatusForm(status = status)
    if form.validate_on_submit():
        status.name = form.name.data
        status.description = form.description.data
        db.session.add(status)
        flash('The status has been updated.')
        return redirect(url_for('.status_list'))
    form.name.data = status.name
    form.description.data = status.description
    return render_template('raceinfo/static-tab/simpleform.html', form=form, obj=status, title=gettext('Edit Status'))

@raceinfo.route('/status/<int:id>/del/', methods=['GET', 'POST'])
@login_required
@admin_required
def status_del(id):
    status = Status.query.get_or_404(id)
    db.session.delete(status)
    flash('The status '+ status.ru_name +' has been deleted.')
    return redirect(url_for('.status_list'))


@raceinfo.route('/tdrole/', methods=['GET', 'POST'])
@login_required
@admin_required
def tdrole_list():
    tdroles = TDRole.query.all()
    return render_template('raceinfo/static-tab/tdrole_list.html', tdroles=tdroles)

@raceinfo.route('/tdrole/add/', methods=['GET', 'POST'])
@login_required
@admin_required
def tdrole_add():
    form = EditTDRoleForm()
    if form.validate_on_submit():
        tdrole = TDRole(name = form.name.data)
        db.session.add(tdrole)
        flash('The tdrole has been added.')
        return redirect(url_for('.tdrole_list'))
    return render_template('raceinfo/static-tab/tdrole_add.html', form=form)

@raceinfo.route('/tdrole/<int:id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def tdrole_edit(id):
    tdrole = TDRole.query.get_or_404(id)
    form = EditTDRoleForm(tdrole = tdrole)
    if form.validate_on_submit():
        tdrole.name = form.name.data
        db.session.add(tdrole)
        flash('The tdrole has been updated.')
        return redirect(url_for('.tdrole_list'))
    form.name.data = tdrole.name
    return render_template('raceinfo/static-tab/tdrole_edit.html', form=form, tdrole=tdrole)

@raceinfo.route('/tdrole/<int:id>/del/', methods=['GET', 'POST'])
@login_required
@admin_required
def tdrole_del(id):
    tdrole = TDRole.query.get_or_404(id)
    db.session.delete(tdrole)
    flash('The tdrole '+ tdrole.ru_name +' has been deleted.')
    return redirect(url_for('.tdrole_list'))

@raceinfo.route('/td/', methods=['GET', 'POST'])
@login_required
@admin_required
def td_list():
    tds = TD.query.all()
    return render_template('raceinfo/static-tab/td_list.html', tds=tds)

@raceinfo.route('/td/add/', methods=['GET', 'POST'])
@login_required
@admin_required
def td_add():
    form = EditTDForm()
    if form.validate_on_submit():
        td = TD(
            ru_firstname = form.ru_firstname.data,
            en_firstname = form.en_firstname.data,
            ru_lastname = form.ru_lastname.data,
            en_lastname = form.en_lastname.data,
            ru_nation = form.ru_nation.data,
            en_nation = form.en_nation.data,
            tdnumber = form.tdnumber.data,
            #tdrole = int(form.tdrole.data)
            tdrole = TDRole.query.get(form.tdrole_ref.data)
        )
        db.session.add(td)
        flash('The td has been added.')
        return redirect(url_for('.td_list'))
    return render_template('raceinfo/static-tab/td_add.html', form=form)

@raceinfo.route('/td/<int:id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def td_edit(id):
    td = TD.query.get_or_404(id)
    form = EditTDForm(td = td)
    form.tdrole_ref.choices = [(tdrole.id, tdrole.name) for tdrole in TDRole.query.order_by(TDRole.name).all()]

    if form.validate_on_submit():
        td.ru_firstname = form.ru_firstname.data
        td.en_firstname = form.en_firstname.data
        td.ru_lastname = form.ru_lastname.data
        td.en_lastname = form.en_lastname.data
        td.ru_nation = form.ru_nation.data
        td.en_nation = form.en_nation.data
        td.tdnumber = form.tdnumber.data
        #td.tdrole_id = int(form.tdrole.data)
        td.tdrole = TDRole.query.get(form.tdrole_ref.data)

        db.session.add(td)
        flash(gettext('The td has been updated.'))
        return redirect(url_for('.td_list'))
    form.ru_firstname.data = td.ru_firstname
    form.en_firstname.data = td.en_firstname
    form.ru_lastname.data = td.ru_lastname
    form.en_lastname.data = td.en_lastname
    form.ru_nation.data = td.ru_nation
    form.en_nation.data = td.en_nation
    form.tdnumber.data = td.tdnumber
    form.tdrole_ref.data = td.tdrole_id

    return render_template('raceinfo/static-tab/td_edit.html', form=form, td=td)

@raceinfo.route('/td/<int:id>/del/', methods=['GET', 'POST'])
@login_required
@admin_required
def td_del(id):
    td = TD.query.get_or_404(id)
    db.session.delete(td)
    flash(gettext('The td '+ td.ru_name +' has been deleted.'))
    return redirect(url_for('.td_list'))

@raceinfo.route('/race/', methods=['GET'])
@admin_required
def race_list():
    items = Race.query.all();
    return render_template('raceinfo/race_list.html', items=items)

@raceinfo.route('/race/<int:id>', methods=['GET', 'POST'])
@admin_required
def race(id):
    race = Race.query.get_or_404(id)
    race.gender=Gender.query.get(race.gender_id)
    race.category=Category.query.get(race.category_id)
    race.discipline=Discipline.query.get(race.discipline_id)
    race.nation=Nation.query.get(race.nation_id)
    return render_template('raceinfo/race_view.html', race=race)

@raceinfo.route('/race/add', methods=['GET', 'POST'])
@admin_required
def race_add():
    form = EditRaceBase()
    if(current_user.lang == 'ru'):
        form.gender_ref.choices = [(item.id, item.fiscode + ' - ' + item.ru_name) for item in Gender.query.all()]
        form.discipline_ref.choices = [(item.id, item.fiscode + ' - ' + item.ru_name) for item in Discipline.query.all()]
        form.nation_ref.choices = [(item.id, item.name + ' - ' + item.ru_description) for item in Nation.query.all()]
    else:
        form.gender_ref.choices = [(item.id, item.fiscode + ' - ' + item.en_name) for item in Gender.query.all()]
        form.discipline_ref.choices = [(item.id, item.fiscode + ' - ' + item.en_name) for item in Discipline.query.all()]
        form.nation_ref.choices = [(item.id, item.name + ' - ' + item.en_description) for item in Nation.query.all()]
    form.category_ref.choices = [(item.id, item.name + ' - ' + item.description) for item in Category.query.all()]
    if form.validate_on_submit():
        race = Race(
            eventname = form.eventname.data,
            racedate = form.racedate.data,
            place = form.place.data,
            gender_id = form.gender_ref.data,
            nation_id = form.nation_ref.data,
            category_id = form.category_ref.data,
            discipline_id = form.discipline_ref.data,
            season = form.season.data,
            sector = form.sector.data,
            codex = form.codex.data,
            speedcodex = form.speedcodex.data,
            training = form.training.data,
        )
        db.session.add(race)
        db.session.commit()

        flash('The Race has been added.')
        return redirect(url_for('.race_list'))
    return render_template('raceinfo/static-tab/simpleform.html', form=form, title=gettext('Add Race'))

@raceinfo.route('/race/<int:id>/editbase', methods=['GET', 'POST'])
@admin_required
def race_editbase(id):
    race=Race.query.get_or_404(id)
    form = EditRaceBase(race=race)
    if(current_user.lang == 'ru'):
        form.gender_ref.choices = [(item.id, item.fiscode + ' - ' + item.ru_name) for item in Gender.query.all()]
        form.discipline_ref.choices = [(item.id, item.fiscode + ' - ' + item.ru_name) for item in Discipline.query.all()]
        form.nation_ref.choices = [(item.id, item.name + ' - ' + item.ru_description) for item in Nation.query.all()]
    else:
        form.gender_ref.choices = [(item.id, item.fiscode + ' - ' + item.en_name) for item in Gender.query.all()]
        form.discipline_ref.choices = [(item.id, item.fiscode + ' - ' + item.en_name) for item in Discipline.query.all()]
        form.nation_ref.choices = [(item.id, item.name + ' - ' + item.en_description) for item in Nation.query.all()]
    form.category_ref.choices = [(item.id, item.name + ' - ' + item.description) for item in Category.query.all()]
    if form.validate_on_submit():
        race.eventname = form.eventname.data
        race.racedate = form.racedate.data
        race.place = form.place.data
        race.gender_id = form.gender_ref.data
        race.nation_id = form.nation_ref.data
        race.category_id = form.category_ref.data
        race.discipline_id = form.discipline_ref.data
        race.season = form.season.data
        race.sector = form.sector.data
        race.codex = form.codex.data
        race.speedcodex = form.speedcodex.data
        race.training = form.training.data

        db.session.add(race)

        flash('The Race has been changed.')
        return redirect(url_for('.race_list'))
    return render_template('raceinfo/static-tab/simpleform.html', form=form, race=race, title=gettext('Edit Race - General properties'))
#  I have no idea, what do you want!!!!
# @raceinfo.route('/race/<int:id>/jury', methods=['GET', 'POST'])
# @admin_required
# def race_editjury(id):
#     race = Race.query.get_or_404(id)
#     form = EditRaceJury(race=race)
#     if(current_user.lang == 'ru'):
#         form.jury_chiefrace_nation_ref.choices = [(item.id, item.name + ' - ' + item.ru_description) for item in Nation.query.all()]
#         form.jury_referee_nation_ref.choices = [(item.id, item.name + ' - ' + item.ru_description) for item in Nation.query.all()]
#         form.jury_assistantreferee_nation_ref.choices = [(item.id, item.name + ' - ' + item.ru_description) for item in Nation.query.all()]
#         form.jury_chiefcourse_nation_ref.choices = [(item.id, item.name + ' - ' + item.ru_description) for item in Nation.query.all()]
#         form.jury_startreferee_nation_ref.choices = [(item.id, item.name + ' - ' + item.ru_description) for item in Nation.query.all()]
#         form.jury_chieftiming_nation_ref.choices = [(item.id, item.name + ' - ' + item.ru_description) for item in Nation.query.all()]
#     else:
#         form.jury_chiefrace_nation_ref.choices = [(item.id, item.name + ' - ' + item.en_description) for item in Nation.query.all()]
#         form.jury_referee_nation_ref.choices = [(item.id, item.name + ' - ' + item.en_description) for item in Nation.query.all()]
#         form.jury_assistantreferee_nation_ref.choices = [(item.id, item.name + ' - ' + item.en_description) for item in Nation.query.all()]
#         form.jury_chiefcourse_nation_ref.choices = [(item.id, item.name + ' - ' + item.en_description) for item in Nation.query.all()]
#         form.jury_startreferee_nation_ref.choices = [(item.id, item.name + ' - ' + item.en_description) for item in Nation.query.all()]
#         form.jury_chieftiming_nation_ref.choices = [(item.id, item.name + ' - ' + item.en_description) for item in Nation.query.all()]
#     if form.validate_on_submit():
#         race.jury_chiefrace_ru_lastname = form.jury_chiefrace_ru_lastname.data
#         race.jury_chiefrace_ru_firstname = form.jury_chiefrace_ru_firstname.data
#         race.jury_chiefrace_en_lastname = form.jury_chiefrace_en_lastname.data
#         race.jury_chiefrace_en_firstname = form.jury_chiefrace_en_firstname.data
#         race.jury_chiefrace_nation_ref = form.jury_chiefrace_nation_ref.data
#         race.jury_chiefrace_phonenbr = form.jury_chiefrace_phonenbr.data
#         race.jury_chiefrace_email = form.jury_chiefrace_email.data
#
#         race.jury_referee_ru_lastname = form.jury_referee_ru_lastname.data
#         race.jury_referee_ru_firstname = form.jury_referee_ru_firstname.data
#         race.jury_referee_en_lastname = form.jury_referee_en_lastname.data
#         race.jury_referee_en_firstname = form.jury_referee_en_firstname.data
#         race.jury_referee_nation_ref = form.jury_referee_nation_ref.data
#         race.jury_referee_phonenbr = form.jury_referee_phonenbr.data
#         race.jury_referee_email = form.jury_referee_email.data
#
#         race.jury_assistantreferee_ru_lastname = form.jury_assistantreferee_ru_lastname.data
#         race.jury_assistantreferee_ru_firstname = form.jury_assistantreferee_ru_firstname.data
#         race.jury_assistantreferee_en_lastname = form.jury_assistantreferee_en_lastname.data
#         race.jury_assistantreferee_en_firstname = form.jury_assistantreferee_en_firstname.data
#         race.jury_assistantreferee_nation_ref = form.jury_assistantreferee_nation_ref.data
#         race.jury_assistantreferee_phonenbr = form.jury_assistantreferee_phonenbr.data
#         race.jury_assistantreferee_email = form.jury_assistantreferee_email.data
#
#         race.jury_chiefcourse_ru_lastname = form.jury_chiefcourse_ru_lastname.data
#         race.jury_chiefcourse_ru_firstname = form.jury_chiefcourse_ru_firstname.data
#         race.jury_chiefcourse_en_lastname = form.jury_chiefcourse_en_lastname.data
#         race.jury_chiefcourse_en_firstname = form.jury_chiefcourse_en_firstname.data
#         race.jury_chiefcourse_nation_ref = form.jury_chiefcourse_nation_ref.data
#         race.jury_chiefcourse_phonenbr = form.jury_chiefcourse_phonenbr.data
#         race.jury_chiefcourse_email = form.jury_chiefcourse_email.data
#
#         race.jury_startreferee_ru_lastname = form.jury_startreferee_ru_lastname.data
#         race.jury_startreferee_ru_firstname = form.jury_startreferee_ru_firstname.data
#         race.jury_startreferee_en_lastname = form.jury_startreferee_en_lastname.data
#         race.jury_startreferee_en_firstname = form.jury_startreferee_en_firstname.data
#         race.jury_startreferee_nation_ref = form.jury_startreferee_nation_ref.data
#         race.jury_startreferee_phonenbr = form.jury_startreferee_phonenbr.data
#         race.jury_startreferee_email = form.jury_startreferee_email.data
#
#         race.jury_chieftiming_ru_lastname = form.jury_chieftiming_ru_lastname.data
#         race.jury_chieftiming_ru_firstname = form.jury_chieftiming_ru_firstname.data
#         race.jury_chieftiming_en_lastname = form.jury_chieftiming_en_lastname.data
#         race.jury_chieftiming_en_firstname = form.jury_chieftiming_en_firstname.data
#         race.jury_chieftiming_nation_ref = form.jury_chieftiming_nation_ref.data
#         race.jury_chieftiming_phonenbr = form.jury_chieftiming_phonenbr.data
#         race.jury_chieftiming_email = form.jury_chieftiming_email.data
#         db.session.add(race)
#
#         flash('The Race Jury has been changed.')
#         return redirect(url_for('.race_list'))
#     return render_template('raceinfo/jury.html', form=form, race=race, title=gettext('Edit Race - General properties'))
@raceinfo.route('/race/<int:id>/jury', methods=['GET', 'POST'])
@admin_required
def edit_race_jury(id):
    race_jury = db.session.query(RaceJury,Jury).\
        outerjoin(Jury,  RaceJury.jury_id==Jury.id).\
        filter(RaceJury.race_id==id).all()
    form = EditRaceJury()
    if current_user.lang =='ru':
        form.jury_ref.choices = [(item.id, item.ru_lastname + ' ' + item.ru_firstname) for item in Jury.query.all()]
        form.jury_function_ref.choices = [(item.id, item.ru_function) for item in Jury_function.query.all()]
    else:
        form.jury_ref.choices = [(item.id, item.en_lastname + ' ' + item.en_firstname) for item in Jury.query.all()]
        form.jury_function_ref.choices = [(item.id, item.en_function) for item in Jury_function.query.all()]

    if form.validate_on_submit():
        selected_jury = Jury.query.filter_by(id=form.jury_ref.data).one()
        raceJury = RaceJury(
            jury_id=selected_jury.id,
            race_id=id,
            jury_function_id=form.jury_function_ref.data,
            phonenbr=selected_jury.phonenbr,
            email=selected_jury.email
        )
        db.session.add(raceJury)
        db.session.commit()

    return render_template('raceinfo/static-tab/jury_race.html', form=form, jury=race_jury)
@raceinfo.route('/race/<int:race_id>/<int:jury_id>/del', methods=['GET', 'POST'])
@admin_required
def remove_race_jury(race_id,jury_id):
    db.session.delete(RaceJury.query.filter_by(id=jury_id).one())
    return redirect(url_for('.edit_race_jury', id=race_id))
@raceinfo.route('/jury_list/', methods=['GET', 'POST'])
@admin_required
def jury_list():
    j = Jury.query.all()
    return render_template('raceinfo/static-tab/jury_list.html', jury=j)



@raceinfo.route('/jury/add/', methods=['GET', 'POST'])
@admin_required
def jury_add():
    form = EditJuryBase()
    if (current_user.lang == 'ru'):
        form.nation_ref.choices = [(item.id, item.name + ' - ' + item.ru_description) for item in
                                                    Nation.query.all()]
    else:
        form.nation_ref.choices = [(item.id, item.name + ' - ' + item.en_description) for item in
                                                  Nation.query.all()]
    if form.validate_on_submit():
        jury = Jury(
            ru_lastname=form.ru_lastname.data,
            ru_firstname=form.ru_firstname.data,
            en_lastname=form.en_lastname.data,
            en_firstname=form.en_firstname.data,
            nation_id=form.nation_ref.data,
            phonenbr=form.phonenbr.data,
            email=form.email.dataс
        )
        db.session.add(jury)
        flash('The  Jury has been added.')
        return redirect(url_for('.jury_list'))
    return render_template('raceinfo/static-tab/jury_add.html', form=form)
