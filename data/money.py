import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase


class Money(SqlAlchemyBase):
    """ Модель "Деньги" """
    __tablename__ = "money"

    event_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("events.id"),
                                 primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"),
                                primary_key=True)
    cost = sqlalchemy.Column(sqlalchemy.Float, default=0.00)

    user = orm.relationship("User", back_populates="money_list")
    event = orm.relationship("Event", back_populates="money_list")

    def get_cost_text(self):
        """ Возврат суммы в текстовом виде с 2мя знаками после запятой """
        return f'{self.cost:.2f}'

    def set_cost(self, cost):
        """ Округление суммы до 2х знаков после запятой """
        self.cost = round(float(cost), 2)
