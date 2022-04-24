from math import floor

import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Event(SqlAlchemyBase, SerializerMixin):
    """ Модель "Мероприятия" """
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
        """ Расчёт сумм мероприятия """
        self.__fill_sums_dicts()
        self.__fill_pays_list()

    def __fill_sums_dicts(self):
        """ Расчёт средней суммы и баланса для каждого участника мероприятия """
        self.sums_dict.clear()
        self.sums_total_dict.clear()

        # Создание словаря для сумм
        for member in self.members:
            self.sums_dict[member.id] = {
                'cost': 0.0,
                'avg': 0.0,
                'balance': 0.0
            }

        # Заполнение потраченной суммы
        for money in self.money_list:
            if money.user_id not in self.sums_dict:
                continue
            self.sums_dict[money.user_id] = {
                'cost': money.cost,
                'avg': 0.0,
                'balance': 0.0
            }

        # Расчёт общей потраченной суммы и средней суммы
        total_cost = 0.0
        for sums in self.sums_dict.values():
            total_cost += sums['cost']
        count = len(self.sums_dict)
        avg = round(floor(total_cost / count * 100) / 100, 2)

        # Расчёт дополнительной суммы для менеджера мероприятия
        total_avg = 0.0
        for sums in self.sums_dict.values():
            sums['avg'] = avg
            total_avg += avg

        if total_avg != total_cost:
            self.sums_dict[self.manager_id]['avg'] += round(total_cost - total_avg, 2)

        # Расчёт баланса
        for sums in self.sums_dict.values():
            sums['balance'] = round(sums['cost'] - sums['avg'], 2)

        # Заполненеи словаря с итоговыми суммами
        self.sums_total_dict = {
            'count': count,
            'cost': total_cost,
            'avg': avg,
            'avg_plus': total_cost - total_avg,
        }

    def __fill_pays_list(self):
        """ Расчёт сумм для списка выплат """
        self.pays_list.clear()

        # Создание словарей с абсолютными суммами в качестве ключей и множеством участников
        pay_dict_from, pay_dict_to = {}, {}
        for user_id in self.sums_dict:
            balance = self.sums_dict[user_id]['balance']
            if balance < 0:
                # Словарь для отправителей
                balance = abs(balance)
                if balance not in pay_dict_from:
                    pay_dict_from[balance] = set()
                pay_dict_from[balance].add(user_id)
            elif balance > 0:
                # Словарь для получателей
                if balance not in pay_dict_to:
                    pay_dict_to[balance] = set()
                pay_dict_to[balance].add(user_id)

        # При формировании списка оплат
        # обработанные отправители и получатели будут удаляться из словарей.
        # Это будет продолжаться до опустошения хотя бы одного из словарей
        while len(pay_dict_from) > 0 and len(pay_dict_to) > 0:

            # Выбор максимальной суммы из словаря отправителя
            pay_sum_from = max(pay_dict_from)
            # Выбор суммы получателя, равной сумме отправителя, или максимальной суммы
            pay_sum_to = pay_sum_from if pay_sum_from in pay_dict_to else max(pay_dict_to)

            # Окончательное вычисление суммы платежа
            pay_sum = min([pay_sum_from, pay_sum_to])
            # Расчёт баланса для отправителя и получателя после оплаты
            new_balance_from = round(pay_sum - pay_sum_from, 2)
            new_balance_to = round(pay_sum_to - pay_sum, 2)

            # Определение пользователей (отправителя и получателя)
            user_from = pay_dict_from[pay_sum_from].pop()
            user_to = pay_dict_to[pay_sum_to].pop()

            # Добавление выплаты в список получателей
            self.pays_list.append({
                'user_from': user_from,
                'user_to': user_to,
                'pay_sum': pay_sum,
                'new_balance_from': new_balance_from,
                'new_balance_to': new_balance_to
            })

            # Удаление суммы из словаря, если все отправители с такой суммой уже обработаны
            if len(pay_dict_from[pay_sum_from]) == 0:
                del pay_dict_from[pay_sum_from]

            # Удаление суммы из словаря, если все получатели с такой суммой уже обработаны
            if len(pay_dict_to[pay_sum_to]) == 0:
                del pay_dict_to[pay_sum_to]

            # Если после оплаты у отправителя баланс не стал нулевым,
            # то он возвращается в словарь отправителей с новой суммой баланса
            if new_balance_from < 0:
                new_balance_from = abs(new_balance_from)
                if new_balance_from not in pay_dict_from:
                    pay_dict_from[new_balance_from] = set()
                pay_dict_from[new_balance_from].add(user_from)

            # Если после оплаты у получателя баланс не стал нулевым,
            # то он возвращается в словарь получателей с новой суммой баланса
            if new_balance_to > 0:
                if new_balance_to not in pay_dict_to:
                    pay_dict_to[new_balance_to] = set()
                pay_dict_to[new_balance_to].add(user_to)
