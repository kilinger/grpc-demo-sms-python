# -*- coding: utf-8 -*-
import time

import grpc
from concurrent import futures

import sms_pb2
from application import db, config
from sms.models.core import Sms
from sms.tasks import do_send_sms
from sms.utils.base import get_or_none
from sms.utils.server import warp


class SmsServer(sms_pb2.SmsServerServicer):

    @warp
    def Send(self, request, context):
        sms = Sms(tel=request.tel, msg=request.msg, sender=request.sender, type=Sms.TYPE.Ordinary)
        db.session.add(sms)
        db.session.commit()
        do_send_sms.apply_async(args=[sms.id])
        return sms_pb2.SmsReply(uuid=sms.uuid)

    @warp
    def Captcha(self, request, context):
        template = config.get('TEMPLATE_CAPTCHA')
        msg = template.format(code=request.code, minute=request.minute)
        sms = Sms(tel=request.tel, msg=msg, sender=request.sender, type=Sms.TYPE.Captcha)
        db.session.add(sms)
        db.session.commit()
        do_send_sms.apply_async(args=[sms.id])
        return sms_pb2.SmsReply(uuid=sms.uuid)

    @warp
    def RetrievePassword(self, request, context):
        template = config.get('TEMPLATE_RETRIEVE_PASSWORD')
        msg = template.format(code=request.code, minute=request.minute)
        sms = Sms(tel=request.tel, msg=msg, sender=request.sender, type=Sms.TYPE.RetrievePassword)
        db.session.add(sms)
        db.session.commit()
        do_send_sms.apply_async(args=[sms.id])
        return sms_pb2.SmsReply(uuid=sms.uuid)

    @warp
    def VerifyPhone(self, request, context):
        template = config.get('TEMPLATE_VERIFY_PHONE')
        msg = template.format(code=request.code, minute=request.minute, company=request.company)
        sms = Sms(tel=request.tel, msg=msg, sender=request.sender, type=Sms.TYPE.VerifyPhone)
        db.session.add(sms)
        db.session.commit()
        do_send_sms.apply_async(args=[sms.id])
        return sms_pb2.SmsReply(uuid=sms.uuid)

    def Inquire(self, request, context):
        status = 0
        sms = get_or_none(Sms, uuid=request.uuid)
        if sms and sms.records.filter_by(is_receipt=True).count():
            status = 1
        return sms_pb2.InquireReply(status=status)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sms_pb2.add_SmsServerServicer_to_server(SmsServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(config['ONE_DAY_IN_SECONDS'])
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
