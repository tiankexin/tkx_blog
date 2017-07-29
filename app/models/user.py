# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals
import datetime
import logging
from app.db import Base
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL, SmallInteger, Date, DateTime, TEXT, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager
from app.db.model import BaseModel
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


logger = logging.getLogger(__name__)


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
    confirmed = Column(Boolean, default=False)
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

    def generate_confirmation_token(self, expiration=3600):
        """
        生成加密验证token
        :param expiration: 过期时间
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def __repr__(self):
        return '<User %r>' % self.username


def confirm_user(user, token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except Exception as e:
        logger.error("serializer confirm token error, exec:{}".format(repr(e)))
        return False
    if data.get('confirm') != user.id:
        return False
    User.update_filter(User.id == user.id, **{"confirmed": True})
    return True


@login_manager.user_loader
def load_user(user_id):
    return User.query_one(User.id == int(user_id))
