# -*- coding: utf-8 -*-
# @Time     : 2021/5/31 下午2:18
# @Author   : binger
import click
from flask import current_app
from flask.cli import FlaskGroup, run_command

from . import config
from .. import __version__
from ..app import create_app


def create(group):
    app = current_app or create_app()
    group.app = app

    return app


@click.group(cls=FlaskGroup, create_app=create)
def manager():
    """Management script for Redash"""


manager.add_command(config.manager, "config")
manager.add_command(run_command, "runserver")


@manager.command()
def version():
    """Displays Asset version."""
    print(__version__)


@manager.command()
def check_settings():
    print("check_settings")
    """Show the settings as Asset sees them (useful for debugging)."""
    for name, item in current_app.config.iteritems():
        print("{} = {}".format(name, item))
