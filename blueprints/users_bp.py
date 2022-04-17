from flask import Blueprint, render_template
from data import db_session
from data.models import User
from forms.users_forms import RegisterForm
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
        params['success'] = f'Пользователь "{user.name} {user.surname}" успешно зарегистрирован'
    return render_template("register_form.html", **params)
