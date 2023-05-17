# -*- coding: utf-8 -*-
import os

from flask import Flask as FlaskBase

from .. import settings
from ..settings import extensions
from ..common.flask_mock import JSONEncoder


class Flask(FlaskBase):
    """A custom Flask app for Project"""
    json_encoder = JSONEncoder

    def __init__(self, *args, **kwargs):
        # kwargs.update({
        #     'template_folder': settings.STATIC_PUSHS_PATH,
        #     'static_folder': settings.STATIC_PUSHS_PATH,
        #     # 'static_path': '/static'
        # })
        super().__init__(__name__, *args, **kwargs)
        # Configure Asset using our settings
        # self.config.from_object('push_center.settings')
        self.config.from_object(settings)


def create_app():
    from . import auto_load
    app = Flask()
    app.secret_key = os.urandom(16).hex()

    # 需要填写蓝图定义
    # from .supplier import api as api_s
    # from .common import api as api_c
    # app.register_blueprint(api_s, url_prefix='/api/v1.0/supplier')
    # app.register_blueprint(api_c, url_prefix='')

    extensions.init_app(app)
    return app
