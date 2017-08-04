# -*- coding: utf-8 -*-

from requests import request

from sms.utils.encoding import parse_str_to_dict, encode_msg
from sms.utils.none import NoValue


def get_or_none(klass, klass_id=None, **kwargs):
    if klass_id:
        query = klass.query.get(klass_id)
    elif kwargs:
        query = klass.query.filter_by(**kwargs).first()
    else:
        query = None
    return query


def get_data(tel, msg, sender, provider):
    msg = encode_msg(msg, sender, provider.msg_encodings)
    data = {provider.param_user: provider.user,
            provider.param_pwd: provider.pwd,
            provider.param_tel: tel,
            provider.param_msg: msg}
    kwargs = provider.param_kwargs if provider.param_kwargs else None
    data.update(kwargs) if isinstance(kwargs, dict) else None
    return data


def get_url(host, path):
    if not host.endswith('/'):
        host += '/'
    if path.startswith('/'):
        path = path[1:]
    url = u'{0}{1}'.format(host, path)
    if url.endswith('/'):
        url = url[:-1]
    return url


def get_values_list(instances, key):
    NOTSET = NoValue()
    values = []
    print 1111111111, instances
    if not instances:
        return values
    for instance in instances:
        value = getattr(instance, key, NOTSET)
        values.append(value) if value is not NOTSET else None
    return values


def get_result(url, method, data):
    if method in ['get', 'GET']:
        response = request('get', url, params=data)
    elif method in ['post', 'POST']:
        response = request('post', url, data=data)
    else:
        response = None
    content = response.content if response else ''
    return parse_str_to_dict(content)


