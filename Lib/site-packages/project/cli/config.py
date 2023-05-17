# -*- coding: utf-8 -*-
# @Time     : 2021/4/6 上午9:46
# @Author   : binger
import os
import sys
from pathlib import Path

from flask.cli import AppGroup
from jinja2 import Environment, FileSystemLoader

manager = AppGroup(help="Manage config (create/remove config).")
ROOT = os.path.abspath(os.path.curdir)
env = Environment(loader=FileSystemLoader(os.path.join(ROOT, "etc", "tpl")))


def get_env(key, default=None):
    key = f"TH_{key}"
    return os.getenv(key, default)


HOST = get_env("HOST", "127.0.0.1:7300") or "127.0.0.1:7300"
PROJECT_NAME = get_env("PROJECT_NAME", os.path.basename(ROOT)) or os.path.basename(ROOT)
ALIAS = get_env('ALIAS', PROJECT_NAME) or PROJECT_NAME
# LOG_LEVEL = (get_env("LOG_LEVEL", "INFO") or "INFO").upper()
LOG_ROOT = get_env("LOG_ROOT", os.path.join(ROOT, "log")) or os.path.join(ROOT, "log")
VENV_PATH = get_env("VENV_PATH", os.path.join(ROOT, "venv")) or os.path.join(ROOT, "venv")
PROTOCOL = get_env("PROTOCOL", "socket") or "socket"


def _create_wsgi_conf(dst_path=None):
    print("create wsgi tpl...")
    dst_path = dst_path or os.path.join(ROOT, "etc", "wsgi.ini")

    template = env.get_template("wsgi.ini.tpl")
    with open(dst_path, "w") as fw:
        fw.write(template.render(
            host=HOST,
            directory=ROOT,
            project_venv=VENV_PATH,
            project_name=PROJECT_NAME,
            protocol=PROTOCOL
        ))
    print("wsgi tpl path:", dst_path)


def _create_web_conf(dst_path=None, wsgi_conf_path=None):
    print("create web tpl...")
    name = f"{ALIAS}_web"
    dst_path = dst_path or os.path.join(ROOT, "etc", "supervisord", f"{name}.ini")
    wsgi_conf_path = wsgi_conf_path or f"{ROOT}/etc/wsgi.ini"
    # os.makedirs(LOG_ROOT, mode=0o755, exist_ok=True)
    Path(dst_path).parent.mkdir(exist_ok=True)

    # uwsgi --ini /opt/pushservice/etc/wsgi.ini
    command = f"/bin/sh -c '{sys.prefix}/bin/uwsgi --ini {wsgi_conf_path}'"

    template = env.get_template("supervisor.ini.tpl")
    with open(dst_path, "w") as fw:
        fw.write(template.render(
            name=name,
            command=command,
            process_name="%(program_name)s",
            logfile=f"{LOG_ROOT}/%(program_name)s.log",
            numprocs=1,
            directory=ROOT,
        ))
    print("web tpl path:", dst_path)


def _create_logrotate_conf(dst_path=None):
    print("create logrotate tpl...")
    dst_path = dst_path or os.path.join(ROOT, "etc", "logrotate", PROJECT_NAME)
    Path(dst_path).parent.mkdir(exist_ok=True)

    template = env.get_template("logrotate.tpl")

    with open(dst_path, "w") as fw:
        fw.write(template.render(
            project_name=PROJECT_NAME,
            logfile=f"{LOG_ROOT}/{ALIAS}_*.log",
        ))
    print("logrotate tpl path:", dst_path)


@manager.command()
def create_wsgi_conf(dst_path=None):
    _create_wsgi_conf(dst_path)


@manager.command()
def create_web_conf(dst_path=None, wsgi_conf_path=None):
    _create_web_conf(dst_path, wsgi_conf_path)


@manager.command()
def create_logrotate_conf(dst_path=None):
    _create_logrotate_conf(dst_path)


@manager.command()
def create():
    print("create tpl...")
    _create_wsgi_conf()
    _create_web_conf()
    _create_logrotate_conf()
    print("create over.")
