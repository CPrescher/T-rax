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

        self.connect_signals()

    def connect_signals(self):
        self.model.pressure_changed.connect(self.pressure_changed)
        self.widget.sample_position_txt.editingFinished.connect(self.sample_position_txt_changed)
        self.widget.reference_position_txt.editingFinished.connect(self.reference_position_txt_changed)
        self.widget.sample_temperature_txt.editingFinished.connect(self.sample_temperature_txt_changed)
        self.widget.reference_temperature_txt.editingFinished.connect(self.reference_temperature_txt_changed)

    def sample_position_txt_changed(self):
        new_value = float(str(self.widget.sample_position_txt.text()))
        self.model.sample_position = new_value

    def pressure_changed(self, new_value):
        self.widget.pressure_lbl.setText("{:.3f}".format(new_value))

    def reference_position_txt_changed(self):
        new_value = float(str(self.widget.reference_position_txt.text()))
        self.model.reference_position = new_value

    def sample_temperature_txt_changed(self):
        new_value = float(str(self.widget.sample_temperature_txt.text()))
        self.model.sample_temperature = new_value

    def reference_temperature_txt_changed(self):
        new_value = float(str(self.widget.reference_temperature_txt.text()))
        self.model.reference_temperature = new_value
