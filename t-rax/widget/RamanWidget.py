# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from .BaseWidget import BaseWidget

from PyQt4 import QtGui


class RamanWidget(BaseWidget, object):
    def __init__(self, parent):
        super(RamanWidget, self).__init__(parent)

        self.test_button = QtGui.QPushButton()
        # self.control_widget._layout.insertWidget(1, self.test_button)
        self.add_control_widget(self.test_button)
