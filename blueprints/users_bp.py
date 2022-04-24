from flask import Blueprint, render_template, redirect, request
from flask_login import login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
from forms.users_forms import RegisterForm, LoginForm, EditUserForm
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


@blueprint.route("/users/edit", methods=['GET', 'POST'])
@login_required
def edit_user():
    params = {
        'app_name': APP_NAME,
    }
    form = EditUserForm()
    params['title'] = "Редактировать данные пользователя"
    params['form'] = form
    if request.method == 'GET':
        form.email.data = current_user.email
        form.surname.data = current_user.surname
        form.name.data = current_user.name
    if form.validate_on_submit():
        session = db_session.create_session()
        same_user = session.query(User).filter(User.id != current_user.id,
                                               User.email == form.email.data).first()
        if same_user:
            params['error'] = f'Пользователь с такой электронной почтой уже существует'
            return render_template("base.html", **params)
        if form.password.data or form.password_again.data:
            if form.password.data != form.password_again.data:
                params['error'] = f'Пароли не совпадают'
                return render_template("base.html", **params)
            current_user.set_password(form.password.data)
        current_user.email = form.email.data
        current_user.surname = form.surname.data
        current_user.name = form.name.data
        session.merge(current_user)
        session.commit()
        params['success'] = f'Данные пользователя "{current_user.get_full_name()}" успешно сохранены'
    return render_template("edit_user_form.html", **params)


@blueprint.route("/users/delete", methods=['GET', 'POST'])
@login_required
def delete_user():
    params = {
        'app_name': APP_NAME,
    }
    session = db_session.create_session()
    user = session.query(User).get(current_user.id)
    for event in user.events:
        if current_user.id in event.sums_dict \
                and event.sums_total_dict[current_user.id]['balance'] != 0:
            params['error'] = f'У пользователя в мероприятии "{event.title}" ненулевой баланс'
            return render_template("base.html", **params)
    logout_user()
    session.delete(user)
    session.commit()
    return redirect("/")
