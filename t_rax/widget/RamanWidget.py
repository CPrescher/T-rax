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

from qtpy import QtWidgets, QtCore

import pyqtgraph as pg
import numpy as np

from .BaseWidget import BaseWidget
from functools import partial
from colorsys import hsv_to_rgb


class RamanWidget(BaseWidget, object):

    overlay_show_cb_state_changed = QtCore.Signal(int, bool)
    overlay_color_btn_clicked = QtCore.Signal(int, QtWidgets.QWidget)

    def __init__(self, parent):
        super(RamanWidget, self).__init__(parent)

        self.display_mode_gb = DisplayModeGroupBox()
        self.add_control_widget(self.display_mode_gb)
        self.overlay_gb = OverlayGroupBox()
        self.add_control_widget(self.overlay_gb)
        self._body_layout = QtWidgets.QHBoxLayout()
        self.overlay_tw = ListTableWidget(columns=3)
        self._body_layout.addWidget(self.overlay_tw, 10)
        self.add_control_widget(self.overlay_tw)

        self.create_raman_shortcuts()
        self.modify_graph_widget()
        self.modify_roi_widget()

        # self.overlay_add_btn = QtWidgets.QPushButton('Add')
        # self._main_layout.addWidget(self.overlay_add_btn)
        self.overlays = []
        self.overlay_show_cbs = []
        self.overlay_labels = []
        self.overlay_color_btns = []

    def create_raman_shortcuts(self):
        self.laser_line_txt = self.display_mode_gb._laser_line_txt
        self.reverse_cm_cb = self.display_mode_gb._reverse_cm_cb
        self.nanometer_cb = self.display_mode_gb._nanometer_cb
        self.sample_position_txt = self.display_mode_gb._sample_pos_txt
        self.overlay_offset_sb = self.overlay_gb.offset_sb

    def modify_graph_widget(self):
        self._raman_vertical_line = pg.InfiniteLine(angle=90, pen=pg.mkPen((0, 197, 3), width=2))
        self.graph_widget.add_item(self._raman_vertical_line)
        self._raman_horizontal_line = pg.InfiniteLine(angle=0, pen=pg.mkPen((0, 197, 3), width=2))
        self.graph_widget.add_item(self._raman_horizontal_line)

    def modify_roi_widget(self):
        self._raman_roi_line = pg.InfiniteLine(pen=pg.mkPen((0, 197, 3), width=2))
        self.roi_widget.add_item(self._raman_roi_line)

    def set_raman_vertical_line_pos(self, value):
        self._raman_vertical_line.setValue(value)

    def get_raman_vertical_line_pos(self):
        return self._raman_vertical_line.value()

    def set_raman_horizontal_line_pos(self, value):
        self._raman_horizontal_line.setValue(value)

    def get_raman_horizontal_line_pos(self):
        return self._raman_horizontal_line.value()


    def set_raman_roi_line_pos(self, value):
        self._raman_roi_line.setValue(value)

    # def update_graph_range(self):
    #     x_range = list(self.plot_item.dataBounds(0))
    #     y_range = list(self.plot_item.dataBounds(1))
    #
    #     for ind, overlay in enumerate(self.overlays):
    #         if self.overlay_show[ind]:
    #             x_range_overlay = overlay.dataBounds(0)
    #             y_range_overlay = overlay.dataBounds(1)
    #             if x_range_overlay[0] < x_range[0]:
    #                 x_range[0] = x_range_overlay[0]
    #             if x_range_overlay[1] > x_range[1]:
    #                 x_range[1] = x_range_overlay[1]
    #             if y_range_overlay[0] < y_range[0]:
    #                 y_range[0] = y_range_overlay[0]
    #             if y_range_overlay[1] > y_range[1]:
    #                 y_range[1] = y_range_overlay[1]
    #
    #     if x_range[1] is not None and x_range[0] is not None:
    #         padding = self.view_box.suggestPadding(0)
    #         diff = x_range[1] - x_range[0]
    #         x_range = [x_range[0] - padding * diff,
    #                    x_range[1] + padding * diff]
    #
    #         self.view_box.setLimits(xMin=x_range[0], xMax=x_range[1])
    #
    #         if self.auto_range:
    #             self.view_box.setRange(xRange=x_range, padding=0)
    #
    #     if y_range[1] is not None and y_range[0] is not None:
    #         padding = self.view_box.suggestPadding(1)
    #         diff = y_range[1] - y_range[0]
    #         y_range = [y_range[0] - padding * diff,
    #                    y_range[1] + padding * diff]
    #
    #         self.view_box.setLimits(yMin=y_range[0], yMax=y_range[1])
    #
    #         if self.auto_range:
    #             self.view_box.setRange(yRange=y_range, padding=0)
    #     self.emit_sig_range_changed()

    def add_overlay(self, spectrum):
        x, y = spectrum.data
        color = calculate_color(len(self.overlays) + 1)
        self.overlays.append(pg.PlotDataItem(x, y, pen=pg.mkPen(color=color, width=2)))
        self.overlay_labels.append(QtWidgets.QTableWidgetItem('None'))
        self.graph_widget.add_item(self.overlays[-1])

        current_rows = self.overlay_tw.rowCount()
        self.overlay_tw.setRowCount(current_rows + 1)
        self.overlay_tw.blockSignals(True)

        show_cb = QtWidgets.QCheckBox()
        show_cb.setChecked(True)
        show_cb.stateChanged.connect(partial(self.overlay_show_cb_changed, show_cb))
        show_cb.setStyleSheet("background-color: transparent")
        self.overlay_tw.setCellWidget(current_rows, 0, show_cb)
        self.overlay_show_cbs.append(show_cb)

        color_button = QtWidgets.QPushButton()
        color_button.setStyleSheet("background-color: rgb({},{},{})".format(color[0], color[1], color[2]))
        color_button.clicked.connect(partial(self.overlay_color_btn_click, color_button))
        self.overlay_tw.setCellWidget(current_rows, 1, color_button)
        self.overlay_color_btns.append(color_button)

        name_item = self.overlay_labels[-1]
        name_item.setFlags(name_item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.overlay_tw.setItem(current_rows, 2, name_item)

        self.overlay_tw.setColumnWidth(0, 20)
        self.overlay_tw.setColumnWidth(1, 25)
        self.overlay_tw.setRowHeight(current_rows, 25)
        self.select_overlay(current_rows)
        self.overlay_tw.blockSignals(False)

    def overlay_show_cb_changed(self, checkbox):
        self.overlay_show_cb_state_changed.emit(self.overlay_show_cbs.index(checkbox), checkbox.isChecked())

    def hide_overlay(self, ind):
        self.graph_widget.remove_item(self.overlays[ind])
        # self.legend.hideItem(ind + 1)
        # self.overlay_show[ind] = False
        # self.update_graph_range()
        QtWidgets.QApplication.processEvents()

    def show_overlay(self, ind):
        self.graph_widget.add_item(self.overlays[ind])
        # self.legend.showItem(ind + 1)
        # self.overlay_show[ind] = True
        # self.update_graph_range()
        QtWidgets.QApplication.processEvents()

    def select_overlay(self, ind):
        if self.overlay_tw.rowCount() > 0:
            self.overlay_tw.selectRow(ind)

    def get_selected_overlay_row(self):
        selected = self.overlay_tw.selectionModel().selectedRows()
        try:
            row = selected[0].row()
        except IndexError:
            row = -1
        return row

    def remove_overlay(self, ind):
        self.overlay_tw.blockSignals(True)
        self.overlay_tw.removeRow(ind)
        self.overlay_tw.blockSignals(False)
        del self.overlay_show_cbs[ind]
        del self.overlay_color_btns[ind]
        del self.overlay_labels[ind]
        self.remove_overlay_from_graph(ind)

        if self.overlay_tw.rowCount() > ind:
            self.select_overlay(ind)
        else:
            self.select_overlay(self.overlay_tw.rowCount() - 1)

    def remove_overlay_from_graph(self, ind):
        self.graph_widget.remove_item(self.overlays[ind])
        del self.overlays[ind]
        # self.legend.hideItem(ind + 1)
        # self.overlay_show[ind] = False
        # self.update_graph_range()
        QtWidgets.QApplication.processEvents()

    def set_overlay_color(self, ind, color):
        self.overlays[ind].setPen(pg.mkPen(color=color, width=1.5))
        # self.legend.setItemColor(ind + 1, color)

    def overlay_color_btn_click(self, button):
        self.overlay_color_btn_clicked.emit(self.overlay_color_btns.index(button), button)

    def update_overlay(self, pattern, ind):
        x, y = pattern.data
        self.overlays[ind].setData(x, y)
        # self.update_graph_range()

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
        self._sample_pos_lbl = QtWidgets.QLabel('Cursor:')
        self._sample_pos_txt = QtWidgets.QLineEdit("0")


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
        self._layout.addWidget(self._sample_pos_lbl, 2, 0)
        self._layout.addWidget(self._sample_pos_txt, 2, 1)

        self.setLayout(self._layout)

    def style_widgets(self):
        self._laser_line_txt.setMaximumWidth(50)

        align = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight
        self._laser_line_lbl.setAlignment(align)
        self._laser_line_txt.setAlignment(align)
        self._mode_lbl.setAlignment(align)
        self._sample_pos_lbl.setAlignment(align)
        self._sample_pos_txt.setAlignment(align)

class OverlayGroupBox(QtWidgets.QGroupBox):
    def __init__(self, title='Overlay'):
        super(OverlayGroupBox, self).__init__(title)

        self.create_widgets()
        self.create_layout()
        self.style_widgets()

    def create_widgets(self):
        self.overlay_add_btn = QtWidgets.QPushButton('Add')
        self.overlay_remove_btn = QtWidgets.QPushButton('Remove')
        self.overlay_clear_btn = QtWidgets.QPushButton('Clear All')
        # self.overlay_tw = ListTableWidget(columns=3)
        self._offset_lbl = QtWidgets.QLabel('Offset:')
        self._scale_lbl = QtWidgets.QLabel('Scale:')
        self._value_lbl = QtWidgets.QLabel('Value')
        self._step_lbl = QtWidgets.QLabel('Step')

        self.scale_sb = QtWidgets.QDoubleSpinBox()
        self.offset_sb = QtWidgets.QDoubleSpinBox()
        self.scale_step_msb = QtWidgets.QDoubleSpinBox()
        self.offset_step_msb = QtWidgets.QDoubleSpinBox()


    def create_layout(self):
        self._overlaylayout = QtWidgets.QGridLayout()
        self._overlaylayout.addWidget(self.overlay_add_btn, 0, 0)
        self._overlaylayout.addWidget(self.overlay_remove_btn, 0, 1)
        self._overlaylayout.addWidget(self.overlay_clear_btn, 0, 2)
        self._overlaylayout.addWidget(self._value_lbl, 1, 1)
        self._overlaylayout.addWidget(self._step_lbl, 1, 2)
        self._overlaylayout.addWidget(self._offset_lbl, 2, 0)
        self._overlaylayout.addWidget(self.offset_sb, 2, 1)
        self._overlaylayout.addWidget(self.offset_step_msb, 2, 2)
        self._overlaylayout.addWidget(self._scale_lbl, 3, 0)
        self._overlaylayout.addWidget(self.scale_sb, 3, 1)
        self._overlaylayout.addWidget(self.scale_step_msb, 3, 2)

        self.setLayout(self._overlaylayout)

    def style_widgets(self):
        # align = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight
        # self.overlay_add_btn.setAlignment(align)
        align = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight
        self.scale_sb.setAlignment(align)
        self.offset_sb.setAlignment(align)
        self.scale_step_msb.setAlignment(align)
        self.offset_step_msb.setAlignment(align)
        self._value_lbl.setAlignment(QtCore.Qt.AlignHCenter)
        self._step_lbl.setAlignment(QtCore.Qt.AlignHCenter)

        self.scale_sb.setMinimum(-9999999)
        self.scale_sb.setMaximum(9999999)
        self.scale_sb.setValue(1.0)
        self.scale_sb.setSingleStep(0.01)

        self.offset_sb.setMaximum(999999998)
        self.offset_sb.setMinimum(-99999999)
        self.offset_sb.setValue(0.0)
        self.offset_sb.setSingleStep(100.0)

        self.scale_step_msb.setMaximum(10.0)
        self.scale_step_msb.setMinimum(0.01)
        self.scale_step_msb.setValue(0.01)
        self.scale_step_msb.setSingleStep(0.01)

        self.offset_step_msb.setMaximum(100000.0)
        self.offset_step_msb.setMinimum(0.01)
        self.offset_step_msb.setValue(100.0)
        self.offset_step_msb.setSingleStep(100.0)
        pass


class ListTableWidget(QtWidgets.QTableWidget):
    def __init__(self, columns=3):
        super(ListTableWidget, self).__init__()

        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setColumnCount(columns)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.setShowGrid(False)

def calculate_color(ind):
    s = 0.8
    v = 0.8
    h = (0.19 * (ind + 2)) % 1
    return np.array(hsv_to_rgb(h, s, v)) * 255


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = RamanWidget(parent=None)
    widget.show()
    app.exec_()
