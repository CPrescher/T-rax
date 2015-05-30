# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtGui, QtCore
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
        self.sample_pos_txt = self._diamond_gb._sample_pos_txt
        self.reference_pos_txt = self._diamond_gb._reference_pos_txt
        self.laser_line_txt = self._diamond_gb._laser_line_txt
        self.derivative_sb = self._diamond_gb._derivative_sb

    def modify_graph_widget(self):
        self._diamond_line = pg.InfiniteLine(1334, pen=pg.mkPen((27, 0, 134), width=2))
        self._derivative_item = pg.PlotDataItem(pen=pg.mkPen((40, 0, 200)))
        self.graph_widget.add_item(self._diamond_line)
        self.graph_widget.add_item(self._derivative_item)

    def plot_derivative(self, x, y):
        self._derivative_item.setData(x, y)

    def set_diamond_line_pos(self, value):
        self._diamond_line.setValue(value)

    def get_diamond_line_pos(self):
        return self._diamond_line.value()


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

        self._derivative_lbl = QtGui.QLabel('Derivative:')
        self._derivative_sb = QtGui.QSpinBox()
        self._derivative_sb.setValue(5)
        self._derivative_sb.setMaximumWidth(100)

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
        self._layout.addWidget(self._pressure_unit_lbl, 6, 2)

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
