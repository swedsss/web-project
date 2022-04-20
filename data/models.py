from math import floor

import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)

    events = orm.relationship("Event", secondary="members", back_populates="members")
    money_list = orm.relationship("Money", back_populates="user")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def get_full_name(self):
        return f"{self.name} {self.surname}"


def float_to_sum(f):
    return round(floor(f * 100) / 100, 2)


class Event(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "events"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    manager_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    is_private = sqlalchemy.Column(sqlalchemy.Boolean)
    is_done = sqlalchemy.Column(sqlalchemy.Boolean)

    members = orm.relationship("User", secondary="members", back_populates="events")
    money_list = orm.relationship("Money", back_populates="event")

    sums_dict = {}
    sums_total_dict = {}

    def update_dicts(self):
        self.__fill_sums_dicts()

    def __fill_sums_dicts(self):
        self.sums_dict.clear()
        self.sums_total_dict.clear()

        for member in self.members:
            self.sums_dict[member.id] = {
                'cost': 0.0,
                'avg': 0.0,
                'balance': 0.0
            }

        for money in self.money_list:
            if money.user_id not in self.sums_dict:
                continue
            self.sums_dict[money.user_id] = {
                'cost': money.cost,
                'avg': 0.0,
                'balance': 0.0
            }

        total_cost = 0.0
        for sums in self.sums_dict.values():
            total_cost += sums['cost']
        count = len(self.sums_dict)
        avg = float_to_sum(total_cost / count)

        total_avg = 0.0
        for sums in self.sums_dict.values():
            sums['avg'] = avg
            total_avg += avg

        if total_avg != total_cost:
            self.sums_dict[self.manager_id]['avg'] += round(total_cost - total_avg, 2)

        for sums in self.sums_dict.values():
            sums['balance'] = float_to_sum(sums['cost'] - sums['avg'])

        self.sums_total_dict = {
            'count': count,
            'cost': total_cost,
            'avg': avg,
            'avg_plus': total_cost - total_avg,
        }


class Member(SqlAlchemyBase):
    __tablename__ = "members"
    event_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("events.id"),
                                 primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"),
                                primary_key=True)


class Money(SqlAlchemyBase):
    __tablename__ = "money"
    event_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("events.id"),
                                 primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"),
                                primary_key=True)
    cost = sqlalchemy.Column(sqlalchemy.Float, default=0.00)

    user = orm.relationship("User", back_populates="money_list")
    event = orm.relationship("Event", back_populates="money_list")

    def get_cost_text(self):
        return f'{self.cost:.2f}'

    def set_cost(self, cost):
        self.cost = floor(float(cost) * 100) / 100
