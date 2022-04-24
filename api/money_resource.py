from flask import jsonify
from flask_restful import Resource, abort
from api.users_resource import abort_if_user_not_found
from api.events_resource import abort_if_event_not_found
from data import db_session
from data.users import User
from data.events import Event
from data.money import Money
from data.members import Member
from api.money_parser import parser_full, parser_sums


class MoneyResource(Resource):
    def get(self, event_id, user_id):
        """ Получение информации о сумме участника """
        abort_if_event_not_found(event_id)
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        money = session.query(Money).get((event_id, user_id))
        if not money:
            abort(404, message=f"У пользователя с id {user_id} "
                               f"отсутствует сумма для мероприятия с id {event_id}")
        event = session.query(Event).get(money.event_id)
        user = session.query(User).get(money.user_id)
        return jsonify(
            {'money': {'event': event.title, 'user': user.get_full_name(), 'cost': money.cost}})

    def put(self, event_id, user_id):
        """ Изменение суммы участника """
        args = parser_sums.parse_args()
        session = db_session.create_session()
        money = session.query(Money).get((event_id, user_id))
        if not money:
            abort(404, message=f"У пользователя с id {user_id} "
                               f"отсутствует сумма для мероприятия с id {event_id}")
        money.cost = args['cost']
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, event_id, user_id):
        """ Удаление суммы участника """
        abort_if_event_not_found(event_id)
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        money = session.query(Money).get((event_id, user_id))
        if not money:
            abort(404, message=f"У пользователя с id {user_id} "
                               f"отсутствует сумма для мероприятия с id {event_id}")
        session.delete(money)
        money = session.query(Money).get((event_id, user_id))
        if money:
            session.delete(money)
        session.commit()
        return jsonify({'success': 'OK'})


class MoneyListResource(Resource):
    def get(self):
        """ Получение информации о всех суммах всех участников """
        session = db_session.create_session()
        money_objects = session.query(Money).all()

        money_list = []
        for money in money_objects:
            event = session.query(Event).get(money.event_id)
            user = session.query(User).get(money.user_id)
            money_list.append(
                {'event': event.title, 'user': user.get_full_name(), 'cost': money.cost})

        return jsonify({'money_list': money_list})

    def post(self):
        """ Добавление суммы участника """
        args = parser_full.parse_args()
        session = db_session.create_session()
        money = session.query(Money).get((args['event_id'], args['user_id']))
        if money:
            abort(404, message=f"У пользователя с id {args['user_id']} "
                               f"уже есть сумма для мероприятия с id {args['event_id']}")
        member = session.query(Member).get((args['event_id'], args['user_id']))
        if not member:
            abort(404, message=f"Пользователь с id {args['user_id']} "
                               f"не является участником мероприятия с id {args['event_id']}")
        money = Money()
        money.event_id = args['event_id']
        money.user_id = args['user_id']
        money.set_cost(args['cost'])
        session.add(money)
        session.commit()
        return jsonify({'success': 'OK'})
