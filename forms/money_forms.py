from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, SelectField, FloatField
from wtforms.validators import DataRequired


class EditMoneyForm(FlaskForm):
    cost = FloatField("Потраченная сумма", validators=[DataRequired()])
    submit = SubmitField('Изменить')
