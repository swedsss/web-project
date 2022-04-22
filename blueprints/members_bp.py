from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from data import db_session
from data.users import User
from data.events import Event
from data.money import Money
from forms.members_forms import InviteUserForm
from constants import *


blueprint = Blueprint(
    'members_bp',
    __name__,
    template_folder='templates'
)


@blueprint.route("/members/invite_user/<int:event_id>", methods=['GET', 'POST'])
@login_required
def choose_user(event_id):
    params = {
        'app_name': APP_NAME,
    }
    session = db_session.create_session()
    event = session.query(Event).get(event_id)
    if not event:
        params['error'] = f'Мероприятия с id {event_id} не существует'
        return render_template("base.html", **params)
    if current_user.id != event.manager_id:
        params['error'] = f'Приглашать пользователей может только менеджер мероприятия'
        return render_template("base.html", **params)
    params['title'] = "Пригласить пользователя"
    form = InviteUserForm()
    users = session.query(User).all()
    form.user_id.choices = [(user.id, user.get_full_name()) for user in users
                            if user not in event.members]
    params['form'] = form
    if form.validate_on_submit():
        return redirect(f"/members/add/{event_id}/{form.user_id.data}")
    return render_template("invite_form.html", **params)


@blueprint.route("/members/add/<int:event_id>/<int:user_id>")
@login_required
def add_user(event_id, user_id):
    params = {
        'app_name': APP_NAME,
    }
    session = db_session.create_session()
    event = session.query(Event).get(event_id)
    if not event:
        params['error'] = f'Мероприятия с id {event_id} не существует'
        return render_template("base.html", **params)
    user = session.query(User).get(user_id)
    if not User:
        params['error'] = f'Пользователь с id {user_id} не существует'
        return render_template("base.html", **params)
    if user_id in event.members:
        params['error'] = f'Пользователь "{user.get_full_name()}" ' \
                          f'уже является участником мероприятия "{event.title}"'
        return render_template("base.html", **params)
    if current_user.id not in [event.manager_id, user_id]:
        params['error'] = f'Добавлять других пользователей может только менеджер мероприятия'
        return render_template("base.html", **params)
    event.members.append(user)

    money = Money()
    money.event_id = event_id
    money.user_id = user_id
    event.money_list.append(money)

    session.merge(event)
    session.commit()
    return redirect(f"/events/{event_id}")


@blueprint.route("/members/delete/<int:event_id>/<int:user_id>")
@login_required
def delete_user(event_id, user_id):
    params = {
        'app_name': APP_NAME,
    }
    session = db_session.create_session()
    event = session.query(Event).get(event_id)
    if not event:
        params['error'] = f'Мероприятия с id {event_id} не существует'
        return render_template("base.html", **params)
    user = session.query(User).get(user_id)
    if not User:
        params['error'] = f'Пользователь с id {user_id} не существует'
        return render_template("base.html", **params)
    if user not in event.members:
        params['error'] = f'Пользователь "{user.get_full_name()}" ' \
                          f'не является участником мероприятия "{event.title}"'
        return render_template("base.html", **params)
    if current_user.id not in [event.manager_id, user_id]:
        params['error'] = f'Удалять других пользователей может только менеджер мероприятия'
        return render_template("base.html", **params)
    event.members.remove(user)
    session.merge(event)

    money = session.query(Money).get((event_id, user_id))
    if money:
        session.delete(money)

    session.commit()
    return redirect(f"/events/{event_id}")
