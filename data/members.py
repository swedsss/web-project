import sqlalchemy
from data.db_session import SqlAlchemyBase


class Member(SqlAlchemyBase):
    __tablename__ = "members"
    event_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("events.id"),
                                 primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"),
                                primary_key=True)
