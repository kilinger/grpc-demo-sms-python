# -*- coding: utf-8 -*-
from . import *  # noqa
from datetime import timedelta


BABEL_DEFAULT_LOCALE = 'en'
LANGUAGES = {
    'en': 'English',
    'zh': 'Chinese'
}

SECRET_KEY = env("SECRET_KEY")

ONE_DAY_IN_SECONDS = env('ONE_DAY_IN_SECONDS', default=60 * 60 * 24)

CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_IMPORTS = ['sms.tasks']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'updata_provider_surplus_count': {
        'task': 'sms.tasks.updata_provider_surplus_count',
        'schedule': timedelta(hours=3),
        'args': ()
    },
}

template_default = dict(
    captcha=u'您好，本次操作的验证码为：{code}，切勿将验证码泄露于他人，{minute}分钟内有效。',
    retrieve_password=u'您好，您正在进行找回密码操作，本次操作的验证码为：{code}，切勿将验证码泄露于他人，{minute}分钟内有效。',
    verify_phone=u'感谢你注册{company}，正在进行手机号验证操作，验证码为：{code}，切勿将验证码泄露于他人，{minute}分钟内有效。',
)
TEMPLATE_RETRIEVE_PASSWORD = env('TEMPLATE_RETRIEVE_PASSWORD', default=template_default.get('retrieve_password'))
TEMPLATE_CAPTCHA = env('TEMPLATE_CAPTCHA', default=template_default.get('captcha'))
TEMPLATE_VERIFY_PHONE = env('TEMPLATE_VERIFY_PHONE', default=template_default.get('verify_phone'))

SENTRY_INCLUDE_PATHS = env.list('SENTRY_INCLUDE_PATHS', default=['sms'])
