# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtCore

from model.RamanModel import RamanModel
from widget.RamanWidget import RamanWidget
from controller.BaseController import BaseController


class RamanController(QtCore.QObject):
    def __init__(self, model, widget):
        """

        :param model:
        :param widget:
        :type model: RamanModel
        :type widget: RamanWidget
        """
        super(RamanController, self).__init__()

        self.file_controller = BaseController(model, widget)

        self.model = model
        self.widget = widget
