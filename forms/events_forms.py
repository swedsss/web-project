from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField
from wtforms.validators import DataRequired


class EventForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    is_private = BooleanField('Приватное мероприятие')
    is_done = BooleanField('Мероприятие завершено')


class AddEventForm(EventForm):
    submit = SubmitField('Добавить')


class EditEventForm(EventForm):
    submit = SubmitField('Изменить')
