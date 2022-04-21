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
    pays_list = []

    def update_sums(self):
        self.__fill_sums_dicts()
        self.__fill_pays_list()

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
        avg = round(total_cost / count, 2)

        total_avg = 0.0
        for sums in self.sums_dict.values():
            sums['avg'] = avg
            total_avg += avg

        if total_avg != total_cost:
            self.sums_dict[self.manager_id]['avg'] += round(total_cost - total_avg, 2)

        for sums in self.sums_dict.values():
            sums['balance'] = round(sums['cost'] - sums['avg'], 2)

        self.sums_total_dict = {
            'count': count,
            'cost': total_cost,
            'avg': avg,
            'avg_plus': total_cost - total_avg,
        }

    def __fill_pays_list(self):
        self.pays_list.clear()

        pay_dict_from, pay_dict_to = {}, {}
        for user_id in self.sums_dict:
            balance = self.sums_dict[user_id]['balance']
            if balance < 0:
                balance = abs(balance)
                if balance not in pay_dict_from:
                    pay_dict_from[balance] = set()
                pay_dict_from[balance].add(user_id)
            elif balance > 0:
                if balance not in pay_dict_to:
                    pay_dict_to[balance] = set()
                pay_dict_to[balance].add(user_id)

        while len(pay_dict_from) > 0 and len(pay_dict_to) > 0:

            max_pay_from = max(pay_dict_from)
            max_pay_to = max(pay_dict_to)
            pay_sum = min([max_pay_from, max_pay_to])
            new_balance_from = round(max_pay_from - pay_sum, 2)
            new_balance_to = round(max_pay_to - pay_sum, 2)

            user_from = pay_dict_from[max_pay_from].pop()
            user_to = pay_dict_to[max_pay_to].pop()

            self.pays_list.append({
                'user_from': user_from,
                'user_to': user_to,
                'pay_sum': pay_sum,
                'new_balance_from': new_balance_from,
                'new_balance_to': new_balance_to
            })

            if len(pay_dict_from[max_pay_from]) == 0:
                del pay_dict_from[max_pay_from]

            if len(pay_dict_to[max_pay_to]) == 0:
                del pay_dict_to[max_pay_to]

            if new_balance_from > 0:
                if new_balance_from not in pay_dict_from:
                    pay_dict_from[new_balance_from] = set()
                pay_dict_from[new_balance_from].add(user_from)

            if new_balance_to > 0:
                if new_balance_to not in pay_dict_to:
                    pay_dict_to[new_balance_to] = set()
                pay_dict_to[new_balance_to].add(user_to)


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
