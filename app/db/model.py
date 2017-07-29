#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    DB封装重写
"""
from app.db.wrapper import cls_transaction
from app.common import constant
from sqlalchemy.orm import class_mapper


class BaseModel(object):
    """ 基础Model """

    __db_alias__ = constant.DEFAULT_DB_NAME
    __table__ = None

    @cls_transaction(readonly=False)
    def add(self, session):
        session.add(self)
        return self

    def asdict(self):
        return dict((col.name, getattr(self, col.name))
                    for col in class_mapper(self.__class__).mapped_table.c)

    def self_update(self, update_dict):
        params = dict(update_dict)
        for k, v in params.viewitems():
            if not hasattr(self, k):
                continue
            setattr(self, k, v)

    @classmethod
    @cls_transaction(readonly=False)
    def update_filter(cls, session, *query_conditions, **update_content):
        return session.query(cls).filter(*query_conditions).update(update_content, synchronize_session='fetch')

    @classmethod
    @cls_transaction(readonly=True)
    def query_all(cls, session, *query_conditions, **other_limits):
        return_fields = other_limits.pop('_fields') if '_fields' in other_limits else None
        query = session.query(*return_fields) if return_fields else session.query(cls)

        if query_conditions:
            query = query.filter(*query_conditions)

        group_by = other_limits.get("_group_by")
        order_by = other_limits.get("_order_by")
        offset = other_limits.get('offset')
        limit = other_limits.get('limit') or other_limits.get('page_size')

        query = query.group_by(*group_by) if group_by else query
        query = query.order_by(*order_by) if order_by else query

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        return query.all()

    @classmethod
    @cls_transaction(readonly=True)
    def query_one(cls, session, *query_conditions, **other_limits):
        return_fields = other_limits.pop('_fields') if '_fields' in other_limits else None
        query = session.query(*return_fields) if return_fields else session.query(cls)
        if query_conditions:
            query = query.filter(*query_conditions)

        group_by = other_limits.get("_group_by")
        order_by = other_limits.get("_order_by")
        offset = other_limits.get('offset')
        limit = other_limits.get('limit') or other_limits.get('page_size')

        query = query.group_by(*group_by) if group_by else query
        query = query.order_by(*order_by) if order_by else query
        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        return query.one()
