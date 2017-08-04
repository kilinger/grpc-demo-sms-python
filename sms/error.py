# -*- coding: utf-8 -*-
import six
from flask_babel import lazy_gettext as _

from sms.utils.encoding import force_text, force_text_recursive
from sms.utils.none import NoValue


NOTSET = NoValue()


class ImproperlyConfigured(Exception):
    pass


class InvalidProvider(Exception):
    pass


class FlaskUnicodeDecodeError(UnicodeDecodeError):
    def __init__(self, obj, *args):
        self.obj = obj
        UnicodeDecodeError.__init__(self, *args)

    def __str__(self):
        original = UnicodeDecodeError.__str__(self)
        return '%s. You passed in %r (%s)' % (original, self.obj, type(self.obj))


class RpcException(Exception):
    default_detail = _('A server error occurred.')

    def __init__(self, detail=NOTSET):
        if detail is not NOTSET:
            self.detail = force_text(detail)
        else:
            self.detail = force_text(self.default_detail)

    def __str__(self):
        return self.detail


class ValidationError(RpcException):

    def __init__(self, key, detail=NOTSET):
        self.key = key
        if detail is NOTSET:
            super(ValidationError, self).__init__(detail)
        else:
            self.detail = force_text_recursive(detail)

    def __str__(self):
        return six.text_type(self.detail)


class EmptyValueError(ValidationError):
    default_detail = _('This Value can not be empty')


class InvalidValueError(ValidationError):
    default_detail = _("Invalid value '{value}'")

    def __init__(self, key, value):
        self.key = key
        self.detail = self.default_detail.format(value=value)
