from flask import Flask, render_template, request, make_response, jsonify
from flask_login import LoginManager, current_user
from flask_restful import Api
from data import db_session
from data.users import User
from data.events import Event
from data.members import Member
from blueprints import users_bp, events_bp, members_bp, money_bp
from api import users_resource, events_resource, members_resource, money_resource
from constants import *

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = APP_SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.errorhandler(401)
def unauthorized(error):
    """ Обработчик для ошибки 401 (Unauthorized) """
    # Проверка на обработку запроса от браузера
    if request.user_agent.browser:
        params = {
            'app_name': APP_NAME,
            'error': 'Эту страницу могут увидеть только зарегистрированные пользователи!'
        }
        return render_template("base.html", **params)
    return make_response(jsonify({'error': error.name}), 401)


@app.errorhandler(404)
def not_found(error):
    """ Обработчик для ошибки 404 (Not found) """
    # Проверка на обработку запроса от браузера
    if request.user_agent.browser:
        params = {
            'app_name': APP_NAME,
            'error': 'Такой страницы не существует!'
        }
        return render_template("base.html", **params)
    return make_response(jsonify({'error': error.name}), 404)


@app.route("/")
def root():
    params = {
        'app_name': APP_NAME,
        'title': 'Список мероприятий'
    }
    event_list = []

    session = db_session.create_session()

    # Выбор мероприятий для авторизованных и анонимных пользователей
    if current_user.is_authenticated:
        events = session.query(Event).join(Member) \
            .filter((Event.is_private == False) | (Member.user_id == current_user.id)).all()
    else:
        events = session.query(Event).filter(Event.is_private == False).all()

    events.sort(key=lambda e: (e.is_done, -e.id))

    for event in events:
        manager = session.query(User).get(event.manager_id)
        event_list.append({'id': event.id,
                           'members_count': len(event.members),
                           'manager_id': event.manager_id,
                           'manager': f"{manager.get_full_name()}" if manager else '?',
                           'title': event.title,
                           'is_private': event.is_private,
                           'is_done': event.is_done,
                           'is_member': current_user.is_authenticated and current_user in event.members})
    params['event_list'] = event_list
    return render_template('event_list.html', **params)


def main():
    db_session.global_init(DB_FILENAME)

    # регистрация дополнительных схем с обработчиками
    app.register_blueprint(users_bp.blueprint)
    app.register_blueprint(events_bp.blueprint)
    app.register_blueprint(members_bp.blueprint)
    app.register_blueprint(money_bp.blueprint)

    # Добавление ресурсов для RESTful-API сервиса
    api.add_resource(users_resource.UserListResource, '/api/users')
    api.add_resource(users_resource.UserResource, '/api/users/<int:user_id>')
    api.add_resource(events_resource.EventListResource, '/api/events')
    api.add_resource(events_resource.EventResource, '/api/events/<int:event_id>')
    api.add_resource(members_resource.MemberListResource, '/api/members')
    api.add_resource(members_resource.MemberResource, '/api/members/<int:event_id>/<int:user_id>')
    api.add_resource(money_resource.MoneyListResource, '/api/money')
    api.add_resource(money_resource.MoneyResource, '/api/money/<int:event_id>/<int:user_id>')

    if LOCAL_MODE:
        app.run(host=LOCAL_HOST, port=LOCAL_PORT)


main()
