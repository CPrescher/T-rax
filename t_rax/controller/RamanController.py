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

from qtpy import QtCore, QtWidgets
import os

from ..model.RamanModel import RamanModel
from ..controller.BaseController import BaseController


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
        self.widget.sample_position_txt.editingFinished.connect(self.sample_pos_txt_changed)

        self.widget.graph_widget.mouse_left_clicked.connect(self.mouse_left_clicked)

        self.widget.overlay_gb.overlay_add_btn.clicked.connect(self.overlay_add_btn_clicked)
        self.model.overlay_added.connect(self.overlay_added)
        self.widget.overlay_gb.overlay_remove_btn.clicked.connect(self.overlay_remove_btn_clicked)
        self.model.overlay_removed.connect(self.overlay_removed)
        self.widget.overlay_gb.overlay_clear_btn.clicked.connect(self.overlay_clear_btn_clicked)
        self.widget.overlay_show_cb_state_changed.connect(self.overlay_show_cb_state_changed)
        self.widget.overlay_color_btn_clicked.connect(self.overlay_color_btn_clicked)
        self.model.overlay_changed.connect(self.overlay_changed)
        self.widget.overlay_tw.currentCellChanged.connect(self.overlay_selected)

        self.widget.overlay_gb.scale_step_msb.editingFinished.connect(self.update_scale_step)
        self.widget.overlay_gb.offset_step_msb.editingFinished.connect(self.update_overlay_offset_step)
        self.widget.overlay_gb.scale_sb.valueChanged.connect(self.overlay_scale_sb_changed)
        self.widget.overlay_gb.offset_sb.valueChanged.connect(self.overlay_offset_sb_changed)

    def laser_line_txt_changed(self):
        new_laser_line = float(str(self.widget.laser_line_txt.text()))
        self.model.laser_line = new_laser_line

    def sample_pos_txt_changed(self):
        new_value = float(str(self.widget.sample_position_txt.text()))
        self.model.sample_position = new_value
        self.widget.set_raman_line_pos(new_value)

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

    def mouse_left_clicked(self, x, y):
        self.model.sample_position = x
        self.widget.sample_position_txt.setText("{:.2f}".format(x))
        self.widget.set_raman_line_pos(x)
        if self.model.mode == RamanModel.REVERSE_CM_MODE:
            x = self.model.convert_reverse_cm_to_wavelength(x, self.model.laser_line)
        ind = self.model.get_roi_ind_from_wavelength(x)
        self.widget.set_raman_roi_line_pos(ind)

    def update_widget_parameter(self):
        self.widget.laser_line_txt.setText("{:.2f}".format(self.model.laser_line))
        self.widget.sample_position_txt.setText("{:.2f}".format(self.model.sample_position))
        self.widget.set_raman_line_pos(self.model.sample_position)
        if self.model.mode == RamanModel.WAVELENGTH_MODE:
            self.widget.nanometer_cb.setChecked(True)

    def save_settings(self, settings):
        settings.setValue("raman data file", self.model.filename)
        settings.setValue("raman autoprocessing", self.widget.autoprocess_cb.isChecked())
        settings.setValue("raman laser line", self.model.laser_line)
        settings.setValue("raman mode", self.model.mode)
        settings.setValue("raman roi", " ".join(str(e) for e in self.model.roi.as_list()))

    def load_settings(self, settings):
        raman_data_path = str(settings.value("raman data file"))
        if os.path.exists(raman_data_path):
            self.base_controller.load_file_btn_clicked(raman_data_path)

        raman_autoprocessing = settings.value("raman autoprocessing") == 'True' or \
                               settings.value("raman autoprocessing") == 'true'
        if raman_autoprocessing:
            self.widget.autoprocess_cb.setChecked(True)

        value = float(settings.value("raman laser line"))
        self.model.laser_line = value

        value = int(settings.value("raman mode"))
        self.model.mode = value

        roi_str = str(settings.value("raman roi"))
        if roi_str != "":
            roi = [float(e) for e in roi_str.split()]
            self.model.roi = roi
            self.widget.roi_widget.set_rois([roi])

        self.update_widget_parameter()

    def overlay_add_btn_clicked(self):
        self.model.add_overlay()

    def overlay_added(self):
        color = self.widget.add_overlay(self.model.overlays[-1])
        # self.widget.add_overlay(self.model.overlays[-1].name,
        #                         '#%02x%02x%02x' % (int(color[0]), int(color[1]), int(color[2])))
        # self.widget.add_overlay(self.model.overlays[-1])
        self.widget.overlay_labels[-1].setText(os.path.basename(self.model.filename))

    def overlay_remove_btn_clicked(self):
        cur_ind = self.widget.get_selected_overlay_row()
        if cur_ind < 0:
            return
        # if self.model.pattern_model.background_pattern == self.model.overlay_model.overlays[cur_ind]:
            # self.model.pattern_model.background_pattern = None
        self.model.remove_overlay(cur_ind)

    def overlay_removed(self, ind):
        self.widget.remove_overlay(ind)


    def overlay_show_cb_state_changed(self, ind, state):
        """
        Callback for the checkboxes in the overlay tablewidget. Controls the visibility of the overlay in the pattern
        view
        :param ind: index of overlay
        :param state: boolean value whether the checkbox was checked or unchecked
        """
        if state:
            self.widget.show_overlay(ind)
        else:
            self.widget.hide_overlay(ind)

    def overlay_color_btn_clicked(self, ind, button):
        """
        Callback for the color buttons in the overlay table. Opens up a color dialog. The color of the overlay and
        its respective button will be changed according to the selection
        :param ind: overlay ind
        :param button: button to color
        """
        previous_color = button.palette().color(1)
        new_color = QtWidgets.QColorDialog.getColor(previous_color, self.widget)
        if new_color.isValid():
            color = str(new_color.name())
        else:
            color = str(previous_color.name())
        self.widget.set_overlay_color(ind, color)
        button.setStyleSheet('background-color:' + color)

    def overlay_clear_btn_clicked(self):
        """
        removes all currently loaded overlays
        """
        while self.widget.overlay_tw.rowCount() > 0:
            self.overlay_remove_btn_clicked()

    def update_scale_step(self):
        """
        Sets the step size for scale spinbox from the step text box.
        """
        value = self.widget.overlay_gb.scale_step_msb.value()
        self.widget.overlay_gb.scale_sb.setSingleStep(value)

    def update_overlay_offset_step(self):
        """
        Sets the step size for the offset spinbox from the offset_step text box.
        """
        value = self.widget.overlay_gb.offset_step_msb.value()
        self.widget.overlay_gb.offset_sb.setSingleStep(value)

    def overlay_scale_sb_changed(self, value):
        """
        Callback for overlay_scale_sb spinbox.
        :param value: new scale value
        """
        cur_ind = self.widget.get_selected_overlay_row()
        self.model.set_overlay_scaling(cur_ind, value)
        # if self.model.overlays[cur_ind] == self.model.background_pattern:
        #     self.model.pattern_changed.emit()

    def overlay_offset_sb_changed(self, value):
        """
        Callback gor the overlay_offset_sb spinbox.
        :param value: new value
        """
        cur_ind = self.widget.get_selected_overlay_row()
        self.model.set_overlay_offset(cur_ind, value)
        # if self.model.overlays[cur_ind] == self.model.background_pattern:
        #     self.model.pattern_changed.emit()

    def overlay_changed(self, ind):
        self.widget.update_overlay(self.model.overlays[ind], ind)
        cur_ind = self.widget.get_selected_overlay_row()
        if ind == cur_ind:
            self.widget.overlay_gb.offset_sb.blockSignals(True)
            self.widget.overlay_gb.scale_sb.blockSignals(True)
            self.widget.overlay_gb.offset_sb.setValue(self.model.get_overlay_offset(ind))
            self.widget.overlay_gb.scale_sb.setValue(self.model.get_overlay_scaling(ind))
            self.widget.overlay_gb.offset_sb.blockSignals(False)
            self.widget.overlay_gb.scale_sb.blockSignals(False)

    def overlay_selected(self, row, *args):
        """
        Callback when the selected row in the overlay table is changed. It will update the scale and offset values
        for the newly selected overlay and check whether it is set as background or not and check the
        the set_as_bkg_btn appropriately.
        :param row: selected row in the overlay table
        """
        cur_ind = row
        self.widget.overlay_gb.scale_sb.blockSignals(True)
        self.widget.overlay_gb.offset_sb.blockSignals(True)
        self.widget.overlay_gb.scale_sb.setValue(self.model.overlays[cur_ind].scaling)
        self.widget.overlay_gb.offset_sb.setValue(self.model.overlays[cur_ind].offset)
        self.widget.overlay_gb.scale_sb.blockSignals(False)
        self.widget.overlay_gb.offset_sb.blockSignals(False)
        # if self.model.background_pattern == self.model.overlay_model.overlays[cur_ind]:
        #     self.widget.set_as_bkg_btn.setChecked(True)
        # else:
        #     self.widget.set_as_bkg_btn.setChecked(False)