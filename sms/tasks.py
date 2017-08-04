# -*- coding: utf-8 -*-
import logging

from application import celery, db, config
from models.core import Sms, SmsRecord, Provider
from utils.core import send_sms, get_provider, check_sms_status, get_provider_surplus_count
from sms.utils.base import get_or_none

logger = logging.getLogger('sms.task')


@celery.task()
def do_send_sms(sms_id, retries=5):
    sms = get_or_none(Sms, sms_id)
    if not sms:
        return
    provider = get_provider(sms)
    if not provider:
        extra = dict(sms_id=sms_id, retries=retries, provider=provider)
        logger.error("Got a invalid provider", exc_info=True, extra=extra)
        return
    record = SmsRecord(sms_id=sms.id, provider_id=provider.id)
    result = send_sms(sms.tel, sms.msg, sms.sender, provider)
    if not result:
        retries -= 1
        countdown = config.get('EXPIRE_TIME_FOR_FAILED_SEND_SMS')
        do_send_sms.apply_async(args=[sms_id, retries], countdown=countdown)
    if provider.param_msg_id in result:
        record.message_id = result[provider.param_msg_id]
    elif provider.param_error in result:
        record.error = result[provider.param_error]
    db.session.add(record)
    db.session.commit()
    check_sms_status_task.apply_async(args=[record.id])


@celery.task()
def check_sms_status_task(record_id, retries=5):
    record = get_or_none(SmsRecord, record_id)
    if not record:
        return
    result = check_sms_status(record.provider)
    print result
    # # if not result and retries:
    # if retries:
    #     retries -= 1
    #     countdown = config.get('EXPIRE_TIME_FOR_FAILED_SEND_SMS')
    #     check_sms_status_task.apply_async(args=[record_id, retries], countdown=countdown)
    # # elif retries is 0:
    # else:
    #     do_send_sms.apply_async(args=[record.sms.id])
    record.is_receipt = True
    db.session.add(record)
    db.session.commit()


@celery.task()
def updata_provider_surplus_count():
    providers = Provider.query.filter_by(charge_type=Provider.CHARGE_TYPE.Fixed).all()
    for provider in providers:
        surplus_count = get_provider_surplus_count(provider)
        if surplus_count is not None:
            provider.surplus_count = surplus_count
            db.session.add(provider)
            db.session.commit()
