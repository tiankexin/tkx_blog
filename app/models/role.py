# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging
import datetime
from app.db.model import BaseModel
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL, SmallInteger, Date, DateTime, TEXT, Boolean
from app.db import Base
from app.db.wrapper import gen_db_session
from app.settings import DEFAULT_ROLES
from app.common.constant import DEFAULT_DB_NAME
from app.utils.serial import digit2str

logger = logging.getLogger(__name__)


class Role(Base, BaseModel):
    """
    Role table model
    """
    __tablename__ = "roles"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(64))
    default = Column(Boolean, default=False)
    permissions = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)

    @property
    def permission_str(self):
        """返回二进制字符串表现形式,易于理解"""
        ori_per = str(bin(self.permissions))
        pre = ori_per[0:2]
        return pre + digit2str(int(ori_per[2:]), total_len=8)

    @staticmethod
    def insert_roles():
        with gen_db_session(db=DEFAULT_DB_NAME, auto_commit=True) as s:
            for r in DEFAULT_ROLES:
                role = s.query(Role).filter(Role.name == r).first()
                if not role:
                    role = Role(name=r)
                role.permissions = DEFAULT_ROLES[r][0]
                role.default = DEFAULT_ROLES[r][1]
                s.add(role)
