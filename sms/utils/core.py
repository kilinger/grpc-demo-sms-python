# -*- coding: utf-8 -*-
from sqlalchemy import text

from sms.models.core import Provider
from sms.utils.base import get_data, get_url, get_values_list, get_result


def send_sms(tel, msg, sender, provider):
    data = get_data(tel, msg, sender, provider)
    url = get_url(provider.host, provider.path_send)
    return get_result(url, provider.method_send, data)


def check_sms_status(provider):
    url = get_url(provider.host, provider.path_status)
    data = {provider.param_user: provider.user,
            provider.param_pwd: provider.pwd}
    data.update(provider.param_kwargs_status) if provider.param_kwargs_status else None
    return get_result(url, provider.method_status, data)


def get_provider(sms):
    provider_ids = get_values_list(sms.records, 'provider_id')
    providers = Provider.query.filter(~Provider.id.in_(provider_ids)) if provider_ids else Provider.query
    provider = providers.filter(Provider.charge_type == Provider.CHARGE_TYPE.Fixed,
                                Provider.surplus_count > 0).order_by(text('-surplus_count')).first()
    if not provider:
        provider = providers.filter_by(charge_type=Provider.CHARGE_TYPE.Single).first()
    return provider


def get_provider_surplus_count(provider):
    url = get_url(provider.host, provider.path_inquire)
    data = {provider.param_user: provider.user,
            provider.param_pwd: provider.pwd}
    result = get_result(url, provider.method_status, data)
    surplus_count = result.get(provider.param_inquire, None)
    return surplus_count


