# -*- coding: utf-8 -*-
import json
import os

# from sms.utils.core import NoValue
from sms.error import ImproperlyConfigured
from sms.utils.none import NoValue


class Env(object):

    NOTSET = NoValue()
    BOOLEAN_TRUE_STRINGS = ('TRUE', 'True', 'true', 'on', 'ok', 'yes', 'y', 'Y', 'T' '1')

    def __init__(self, **scheme):
        self.scheme = scheme

    def __call__(self, key, convert=None, default=NOTSET):
        return self.get_value(key, convert=convert, default=default)

    def get_env(self, key, default=NOTSET):
        env_string = os.environ.get(key, default)
        if env_string is self.NOTSET:
            error_msg = "Set the {0} environment variable".format(key)
            raise ImproperlyConfigured(error_msg)
        return env_string

    def get_value(self, key, convert=None, default=NOTSET):
        env_string = self.get_env(key, default)
        value = convert(env_string) if convert else env_string
        if hasattr(value, 'startswith') and value.startswith('$'):
            value = value.lstrip('$')
            value = self.get_value(value, convert=convert, default=default)
        return value

    def bool(self, key, default=NOTSET):
        value = self.get_value(key, convert=bool, default=default)
        if not value:
            value = self.get_env(key, default)
            value = value in self.BOOLEAN_TRUE_STRINGS
        return value

    def str(self, key, default=NOTSET):
        return self.get_value(key, default=default)

    def unicode(self, key, default=NOTSET):
        return self.get_value(key, convert=str, default=default)

    def int(self, key, default=NOTSET):
        return self.get_value(key, convert=int, default=default)

    def float(self, key, default=NOTSET):
        return self.get_value(key, convert=float, default=default)

    def json(self, key, default=NOTSET):
        return self.get_value(key, convert=json.loads, default=default)

    def list(self, key, convert=None, default=NOTSET):
        return self.get_value(key, convert=list if not convert else [convert], default=default)

    def tuple(self, key, convert=None, default=NOTSET):
        return self.get_value(key, convert=tuple if not convert else (convert,), default=default)

    def dict(self, key, convert=dict, default=NOTSET):
        return self.get_value(key, convert=convert, default=default)