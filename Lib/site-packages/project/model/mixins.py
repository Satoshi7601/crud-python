# -*- coding: utf-8 -*-
# @Time     : 2020/7/22 7:29 下午
# @Author   : binger
from sqlalchemy import ARRAY
from sqlalchemy.ext.mutable import MutableSet, MutableList
from sqlalchemy.event import listens_for

from .base import db, Column
from .types import PseudoJSON


def handler(filed, mapper):
    if mapper:
        return mapper.get(filed, filed)
    return filed


def model_to_dict(model, mapper=None, exclude=None):
    exclude = exclude or []
    # return [c.name for c in self.query.selectable.columns]
    return {handler(c.name, mapper): getattr(model, c.name) for c in model.__table__.columns if c.name not in exclude}


class DbMixin(db.Model):
    __abstract__ = True
    id = Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = Column(db.DateTime(True), server_default=db.func.now(), comment="修改时间", default=db.func.now())

    @classmethod
    def object(cls):
        return cls.query

    def to_dict(self, mapper=None, exclude=None):
        """

        :param mapper: 字段输出映射
        :param exclude: 排除字段
        :return:
        """
        return model_to_dict(self, mapper, exclude)

    def delete(self):
        return self.object().filter_by(id=self.id).delete()

    def update_data(self, data: dict):
        for key, value in data.items():
            if key == "_sa_instance_state":
                continue
            setattr(self, key, value)


class TimestampMixin(DbMixin):
    __abstract__ = True
    updated_at = Column(db.DateTime(True), server_default=db.func.now(), default=db.func.now(), onupdate=db.func.now(),
                        comment="更新时间")


@listens_for(TimestampMixin, 'before_update', propagate=True)
def timestamp_before_update(mapper, connect, target):
    print("timestamp_before_update")
    if hasattr(target, 'skip_update_at'):
        return

    target.updated_at = db.func.now()


class DeleteMixin(DbMixin):
    __abstract__ = True
    enabled = Column(db.Boolean, default=True, comment="是否可用")

    @classmethod
    def object(cls):
        return cls.query.filter_by(enabled=True)

    def delete(self):
        self.enabled = False


class AuthorMixin(db.Model):
    __abstract__ = True
    # ding_talk_id
    author_id = Column(db.Integer, nullable=True, comment="用户唯一id")
    author = Column(db.String(32), nullable=True, comment="真实姓名")


class PeriodicMixin(db.Model):
    __abstract__ = True
    labels = ("minute", "hour", "day_of_month", "month_of_year", "day_of_week")
    TIMEZONE = 'Asia/Shanghai'
    periodic_tasks = Column(MutableList.as_mutable(PseudoJSON), default=[], nullable=True,
                            comment="periodic id array")
