# -*- coding: utf-8 -*-

__version__ = '0.1'
__project__ = __package__

import logging
import sys

from . import settings

print("version: {} {}".format(__project__, __version__))


def setup_logging():
    handler = logging.StreamHandler(sys.stdout if settings.LOG_STDOUT else sys.stderr)
    formatter = logging.Formatter(settings.LOG_FORMAT)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    update_stream_name = handler.stream.name
    for index, _handler in enumerate(root.handlers):
        if getattr(_handler, 'stream', None) and _handler.stream.name == update_stream_name:
            root.handlers[index] = handler
            break
    else:
        logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(settings.LOG_LEVEL)


setup_logging()
