from flask import Blueprint, render_template, redirect
from flask_login import login_user, login_required, logout_user
from data import db_session
from data.models import User
from forms.users_forms import RegisterForm, LoginForm
from constants import *


blueprint = Blueprint(
    'users_bp',
    __name__,
    template_folder='templates'
)


@blueprint.route("/users/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    params = {
        'app_name': APP_NAME,
        'title': "Регистрация",
        'form': form,
    }
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            params['error'] = "Пароли не совпадают"
            return render_template('register_form.html', **params)
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            params['error'] = "Такой пользователь уже есть"
            return render_template('register_form.html', **params)
        user = User()
        user.email = form.email.data
        user.surname = form.surname.data
        user.name = form.name.data
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        params['success'] = f'Пользователь "{user.get_full_name()}" успешно зарегистрирован'
    return render_template("register_form.html", **params)


@blueprint.route("/users/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    params = {
        'app_name': APP_NAME,
        'title': "Авторизация",
        'form': form,
    }
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        params['error'] = "Неправильный логин или пароль"
    return render_template('login_form.html', **params)


@blueprint.route('/users/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")
