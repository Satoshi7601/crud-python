# -*- coding: utf-8 -*-
import re
import functools
from contextlib import contextmanager

from flask_sqlalchemy import BaseQuery, SQLAlchemy
# from psycopg2 import IntegrityError
# from psycopg2._psycopg import IntegrityError
from sqlalchemy.exc import IntegrityError, DataError

from ..metrics.exception import ProRunError, DBErrorCode

db = SQLAlchemy(session_options={'expire_on_commit': False})
Column = functools.partial(db.Column, nullable=False)


@contextmanager
def get_session():
    session = db.session
    try:
        yield session
        session.flush()
    except IntegrityError as e:
        # e.params # 参数
        # e.statement  # sql
        session.rollback()
        if "unique constraint" in e.args[0]:
            raise ProRunError(DBErrorCode.no_allow, "已经存在：添加的信息已经存在，不允许添加")
        else:
            raise ProRunError(DBErrorCode.no_allow, e.args[0])
        # resp = re.search("\)\s(?P<title>.+)\n(?P<detail>.+)\n", e.args[0])
        # if resp:
        #     info = resp.groupdict()
        #     raise ProRunError(DBErrorCode.no_allow, f"{info['title']}\n{info['detail'].replace('DETAIL:  ', '')}")
        # else:
        #     raise ProRunError(DBErrorCode.no_allow, e.args[0])
    except DataError as e:
        session.rollback()
        resp = re.search(r"\)\s(?P<title>[^\"]+).*\n(?P<detail>.+)\n", e.args[0])
        if resp:
            info = resp.groupdict()
            raise ProRunError(DBErrorCode.no_allow, f"{info['title']}\n{info['detail'].replace('DETAIL:  ', '')}")
        else:
            raise ProRunError(DBErrorCode.no_allow, e.args[0])
    except Exception as e:
        session.rollback()
        raise
    else:
        session.commit()
