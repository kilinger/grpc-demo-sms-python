# -*- coding: utf-8 -*-
from .base import *  # noqa


DEBUG = True

BROKER_URL = env("BROKER_URL", default="redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://127.0.0.1:6379/1")
SQLALCHEMY_TRACK_MODIFICATIONS = env.bool("SQLALCHEMY_TRACK_MODIFICATIONS", default=True)
SQLALCHEMY_DATABASE_URI = env("SQLALCHEMY_DATABASE_URI", default="mysql://127.0.01:3306/sms")

SMS_HOST = env('SMS_HOST', default='http://101.227.68.49:7891/mt?')
SMS_USER = env('SMS_USER', default='10690116')
SMS_PWD = env('SMS_PWD', default='SihAi429')

EXPIRE_TIME_FOR_FAILED_SEND_SMS = env.int('EXPIRE_TIME_FOR_FAILED_SEND_SMS', default=60)  # seconds

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
}
