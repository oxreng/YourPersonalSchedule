import sqlalchemy
from sqlalchemy import orm
import datetime
from .db_session import SqlAlchemyBase


class Task(SqlAlchemyBase):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    date_start = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    date_end = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    time_start = sqlalchemy.Column(sqlalchemy.Time, nullable=False)
    time_end = sqlalchemy.Column(sqlalchemy.Time, nullable=False)

    users_relationship = orm.relationship("User", back_populates="tasks_relationship")
