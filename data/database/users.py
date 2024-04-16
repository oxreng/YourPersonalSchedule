from .db_session import SqlAlchemyBase
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    bday = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    avatar = sqlalchemy.Column(sqlalchemy.Text, nullable=True, default=None)

    calendar_relationship = orm.relationship("Calendar", back_populates="users_relationship")
    notes_relationship = orm.relationship("Note", back_populates="users_relationship")
    tasks_relationship = orm.relationship("Task", back_populates="users_relationship")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
