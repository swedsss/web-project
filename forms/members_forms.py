from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired


class InviteUserForm(FlaskForm):
    user_id = SelectField('Выберите пользователя', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Добавить')
