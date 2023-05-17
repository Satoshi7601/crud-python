# -*- coding: utf-8 -*- 
# @Time     : 2021/6/9 上午10:26
# @Author   : binger
from . import request, database

__BLUEPRINT_SET = {}


def register_blueprint(blueprint, **options):
    __BLUEPRINT_SET[blueprint] = options


def init_app(app):
    request.init_app(app)
    for blueprint, options in __BLUEPRINT_SET.items():
        app.register_blueprint(blueprint, **options)