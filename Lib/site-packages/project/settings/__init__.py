# -*- coding: utf-8 -*-

import os
from datetime import timedelta
from pathlib import Path

from ..common.utils import int_or_none, parse_boolean
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

PROPAGATE_EXCEPTIONS = True  # 异常穿透
JSON_AS_ASCII = False

PERMANENT_SESSION_LIFETIME = timedelta(days=1)  # 设置cookie 的时间为1天

SECRET_KEY = os.urandom(16).hex()
ISSUER = "6EF8D1EE92DF402083021CC6C972F4EF"
ALIAS = "AWD"


def get_env(key, default, can_false=False):
    v = os.environ.get(f"{ALIAS}_{key}", default)
    if not v and not can_false:
        return default
    return v


##############
# 路径 配置 #
##############
ROOT_PATH = str(Path(os.path.abspath(os.path.dirname(__file__))).parent.parent)
UPLOAD_PATH = os.path.join(ROOT_PATH, "data", "upload")
os.makedirs(UPLOAD_PATH, exist_ok=True)
CONF_PATH = os.path.join(ROOT_PATH, "etc", "tpl")

#####################
# 日志 logging 配置 #
#####################
LOG_LEVEL = get_env("LOG_LEVEL", "INFO")
LOG_STDOUT = parse_boolean(get_env('LOG_STDOUT', 'false'))
__LOG_PREFIX = get_env('LOG_PREFIX', '')
LOG_FORMAT = get_env('LOG_FORMAT',
                     __LOG_PREFIX + "[%(asctime)s] [%(module)12s:%(funcName)16s:%(lineno)04d] [%(levelname)8s] [%(threadName)s] %(message)s")
