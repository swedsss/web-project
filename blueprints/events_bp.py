from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from data import db_session
from data.models import User, Event, Money
from forms.events_forms import AddEventForm, EditEventForm, AddUserForm
from constants import *


blueprint = Blueprint(
    'events_bp',
    __name__,
    template_folder='templates'
)


@blueprint.route("/events/add", methods=['GET', 'POST'])
@login_required
def add_event():
    form = AddEventForm()
    params = {
        'app_name': APP_NAME,
        'title': "Добавить мероприятие",
        'form': form,
    }
    if form.validate_on_submit():
        session = db_session.create_session()
        event = Event()
        event.title = form.title.data
        event.manager_id = current_user.id
        event.is_private = form.is_private.data
        event.is_done = form.is_done.data
        current_user.events.append(event)
        session.merge(current_user)
        money = Money()
        money.event_id = event.id
        money.user_id = current_user.id
        event.money_list.append(money)
        session.merge(event)
        session.commit()
        params['success'] = f'Мероприятие "{event.title}" успешно создано'
    return render_template("event_form.html", **params)


@blueprint.route("/events/edit/<int:event_id>", methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    params = {
        'app_name': APP_NAME,
    }
    session = db_session.create_session()
    event = session.query(Event).get(event_id)
    if not event:
        params['error'] = f'Мероприятия с id {event_id} не существует'
        return render_template("base.html", **params)

    form = EditEventForm()
    params['title'] = "Изменить мероприятие"
    params['form'] = form
    if request.method == 'GET':
        form.title.data = event.title
        form.is_private.data = event.is_private
        form.is_done.data = event.is_done
    if form.validate_on_submit():
        event.title = form.title.data
        event.manager_id = current_user.id
        event.is_private = form.is_private.data
        event.is_done = form.is_done.data
        session.commit()
        params['success'] = f'Мероприятие "{event.title}" успешно изменено'
    return render_template("event_form.html", **params)


@blueprint.route("/events/delete/<int:event_id>", methods=['GET', 'POST'])
@login_required
def delete_event(event_id):
    params = {
        'app_name': APP_NAME,
    }
    session = db_session.create_session()
    event = session.query(Event).get(event_id)
    if not event:
        params['error'] = f'Мероприятия с id {event_id} не существует'
        return render_template("base.html", **params)
    params['title'] = "Удалить мероприятие"
    params['success'] = f'Мероприятие "{event.title}" успешно удалено'
    session.delete(event)
    session.commit()
    return render_template("base.html", **params)


@blueprint.route("/events/<int:event_id>")
def show_event(event_id):
    params = {
        'app_name': APP_NAME,
    }
    session = db_session.create_session()
    event = session.query(Event).get(event_id)
    if not event:
        params['error'] = f'Мероприятия с id {event_id} не существует'
        return render_template("base.html", **params)

    members_list = []
    init_cost = 0.0
    for member in event.members:
        money = session.query(Money).get((event.id, member.id))
        cost = money.cost if money else init_cost
        members_list.append({
            'id': member.id,
            'fullname': member.get_full_name(),
            'is_manager': member.id == event.manager_id,
            'cost': cost,
            'cost_text': f'{cost:.2f}'
        })
    params['title'] = event.title
    params['event_id'] = event_id
    params['manager_id'] = event.manager_id
    if current_user.is_authenticated:
        params['is_event_member'] = current_user in event.members
    params['members_list'] = members_list
    return render_template("event.html", **params)
