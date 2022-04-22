from math import floor

import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


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
        avg = round(floor(total_cost / count * 100) / 100, 2)

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

            pay_sum_from = max(pay_dict_from)
            pay_sum_to = pay_sum_from if pay_sum_from in pay_dict_to else max(pay_dict_to)

            pay_sum = min([pay_sum_from, pay_sum_to])
            new_balance_from = round(pay_sum - pay_sum_from, 2)
            new_balance_to = round(pay_sum_to - pay_sum, 2)

            user_from = pay_dict_from[pay_sum_from].pop()
            user_to = pay_dict_to[pay_sum_to].pop()

            self.pays_list.append({
                'user_from': user_from,
                'user_to': user_to,
                'pay_sum': pay_sum,
                'new_balance_from': new_balance_from,
                'new_balance_to': new_balance_to
            })

            if len(pay_dict_from[pay_sum_from]) == 0:
                del pay_dict_from[pay_sum_from]

            if len(pay_dict_to[pay_sum_to]) == 0:
                del pay_dict_to[pay_sum_to]

            if new_balance_from < 0:
                new_balance_from = abs(new_balance_from)
                if new_balance_from not in pay_dict_from:
                    pay_dict_from[new_balance_from] = set()
                pay_dict_from[new_balance_from].add(user_from)

            if new_balance_to > 0:
                if new_balance_to not in pay_dict_to:
                    pay_dict_to[new_balance_to] = set()
                pay_dict_to[new_balance_to].add(user_to)
