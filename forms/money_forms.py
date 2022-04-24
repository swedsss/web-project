from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired


class EditMoneyForm(FlaskForm):
    """ Форма для изменения потраченной суммы участника """
    cost = FloatField("Потраченная сумма")
    submit = SubmitField('Изменить')


class PayForm(FlaskForm):
    """ Форма для оплаты """
    user_to_id = SelectField('Выберите получателя', coerce=int)
    pay_sum = FloatField("Сумма платежа", validators=[DataRequired()])
    submit = SubmitField('Оплатить')
