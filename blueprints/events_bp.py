from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from data import db_session
from data.models import Event
from forms.events_forms import AddEventForm, EditEventForm
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
        event = Event()
        event.title = form.title.data
        event.manager_id = current_user.id
        event.is_private = form.is_private.data
        event.is_done = form.is_done.data
        current_user.events.append(event)
        session = db_session.create_session()
        session.merge(current_user)
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

    members = []
    init_cost = 0.0
    for user in event.users:
        members.append({
            'fullname': user.get_full_name(),
            'is_manager': user.id == event.manager_id,
            'cost': init_cost,
            'cost_text': f'{init_cost:.2f}'
        })

    if not event:
        params['error'] = f'Мероприятия с id {event_id} не существует'
        return render_template("base.html", **params)
    params['title'] = event.title
    params['members'] = members
    return render_template("event.html", **params)
