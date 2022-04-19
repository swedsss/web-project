from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from data import db_session
from data.models import User, Event, Money
from forms.money_forms import EditMoneyForm
from constants import *


blueprint = Blueprint(
    'money_bp',
    __name__,
    template_folder='templates'
)


@blueprint.route('/money/<int:event_id>/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_money(event_id, user_id):
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
    if current_user.id not in [event.manager_id, user_id]:
        params['error'] = f'Редактировать суммы других участников может только менеджер мероприятия'
        return render_template("base.html", **params)
    money = session.query(Money).get((event_id, user_id))
    form = EditMoneyForm()
    params['title'] = "Редактирование суммы"
    params['form'] = form
    if request.method == "GET":
        form.cost.data = money.get_cost_text() if money else f'{0.00:.2f}'
    if form.validate_on_submit():
        if not money:
            money = Money()
            money.event_id = event.id
            money.user_id = user.id
            event.money_list.append(money)
            session.merge(event)
        money.set_cost(form.cost.data)
        session.commit()
        return redirect(f"/events/{event.id}")
    return render_template("money_form.html", **params)
