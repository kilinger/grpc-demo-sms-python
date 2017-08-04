# -*- coding: utf-8 -*-
from sqlalchemy import types


class ChoiceType(types.TypeDecorator):

    def process_literal_param(self, value, dialect):
        pass

    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.iteritems() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]
