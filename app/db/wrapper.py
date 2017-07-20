#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    提供清算相关DB操作
"""
import functools

from sqlalchemy.orm.exc import NoResultFound
from contextlib import contextmanager
from . import db_session


@contextmanager
def gen_db_session(db="default", auto_commit=False, auto_flush=False, need_close=True):
    session = db_session.using_bind(db)
    try:
        yield session
        if auto_flush:
            session.flush()
        if auto_commit:
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        if need_close:
            session.close()


def cls_transaction(readonly=False):
    """ model方法事务装时器 """

    def wrapper(fn):
        @functools.wraps(fn)
        def inner_wrapper(*args, **kwargs):
            args = list(args)
            cls = args.pop(0)
            db_name = cls.__db_alias__
            session = db_session.using_bind(db_name)
            try:
                result = fn(cls, session, *args, **kwargs)
                if not readonly:
                    session.commit()
                return result
            except NoResultFound:
                return None
            except Exception as e:
                if not readonly:
                    session.rollback()
                raise e
            finally:
                if session:
                    session.close()

        return inner_wrapper

    return wrapper
