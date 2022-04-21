from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired


class EditMoneyForm(FlaskForm):
    cost = FloatField("Потраченная сумма", validators=[DataRequired()])
    submit = SubmitField('Изменить')


class PayForm(FlaskForm):
    user_to_id = SelectField('Выберите получателя', coerce=int)
    pay_sum = FloatField("Сумма платежа", validators=[DataRequired()])
    submit = SubmitField('Оплатить')
