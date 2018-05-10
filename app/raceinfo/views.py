from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from . import raceinfo
from ..decorators import admin_required
from .forms import *
from flask_babel import gettext
import json
from sqlalchemy import and_
from . import jsonencoder


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
        return redirect(url_for('.discipline_list', _external=True))
    return render_template('raceinfo/static-tab/discipline_add.html', form=form)

@raceinfo.route('/discipline/<int:id>/edit', methods=['GET', 'POST'])
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
        return redirect(url_for('.discipline_list',_external=True))
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
    return redirect(url_for('.discipline_list',_external=True))

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
        return redirect(url_for('.gender_list',_external=True))
    return render_template('raceinfo/static-tab/gender_add.html', form=form)

@raceinfo.route('/gender/<int:id>/edit', methods=['GET', 'POST'])
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
        return redirect(url_for('.gender_list',_external=True))
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
    return redirect(url_for('.gender_list',_external=True))

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
        return redirect(url_for('.category_list',_external=True))
    return render_template('raceinfo/static-tab/simpleform.html', form=form, title='Add category')

@raceinfo.route('/category/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def category_edit(id):
    category = Category.query.get_or_404(id)
    form = EditCategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        category.level = form.level.data
        db.session.add(category)
        flash('The category has been updated.')
        return redirect(url_for('.category_list',_external=True))
    form.name.data = category.name
    form.description.data = category.description
    form.level.data = category.level
    return render_template('raceinfo/static-tab/simpleform.html', form=form, category=category, title='Edit category')

@raceinfo.route('/category/<int:id>/del/', methods=['GET', 'POST'])
@login_required
@admin_required
def category_del(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    flash('The category '+ category.name +' has been deleted.')
    return redirect(url_for('.category_list',_external=True))

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
        return redirect(url_for('.mark_list',_external=True))
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
        return redirect(url_for('.mark_list',_external=True))
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
    return redirect(url_for('.mark_list',_external=True))


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
        return redirect(url_for('.nation_list',_external=True))
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
        return redirect(url_for('.nation_list',_external=True))
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
    flash('The nation has been deleted.')
    return redirect(url_for('.nation_list',_external=True))


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
        return redirect(url_for('.status_list',_external=True))
    return render_template('raceinfo/static-tab/status_add.html', form=form)

@raceinfo.route('/status/<int:id>/edit', methods=['GET', 'POST'])
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
        return redirect(url_for('.status_list',_external=True))
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
    return redirect(url_for('.status_list',_external=True))


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
        return redirect(url_for('.tdrole_list',_external=True))
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
        return redirect(url_for('.tdrole_list',_external=True))
    form.name.data = tdrole.name
    return render_template('raceinfo/static-tab/tdrole_edit.html', form=form, tdrole=tdrole)

@raceinfo.route('/tdrole/<int:id>/del/', methods=['GET', 'POST'])
@login_required
@admin_required
def tdrole_del(id):
    tdrole = TDRole.query.get_or_404(id)
    db.session.delete(tdrole)
    flash('The tdrole '+ tdrole.ru_name +' has been deleted.')
    return redirect(url_for('.tdrole_list',_external=True))

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
        return redirect(url_for('.td_list',_external=True))
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
        return redirect(url_for('.td_list',_external=True))
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
    return redirect(url_for('.td_list',_external=True))

@raceinfo.route('/race/', methods=['GET'])
@admin_required
def race_list():
    items = Race.query.all()
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


@raceinfo.route('/race/<int:id>/additional', methods=['GET', 'POST'])
@admin_required
def additional_params(id):
    race  = Race.query.get_or_404(id)
    form = EditRaceAdditional()
    if form.validate_on_submit():
        race.usedfislist = form.usedfislist.data
        race.appliedpenalty = form.appliedpenalty.data
        race.calculatedpenalty = form.calculatedpenalty.data
        race.fvalue = form.fvalue.data
        race.timingby = form.timingby.data
        race.dataprocessingby = form.dataprocessingby.data
        race.softwarecompany = form.softwarecompany.data
        race.softwarename = form.softwarename.data
        race.softwareversion = form.softwareversion.data
        db.session.add(race)
        db.session.commit()
        return redirect(url_for('.race', id=id,_external=True))
    form.usedfislist.data = race.usedfislist
    form.appliedpenalty.data = race.appliedpenalty
    form.calculatedpenalty.data = race.calculatedpenalty
    form.fvalue.data = race.fvalue
    form.timingby.data = race.timingby
    form.dataprocessingby.data = race.dataprocessingby
    form.softwarecompany.data = race.softwarecompany
    form.softwarename.data = race.softwarename
    form.softwareversion.data = race.softwareversion
    return render_template('raceinfo/static-tab/form_page.html', title='Race additional parameters', race=race, form=form)


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
    form.result_method_ref.choices=[(item.id, item.name) for item in ResultFunction.query.all()]
    if form.validate_on_submit():
        race = Race(
            gender_id = form.gender_ref.data,
            nation_id = form.nation_ref.data,
            isTeam = form.race_type.data,
            category_id = form.category_ref.data,
            discipline_id = form.discipline_ref.data,
            result_function = form.result_method_ref.data
        )
        if form.eventname.data != "":
            race.eventname = form.eventname.data
        if form.racedate.data != "":
            race.racedate = form.racedate.data
        if form.place.data != "":
            race.place = form.place.data
        if form.season.data != "":
            race.season = form.season.data
        if form.sector.data != "":
            race.sector = form.sector.data
        if form.codex.data != "":
            race.codex = form.codex.data
        if form.speedcodex.data != "":
            race.speedcodex = form.speedcodex.data
        if form.training.data != "":
            race.training = form.training.data
        db.session.add(race)
        db.session.commit()

        flash('The Race has been added.')
        return redirect(url_for('.race_list',_external=True))
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
    form.result_method_ref.choices=[(item.id, item.name) for item in ResultFunction.query.all()]

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
        race.result_function = form.result_method_ref.data

        db.session.add(race)

        flash('The Race has been changed.')
        return redirect(url_for('.race_list',_external=True))
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

# !!!!!!!!!!!!!!!!!!

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

    return render_template('raceinfo/static-tab/jury_race.html', title='Jury list', form=form, jury=race_jury)

@raceinfo.route('/race/<int:race_id>/jury/<int:jury_id>/del', methods=['GET', 'POST'])
@admin_required
def remove_race_jury(race_id,jury_id):
    db.session.delete(RaceJury.query.filter_by(id=jury_id).one())
    return redirect(url_for('.edit_race_jury', id=race_id,_external=True))

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
            email=form.email.data
        )
        db.session.add(jury)
        flash('The  Jury has been added.')
        return redirect(url_for('.jury_list',_external=True))
    return render_template('raceinfo/static-tab/jury_add.html', form=form)

@raceinfo.route('/jury_list/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def jury_edit(id):
    jury=  Jury.query.get_or_404(id)
    form = EditJuryBase()

    if (current_user.lang == 'ru'):
        form.nation_ref.choices = [(item.id, item.name + ' - ' + item.ru_description) for item in
                                                    Nation.query.all()]
    else:
        form.nation_ref.choices = [(item.id, item.name + ' - ' + item.en_description) for item in
                                                  Nation.query.all()]
    if form.validate_on_submit():
        jury.ru_lastname=form.ru_lastname.data,
        jury.ru_firstname=form.ru_firstname.data,
        jury.en_lastname=form.en_lastname.data,
        jury.en_firstname=form.en_firstname.data,
        jury.nation_id=form.nation_ref.data,
        jury.phonenbr=form.phonenbr.data,
        jury.email=form.email.data

        db.session.add(jury)
        flash('The  Jury has been updated.')
        return redirect(url_for('.jury_list',_external=True))
    form.ru_lastname.data = jury.ru_lastname
    form.ru_firstname.data = jury.ru_firstname
    form.en_lastname.data = jury.en_lastname
    form.en_firstname.data = jury.en_firstname
    form.nation_ref.data = jury.nation_id
    form.phonenbr.data = jury.phonenbr
    form.email.data = jury.email
    return render_template('raceinfo/static-tab/form_page.html',title='Edit jury', form=form)


@raceinfo.route('/jury_list/<int:id>/del', methods=['GET', 'POST'])
@admin_required
def jury_del(id):
    jury=  Jury.query.get_or_404(id)
    db.session.delete(jury)
    flash('The jury has been deleted.')
    return redirect(url_for('.jury_list', _external=True))

@raceinfo.route('/competitor/', methods=['GET', 'POST'])
@login_required
@admin_required
def competitor_list():
    competitor = Competitor.query.all()
    return render_template('raceinfo/static-tab/competitors_list.html', competitors=competitor)

@raceinfo.route('/competitor/add/', methods=['GET', 'POST'])
@login_required
@admin_required
def competitor_add():
    form = EditCompetitorBase()
    if (current_user.lang == 'ru'):
        form.nation_code_ref.choices = [(item.id, item.name + ' - ' + item.ru_description) for item in
                                                  Nation.query.all()]
        form.gender_ref.choices = [(item.id, item.ru_name) for item in
                                   Gender.query.all()]
    else:
        form.nation_code_ref.choices = [(item.id, item.name + ' - ' + item.en_description) for item in
                                                  Nation.query.all()]
        form.gender_ref.choices = [(item.id, item.en_name) for item in
                                   Gender.query.all()]
    form.category_ref.choices = [(item.id, item.name) for item in
                                Category.query.all()]
    if form.validate_on_submit():
        competitor = Competitor(
            fiscode = form.fis_code.data,
            ru_firstname = form.ru_firstname.data,
            en_firstname = form.en_firstname.data,
            ru_lastname = form.ru_lastname.data,
            en_lastname = form.en_lastname.data,
            gender_id = form.gender_ref.data,
            birth=form.birth.data,
            nation_code_id=form.nation_code_ref.data,
            national_code=form.national_code.data,
            category_id=form.category_ref.data,
        )
        if form.NSA.data != "":
            competitor.NSA = form.NSA.data
        db.session.add(competitor)
        if form.is_ajax.data is None or form.is_ajax.data == "":
            flash('The competitor has been added.')
            return redirect(url_for('.competitor_list',_external=True))
        else:
            return json.dumps(competitor, cls=jsonencoder.AlchemyEncoder)
    tmp = form.is_ajax
    if form.is_ajax.data is None or form.is_ajax.data =="":
        return render_template('raceinfo/static-tab/comptitors_add.html', form=form)
    else:
        form_rener = render_template('raceinfo/static-tab/form_render.html', form=form)
        return json.dumps(dict(form=form_rener, result='form'))

@raceinfo.route('/competitor/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def competitor_edit(id):
    competitor = Competitor.query.get_or_404(id)
    form = EditCompetitorBase(competitor = competitor)
    if (current_user.lang == 'ru'):
        form.nation_code_ref.choices = [(item.id, item.name + ' - ' + item.ru_description) for item in
                                                  Nation.query.all()]
        form.gender_ref.choices = [(item.id, item.ru_name) for item in
                                   Gender.query.all()]
    else:
        form.nation_code_ref.choices = [(item.id, item.name + ' - ' + item.en_description) for item in
                                                  Nation.query.all()]
        form.gender_ref.choices = [(item.id, item.en_name) for item in
                                   Gender.query.all()]
    form.category_ref.choices = [(item.id, item.name) for item in
                                Category.query.all()]
    if form.validate_on_submit():
        competitor.fiscode=form.fis_code.data
        competitor.ru_firstname=form.ru_firstname.data
        competitor.en_firstname=form.en_firstname.data
        competitor.ru_lastname=form.ru_lastname.data
        competitor.en_lastname=form.en_lastname.data
        competitor.gender_id=form.gender_ref.data

        competitor.birth=form.birth.data
        competitor.nation_code_id=form.nation_code_ref.data

        competitor.national_code=form.national_code.data
        competitor.NSA=form.NSA.data
        competitor.category_id=form.category_ref.data

        db.session.add(competitor)
        flash('The competitor has been updated.')
        return redirect(url_for('.competitor_list',_external=True))
    form.fis_code.data = competitor.fiscode
    form.ru_firstname.data = competitor.ru_firstname
    form.en_firstname.data = competitor.en_firstname
    form.ru_lastname.data = competitor.ru_lastname
    form.en_lastname.data = competitor.en_lastname
    form.gender_ref.data = competitor.gender_id
    form.birth.dat = competitor.birth
    form.nation_code_ref.data = competitor.nation_code_id

    form.national_code.data = competitor.national_code
    form.NSA.data = competitor.NSA
    form.category_ref.data = competitor.category_id

    return render_template('raceinfo/static-tab/comptitors_add.html', form=form, competitor=competitor)

@raceinfo.route('/competitor/<int:id>/del/', methods=['GET', 'POST'])
@login_required
@admin_required
def competitor_del(id):
    competitor = Competitor.query.get_or_404(id)
    db.session.delete(competitor)
    flash('The competitor has been deleted.')
    return redirect(url_for('.competitor_list',_external=True))



@raceinfo.route('/race/<int:id>/competitors', methods=['GET', 'POST'])
@admin_required
def edit_race_competitor(id):
    race = Race.query.filter_by(id=id).one()
    add_competitor_form = EditCompetitorBase()
    add_competitor_form.is_ajax.data = True
    if race.isTeam:
        form = EditRaceCompetitorTeamForm()

        race_competitors = db.session.query(RaceCompetitor, Competitor). \
            outerjoin(Competitor, RaceCompetitor.competitor_id == Competitor.id). \
            filter(RaceCompetitor.race_id == id, RaceCompetitor.team_id==request.args.get('team_id')).all()

        form.team_ref.data = request.args.get('team_id')

    else:
        form = EditRaceCompetitor()
        race_competitors = db.session.query(RaceCompetitor, Competitor). \
            outerjoin(Competitor, RaceCompetitor.competitor_id == Competitor.id). \
            filter(RaceCompetitor.race_id == id).all()

    if current_user.lang =='ru':
        form.competitor_ref.choices = [(item.id, item.ru_lastname + ' ' + item.ru_firstname) for item in Competitor.query.all()]
        add_competitor_form.nation_code_ref.choices = [(item.id, item.name + ' - ' + item.ru_description) for item in
                                                  Nation.query.all()]
        add_competitor_form.gender_ref.choices = [(item.id, item.ru_name) for item in
                                   Gender.query.all()]
    else:
        form.competitor_ref.choices = [(item.id, item.en_lastname + ' ' + item.en_firstname) for item in Competitor.query.all()]
        add_competitor_form.nation_code_ref.choices = [(item.id, item.name + ' - ' + item.en_description) for item in
                                                  Nation.query.all()]
        add_competitor_form.gender_ref.choices = [(item.id, item.en_name) for item in
                                   Gender.query.all()]
    add_competitor_form.category_ref.choices = [(item.id, item.name) for item in
                                Category.query.all()]
    if form.validate_on_submit():
        # selected_competitor = Competitor.query.filter_by(id=form.competitor_ref.data).one()
        raceCompetitor = RaceCompetitor(
            competitor_id= form.competitor_ref.data,
            race_id = id,
            age_class =form.age_class.data,
            transponder_1 = form.transponder_1.data,
            transponder_2=form.transponder_2.data,
            bib = form.chip.data
        )
        if race.isTeam:
            raceCompetitor.team_id = form.team_ref.data
        db.session.add(raceCompetitor)
        db.session.commit()
        flash('The competitor has been added')

    return render_template('raceinfo/static-tab/competitors_race.html', form=form, competitors=race_competitors, competitor_form=add_competitor_form)

@raceinfo.route('/race/<int:race_id>/competitor/<int:competitor_id>/del', methods=['GET', 'POST'])
@admin_required
def remove_race_competitor(race_id,competitor_id):
    db.session.delete(RaceCompetitor.query.filter_by(id=competitor_id).one())
    return redirect(url_for('.edit_race_competitor', id=race_id,_external=True))

@raceinfo.route('/race/<int:race_id>/competitor/<int:competitor_id>/edit', methods=['GET', 'POST'])
@admin_required
def race_competitor_edit(race_id,competitor_id):
    race = Race.query.filter_by(id=race_id).one()
    race_competitor = RaceCompetitor.query.filter_by(id=competitor_id).one()
    if race.isTeam:
        form = EditRaceCompetitorTeamForm()
        form.team_ref.data = request.args.get('team_id')

    else:
        form = EditRaceCompetitor()
    if current_user.lang == 'ru':
        form.competitor_ref.choices = [(item.id, item.ru_lastname + ' ' + item.ru_firstname) for item in
                                       Competitor.query.all()]

    else:
        form.competitor_ref.choices = [(item.id, item.en_lastname + ' ' + item.en_firstname) for item in
                                       Competitor.query.all()]
    if form.validate_on_submit():
        # selected_competitor = Competitor.query.filter_by(id=form.competitor_ref.data).one()

        race_competitor.competitor_id = form.competitor_ref.data
        race_competitor.age_class = form.age_class.data
        race_competitor.transponder_1 = form.transponder_1.data
        race_competitor.transponder_2 = form.transponder_2.data
        race_competitor.bib = form.bib.data
        db.session.add(race_competitor)
        db.session.commit()
        flash('The competitor has been updated')
        return redirect(url_for('.edit_race_competitor',_external=True))
    form.competitor_ref.data = race_competitor.competitor_id
    form.age_class.data = race_competitor.age_class
    form.transponder_1.data = race_competitor.transponder_1
    form.transponder_2.data = race_competitor.transponder_2
    form.bib.data = race_competitor.bib

    return render_template('raceinfo/static-tab/form_page.html', form=form, title='Edit competitor')



@raceinfo.route('/forerunner/', methods=['GET', 'POST'])
@login_required
@admin_required
def forerunner_list():
    forerunners = Forerunner.query.all()
    return render_template('raceinfo/static-tab/forerunner_list.html', forerunners=forerunners)

@raceinfo.route('/forerunner/add/', methods=['GET', 'POST'])
@login_required
@admin_required
def forerunner_add():
    form = EditForerunnerBase()
    if (current_user.lang == 'ru'):
        form.nation_ref.choices = [(item.id, item.name + ' - ' + item.ru_description) for item in
                                                  Nation.query.all()]
    else:
        form.nation_ref.choices = [(item.id, item.name + ' - ' + item.en_description) for item in
                                                  Nation.query.all()]
    if form.validate_on_submit():
        forerunner = Forerunner(
            ru_lastname = form.ru_lastname.data,
            ru_firstname = form.ru_firstname.data,
            en_lastname = form.en_lastname.data,
            en_firstname = form.en_firstname.data,
            nation_id = form.nation_ref.data
        )

        db.session.add(forerunner)
        db.session.commit()
        flash('The forerunner has been added.')
        return redirect(url_for('.forerunner_list',_external=True))
    return render_template('raceinfo/static-tab/form_page.html', form=form, title="Add forerunner")

@raceinfo.route('/forerunner/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def forerunner_edit(id):
    form = EditForerunnerBase()
    forerunner = Forerunner.query.get_or_404(id)
    if (current_user.lang == 'ru'):
        form.nation_ref.choices = [(item.id, item.name + ' - ' + item.ru_description) for item in
                                                  Nation.query.all()]
    else:
        form.nation_ref.choices = [(item.id, item.name + ' - ' + item.en_description) for item in
                                                  Nation.query.all()]
    if form.validate_on_submit():
        forerunner.ru_lastname  = form.ru_lastname.data,
        forerunner.ru_firstname = form.ru_firstname.data,
        forerunner.en_lastname = form.en_lastname.data,
        forerunner.en_firstname = form.en_firstname.data,
        forerunner.nation_id = form.nation_ref.data
        db.session.add(forerunner)
        flash('The forerunner has been updated.')
        return redirect(url_for('.competitor_list',_external=True))
    form.ru_lastname.data = forerunner.ru_lastname
    form.ru_firstname.data = forerunner.ru_firstname
    form.en_lastname.data = forerunner.en_lastname
    form.en_firstname.data = forerunner.en_firstname
    form.nation_ref.data = forerunner.nation_id
    return render_template('raceinfo/static-tab/form_page.html', title='Edit forerunner', form=form, forerunner=forerunner)

@raceinfo.route('/forerunner/<int:id>/del/', methods=['GET', 'POST'])
@login_required
@admin_required
def forerunner_del(id):
    forerunner = Forerunner.query.get_or_404(id)
    db.session.delete(forerunner)
    flash('The forerunner ' + forerunner.ru_firstname + ' has been deleted.')
    return redirect(url_for('.forerunner_list',_external=True))


@raceinfo.route('/coursetter/', methods=['GET', 'POST'])
@login_required
@admin_required
def coursetter_list():
    coursetter = Coursetter.query.all()
    return render_template('raceinfo/static-tab/coursetter_list.html', coursetters=coursetter)

@raceinfo.route('/coursetter/add/', methods=['GET', 'POST'])
@login_required
@admin_required
def coursetter_add():
    form = EditCoursetterBase()
    if (current_user.lang == 'ru'):
        form.nation_ref.choices = [(item.id, item.name + ' - ' + item.ru_description) for item in
                                                  Nation.query.all()]
    else:
        form.nation_ref.choices = [(item.id, item.name + ' - ' + item.en_description) for item in
                                                  Nation.query.all()]
    if form.validate_on_submit():
        coursetter = Coursetter(
            ru_lastname=form.ru_lastname.data,
            ru_firstname=form.ru_firstname.data,
            en_lastname=form.en_lastname.data,
            en_firstname=form.en_firstname.data,
            nation_id=form.nation_ref.data
        )
        db.session.add(coursetter)
        db.session.commit()
        flash('The coursetter has been added.')
        return redirect(url_for('.coursetter_list',_external=True))
    return render_template('raceinfo/static-tab/form_page.html',  form=form, title="Coursetter add")

@raceinfo.route('/coursetter/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def coursetter_edit(id):
    form = EditCoursetterBase()
    coursetter = Coursetter.query.get_or_404(id)
    if (current_user.lang == 'ru'):
        form.nation_ref.choices = [(item.id, item.name + ' - ' + item.ru_description) for item in
                                                  Nation.query.all()]
    else:
        form.nation_ref.choices = [(item.id, item.name + ' - ' + item.en_description) for item in
                                                  Nation.query.all()]
    if form.validate_on_submit():
        coursetter.ru_lastname = form.ru_lastname.data,
        coursetter.ru_firstname = form.ru_firstname.data,
        coursetter.en_lastname = form.en_lastname.data,
        coursetter.en_firstname = form.en_firstname.data,
        coursetter.nation_id = form.nation_ref.data
        db.session.add(coursetter)
        flash('The coursetter has been updated.')
        return redirect(url_for('.competitor_list',_external=True))
    form.ru_lastname.data = coursetter.ru_lastname
    form.ru_firstname.data = coursetter.ru_firstname
    form.en_lastname.data = coursetter.en_lastname
    form.en_firstname.data = coursetter.en_firstname
    form.nation_ref.data = coursetter.nation_id
    return render_template('raceinfo/static-tab/form_page.html', form=form, coursetter=coursetter)

@raceinfo.route('/coursetter/<int:id>/del/', methods=['GET', 'POST'])
@login_required
@admin_required
def coursetter_del(id):
    coursetter = Coursetter.query.get_or_404(id)
    db.session.delete(coursetter)
    flash('The coursetter ' + coursetter.ru_firstname + ' has been deleted.')
    return redirect(url_for('.coursetter_list',_external=True))


@raceinfo.route('/race/<int:id>/course', methods=['GET', 'POST'])
@admin_required
def race_сourse_list(id):
    race = Race.query.filter_by(id=id).one()
    race_course = Course.query.filter_by(race_id=id)
    return render_template('raceinfo/static-tab/course_list.html', race=race, race_course=race_course)

@raceinfo.route('/race/<int:id>/course/add', methods=['GET', 'POST'])
@admin_required
def race_сourse_add(id):
    form = EditCourseBase()
    if current_user.lang =='ru':
        form.course_coursetter_ref.choices = [(item.id, item.ru_lastname + ' ' + item.ru_firstname) for item in Coursetter.query.all()]

    else:
        form.course_coursetter_ref.choices = [(item.id, item.en_lastname + ' ' + item.en_firstname) for item in Coursetter.query.all()]
    if form.validate_on_submit():
        course = Course(
            race_id=id,
            course_coursetter_id=form.course_coursetter_ref.data,
            run=form.run.data,
            ru_name=form.ru_name.data,
            en_name=form.en_name.data,
            homologation=form.homologation.data,
            length=form.length.data,
            gates=form.gates.data,
            tuminggates=form.tuminggates.data,
            startelev=form.startelev.data,
            finishelev=form.finishelev.data,
        )
        db.session.add(course)
        db.session.commit()
        flash('The course has been added.')
        return redirect(url_for('.race_сourse_list', id=id,_external=True))
    return render_template('raceinfo/static-tab/course_edit.html', form=form)

@raceinfo.route('/race/<int:id>/course/<int:course_id>/base/edit', methods=['GET', 'POST'])
@admin_required
def race_сourse_base_edit(id, course_id):
    сourse = Course.query.get_or_404(course_id)
    form = EditCourseBase()
    if current_user.lang =='ru':
        form.course_coursetter_ref.choices = [(item.id, item.ru_lastname + ' ' + item.ru_firstname) for item in Coursetter.query.all()]
    else:
        form.course_coursetter_ref.choices = [(item.id, item.en_lastname + ' ' + item.en_firstname) for item in Coursetter.query.all()]
    if form.validate_on_submit():
        сourse.race_id= id
        сourse.course_coursetter_id = form.course_coursetter_ref.data
        сourse.run = form.run.data
        сourse.ru_name = form.ru_name.data
        сourse.en_name =form.en_name.data
        сourse.homologation = form.homologation.data
        сourse.length = form.length.data
        сourse.gates = form.gates.data
        сourse.tuminggates = form.tuminggates.data
        сourse.startelev = form.startelev.data
        сourse.finishelev = form.finishelev.data
        db.session.add(сourse)
        db.session.commit()
        flash('The course has been updated.')
        return redirect(url_for('.race_сourse_edit', id=id, course_id=course_id,_external=True))
    form.course_coursetter_ref.data = сourse.course_coursetter_id
    form.run.data = сourse.run
    form.ru_name.data = сourse.ru_name
    form.en_name.data = сourse.en_name
    form.homologation.data = сourse.homologation
    form.length.data = сourse.length
    form.gates.data = сourse.gates
    form.tuminggates.data = сourse .tuminggates
    form.startelev.data = сourse.startelev
    form.finishelev.data = сourse.finishelev
    return render_template('raceinfo/static-tab/course_edit.html', form = form)

@raceinfo.route('/race/<int:id>/course/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_required
def race_сourse_edit(id, course_id):
    сourse = Course.query.get_or_404(course_id)
    race =Race.query.filter_by(id=id).one()
    course_forerunners = (db.session.query(CourseForerunner, Forerunner, Course). \
        join(Forerunner).join(Course).filter(Course.race_id == id)).all()

    race_inter_dev = CourseDevice.query.filter(course_id==course_id).all()

    return render_template('raceinfo/course_view.html', course=сourse, race=race,course_forerunners=course_forerunners, race_inter_dev=race_inter_dev)

@raceinfo.route('/race/<int:id>/course/<int:course_id>/del', methods=['GET', 'POST'])
@admin_required
def race_сourse_del(id, course_id):
    сourse = Course.query.get_or_404(course_id)
    db.session.delete(сourse)
    flash('The сourse ' + сourse.ru_name + ' has been deleted.')
    return redirect(url_for('.race_сourse_list', id=id,_external=True))


@raceinfo.route('/race/<int:id>/course/<int:course_id>/forerunner/add', methods=['GET', 'POST'])
@admin_required
def race_сourse_forerunner(id, course_id):
    form = EditCourseForerunnerBase()
    # course_forerunners = db.session.query(CourseForerunner, Forerunner, Course). \
    #     outerjoin(Forerunner, CourseForerunner.forerunner_id == Forerunner.id).all(). \
    #     outerjoin(Course, CourseForerunner.course_id == Course.id). \
    #     filter(Course.id == id).all()

    if current_user.lang == 'ru':
        form.forerunner_ref.choices = [(item.id, item.ru_lastname + ' ' + item.ru_firstname) for item in
                                       Forerunner.query.all()]
        # form.course_ref.choices = [(item.id, item.ru_name ) for item in
        #                            Course.query.filter_by(race_id=id).all()]
    else:
        form.forerunner_ref.choices = [(item.id, item.ru_lastname + ' ' + item.ru_firstname) for item in
                                       Forerunner.query.all()]
        # form.course_ref.choices = [(item.id, item.ru_name ) for item in
        #                            Course.query.filter_by(race_id=id).all()]
    if form.validate_on_submit():
        course_forerunner = CourseForerunner(
            order=form.order.data,
            forerunner_id=form.forerunner_ref.data,
            course_id=course_id
        )
        db.session.add(course_forerunner)
        db.session.commit()
        flash('The course forerunner has been added.')
        return redirect(url_for('.race_сourse_edit', id=id, course_id=course_id,_external=True))
    return render_template('raceinfo/static-tab/cource_forerunner_list.html', form = form)


@raceinfo.route('/race/<int:id>/course/<int:course_id>/forerunner/<int:forerunner_id>/edit', methods=['GET', 'POST'])
@admin_required
def race_сourse_forerunner_edit(id, course_id,forerunner_id):
    form = EditCourseForerunnerBase()
    course_forerunner=CourseForerunner.query.get_or_404(forerunner_id)
    if current_user.lang == 'ru':
        form.forerunner_ref.choices = [(item.id, item.ru_lastname + ' ' + item.ru_firstname) for item in
                                       Forerunner.query.all()]

    else:
        form.forerunner_ref.choices = [(item.id, item.ru_lastname + ' ' + item.ru_firstname) for item in
                                       Forerunner.query.all()]
    if form.validate_on_submit():
        course_forerunner.order=form.order.data
        course_forerunner.forerunner_id=form.forerunner_ref.data
        db.session.add(course_forerunner)
        db.session.commit()
        flash('The course forerunner has been updated.')
        return redirect(url_for('.race_сourse_edit', id=id, course_id=course_id,_external=True))
    form.order.data = course_forerunner.order
    form.forerunner_ref.data = course_forerunner.forerunner_id
    return render_template('raceinfo/static-tab/cource_forerunner_list.html', form = form)


@raceinfo.route('/race/<int:id>/course/<int:course_id>/forerunner/<int:forerunner_id>/del', methods=['GET', 'POST'])
@admin_required
def race_сourse_forerunner_del(id,course_id,forerunner_id):
    course_forerunner = CourseForerunner.query.get_or_404(forerunner_id)
    db.session.delete(course_forerunner)
    flash('The forerunner has been deleted.')
    return redirect(url_for('.race_сourse_edit', id=id, course_id=course_id,_external=True))


@raceinfo.route('/team/', methods=['GET'])
@admin_required
def team_list():
    items = Team.query.all()
    return render_template('raceinfo/static-tab/team_list.html', items=items)

@raceinfo.route('/team/add', methods=['GET', 'POST'])
@admin_required
def team_add():
    form = EditTeamForm()
    if (current_user.lang == 'ru'):
        form.nation_ref.choices = [(item.id, item.name + ' - ' + item.ru_description) for item in
                                                  Nation.query.all()]
    else:
        form.nation_ref.choices = [(item.id, item.name + ' - ' + item.en_description) for item in
                                                  Nation.query.all()]
    if form.validate_on_submit():
        team = Team(
            fis_code=form.fis_code.data,
            en_teamname=form.en_teamname.data,
            ru_teamname=form.ru_teamname.data,
            nation_id=form.nation_ref.data
        )
        db.session.add(team)
        flash('The team has been added.')
        return redirect(url_for('.team_list',_external=True))
    return render_template('raceinfo/static-tab/form_page.html', title='Add team', form=form)

@raceinfo.route('/team/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def team_edit(id):
    form = EditTeamForm()
    team = Team.query.filter_by(id=id).one()
    if (current_user.lang == 'ru'):
        form.nation_ref.choices = [(item.id, item.name + ' - ' + item.ru_description) for item in
                                                  Nation.query.all()]
    else:
        form.nation_ref.choices = [(item.id, item.name + ' - ' + item.en_description) for item in
                                                  Nation.query.all()]
    if form.validate_on_submit():
        team.fis_code=form.fis_code.data
        team.en_teamname=form.en_teamname.data
        team.ru_teamname=form.ru_teamname.data
        team.nation_id=form.nation_ref.data
        db.session.add(team)
        flash('The team has been changed.')
        return redirect(url_for('.team_list',_external=True))
    form.fis_code.data = team.fis_code
    form.en_teamname.data = team.en_teamname
    form.ru_teamname.data = team.ru_teamname
    form.nation_ref.data = team.nation_id
    return render_template('raceinfo/static-tab/form_page.html', title='Edit team', form=form)

@raceinfo.route('/team/<int:id>/del', methods=['GET', 'POST'])
@admin_required
def team_remove(id):
    team = Team.query.get_or_404(id)
    db.session.delete(team)
    flash('The team has been deleted.')
    return redirect(url_for('.team_list',_external=True))


@raceinfo.route('/race/<int:id>/run', methods=['GET', 'POST'])
@admin_required
def race_run(id):
    form = EditRunInfoForm()
    race = Race.query.filter_by(id=id).one()
    course_runs = (db.session.query(RunInfo, Course).join(Course).filter(Course.race_id == id)).all()
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
            starttime=form.starttime.data,
            endtime=form.endtime.data
        )
        db.session.add(run_info)
        db.session.commit()
        flash('The run has been added.')
    return render_template('raceinfo/static-tab/run_list.html',race=race, course_runs=course_runs)

@raceinfo.route('/race/<int:id>/run/<int:run_id>/del', methods=['GET', 'POST'])
@admin_required
def race_course_run_del(id,run_id):
    run_info = RunInfo.query.get_or_404(run_id)
    db.session.delete(run_info)
    flash('The run has been deleted.')
    return redirect(url_for('.race_run', id=id,_external=True))


@raceinfo.route('/race/<int:id>/run/<int:run_id>/start', methods=['GET', 'POST'])
@admin_required
def race_course_run_start(id,run_id):
    try:
        run_info = RunInfo.query.get_or_404(run_id)
        run_info.starttime = datetime.now()
        db.session.add(run_info)
        db.session.commit()
    except:
        return 'fail', 200
    return json.dumps({'start_time': str(run_info.starttime)})

@raceinfo.route('/race/<int:id>/run/<int:run_id>/stop', methods=['GET', 'POST'])
@admin_required
def race_course_run_stop(id,run_id):
    # CHECK IT, IT LOOKS like a shi...t
    run_info = RunInfo.query.get_or_404(run_id)
    run_info.endtime = datetime.now()
    db.session.add(run_info)
    try:
        news_run = db.session.query(RunInfo.id).filter(RunInfo.race_id==run_info.race_id, RunInfo.number==run_info.number+1).one()
        RunOrder.query.filter(RunOrder.run_id == news_run.id).delete()

        sub_query = db.session.query(ResultApproved.race_competitor_id, Status.filter_order).join(Status).filter(ResultApproved.run_id == run_id).subquery()

        race_competitors = db.session.query(RaceCompetitor, sub_query)\
            .outerjoin(sub_query, and_(sub_query.c.race_competitor_id == RaceCompetitor.id))\
            .order_by(sub_query.c.filter_order.asc())\
            .all()

        print('Компетиторы список ', len(race_competitors))
        for i in range(len(race_competitors)):
            run_order = RunOrder(
                race_competitor_id=race_competitors[i][0].id,
                run_id=news_run.id,
                order=i+1
            )
            db.session.add(run_order)
        db.session.commit()
    except:
        return json.dumps({'stop_time': str(run_info.endtime)})
    return json.dumps({'stop_time': str(run_info.endtime)})


@raceinfo.route('/race/<int:id>/run/add', methods=['GET', 'POST'])
@admin_required
def race_run_add(id):
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
        db.session.add(run_info)
        db.session.commit()
        flash('The run has been added.')
        return redirect(url_for('.race_run', id=id,_external=True))
    return render_template('raceinfo/static-tab/form_page.html',title='Add run', form=form)

@raceinfo.route('/race/<int:id>/run/<int:run_id>/edit', methods=['GET', 'POST'])
@admin_required
def race_run_edit(id,run_id):
    form = EditRunInfoForm()
    run_info = RunInfo.query.filter_by(id=run_id).one()
    if current_user.lang == 'ru':
        form.course_ref.choices = [(item.id, item.ru_name ) for item in
                                   Course.query.filter_by(race_id=id).all()]
    else:

        form.course_ref.choices = [(item.id, item.ru_name ) for item in
                                   Course.query.filter_by(race_id=id).all()]
    if form.validate_on_submit():
        run_info.race_id=id
        run_info.course_id=form.course_ref.data
        run_info.number=form.number.data
        db.session.add(run_info)
        db.session.commit()
        flash('The run has been updated.')
        return redirect(url_for('.race_run', id=id,_external=True))

    form.course_ref.data = run_info.course_id
    form.number.data = run_info.number
    return render_template('raceinfo/static-tab/form_page.html', title='Edit run', form=form)



@raceinfo.route('/race/<int:id>/course/<int:course_id>/dev/add', methods=['GET', 'POST'])
@admin_required
def race_сourse_dev_add(id, course_id):
    form = EditCourseDeviceForm()
    # if current_user.lang == 'ru':
    #     form.course_ref.choices = [(item.id, item.ru_name) for item in
    #                                Course.query.filter_by(race_id=id).all()]
    # else:
    #
    form.device_ref.choices = [(item.id, item.name) for item in
                               Device.query.all()]
    form.course_device_type_ref.choices = [(item.id, item.name) for item in
                                           CourseDeviceType.query.all()]
    if form.validate_on_submit():
        dev = CourseDevice(
            course_id = course_id,
            order = form.order.data,
            distance = form.distance.data,
            device_id=form.device_ref.data,
            course_device_type_id=form.course_device_type_ref.data

        )
        db.session.add(dev)
        flash('The device has been added.')
        return redirect(url_for('.race_сourse_edit', id=id, course_id=course_id,_external=True))
    return render_template('raceinfo/static-tab/form_page.html', title='Add device', form=form)


@raceinfo.route('/race/<int:id>/course/<int:course_id>/dev/<int:dev_id>/edit', methods=['GET', 'POST'])
@admin_required
def race_сourse_dev_edit(id,course_id, dev_id):
    form = EditCourseDeviceForm()
    dev = CourseDevice.query.filter_by(id=dev_id).one()
    form.device_ref.choices = [(item.id, item.name) for item in
                               Device.query.all()]
    form.course_device_type_ref.choices = [(item.id, item.name) for item in
                                           CourseDeviceType.query.all()]
    if form.validate_on_submit():
        # intermediate_dev.course_id = form.course_ref.data
        dev.order = form.order.data
        dev.distance = form.distance.data
        dev.device_id = form.device_ref.data,
        dev.course_device_type_id = form.course_device_type_ref.data

        db.session.add(dev)
        flash('The device has been added.')
        return redirect(url_for('.race_сourse_edit', id=id, course_id=course_id,_external=True))
    form.order.data = dev.order
    form.distance.data = dev.distance
    form.device_ref.data = dev.device_id
    form.course_device_type_ref.data = dev.course_device_type_id

    return render_template('raceinfo/static-tab/form_page.html', title='Edit device', form=form)

@raceinfo.route('/race/<int:id>/course/<int:course_id>/dev/<int:dev_id>/del', methods=['GET', 'POST'])
@admin_required
def race_сourse_dev_del(id,course_id, dev_id):
    intermediate_dev = CourseDevice.query.get_or_404(dev_id)
    db.session.delete(intermediate_dev)
    flash('The device has been deleted.')
    return redirect(url_for('.race_сourse_edit', id=id, course_id=course_id,_external=True))


# ========================================================================================================================================
@raceinfo.route('/race/<int:id>/team', methods=['GET', 'POST'])
@admin_required
def race_team_list(id):
    race = Race.query.filter_by(id=id).one()
    race_team = db.session.query(RaceTeam, Team).join(Team).filter(RaceTeam.race_id==id).all()
    return render_template('raceinfo/static-tab/race_team_list.html', race=race, race_team=race_team)

@raceinfo.route('/race/<int:id>/team/add', methods=['GET', 'POST'])
@admin_required
def race_team_add(id):
    form = EditRaceTeamForm()
    if current_user.lang =='ru':
        form.team_ref.choices = [(item.id, item.ru_teamname) for item in Team.query.all()]
    else:
        form.team_ref.choices = [(item.id, item.en_teamname) for item in Team.query.all()]
    if form.validate_on_submit():
        race_team = RaceTeam(
            race_id=id,
            team_id=form.team_ref.data,
            bib=form.bib.data,
        )
        db.session.add(race_team)
        db.session.commit()
        flash('The team has been added.')
        return redirect(url_for('.race_team_list', id=id,_external=True))
    return render_template('raceinfo/static-tab/form_page.html', title='Add team',form=form)

@raceinfo.route('/race/<int:id>/team/<int:team_id>/edit', methods=['GET', 'POST'])
@admin_required
def race_team_edit(id, team_id):
    race_team = db.session.query(RaceTeam, Team).join(Team).filter(RaceTeam.id==team_id).one()
    race = Race.query.filter_by(id=id).one()

    return render_template('raceinfo/team_view.html', team=race_team, race=race)

@raceinfo.route('/race/<int:id>/team/<int:team_id>/base/edit', methods=['GET', 'POST'])
@admin_required
def race_team_edit_base(id, team_id):
    race_team = RaceTeam.query.get_or_404(team_id)
    form = EditRaceTeamForm()
    if current_user.lang =='ru':
        form.team_ref.choices = [(item.id, item.ru_teamname) for item in Team.query.all()]
    else:
        form.team_ref.choices = [(item.id, item.en_teamname) for item in Team.query.all()]
    if form.validate_on_submit():
        race_team.bib = form.bib.data
        race_team.team_id = form.team_ref.data
        db.session.add(race_team)
        db.session.commit()
        flash('The team has been updated.')
        return redirect(url_for('.race_team_list', id=id,_external=True))
    form.team_ref.data = race_team.team_id
    form.bib.data = race_team.bib
    return render_template('raceinfo/static-tab/form_page.html', titile='Edit team', form=form)


@raceinfo.route('/race/<int:id>/team/<int:team_id>/del', methods=['GET', 'POST'])
@admin_required
def race_team_del(id, team_id):
    race_team = RaceTeam.query.get_or_404(team_id)
    db.session.delete(race_team)
    flash('The team has been deleted.')
    return redirect(url_for('.race_team_list', id=id,_external=True))
# ========================================================================================================================================


@raceinfo.route('/device/', methods=['GET', 'POST'])
@login_required
@admin_required
def device_list():
    devices = db.session.query(Device, DeviceType).join(DeviceType).all()
    return render_template('raceinfo/static-tab/device_list.html', devices=devices)

@raceinfo.route('/device/add/', methods=['GET', 'POST'])
@login_required
@admin_required
def device_add():
    form = EditDeviceForm()
    form.type_ref.choices = [(item.id, item.name) for item in DeviceType.query.all()]

    if form.validate_on_submit():
        device = Device(
            src_dev=form.src_dev.data,
            name=form.name.data,
            type_id=form.type_ref.data
        )
        db.session.add(device)
        db.session.commit()
        flash('The device has been added.')
        return redirect(url_for('.device_list',_external=True))
    return render_template('raceinfo/static-tab/form_page.html', form=form, title="Add device ")

@raceinfo.route('/device/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def device_edit(id):
    form = EditDeviceForm()
    device = Device.query.get_or_404(id)
    form.type_ref.choices = [(item.id, item.name) for item in DeviceType.query.all()]

    if form.validate_on_submit():
        device.src_dev=form.src_dev.data
        device.name=form.name.data
        device.type_id=form.type_ref.data
        db.session.add(device)
        flash('The device has been updated.')
        return redirect(url_for('.device_list',_external=True))
    form.src_dev.data = device.src_dev
    form.name.data = device.name
    form.type_ref.data = device.type_id
    return render_template('raceinfo/static-tab/form_page.html', title='Edit device',form=form, device=device)

@raceinfo.route('/device/<int:id>/del/', methods=['GET', 'POST'])
@login_required
@admin_required
def device_del(id):
    device = Device.query.get_or_404(id)
    db.session.delete(device)
    flash('The device has been deleted.')
    return redirect(url_for('.device_list',_external=True))

@raceinfo.route('/device/type/', methods=['GET', 'POST'])
@login_required
@admin_required
def device_type():
    form = EditDeviceTypeForm()
    devices = DeviceType.query.all()

    if form.validate_on_submit():
        device = DeviceType(
            name=form.name.data,
        )
        db.session.add(device)
        db.session.commit()
        flash('The device has been added.')
        return redirect(url_for('.device_type',_external=True))
    return render_template('raceinfo/static-tab/device_type_list.html', form=form, title="Add forerunner", devices=devices)

@raceinfo.route('/device/type/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def device_type_edit(id):
    form = EditDeviceTypeForm()
    device = DeviceType.query.get_or_404(id)
    if form.validate_on_submit():
        device.name = form.name.data

        db.session.add(device)
        flash('The device has been updated.')
        return redirect(url_for('.device_type',_external=True))
    form.name.data = device.name
    return render_template('raceinfo/static-tab/form_page.html', form=form, devices=device)

@raceinfo.route('/device/type/<int:id>/del/', methods=['GET', 'POST'])
@login_required
@admin_required
def device_type_del(id):
    device = DeviceType.query.get_or_404(id)
    db.session.delete(device)
    flash('The device has been deleted.')
    return redirect(url_for('.device_type',_external=True))


@raceinfo.route('/race/<int:id>/order_list/buld', methods=['GET', 'POST'])
@login_required
@admin_required
def race_order_list(id):
    race = Race.query.filter_by(id=id).one()
    try:
        run = RunInfo.query.filter_by(race_id=id, number=1).one()
    except:
        return redirect(url_for('.race', id=id, _external=True))

    RunOrder.query.filter(RunOrder.run_id==run.id).delete()

    race_competitors = db.session.query(RaceCompetitor, FisPoints).\
        join(FisPoints, FisPoints.competitor_id == RaceCompetitor.competitor_id).\
        filter(RaceCompetitor.race_id == id, FisPoints.discipline_id==race.discipline_id).\
        order_by(FisPoints.fispoint.desc()).all()

    for i in range(len(race_competitors)):
        run_order = RunOrder(
            race_competitor_id = race_competitors[i][0].id,
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


@raceinfo.route('/status/get', methods=['GET'])

def status_get_list():
    return json.dumps(Status.query.all(), cls=jsonencoder.AlchemyEncoder)
