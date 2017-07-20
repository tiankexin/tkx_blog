from __future__ import absolute_import, unicode_literals
import datetime
from app.db import Base
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL, SmallInteger, Date, DateTime, TEXT
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager
from app.db.model import BaseModel


class User(Base, BaseModel, UserMixin):
    """
    user table model
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64))
    email = Column(String(128))
    role_id = Column(Integer)
    password_hash = Column(String(128))
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query_one(User.id == int(user_id))
