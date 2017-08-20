# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals
import datetime
import logging
import hashlib
from app.db import Base
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL, SmallInteger, Date, DateTime, TEXT, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from app import login_manager
from app.db.model import BaseModel
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.common.constant import Permission
from flask import current_app, request
from app.models.role import Role


logger = logging.getLogger(__name__)


class User(Base, BaseModel, UserMixin):
    """
    user table model
    """
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    username = Column(String(64))
    email = Column(String(128))
    role_id = Column(Integer)
    password_hash = Column(String(128))
    confirmed = Column(Boolean, default=False)
    avatar_hash = Column(String(32))
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role_id is None:
            default_role = Role.query_one(Role.default == True)
            self.role_id = default_role.id
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

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

    def can(self, permissions):
        role = Role.query_one(Role.id == self.role_id)
        return role is not None and (role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def update_last_seen(self):
        UserProfile.update_filter(UserProfile.user_id == self.id, **{'last_seen': datetime.datetime.now()})

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


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


class UserProfile(Base, BaseModel):

    __tablename__ = 'user_profile'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    name = Column(String(64), default="")
    location = Column(String(64), default="来自火星")
    about_me = Column(TEXT, default="该用户很懒, 什么都没留下")
    last_seen = Column(DateTime, default=datetime.datetime.now)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)

