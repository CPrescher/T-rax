# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtCore

from model.DiamondModel import DiamondModel
from widget.DiamondWidget import DiamondWidget
from controller.BaseController import BaseController


class DiamondController(QtCore.QObject):
    def __init__(self, model, widget):
        """
        
        :type model: DiamondModel
        :type widget: DiamondWidget
        """

        super(DiamondController, self).__init__()

        self.base_controller = BaseController(model, widget)
        self.model = model
        self.widget = widget
