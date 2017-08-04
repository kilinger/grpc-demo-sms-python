# -*- coding: utf-8 -*-
import datetime
from collections import OrderedDict
from decimal import Decimal

import six

_PROTECTED_TYPES = six.integer_types + (type(None), float, Decimal,
                                        datetime.datetime, datetime.date, datetime.time)


def is_protected_type(obj):
    return isinstance(obj, _PROTECTED_TYPES)


class ReturnList(list):

    def __init__(self, *args, **kwargs):
        self.serializer = kwargs.pop('serializer')
        super(ReturnList, self).__init__(*args, **kwargs)

    def __repr__(self):
        return list.__repr__(self)

    def __reduce__(self):
        return (list, (list(self),))


class ReturnDict(OrderedDict):

    def __init__(self, *args, **kwargs):
        self.serializer = kwargs.pop('serializer')
        super(ReturnDict, self).__init__(*args, **kwargs)

    def copy(self):
        return ReturnDict(self, serializer=self.serializer)

    def __repr__(self):
        return dict.__repr__(self)

    def __reduce__(self):
        return (dict, (dict(self),))