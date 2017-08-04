# -*- coding: utf-8 -*-
from flask_babel import lazy_gettext as _
from sqlalchemy.orm import validates

from application import db
from sms.error import ValidationError, EmptyValueError, InvalidValueError
from sms.models.base import BaseModel
from .choices import Choices


class Sms(BaseModel, db.Model):

    TYPE = Choices(
        ('ordinary', 'Ordinary', _('Ordinary')),
        ('captcha', 'Captcha', _("Captcha")),
        ('retrieve password', 'RetrievePassword', _("Retrieve password")),
        ('verify phone', 'VerifyPhone', _("Verify Phone")),
    )

    records = db.relationship('SmsRecord', backref=db.backref('sms', lazy='joined'), lazy='dynamic')

    type = db.Column(db.String(64), default=TYPE.Ordinary)
    msg = db.Column(db.Text, nullable=False)
    tel = db.Column(db.Text, nullable=False)
    sender = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<SMS %r>' % self.id

    @validates('type')
    def validate_type(self, key, value):
        if value not in self.TYPE:
            raise InvalidValueError(key, value)
        return value

    @validates('msg')
    def validate_msg(self, key, value):
        if not value:
            raise EmptyValueError(key)
        return value

    @validates('tel')
    def validate_tel(self, key, value):
        if not value:
            raise EmptyValueError(key)
        return value

    @validates('sender')
    def validate_sender(self, key, value):
        if not value:
            raise EmptyValueError(key)
        return value


class SmsRecord(BaseModel, db.Model):

    sms_id = db.Column(db.Integer, db.ForeignKey('sms.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)

    message_id = db.Column(db.String(120))
    error = db.Column(db.String(256))
    is_receipt = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<SmsRecord %r>' % self.uuid


class Provider(BaseModel, db.Model):

    CHARGE_TYPE = Choices(
        ('single', 'Single', _('single billing')),
        ('fixed', 'Fixed', _("fixed billing")),
    )

    records = db.relationship('SmsRecord', backref=db.backref('provider', lazy='joined'), lazy='dynamic')

    name = db.Column(db.String(120))
    host = db.Column(db.String(256), nullable=False)
    user = db.Column(db.String(120), nullable=False)
    pwd = db.Column(db.String(120), nullable=False)

    charge_type = db.Column(db.String(15), default=CHARGE_TYPE.Single)
    surplus_count = db.Column(db.Integer)  # exist when charge_type was fixed

    path_send = db.Column(db.String(10), nullable=False)
    path_inquire = db.Column(db.String(10), nullable=False)  # search for surplus_count
    path_status = db.Column(db.String(10))

    method_send = db.Column(db.String(10), nullable=False)
    method_inquire = db.Column(db.String(10), nullable=False)
    method_status = db.Column(db.String(10))

    msg_encodings = db.Column(db.String(256))  # default delimiter is ','

    # send params
    param_user = db.Column(db.String(10), nullable=False)
    param_pwd = db.Column(db.String(10), nullable=False)
    param_tel = db.Column(db.String(10), nullable=False)
    param_msg = db.Column(db.String(10), nullable=False)
    param_kwargs = db.Column(db.JSON(), default=db.JSON.NULL)
    param_msg_id = db.Column(db.String(10), nullable=False)
    param_error = db.Column(db.String(10), nullable=False)

    # inquire param
    param_inquire = db.Column(db.String(10), nullable=False)

    # status param
    param_kwargs_status = db.Column(db.JSON(), default=db.JSON.NULL)

    def __repr__(self):
        return '<Provider %r>' % self.user

    @validates('charge_type')
    def validate_charge_type(self, key, value):
        if value not in self.TYPE:
            raise InvalidValueError(key, value)
        return value

    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise EmptyValueError(key)
        return value

    @validates('host')
    def validate_host(self, key, value):
        if not value:
            raise EmptyValueError(key)
        return value

    @validates('user')
    def validate_user(self, key, value):
        if not value:
            raise EmptyValueError(key)
        return value

    @validates('pwd')
    def validate_pwd(self, key, value):
        if not value:
            raise EmptyValueError(key)
        return value

    @validates('path_send')
    def validate_path_send(self, key, value):
        if not value:
            raise EmptyValueError(key)
        return value

    @validates('path_inquire')
    def validate_path_inquire(self, key, value):
        if not value:
            raise EmptyValueError(key)
        return value

    @validates('path_status')
    def validate_path_status(self, key, value):
        if not value:
            raise EmptyValueError(key)
        return value

    @validates('method_send')
    def validate_method_send(self, key, value):
        if not value:
            raise EmptyValueError(key)
        return value

    @validates('method_inquire')
    def validate_method_inquire(self, key, value):
        if not value:
            raise EmptyValueError(key)
        return value

    @validates('method_status')
    def validate_method_status(self, key, value):
        if not value:
            raise EmptyValueError(key)
        return value

    @validates('param_user')
    def validate_param_user(self, key, value):
        if not value:
            raise EmptyValueError(key)
        return value

    @validates('param_pwd')
    def validate_param_pwd(self, key, value):
        if not value:
            raise EmptyValueError(key)
        return value

    @validates('param_tel')
    def validate_param_tel(self, key, value):
        if not value:
            raise EmptyValueError(key)
        return value

    @validates('param_msg')
    def validate_param_msg(self, key, value):
        if not value:
            raise EmptyValueError(key)
        return value

    @validates('param_msg_id')
    def validate_param_msg_id(self, key, value):
        if not value:
            raise EmptyValueError(key)
        return value

    @validates('param_error')
    def validate_param_error(self, key, value):
        if not value:
            raise EmptyValueError(key)
        return value

    @validates('param_inquire')
    def validate_param_inquire(self, key, value):
        if not value:
            raise EmptyValueError(key)
        return value
