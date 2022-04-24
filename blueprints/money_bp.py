from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from data import db_session
from data.users import User
from data.events import Event
from data.members import Member
from data.money import Money
from forms.money_forms import EditMoneyForm, PayForm
from constants import *

blueprint = Blueprint(
    'money_bp',
    __name__,
    template_folder='templates'
)


@blueprint.route('/money/<int:event_id>/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_money(event_id, user_id):
    """ Обработчик для изменения потраченной суммы участника """
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
        if form.cost.data < 0:
            params['error'] = f'Можно указать только неотрицательную сумму'
            return render_template("money_form.html", **params)
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


@blueprint.route('/money/set_pay/<int:event_id>', methods=['GET', 'POST'])
@login_required
def set_pay(event_id):
    """ Обработчик для отображения формы оплаты """
    params = {
        'app_name': APP_NAME,
    }
    session = db_session.create_session()
    event = session.query(Event).get(event_id)
    if not event:
        params['error'] = f'Мероприятия с id {event_id} не существует'
        return render_template("base.html", **params)
    if current_user not in event.members:
        params['error'] = f'Производить оплату могут только участники этого мероприятия'
        return render_template("base.html", **params)
    params['title'] = "Оплата"
    form = PayForm()
    form.user_to_id.choices = [(user.id, user.get_full_name()) for user in event.members
                               if user != current_user]
    params['form'] = form
    if form.validate_on_submit():
        if form.pay_sum.data <= 0:
            params['error'] = f'Для оплаты принимается только положительная сумма'
            return render_template("pay_form.html", **params)
        return redirect(f"/money/do_pay/{event_id}/{current_user.id}"
                        f"/{form.user_to_id.data}/{form.pay_sum.data}")
    return render_template("pay_form.html", **params)


@blueprint.route('/money/do_pay/<int:event_id>/<int:user_from_id>'
                 '/<int:user_to_id>/<float:pay_sum>')
@login_required
def do_pay(event_id, user_from_id, user_to_id, pay_sum):
    """ Обработчик, который производит оплату в пользу другого участника """
    params = {
        'app_name': APP_NAME,
    }
    session = db_session.create_session()
    event = session.query(Event).get(event_id)
    if not event:
        params['error'] = f'Мероприятия с id {event_id} не существует'
        return render_template("base.html", **params)
    for user_id in [user_from_id, user_to_id]:
        member = session.query(Member).get((event_id, user_id))
        if not member:
            params['error'] = f'Пользователь с id {user_id} не является участником ' \
                              f'мероприятия с id {event_id}'
            return render_template("base.html", **params)
    pay_sum = round(pay_sum, 2)
    if pay_sum <= 0:
        params['error'] = f'Сумма платежа не может быть отрицательной: {pay_sum}'
        return render_template("base.html", **params)

    money_from = session.query(Money).get((event_id, user_from_id))
    if not money_from:
        money_from = Money()
        money_from.event_id = event_id
        money_from.user_id = user_from_id
        event.money_list.append(money_from)
        session.merge(event)
    money_to = session.query(Money).get((event_id, user_to_id))
    if not money_to:
        money_to = Money()
        money_to.event_id = event_id
        money_to.user_id = user_from_id
        event.money_list.append(money_to)
        session.merge(event)

    # Добавление суммы плательщику и вычитание суммы у получателя
    money_from.cost += pay_sum
    money_to.cost -= pay_sum

    session.commit()
    return redirect(f"/events/{event_id}")
