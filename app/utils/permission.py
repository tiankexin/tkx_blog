from __future__ import absolute_import, unicode_literals
import functools
from flask import abort
from flask_login import current_user
from app.common.constant import Permission


def permission_required(perimission):

    def wrapper(fn):

        @functools.wraps(fn)
        def inner_wrapper(*args, **kwargs):
            if not current_user.can(perimission):
                abort(403)
            return fn(*args, **kwargs)

        return inner_wrapper
    return wrapper


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)

