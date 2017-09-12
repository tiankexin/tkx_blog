# -*- coding:utf-8 -*-
import os
from flask import Blueprint, url_for, app

main = Blueprint('main', __name__)

from . import view, errors
from app.common.constant import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@main.app_context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    """
    因为flask从static目录读取静态文件css或js会由于浏览器缓存的原因,导致更改不会发生
    动态变化, 所以需要重写url_for,来加入文件最后修改时间的时间戳来解决这个问题
    :param endpoint:
    :param values:
    :return:
    """
    print 'aaaaaaaa'
    root_path = os.path.abspath(os.path.dirname("app/__init__.py"))
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    print 'bbbbbbbb', url_for(endpoint, **values)
    return url_for(endpoint, **values)
