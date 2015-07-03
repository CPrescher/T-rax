# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtGui, QtCore

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


class DisplayModeGroupBox(QtGui.QGroupBox):
    def __init__(self, title='Options'):
        super(DisplayModeGroupBox, self).__init__(title)

        self.create_widgets()
        self.create_layout()
        self.style_widgets()

        self._reverse_cm_cb.setChecked(True)

    def create_widgets(self):
        self._laser_line_lbl = QtGui.QLabel('Laser Line:')
        self._laser_line_txt = QtGui.QLineEdit('532')
        self._laser_lint_unit_lbl = QtGui.QLabel('nm')

        self._mode_lbl = QtGui.QLabel('Unit:')
        self._reverse_cm_cb = QtGui.QRadioButton('cm-1')
        self._nanometer_cb = QtGui.QRadioButton('nm')

    def create_layout(self):
        self._laser_line_layout = QtGui.QHBoxLayout()
        self._laser_line_layout.addWidget(self._laser_line_txt)
        self._laser_line_layout.addWidget(self._laser_lint_unit_lbl)

        self._mode_layout = QtGui.QHBoxLayout()
        self._reverse_cm_layout = QtGui.QHBoxLayout()
        self._reverse_cm_layout.setSpacing(1)
        self._reverse_cm_layout.addWidget(self._reverse_cm_cb)
        self._mode_layout.addLayout(self._reverse_cm_layout)
        self._mode_layout.addWidget(self._nanometer_cb)

        self._layout = QtGui.QGridLayout()
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
    app = QtGui.QApplication([])
    widget = RamanWidget(parent=None)
    widget.show()
    app.exec_()
