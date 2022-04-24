from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField
from wtforms.validators import DataRequired


class EventForm(FlaskForm):
    """ Общая форма для мероприятия """
    title = StringField('Название', validators=[DataRequired()])
    is_private = BooleanField('Приватное мероприятие')
    is_done = BooleanField('Завершённое мероприятие')


class AddEventForm(EventForm):
    """ Форма добавления мероприятия """
    submit = SubmitField('Добавить')


class EditEventForm(EventForm):
    """ Форма изменения данных мероприятия """
    submit = SubmitField('Изменить')
