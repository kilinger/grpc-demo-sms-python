# -*- coding: utf-8 -*-
from __future__ import absolute_import

import raven

from celery import Celery
from raven.contrib.celery import register_signal, register_logger_signal


class MyCelery(Celery):

    def on_configure(self):
        from application import app
        dsn = app.config.get('SENTRY_DSN', None)
        if dsn:
            client = raven.Client(dsn)
            register_logger_signal(client)
            register_signal(client)


def make_celery(app):

    celery = MyCelery(app.import_name,
                      include=['sms.tasks'],
                      broker=app.config['BROKER_URL'],
                      backend=app.config['CELERY_RESULT_BACKEND'])

    celery.conf.update(app.config)

    BaseTask = celery.Task

    class ContextTask(BaseTask):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return BaseTask.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
