#!/usr/bin/python
# -*- coding: UTF-8 -*-
import decimal
import uuid
import datetime

import simplejson
from flask import jsonify
from six import text_type
from flask.json import JSONEncoder as BaseJsonEncoder


# from push_center.model.mixins import DbMixin


def _get_duration_components(duration):
    days = duration.days
    seconds = duration.seconds
    microseconds = duration.microseconds

    minutes = seconds // 60
    seconds = seconds % 60

    hours = minutes // 60
    minutes = minutes % 60

    return days, hours, minutes, seconds, microseconds


def duration_iso_string(duration):
    if duration < datetime.timedelta(0):
        sign = '-'
        duration *= -1
    else:
        sign = ''

    days, hours, minutes, seconds, microseconds = _get_duration_components(duration)
    ms = '.{:06d}'.format(microseconds) if microseconds else ""
    return '{}P{}DT{:02d}H{:02d}M{:02d}{}S'.format(sign, days, hours, minutes, seconds, ms)


_JSON_ENCODER = {}


def register_json_encode(kind, do_encoder):
    _JSON_ENCODER[kind] = do_encoder


class JSONEncoder(BaseJsonEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time, decimal types, and
    UUIDs.
    """

    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        for kind, do_decoder in _JSON_ENCODER.items():
            if isinstance(o, kind):
                return do_decoder(o)

        if isinstance(o, datetime.datetime):
            if o.tzname():
                o = o.astimezone()

            return o.strftime("%Y-%m-%d %H:%M:%S")
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, datetime.timedelta):
            return duration_iso_string(o)
        elif isinstance(o, (decimal.Decimal, uuid.UUID)):
            return str(o)
        # elif isinstance(o, DbMixin):
        #     return o.to_dict()
        elif hasattr(o, '__html__'):
            return text_type(o.__html__())
        else:
            return super().default(o)


def json_loads(data, *args, **kwargs):
    """A custom JSON loading function which passes all parameters to the
    simplejson.loads function."""
    return simplejson.loads(data, *args, **kwargs)


def json_dumps(data, *args, **kwargs):
    """A custom JSON dumping function which passes all parameters to the
    simplejson.dumps function."""
    kwargs.setdefault('cls', JSONEncoder)
    return simplejson.dumps(data, *args, **kwargs)


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
