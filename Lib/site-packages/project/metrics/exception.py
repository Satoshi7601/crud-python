# -*- coding: utf-8 -*-
# @Time     : 2019-07-22 14:06
# @Author   : binger


class BaseError(Exception):
    def __init__(self, code, message=""):
        super(BaseError, self).__init__(code, message)

    def __len__(self):
        return len(self.args)


class ProRunError(BaseError): pass


class ProArgError(BaseError): pass


class ProViewError(BaseError): pass


class TypeExtend(type):
    def __init__(self, class_name, class_parents, class_attr):
        if class_name != "ErrorCode":
            self.__code__ = class_attr["__code__"]
        super(TypeExtend, self).__init__(class_name, class_parents, class_attr)

    def __getattribute__(self, item):
        value = type.__getattribute__(self, item)
        if item != "__code__":
            return self.__code__ + value
        else:
            return value


# 状态码
class ErrorCode(metaclass=TypeExtend):
    unKnow = 999  # 位置错误
    invalid = 998  # 无效
    timeout = 997  # 请求超时
    no_found = 996  # 不存在

    # 服务\处理
    busy = 989  # 服务器忙
    no_allow = 987  # 被拒绝
    illegal = 986  # 非法操作
    is_running = 985  # 任务正在运行
    is_ban_run = 984  # 限制运行
    is_existed = 983  # 已经存在
    error_exit = 982  # 异常退出
    build_fail = 981  # 创建，构建失败
    plugin_error = 980  # 插件异常

    # 登陆
    token_invalid = 949

    # 参数
    arg_error = 899  # 参数错误
    format_error = 898  # 格式错误
    arg_miss = 897  # 缺少参数
    len_limit = 896  # 长度受限
    invalid_route = 895  # 无效的路由、路径

    server_error = 500


class ViewErrorCode(ErrorCode):
    __code__ = 10000


class DBErrorCode(ErrorCode):
    __code__ = 20000


class RunErrorCode(ErrorCode):
    __code__ = 30000


class ArgErrorCode(ErrorCode):
    __code__ = 40000


if __name__ == "__main__":
    pass
