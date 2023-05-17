# -*- coding: utf-8 -*-
# @Time     : 2019-07-22 14:17
# @Author   : binger
import sys
import time
import logging
import traceback
from .mock import MockResp
from .exception import BaseError, ProViewError
from flask import request, g

logger = logging.getLogger(__name__)


def collect_view_error(e):
    if not e:
        return e
    if isinstance(e, BaseError):
        logger.debug(sys.exc_info()[1])
        result = MockResp.exception(e)
    else:
        logger.error(sys.exc_info()[1])
        result = MockResp.fail(code=500, message=str(sys.exc_info()[1]))

    print("****** start Exception *****>>>>")
    print(type(sys.exc_info()[1]))
    print(sys.exc_info()[1])
    if not isinstance(e, ProViewError):
        print(traceback.print_exception(*sys.exc_info()))
    # sys.excepthook(*sys.exc_info())
    # from push_center.app.common.utils import record_error_event
    # record_error_event(title="api请求异常:", content=traceback.format_exc())
    print("<<<<**  end Exception  **********")
    return result


def before_request():
    """
    前置钩子
    :return:
    """

    # 框架记录入参参数
    if request.path == "/health_check":
        return

    if request.method in ("option", "OPTION"):
        logger.debug(">>> rcv(option): ", request.args)
        return "", 204
    elif request.method in ("get", "GET"):
        logger.debug(">>> rcv(get): {}".format(request.args))
    else:
        if request.headers.get("user-agent") == 'service':
            return MockResp.success()
        logger.info(">>> rcv(json): {}".format(request.json))

    g.start_time = time.time()
    return


def after_request(response):
    """
    后置钩子
    :param response:
    :return:
    """
    if request.path == "/health_check":
        return response

    if 'start_time' not in g:
        return response
    request_duration = (time.time() - g.start_time) * 1000
    queries_duration = g.get('queries_duration', 0.0)
    queries_count = g.get('queries_count', 0.0)
    endpoint = (request.endpoint or 'unknown').replace('.', '_')

    logger.info(
        "method=%s path=%s endpoint=%s status=%d content_type=%s content_length=%d duration=%.2f query_count=%d query_duration=%.2f",
        request.method,
        request.path,
        endpoint,
        response.status_code,
        response.content_type,
        response.content_length or -1,
        request_duration,
        queries_count,
        queries_duration)
    response.headers.add_header("server", f"ximalaya-security-xassets({request.host.split(':')[0]})")
    return response


def init_app(app):
    global logger
    # app.errorhandler(Exception)(collect_view_error)
    app.register_error_handler(Exception, collect_view_error)
    # app.teardown_request(collect_view_error)
    app.before_request(before_request)
    app.after_request(after_request)
    # logger = app.logger
