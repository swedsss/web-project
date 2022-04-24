from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.users import User
from api.users_parser import *


def abort_if_user_not_found(user_id):
    """ Проверка на успешный поиск пользователя из запроса """
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"Пользователь с id {user_id} не найден")


class UserResource(Resource):
    def get(self, user_id):
        """ Получение информации о пользователе """
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify(
            {
                'user': user.to_dict(only=('email', 'surname', 'name'))
            }
        )

    def put(self, user_id):
        """ Изменение данных пользователя """
        args = parser.parse_args()
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        user.email = args['email']
        user.surname = args['surname']
        user.name = args['name']
        user.set_password(args['password'])
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, user_id):
        """ Удаление пользователя """
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        """ Получение информации о всех польщователях """
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify(
            {'users': [user.to_dict(only=('email', 'surname', 'name')) for user in users]})

    def post(self):
        """ Создание нового пользователя """
        args = parser.parse_args()
        session = db_session.create_session()
        user = User()
        user.email = args['email']
        user.surname = args['surname']
        user.name = args['name']
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
