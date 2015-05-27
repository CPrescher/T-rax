# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtGui, QtCore

from .BaseWidget import BaseWidget


class RubyWidget(BaseWidget, object):
    def __init__(self, parent):
        super(RubyWidget, self).__init__()
