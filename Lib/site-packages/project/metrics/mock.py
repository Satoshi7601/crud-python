#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime

from flask import jsonify

from ..model.mixins import DbMixin
from ..common.flask_mock import register_json_encode

register_json_encode(DbMixin, lambda o: o.to_dict())


class MockResp(object):
    """
    api对外暴露统一的接口
    """

    @staticmethod
    def success(data=None, message='success', code=0, desc=''):
        """
        返回成功调用方法
        :param desc:
        :param data:
        :param message:
        :param code:
        :return:
        """
        obj = dict(code=code, message=message, desc=desc)
        obj['data'] = data
        obj["time"] = datetime.datetime.now()
        return jsonify(obj)

    @staticmethod
    def fail(message, code=500, data=None, desc=''):
        """
        返回失败调用方法
        :param desc:
        :param message:
        :param code:
        :param data:
        :return:
        """
        obj = dict(code=code, message=message, desc=desc)
        obj['data'] = data
        obj["time"] = datetime.datetime.now()
        return jsonify(obj)

    @classmethod
    def exception(cls, e):
        return cls.fail(code=e.args[0], message=e.args[1])
