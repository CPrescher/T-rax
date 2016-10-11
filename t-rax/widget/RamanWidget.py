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

from qtpy import QtWidgets, QtCore

import pyqtgraph as pg

from .BaseWidget import BaseWidget


class RamanWidget(BaseWidget, object):
    def __init__(self, parent):
        super(RamanWidget, self).__init__(parent)

        self.display_mode_gb = DisplayModeGroupBox()
        self.add_control_widget(self.display_mode_gb)

        self.create_raman_shortcuts()

    def create_raman_shortcuts(self):
        self.laser_line_txt = self.display_mode_gb._laser_line_txt
        self.reverse_cm_cb = self.display_mode_gb._reverse_cm_cb
        self.nanometer_cb = self.display_mode_gb._nanometer_cb


class DisplayModeGroupBox(QtWidgets.QGroupBox):
    def __init__(self, title='Options'):
        super(DisplayModeGroupBox, self).__init__(title)

        self.create_widgets()
        self.create_layout()
        self.style_widgets()

        self._reverse_cm_cb.setChecked(True)

    def create_widgets(self):
        self._laser_line_lbl = QtWidgets.QLabel('Laser Line:')
        self._laser_line_txt = QtWidgets.QLineEdit('532')
        self._laser_lint_unit_lbl = QtWidgets.QLabel('nm')

        self._mode_lbl = QtWidgets.QLabel('Unit:')
        self._reverse_cm_cb = QtWidgets.QRadioButton('cm-1')
        self._nanometer_cb = QtWidgets.QRadioButton('nm')

    def create_layout(self):
        self._laser_line_layout = QtWidgets.QHBoxLayout()
        self._laser_line_layout.addWidget(self._laser_line_txt)
        self._laser_line_layout.addWidget(self._laser_lint_unit_lbl)

        self._mode_layout = QtWidgets.QHBoxLayout()
        self._reverse_cm_layout = QtWidgets.QHBoxLayout()
        self._reverse_cm_layout.setSpacing(1)
        self._reverse_cm_layout.addWidget(self._reverse_cm_cb)
        self._mode_layout.addLayout(self._reverse_cm_layout)
        self._mode_layout.addWidget(self._nanometer_cb)

        self._layout = QtWidgets.QGridLayout()
        self._layout.addWidget(self._laser_line_lbl, 0, 0)
        self._layout.addLayout(self._laser_line_layout, 0, 1)
        self._layout.addWidget(self._mode_lbl, 1, 0)
        self._layout.addLayout(self._mode_layout, 1, 1)

        self.setLayout(self._layout)

    def style_widgets(self):
        self._laser_line_txt.setMaximumWidth(50)

        align = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight
        self._laser_line_lbl.setAlignment(align)
        self._laser_line_txt.setAlignment(align)
        self._mode_lbl.setAlignment(align)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = RamanWidget(parent=None)
    widget.show()
    app.exec_()
