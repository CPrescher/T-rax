# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtCore

from model.RamanModel import RamanModel, REVERSE_CM_MODE, WAVELENGTH_MODE
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

        self.connect_signals()

    def connect_signals(self):
        self.widget.laser_line_txt.editingFinished.connect(self.laser_line_txt_changed)
        self.widget.nanometer_cb.toggled.connect(self.display_mode_changed)

    def laser_line_txt_changed(self):
        new_laser_line = float(str(self.widget.laser_line_txt.text()))
        self.model.laser_line = new_laser_line

    def display_mode_changed(self):
        if self.widget.nanometer_cb.isChecked():
            self.model.mode = WAVELENGTH_MODE
        else:
            self.model.mode = REVERSE_CM_MODE
