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

from PyQt4 import QtGui, QtCore
import pyqtgraph as pg

from .BaseWidget import BaseWidget


class RubyWidget(BaseWidget, object):
    def __init__(self, parent):
        super(RubyWidget, self).__init__()

        self._ruby_pressure_gb = RubyPressureGroupBox()
        self.add_control_widget(self._ruby_pressure_gb)

        self.create_ruby_shortcuts()
        self.modify_graph_widget()

    def create_ruby_shortcuts(self):
        self.sample_position_txt = self._ruby_pressure_gb._sample_position_txt
        self.reference_position_txt = self._ruby_pressure_gb._reference_position_txt
        self.sample_temperature_txt = self._ruby_pressure_gb._sample_temperature_txt
        self.reference_temperature_txt = self._ruby_pressure_gb._reference_temperature_txt
        self.pressure_lbl = self._ruby_pressure_gb._pressure_lbl

        self.ruby_scale_cb = self._ruby_pressure_gb._ruby_scale_cb

        self.fit_ruby_btn = self._ruby_pressure_gb._fit_ruby_btn
        self.fit_ruby_automatic_cb = self._ruby_pressure_gb._fit_automatic_cb

    def modify_graph_widget(self):
        self._ruby_line = pg.InfiniteLine(pen=pg.mkPen((197, 0, 3), width=2))
        self.graph_widget.add_item(self._ruby_line)

        self._fitted_spectrum = pg.PlotDataItem(pen=pg.mkPen("#f00", width=1.5))
        self.graph_widget.add_item(self._fitted_spectrum)

    def set_ruby_line_pos(self, value):
        self._ruby_line.setValue(value)

    def get_ruby_line_pos(self):
        return self._ruby_line.value()

    def set_fitted_spectrum(self, x, y):
        self._fitted_spectrum.setData(x, y)


class RubyPressureGroupBox(QtGui.QGroupBox):
    def __init__(self, title="Ruby Pressure"):
        super(RubyPressureGroupBox, self).__init__(title)

        self._create_widgets()
        self._create_layout()
        self._style_widgets()

    def _create_widgets(self):
        self._reference_lbl = QtGui.QLabel("Reference")
        self._sample_lbl = QtGui.QLabel("Sample")

        self._position_lbl = QtGui.QLabel("Position")
        self._position_unit_lbl = QtGui.QLabel("(nm)")
        self._temperature_lbl = QtGui.QLabel("Temp.")
        self._temperature_unit_lbl = QtGui.QLabel("(K)")

        self._reference_position_txt = QtGui.QLineEdit("694.35")
        self._reference_temperature_txt = QtGui.QLineEdit("298")

        self._sample_position_txt = QtGui.QLineEdit("694.35")
        self._sample_temperature_txt = QtGui.QLineEdit("298")

        self._ruby_scale_cb = QtGui.QComboBox()
        self._ruby_scale_cb.addItems(["Dewaele et al. 2008",
                                      "Mao et al. 1988 hydrostatic",
                                      "Mao et al. 1988 nonhydrostatic"])

        self._pressure_lbl = QtGui.QLabel("0")
        self._pressure_unit_lbl = QtGui.QLabel("GPa")

        self._fit_ruby_btn = QtGui.QPushButton('Fit Ruby Peaks')
        self._fit_automatic_cb = QtGui.QCheckBox('auto')

    def _create_layout(self):
        self._layout = QtGui.QGridLayout()

        self._layout.addWidget(self._ruby_scale_cb, 0, 0, 1, 3)

        self._layout.addWidget(self._position_lbl, 1, 1)
        self._layout.addWidget(self._position_unit_lbl, 2, 1)

        self._layout.addWidget(self._temperature_lbl, 1, 2)
        self._layout.addWidget(self._temperature_unit_lbl, 2, 2)

        self._layout.addWidget(self._reference_lbl, 3, 0)
        self._layout.addWidget(self._sample_lbl, 4, 0)

        self._layout.addWidget(self._reference_position_txt, 3, 1)
        self._layout.addWidget(self._reference_temperature_txt, 3, 2)

        self._layout.addWidget(self._sample_position_txt, 4, 1)
        self._layout.addWidget(self._sample_temperature_txt, 4, 2)

        self._layout.addWidget(self._pressure_lbl, 6, 0, 1, 2)
        self._layout.addWidget(self._pressure_unit_lbl, 6, 2)

        self._layout.addWidget(self._fit_ruby_btn, 7, 0, 1, 2)
        self._layout.addWidget(self._fit_automatic_cb, 7, 2)

        self.setLayout(self._layout)

    def _style_widgets(self):
        vcenter_hright = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight
        vcenter_hcenter = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter
        self._position_lbl.setAlignment(vcenter_hcenter)
        self._temperature_lbl.setAlignment(vcenter_hcenter)
        self._position_unit_lbl.setAlignment(vcenter_hcenter)
        self._temperature_unit_lbl.setAlignment(vcenter_hcenter)

        self._reference_lbl.setAlignment(vcenter_hright)
        self._sample_lbl.setAlignment(vcenter_hright)
        self._reference_position_txt.setAlignment(vcenter_hright)
        self._reference_temperature_txt.setAlignment(vcenter_hright)
        self._sample_position_txt.setAlignment(vcenter_hright)
        self._sample_temperature_txt.setAlignment(vcenter_hright)

        max_width_position = 70
        max_width_temperature = 50
        self._reference_position_txt.setMaximumWidth(max_width_position)
        self._sample_position_txt.setMaximumWidth(max_width_position)
        self._reference_temperature_txt.setMaximumWidth(max_width_temperature)
        self._sample_temperature_txt.setMaximumWidth(max_width_temperature)

        self._reference_position_txt.setValidator(QtGui.QDoubleValidator())
        self._reference_temperature_txt.setValidator(QtGui.QDoubleValidator())
        self._sample_position_txt.setValidator(QtGui.QDoubleValidator())
        self._sample_temperature_txt.setValidator(QtGui.QDoubleValidator())

        self._pressure_lbl.setAlignment(vcenter_hright)

        self._pressure_lbl.setStyleSheet("font:bold 20px")
        self._pressure_unit_lbl.setStyleSheet("font:bold 20px")

        cleanlooks = QtGui.QStyleFactory.create('plastique')
        self._ruby_scale_cb.setStyle(cleanlooks)


def horizontal_line():
    frame = QtGui.QFrame()
    frame.setFrameShape(QtGui.QFrame.HLine)
    frame.setFrameShadow(QtGui.QFrame.Sunken)
    return frame


if __name__ == '__main__':
    app = QtGui.QApplication([])
    widget = RubyPressureGroupBox()
    widget.show()
    widget.raise_()
    app.exec_()
