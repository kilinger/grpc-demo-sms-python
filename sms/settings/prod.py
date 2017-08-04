# -*- coding: utf-8 -*-
from .base import *  # noqa


DEBUG = False

BROKER_URL = env("BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")
SQLALCHEMY_TRACK_MODIFICATIONS = env.bool("SQLALCHEMY_TRACK_MODIFICATIONS")
SQLALCHEMY_DATABASE_URI = env("SQLALCHEMY_DATABASE_URI")

SMS_HOST = env('SMS_HOST')
SMS_USER = env('SMS_USER')
SMS_PWD = env('SMS_PWD')

EXPIRE_TIME_FOR_FAILED_SEND_SMS = env.int('EXPIRE_TIME_FOR_FAILED_SEND_SMS')  # seconds

SENTRY_DSN = env('SENTRY_DSN')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'sms': {
        'level': 'WARNING',
        'handlers': ['sentry', 'console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
    },
    'handlers': {
        'sentry': {
            'level': 'INFO',
            'class': 'raven.handlers.logging.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
            'propagate': False,
        },
        'sms': {
            'level': 'WARNING',
            'handlers': ['sentry'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
