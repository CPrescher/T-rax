# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtGui, QtCore

from .BaseWidget import BaseWidget


class DiamondWidget(BaseWidget, object):
    def __init__(self, parent):
        super(DiamondWidget, self).__init__()
        self._diamond_gb = DiamondPressureGroupBox()
        self.add_control_widget(self._diamond_gb)

        self.create_diamond_shortcuts()

    def create_diamond_shortcuts(self):
        self.pressure_lbl = self._diamond_gb._pressure_lbl
        self.sample_pos_txt = self._diamond_gb._sample_pos_txt
        self.reference_pos_txt = self._diamond_gb._reference_pos_txt
        self.laser_line_txt = self._diamond_gb._laser_line_txt


class DiamondPressureGroupBox(QtGui.QGroupBox):
    def __init__(self, title="Diamond Pressure"):
        super(DiamondPressureGroupBox, self).__init__(title)

        self._create_widgets()
        self._create_layout()
        self._style_widgets()

    def _create_widgets(self):
        self._laser_line_lbl = QtGui.QLabel('Laser Line:')
        self._laser_line_txt = QtGui.QLineEdit("532")
        self._laser_line_unit_lbl = QtGui.QLabel('nm')

        self._reference_pos_lbl = QtGui.QLabel('Reference:')
        self._reference_pos_txt = QtGui.QLineEdit('1334')
        self._reference_pos_unit_lbl = QtGui.QLabel('cm<sup>-1</sup>')

        self._sample_pos_lbl = QtGui.QLabel("Sample:")
        self._sample_pos_txt = QtGui.QLineEdit("1334")
        self._sample_pos_unit_lbl = QtGui.QLabel('cm<sup>-1</sup>')

        self._pressure_lbl = QtGui.QLabel("0")
        self._pressure_unit_lbl = QtGui.QLabel("GPa")

    def _create_layout(self):
        self._layout = QtGui.QGridLayout()

        self._layout.addWidget(self._laser_line_lbl, 0, 0)
        self._layout.addWidget(self._laser_line_txt, 0, 1)
        self._layout.addWidget(self._laser_line_unit_lbl, 0, 2)

        self._layout.addWidget(horizontal_line(), 1, 0, 1, 3)

        self._layout.addWidget(self._reference_pos_lbl, 2, 0)
        self._layout.addWidget(self._reference_pos_txt, 2, 1)
        self._layout.addWidget(self._reference_pos_unit_lbl, 2, 2)

        self._layout.addWidget(self._sample_pos_lbl, 3, 0)
        self._layout.addWidget(self._sample_pos_txt, 3, 1)
        self._layout.addWidget(self._sample_pos_unit_lbl, 3, 2)

        self._layout.addWidget(self._pressure_lbl, 4, 0, 1, 2)
        self._layout.addWidget(self._pressure_unit_lbl, 4, 2)

        self.setLayout(self._layout)

    def _style_widgets(self):
        vcenter_hright = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight
        vcenter_hcenter = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter

        self._laser_line_lbl.setAlignment(vcenter_hright)
        self._reference_pos_lbl.setAlignment(vcenter_hright)
        self._sample_pos_lbl.setAlignment(vcenter_hright)

        self._laser_line_txt.setAlignment(vcenter_hright)
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
    frame = QtGui.QFrame()
    frame.setFrameShape(QtGui.QFrame.HLine)
    frame.setFrameShadow(QtGui.QFrame.Sunken)
    return frame


if __name__ == '__main__':
    app = QtGui.QApplication([])
    widget = DiamondPressureGroupBox()
    widget.show()
    widget.raise_()
    app.exec_()
