# -*- coding: utf-8 -*-
import datetime

import uuid

from application import db


class TimeStampedModel(object):

    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    modified = db.Column(db.DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())


class PrimaryKeyModel(object):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class UUIDModel(object):

    uuid = db.Column(db.String(256), default=uuid.uuid4)


class BaseModel(PrimaryKeyModel, TimeStampedModel, UUIDModel):

    pass
