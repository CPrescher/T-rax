# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtCore

from model.RubyModel import RubyModel
from widget.RubyWidget import RubyWidget
from controller.BaseController import BaseController


class RubyController(QtCore.QObject):
    def __init__(self, model, widget):
        """
        
        :param model: 
        :param widget: 
        :type model: RubyModel
        :type widget: RubyWidget
        """
        super(RubyController, self).__init__()

        self.file_controller = BaseController(model, widget)

        self.model = model
        self.widget = widget
