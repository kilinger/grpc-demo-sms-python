# -*- coding: utf-8 -*-
import logging
import logging.config
import os

from flask import Flask
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry

from sms.celery import make_celery


app = Flask('sms', instance_relative_config=True)
app.config.from_object(os.environ.get("FLASKR_SETTINGS", "sms.settings"))
logging.config.dictConfig(app.config['LOGGING'])

babel = Babel(app)

config = app.config

db = SQLAlchemy(app)

celery = make_celery(app)

dsn = config.get('SENTRY_DSN', None)
if dsn:
    try:
        sentry = Sentry(app, logging=True, level=logging.ERROR, dsn=dsn)
    except RuntimeError:
        sentry = Sentry(app, logging=True, level=logging.ERROR, dsn=dsn, register_signal=False)
