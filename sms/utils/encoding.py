# -*- coding: utf-8 -*-
import urlparse

import six

from sms.utils.types import is_protected_type, ReturnList, ReturnDict


def parse_str_to_dict(params):
    qs = urlparse.parse_qs(params)
    for k, v in qs.iteritems():
        qs.update(**{k: v[-1]})
    return qs


def encode_msg(msg, sender, encodings, delimiter=','):
    if not (isinstance(msg, basestring) and isinstance(encodings, basestring) and isinstance(sender, basestring)):
        return msg
    msg = u'{0}【{1}】'.format(msg.strip(), sender.strip())
    if not encodings:
        return msg
    for encoding in encodings.split(delimiter):
        encoding = encoding.strip()
        msg = msg.encode(encoding)
    return msg


def force_text(s, encoding='utf-8', strings_only=False, errors='strict'):
    if isinstance(s, six.text_type):
        return s
    if strings_only and is_protected_type(s):
        return s
    try:
        if not isinstance(s, six.string_types):
            if six.PY3:
                if isinstance(s, bytes):
                    s = six.text_type(s, encoding, errors)
                else:
                    s = six.text_type(s)
            elif hasattr(s, '__unicode__'):
                s = six.text_type(s)
            else:
                s = six.text_type(bytes(s), encoding, errors)
        else:
            s = s.decode(encoding, errors)
    except UnicodeDecodeError as e:
        if not isinstance(s, Exception):
            from sms.error import FlaskUnicodeDecodeError
            raise FlaskUnicodeDecodeError(s, *e.args)
        else:
            s = ' '.join(force_text(arg, encoding, strings_only, errors)
                         for arg in s)
    return s


def force_text_recursive(data):
    if isinstance(data, list):
        ret = [
            force_text_recursive(item) for item in data
            ]
        if isinstance(data, ReturnList):
            return ReturnList(ret, serializer=data.serializer)
        return data
    elif isinstance(data, dict):
        ret = {
            key: force_text_recursive(value)
            for key, value in data.items()
        }
        if isinstance(data, ReturnDict):
            return ReturnDict(ret, serializer=data.serializer)
        return data
    return force_text(data)