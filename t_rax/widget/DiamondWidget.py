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

from qtpy import QtWidgets, QtCore, QtGui
import pyqtgraph as pg

from .BaseWidget import BaseWidget


class DiamondWidget(BaseWidget, object):
    def __init__(self, parent):
        super(DiamondWidget, self).__init__()
        self._diamond_gb = DiamondPressureGroupBox()
        self.add_control_widget(self._diamond_gb)

        self.create_diamond_shortcuts()
        self.modify_graph_widget()

    def create_diamond_shortcuts(self):
        self.pressure_lbl = self._diamond_gb._pressure_lbl
        self.sample_position_txt = self._diamond_gb._sample_pos_txt
        self.reference_position_txt = self._diamond_gb._reference_pos_txt
        self.laser_line_txt = self._diamond_gb._laser_line_txt
        self.derivative_sb = self._diamond_gb._derivative_sb

    def modify_graph_widget(self):
        self._diamond_line = pg.InfiniteLine(1334, pen=pg.mkPen((150, 150, 250), width=2))
        self._derivative_item = pg.PlotDataItem(pen=pg.mkPen((100, 100, 200)))
        self.graph_widget.add_item(self._diamond_line)
        self.graph_widget.add_item(self._derivative_item)

    def plot_derivative(self, x, y):
        self._derivative_item.setData(x, y)

    def set_diamond_line_pos(self, value):
        self._diamond_line.setValue(value)

    def get_diamond_line_pos(self):
        return self._diamond_line.value()


class DiamondPressureGroupBox(QtWidgets.QGroupBox):
    def __init__(self, title="Diamond Pressure"):
        super(DiamondPressureGroupBox, self).__init__(title)

        self._create_widgets()
        self._create_layout()
        self._style_widgets()

    def _create_widgets(self):
        self._laser_line_lbl = QtWidgets.QLabel('Laser Line:')
        self._laser_line_txt = QtWidgets.QLineEdit("532")
        self._laser_line_unit_lbl = QtWidgets.QLabel('nm')

        self._derivative_lbl = QtWidgets.QLabel('Derivative:')
        self._derivative_sb = QtWidgets.QSpinBox()
        self._derivative_sb.setValue(5)
        self._derivative_sb.setMaximumWidth(100)

        self._reference_pos_lbl = QtWidgets.QLabel('Reference:')
        self._reference_pos_txt = QtWidgets.QLineEdit('1334')
        self._reference_pos_unit_lbl = QtWidgets.QLabel('cm<sup>-1</sup>')

        self._sample_pos_lbl = QtWidgets.QLabel("Sample:")
        self._sample_pos_txt = QtWidgets.QLineEdit("1334")
        self._sample_pos_unit_lbl = QtWidgets.QLabel('cm<sup>-1</sup>')

        self._pressure_lbl = QtWidgets.QLabel("0")
        self._pressure_unit_lbl = QtWidgets.QLabel("GPa")

    def _create_layout(self):
        self._layout = QtWidgets.QGridLayout()

        self._layout.addWidget(self._laser_line_lbl, 0, 0)
        self._layout.addWidget(self._laser_line_txt, 0, 1)
        self._layout.addWidget(self._laser_line_unit_lbl, 0, 2)

        self._layout.addWidget(self._derivative_lbl, 1, 0)
        self._layout.addWidget(self._derivative_sb, 1, 1)

        self._layout.addWidget(horizontal_line(), 2, 0, 1, 3)

        self._layout.addWidget(self._reference_pos_lbl, 3, 0)
        self._layout.addWidget(self._reference_pos_txt, 3, 1)
        self._layout.addWidget(self._reference_pos_unit_lbl, 3, 2)

        self._layout.addWidget(self._sample_pos_lbl, 4, 0)
        self._layout.addWidget(self._sample_pos_txt, 4, 1)
        self._layout.addWidget(self._sample_pos_unit_lbl, 4, 2)

        self._layout.addWidget(self._pressure_lbl, 5, 0, 1, 2)
        self._layout.addWidget(self._pressure_unit_lbl, 5, 2)

        self.setLayout(self._layout)

    def _style_widgets(self):
        vcenter_hright = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight

        self._laser_line_lbl.setAlignment(vcenter_hright)
        self._derivative_lbl.setAlignment(vcenter_hright)
        self._reference_pos_lbl.setAlignment(vcenter_hright)
        self._sample_pos_lbl.setAlignment(vcenter_hright)

        self._laser_line_txt.setAlignment(vcenter_hright)
        self._derivative_sb.setAlignment(vcenter_hright)
        self._reference_pos_txt.setAlignment(vcenter_hright)
        self._sample_pos_txt.setAlignment(vcenter_hright)

        self._pressure_lbl.setAlignment(vcenter_hright)

        max_width = 60

        self._laser_line_txt.setMaximumWidth(max_width)
        self._reference_pos_txt.setMaximumWidth(max_width)
        self._sample_pos_txt.setMaximumWidth(max_width)

        self._laser_line_txt.setValidator(QtGui.QDoubleValidator())
        self._reference_pos_txt.setValidator(QtGui.QDoubleValidator())
        self._sample_pos_txt.setValidator(QtGui.QDoubleValidator())

        self._pressure_lbl.setStyleSheet("font:bold 20px")
        self._pressure_unit_lbl.setStyleSheet("font:bold 20px")


def horizontal_line():
    frame = QtWidgets.QFrame()
    frame.setFrameShape(QtWidgets.QFrame.HLine)
    frame.setFrameShadow(QtWidgets.QFrame.Sunken)
    return frame


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = DiamondPressureGroupBox()
    widget.show()
    widget.raise_()
    app.exec_()
