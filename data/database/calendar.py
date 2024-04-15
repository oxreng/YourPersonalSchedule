import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Calendar(SqlAlchemyBase):
    __tablename__ = 'calendar'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    datetime_start = sqlalchemy.Column(sqlalchemy.DateTime)
    datetime_end = sqlalchemy.Column(sqlalchemy.DateTime)

    users_relationship = orm.relationship("User", back_populates="calendar_relationship")
