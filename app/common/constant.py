#!/usr/bin/env python
# -*- coding:utf-8 -*-

DEFAULT_DB_NAME = 'blog'

# ========= user role permissions ========


class Permission(object):
    # 查看文章 0b00000001
    READ_ARTICLES = 0x01
    # 评论 0b00000010
    COMMENT = 0x02
    # 发表文章 0b00000100
    WRITE_ARTICLES = 0x04
    # 管理员权限 0b10000000
    ADMINISTER = 0x80

