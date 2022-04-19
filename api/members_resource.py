from flask import jsonify
from flask_restful import Resource, abort
from api.users_resource import abort_if_user_not_found
from api.events_resource import abort_if_event_not_found
from data import db_session
from data.models import User, Event, Money, Member
from api.members_parser import parser


class MemberResource(Resource):
    def get(self, event_id, user_id):
        abort_if_event_not_found(event_id)
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        member = session.query(Member).get((event_id, user_id))
        if not member:
            abort(404, message=f"Пользователь с id {user_id} "
                               f"не является участником мероприятия с id {event_id}")
        event = session.query(Event).get(member.event_id)
        user = session.query(User).get(member.user_id)
        return jsonify({'member': {'event': event.title, 'user': user.get_full_name()}})

    def delete(self, event_id, user_id):
        abort_if_event_not_found(event_id)
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        member = session.query(Member).get((event_id, user_id))
        if not member:
            abort(404, message=f"Пользователь с id {user_id} "
                               f"не является участником мероприятия с id {event_id}")
        session.delete(member)
        money = session.query(Money).get((event_id, user_id))
        if money:
            session.delete(money)
        session.commit()
        return jsonify({'success': 'OK'})


class MemberListResource(Resource):
    def get(self):
        session = db_session.create_session()
        members = session.query(Member).all()

        members_list = []
        for member in members:
            event = session.query(Event).get(member.event_id)
            user = session.query(User).get(member.user_id)
            members_list.append({'event': event.title, 'user': user.get_full_name()})

        return jsonify({'members': members_list})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        member = session.query(Member).get((args['event_id'], args['user_id']))
        if member:
            abort(404, message=f"Пользователь с id {member.user_id} "
                               f"уже является участником мероприятия с id {member.event_id}")
        member = Member()
        member.event_id = args['event_id']
        member.user_id = args['user_id']
        session.add(member)
        session.commit()
        return jsonify({'success': 'OK'})
