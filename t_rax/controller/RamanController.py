# -*- coding: utf-8 -*-
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

from ..model.RamanModel import RamanModel
from ..widget.RamanWidget import RamanWidget
from .BaseController import BaseController


class RamanController(QtCore.QObject):
    def __init__(self, model, widget):
        """

        :param model:
        :param widget:
        :type model: RamanModel
        :type widget: RamanWidget
        """
        super(RamanController, self).__init__()

        self.base_controller = BaseController(model, widget)

        self.model = model
        self.widget = widget

        self.connect_signals()

    def connect_signals(self):
        self.widget.laser_line_txt.editingFinished.connect(self.laser_line_txt_changed)
        self.widget.nanometer_cb.toggled.connect(self.display_mode_changed)
        self.model.spectrum_changed.connect(self.spectrum_changed)

    def laser_line_txt_changed(self):
        new_laser_line = float(str(self.widget.laser_line_txt.text()))
        self.model.laser_line = new_laser_line

    def display_mode_changed(self):
        if self.widget.nanometer_cb.isChecked():
            self.model.mode = RamanModel.WAVELENGTH_MODE
        else:
            self.model.mode = RamanModel.REVERSE_CM_MODE

    def spectrum_changed(self):
        if self.model.mode == RamanModel.WAVELENGTH_MODE:
            self.widget.graph_widget.set_xlabel('&lambda; (nm)')
        elif self.model.mode == RamanModel.REVERSE_CM_MODE:
            self.widget.graph_widget.set_xlabel('v (cm<sup>-1</sup>)')

    def update_widget_parameter(self):
        self.widget.laser_line_txt.setText("{:.2f}".format(self.model.laser_line))
        if self.model.mode == RamanModel.WAVELENGTH_MODE:
            self.widget.nanometer_cb.setChecked(True)

    def save_settings(self, settings):
        settings.setValue("raman data file", self.model.filename)
        settings.setValue("raman autoprocessing", self.widget.autoprocess_cb.isChecked())
        settings.setValue("raman laser line", self.model.laser_line)
        settings.setValue("raman mode", self.model.mode)
        settings.setValue("raman roi", " ".join(str(e) for e in self.model.roi.as_list()))

    def load_settings(self, settings):
        raman_data_path = str(settings.value("raman data file").toString())
        if os.path.exists(raman_data_path):
            self.base_controller.load_file_btn_clicked(raman_data_path)

        raman_autoprocessing = settings.value("raman autoprocessing").toBool()
        if raman_autoprocessing:
            self.widget.autoprocess_cb.setChecked(True)

        value = settings.value("raman laser line").toFloat()
        self.model.laser_line = value[0] if value[1] else self.model.laser_line

        value = settings.value("raman mode").toInt()
        self.model.mode = value[0] if value[1] else self.model.mode

        roi_str = str(settings.value("raman roi").toString())
        if roi_str != "":
            roi = [float(e) for e in roi_str.split()]
            self.model.roi = roi
            self.widget.roi_widget.set_rois([roi])

        self.update_widget_parameter()
