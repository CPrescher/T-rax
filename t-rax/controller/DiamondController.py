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

        self.connect_signals()

    def connect_signals(self):
        self.widget.laser_line_txt.editingFinished.connect(self.laser_line_txt_changed)

        self.model.pressure_changed.connect(self.pressure_changed)
        self.widget.sample_pos_txt.editingFinished.connect(self.sample_pos_txt_changed)
        self.widget.reference_pos_txt.editingFinished.connect(self.reference_pos_txt_changed)

    def laser_line_txt_changed(self):
        new_value = float(str(self.widget.laser_line_txt.text()))
        self.model.laser_line = new_value

    def sample_pos_txt_changed(self):
        new_value = float(str(self.widget.sample_pos_txt.text()))
        self.model.sample_position = new_value

    def reference_pos_txt_changed(self):
        new_value = float(str(self.widget.reference_pos_txt.text()))
        self.model.reference_position = new_value

    def pressure_changed(self, value):
        self.widget.pressure_lbl.setText("{:.2f}".format(value))
