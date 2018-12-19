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

import os

from qtpy import QtCore

from ..model.RubyModel import RubyModel
from ..widget.RubyWidget import RubyWidget
from .BaseController import BaseController


class RubyController(QtCore.QObject):
    def __init__(self, model, widget):
        """
        
        :param model: 
        :param widget: 
        :type model: RubyModel
        :type widget: RubyWidget
        """
        super(RubyController, self).__init__()

        self.base_controller = BaseController(model, widget)

        self.model = model
        self.widget = widget

        self.widget.set_ruby_line_pos(self.model.sample_position)

        self.connect_signals()

    def connect_signals(self):
        self.model.pressure_changed.connect(self.pressure_changed)
        self.model.param_changed.connect(self.params_changed)
        self.model.ruby_fitted.connect(self.ruby_fitted)

        self.widget.ruby_scale_cb.currentIndexChanged.connect(self.ruby_scale_cb_changed)
        self.widget.sample_position_txt.editingFinished.connect(self.sample_position_txt_changed)
        self.widget.reference_position_txt.editingFinished.connect(self.reference_position_txt_changed)
        self.widget.sample_temperature_txt.editingFinished.connect(self.sample_temperature_txt_changed)
        self.widget.reference_temperature_txt.editingFinished.connect(self.reference_temperature_txt_changed)

        self.widget.graph_widget.mouse_left_clicked.connect(self.mouse_left_clicked)
        self.widget.fit_ruby_btn.clicked.connect(self.model.fit_ruby_peaks)
        self.widget.show_ruby_fit_cb.stateChanged.connect(self.toggle_show_ruby)
        self.widget.fit_ruby_automatic_cb.stateChanged.connect(self.model.set_fit_automatic)

    def sample_position_txt_changed(self):
        new_value = float(str(self.widget.sample_position_txt.text()))
        self.widget.set_ruby_line_pos(new_value)
        self.model.sample_position = new_value

    def mouse_left_clicked(self, x, y):
        self.model.sample_position = x

    def pressure_changed(self, new_value):
        self.widget.pressure_lbl.setText("{:.2f}".format(new_value))

    def params_changed(self):
        self.widget.reference_position_txt.setText("{:.2f}".format(self.model.reference_position))
        self.widget.reference_temperature_txt.setText("{:.2f}".format(self.model.reference_temperature))
        self.widget.sample_position_txt.setText("{:.2f}".format(self.model.sample_position))
        self.widget.sample_temperature_txt.setText("{:.2f}".format(self.model.sample_temperature))

        self.widget.ruby_scale_cb.setCurrentIndex(self.model.ruby_scale)

        self.widget.set_ruby_line_pos(self.model.sample_position)

    def ruby_fitted(self):
        self.widget.set_fitted_spectrum(*self.model.fitted_spectrum.data)
        self.widget.show_ruby_fit_cb.setEnabled(True)
        self.widget.show_ruby_fit_cb.setChecked(True)

    def reference_position_txt_changed(self):
        new_value = float(str(self.widget.reference_position_txt.text()))
        self.model.reference_position = new_value

    def sample_temperature_txt_changed(self):
        new_value = float(str(self.widget.sample_temperature_txt.text()))
        self.model.sample_temperature = new_value

    def reference_temperature_txt_changed(self):
        new_value = float(str(self.widget.reference_temperature_txt.text()))
        self.model.reference_temperature = new_value

    def ruby_scale_cb_changed(self, index):
        self.model.ruby_scale = index

    def toggle_show_ruby(self):
        if self.widget.show_ruby_fit_cb.isChecked():
            self.widget.set_fitted_spectrum(*self.model.fitted_spectrum.data)
        else:
            self.widget.remove_fitted_spectrum_from_graph()

    def save_settings(self, settings):
        settings.setValue("ruby data file", self.model.filename)
        settings.setValue("ruby autoprocessing", self.widget.autoprocess_cb.isChecked())
        settings.setValue("ruby reference position", self.model.reference_position)
        settings.setValue("ruby reference temperature", self.model.reference_temperature)
        settings.setValue("ruby sample position", self.model.sample_position)
        settings.setValue("ruby sample temperature", self.model.sample_temperature)
        settings.setValue("ruby scale", self.model.ruby_scale)
        settings.setValue("ruby roi", " ".join(str(e) for e in self.model.roi.as_list()))

    def load_settings(self, settings):
        data_path = str(settings.value("ruby data file").toString())
        if os.path.exists(data_path):
            self.base_controller.load_file_btn_clicked(data_path)

        autoprocessing_flag = settings.value("ruby autoprocessing").toBool()
        if autoprocessing_flag:
            self.widget.autoprocess_cb.setChecked(True)

        self.model.blockSignals(True)
        value = settings.value("ruby scale").toInt()
        self.model.ruby_scale = value[0] if value[1] else self.model.ruby_scale

        value = settings.value("ruby reference position").toFloat()
        self.model.reference_position = value[0] if value[1] else self.model.reference_position

        value = settings.value("ruby reference temperature").toFloat()
        self.model.reference_temperature = value[0] if value[1] else self.model.reference_temperature

        value = settings.value("ruby sample position").toFloat()
        self.model.sample_position = value[0] if value[1] else self.model.sample_position

        self.model.blockSignals(False)
        value = settings.value("ruby sample temperature").toFloat()
        self.model.sample_temperature = value[0] if value[1] else self.model.sample_temperature

        roi_str = str(settings.value("ruby roi").toString())
        if roi_str is not "":
            roi = [float(e) for e in roi_str.split()]
            self.model.roi = roi
            self.widget.roi_widget.set_rois([roi])
