# -*- coding: utf-8 -*-
from __future__ import print_function

import grpc

import sms_pb2


tel = '15633721242'


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = sms_pb2.SmsServerStub(channel)

    # msg = u'What kind of foods would you like?'
    # sender = 'SUN'
    # response = stub.Send(sms_pb2.SmsRequest(tel=tel, msg=msg, sender=sender))
    # print(response.uuid)
    #
    # uuid = '2e13bc86-a232-4227-a62f-41c646b946f3'
    # response = stub.Inquire(sms_pb2.InquireRequest(uuid=uuid))
    # print(response.status)
    #
    # code = u'203821'
    # minute = '10'
    # sender = 'LILI'
    # response = stub.Captcha(sms_pb2.CaptchaRequest(tel=tel, code=code, minute=minute, sender=sender))
    # print(response.uuid)
    #
    # response = stub.Inquire(sms_pb2.InquireRequest(uuid=response.uuid))
    # print(response.status)
    #
    # code = u'938247'
    # minute = '30'
    # sender = 'Submen'
    # response = stub.RetrievePassword(sms_pb2.RetrievePasswordRequest(tel=tel, code=code, minute=minute, sender=sender))
    # print(response.uuid)
    #
    # response = stub.Inquire(sms_pb2.InquireRequest(uuid=response.uuid))
    # print(response.status)

    code = u'895647'
    minute = '20'
    company = '金东方'
    sender = 'we join'
    response = stub.VerifyPhone(sms_pb2.VerifyPhoneRequest(tel=tel, code=code, minute=minute, sender=sender, company=company))
    print(response)

    response = stub.Inquire(sms_pb2.InquireRequest(uuid=response.uuid))
    print(response.status)


if __name__ == '__main__':
    run()
