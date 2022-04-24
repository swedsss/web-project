from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField, StringField, BooleanField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    """ Форма регистрации """
    email = EmailField('Электронная почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    """ Форма авторизации """
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class EditUserForm(FlaskForm):
    """ Форма редактирования данных пользователя """
    email = EmailField('Электронная почта', validators=[DataRequired()])
    password = PasswordField('Новый пароль')
    password_again = PasswordField('Повторите пароль')
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
