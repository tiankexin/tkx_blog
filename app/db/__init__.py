from __future__ import absolute_import, unicode_literals
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.settings import DB_SETTINGS

Base = declarative_base()
engines = {}


def init_engines():
    for k, v in DB_SETTINGS.viewitems():
        engines[k] = create_engine(v["urls"], pool_size=50, pool_recycle=1200, echo=False)

init_engines()


class DBSession(object):

    def __init__(self):
        self.session_map = {}
        self.init_session()

    def init_session(self):
        self.session_map = {
            key: scoped_session(sessionmaker(bind=engines[key], expire_on_commit=False))
            for key in DB_SETTINGS.keys()}

    def using_bind(self, name='default'):

        if name not in self.session_map:
            raise ValueError("{0} is not in register db engines".format(name))
        return self.session_map[name]()

db_session = DBSession()
