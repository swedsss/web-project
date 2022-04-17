from flask import Flask, render_template, request, make_response, jsonify
from flask_login import LoginManager
from flask_restful import Api
from data import db_session
from data.models import User
from blueprints import users_bp, events_bp
from api import users_resource, events_resource
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
    if request.user_agent.browser:
        params = {
            'app_name': APP_NAME,
            'error': 'Эту страницу могут увидеть только зарегистрированные пользователи!'
        }
        return render_template("base.html", **params)
    return make_response(jsonify({'error': error.name}), 401)


@app.errorhandler(404)
def not_found(error):
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
        'app_name': APP_NAME
    }
    return render_template('base.html', **params)


def main():
    db_session.global_init(DB_FILENAME)
    app.register_blueprint(users_bp.blueprint)
    app.register_blueprint(events_bp.blueprint)
    api.add_resource(users_resource.UserListResource, '/api/users')
    api.add_resource(users_resource.UserResource, '/api/users/<int:user_id>')
    api.add_resource(events_resource.EventListResource, '/api/events')
    api.add_resource(events_resource.EventResource, '/api/events/<int:event_id>')
    app.run(host=APP_HOST, port=APP_PORT)


if __name__ == '__main__':
    main()
