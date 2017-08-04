# -*- coding: utf-8 -*-
class NoValue(object):

    def __repr__(self):
        return '<{0}>'.format(self.__class__.__name__)