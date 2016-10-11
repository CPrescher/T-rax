# -*- coding: utf8 -*-
# T-Rax - GUI program for analysis of spectroscopy data during
# diamond anvil cell experiments
# Copyright (C) 2016 Clemens Prescher (clemens.prescher@gmail.com)
# Institute for Geology and Mineralogy, University of Cologne
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from qtpy import QtCore
import os

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

        self.widget.laser_line_txt.editingFinished.connect(self.laser_line_txt_changed)
        self.widget.derivative_sb.valueChanged.connect(self.spectrum_changed)
        self.widget.sample_position_txt.editingFinished.connect(self.sample_pos_txt_changed)
        self.widget.reference_position_txt.editingFinished.connect(self.reference_pos_txt_changed)

        self.widget.graph_widget.mouse_left_clicked.connect(self.mouse_left_clicked)

    def spectrum_changed(self):
        derivative_smoothing = float(self.widget.derivative_sb.value())
        derivative_spectrum = self.model.calculate_derivative_spectrum(derivative_smoothing)
        if derivative_spectrum is not None:
            self.widget.plot_derivative(*derivative_spectrum.data)

    def laser_line_txt_changed(self):
        new_value = float(str(self.widget.laser_line_txt.text()))
        self.model.laser_line = new_value

    def sample_pos_txt_changed(self):
        new_value = float(str(self.widget.sample_position_txt.text()))
        self.model.sample_position = new_value
        self.widget.set_diamond_line_pos(new_value)

    def reference_pos_txt_changed(self):
        new_value = float(str(self.widget.reference_position_txt.text()))
        self.model.reference_position = new_value

    def pressure_changed(self, value):
        self.widget.pressure_lbl.setText("{:.2f}".format(value))

    def mouse_left_clicked(self, x, y):
        self.model.sample_position = x
        self.widget.sample_position_txt.setText("{:.2f}".format(x))
        self.widget.set_diamond_line_pos(x)

    def update_widget_parameter(self):
        self.widget.laser_line_txt.setText("{:.2f}".format(self.model.laser_line))
        self.widget.sample_position_txt.setText("{:.2f}".format(self.model.sample_position))
        self.widget.set_diamond_line_pos(self.model.sample_position)
        self.widget.reference_position_txt.setText("{:.2f}".format(self.model.reference_position))

    def save_settings(self, settings):
        settings.setValue("diamond data file", self.model.filename)
        settings.setValue("diamond autoprocessing", self.widget.autoprocess_cb.isChecked())
        settings.setValue("diamond laser line", self.model.laser_line)
        settings.setValue("diamond derivative", self.widget.derivative_sb.value())
        settings.setValue("diamond reference position", self.model.reference_position)
        settings.setValue("diamond sample position", self.model.sample_position)
        settings.setValue("diamond roi", " ".join(str(e) for e in self.model.roi.as_list()))

    def load_settings(self, settings):
        data_path = str(settings.value("diamond data file").toString())
        if os.path.exists(data_path):
            self.base_controller.load_data_file(data_path)

        autoprocessing = settings.value("diamond autoprocessing").toBool()
        if autoprocessing:
            self.widget.autoprocess_cb.setChecked(True)

        value = settings.value("diamond laser line").toFloat()
        self.model.laser_line = value[0] if value[1] else self.model.laser_line

        value = settings.value("diamond derivative").toInt()
        self.widget.derivative_sb.setValue(value[0])

        value = settings.value("diamond reference position").toFloat()
        self.model.reference_position = value[0] if value[1] else self.model.reference_position

        value = settings.value("diamond sample position").toFloat()
        self.model.sample_position = value[0] if value[1] else self.model.sample_position

        self.update_widget_parameter()

        roi_str = str(settings.value("diamond roi").toString())
        if roi_str != "":
            roi = [float(e) for e in roi_str.split()]
            self.model.roi = roi
            self.widget.roi_widget.set_rois([roi])
