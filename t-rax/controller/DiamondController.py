# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtCore
import numpy as np

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
        self.model.pressure_changed.connect(self.pressure_changed)
        self.model.spectrum_changed.connect(self.spectrum_changed)
        self.model.data_changed.connect(self.spectrum_changed)

        self.widget.laser_line_txt.editingFinished.connect(self.laser_line_txt_changed)
        self.widget.sample_pos_txt.editingFinished.connect(self.sample_pos_txt_changed)
        self.widget.reference_pos_txt.editingFinished.connect(self.reference_pos_txt_changed)

        self.widget.graph_widget.mouse_left_clicked.connect(self.mouse_left_clicked)

    def spectrum_changed(self):
        derivative_smoothing = float(self.widget.derivative_sb.value())
        derivative_spectrum = self.model.calculate_derivative_spectrum(derivative_smoothing)
        self.widget.plot_derivative(*derivative_spectrum.data)

    def laser_line_txt_changed(self):
        new_value = float(str(self.widget.laser_line_txt.text()))
        self.model.laser_line = new_value

    def sample_pos_txt_changed(self):
        new_value = float(str(self.widget.sample_pos_txt.text()))
        self.model.sample_position = new_value
        self.widget.set_diamond_line_pos(new_value)

    def reference_pos_txt_changed(self):
        new_value = float(str(self.widget.reference_pos_txt.text()))
        self.model.reference_position = new_value

    def pressure_changed(self, value):
        self.widget.pressure_lbl.setText("{:.2f}".format(value))

    def mouse_left_clicked(self, x, y):
        self.model.sample_position = x
        self.widget.sample_pos_txt.setText("{:.2f}".format(x))
        self.widget.set_diamond_line_pos(x)
