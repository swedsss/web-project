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

    events = orm.relationship("Event", secondary="event_users", back_populates="users")
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

    users = orm.relationship("User", secondary="event_users", back_populates="events")
    money_list = orm.relationship("Money", back_populates="event")


class EventUser(SqlAlchemyBase):
    __tablename__ = "event_users"
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
        self.cost = floor(cost * 100) / 100
