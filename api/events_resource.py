from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.users import User
from data.events import Event
from data.money import Money
from api.events_parser import *


def abort_if_event_not_found(event_id):
    """ Проверка на успешный поиск мероприятия из запроса """
    session = db_session.create_session()
    event = session.query(Event).get(event_id)
    if not event:
        abort(404, message=f"Мероприятие с id {event_id} не найдено")


class EventResource(Resource):
    def get(self, event_id):
        """ Получение информации о мероприятии """
        abort_if_event_not_found(event_id)
        session = db_session.create_session()
        event = session.query(Event).get(event_id)
        return jsonify(
            {
                'event': event.to_dict(only=('id', 'title', 'manager_id', 'is_private', 'is_done'))
            }
        )

    def put(self, event_id):
        """ Изменение данных мероприятия """
        args = parser.parse_args()
        abort_if_event_not_found(event_id)
        session = db_session.create_session()
        event = session.query(Event).get(event_id)
        event.title = args['title']
        event.manager_id = args['manager_id']
        event.is_private = bool(args['is_private'])
        event.is_done = bool(args['is_done'])
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, event_id):
        """ Удаление мероприятия """
        abort_if_event_not_found(event_id)
        session = db_session.create_session()
        event = session.query(Event).get(event_id)
        for money in event.money_list:
            session.delete(money)
        session.delete(event)
        session.commit()
        return jsonify({'success': 'OK'})


class EventListResource(Resource):
    def get(self):
        """ Получение информации о всех мероприятиях """
        session = db_session.create_session()
        events = session.query(Event).all()
        return jsonify(
            {'events': [event.to_dict(only=('id', 'title', 'manager_id', 'is_private', 'is_done'))
                        for event in events]})

    def post(self):
        """ Создание нового мероприятия """
        args = parser.parse_args()
        session = db_session.create_session()
        manager = session.query(User).get(args['manager_id'])
        if not manager:
            abort(404, message=f"Менеджер с id {args['manager_id']} не найден")
        event = Event()
        event.title = args['title']
        event.manager_id = manager.id
        event.is_private = args['is_private'] == 'True'
        event.is_done = args['is_done'] == 'True'
        manager.events.append(event)
        session.merge(manager)
        money = Money()
        money.event_id = event.id
        money.user_id = manager.id
        event.money_list.append(money)
        session.merge(event)
        session.commit()
        return jsonify({'success': 'OK'})
