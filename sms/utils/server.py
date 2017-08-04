# -*- coding: utf-8 -*-
import sms_pb2


def warp(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if hasattr(e, 'key') and hasattr(e, 'detail'):
                return sms_pb2.SmsReply(error=sms_pb2.Error(**{e.key: e.detail}))
            return sms_pb2.SmsReply(error=sms_pb2.Error(default=str(e)))
    return wrapper
