from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from data import db_session
from data.models import Event, Money
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
        session = db_session.create_session()
        event = Event()
        event.title = form.title.data
        event.manager_id = current_user.id
        event.is_private = form.is_private.data
        event.is_done = form.is_done.data
        current_user.events.append(event)
        money = Money()
        money.event_id = event.id
        money.user_id = current_user.id
        event.money_list.append(money)
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
    for money in event.money_list:
        session.delete(money)
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

    event.update_dicts()

    members_list = []
    init_cost = 0.0
    for member in event.members:
        if member.id in event.sums_dict:
            sums = event.sums_dict[member.id]
        else:
            sums = {
                'cost': init_cost,
                'avg': init_cost,
                'balance': init_cost
            }

        members_list.append({
            'id': member.id,
            'fullname': member.get_full_name(),
            'is_manager': member.id == event.manager_id,
            'cost': sums['cost'],
            'cost_text': f"{sums['cost']:.2f}",
            'avg': sums['avg'],
            'avg_text': f"{sums['avg']:.2f}",
            'balance': sums['balance'],
            'balance_text': f"{sums['balance']:.2f}",
        })
        members_list.sort(key=lambda d: (not d['is_manager'], d['id']))

    total_dict = {
        'count': event.sums_total_dict['count'],
        'cost_text': f"{event.sums_total_dict['cost']:.2f}",
        'avg_text': f"{event.sums_total_dict['avg']:.2f}",
        'avg_plus': event.sums_total_dict['avg_plus'],
        'avg_plus_text': f"{event.sums_total_dict['avg_plus']:.2f}"
    }

    params['title'] = event.title
    params['event_id'] = event_id
    params['manager_id'] = event.manager_id
    if current_user.is_authenticated:
        params['is_event_member'] = current_user in event.members
    params['members_list'] = members_list
    params['total_dict'] = total_dict
    return render_template("event.html", **params)
