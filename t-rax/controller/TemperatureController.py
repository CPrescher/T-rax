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

import os

from qtpy import QtWidgets, QtCore

from widget.TemperatureWidget import TemperatureWidget
from widget.Widgets import open_file_dialog, save_file_dialog
from model.TemperatureModel import TemperatureModel
from .NewFileInDirectoryWatcher import NewFileInDirectoryWatcher
import numpy as np

try:
    import epics
except ImportError:
    epics = None


class TemperatureController(QtCore.QObject):
    def __init__(self, temperature_widget, model):
        """
        :param temperature_widget: reference to the temperature widget
        :type temperature_widget: TemperatureWidget
        :param temperature_model: reference to the global temperature model
        :type model: TemperatureModel
        :return:
        """
        super(TemperatureController, self).__init__()
        self.widget = temperature_widget
        self.model = model

        self._exp_working_dir = ''
        self._setting_working_dir = ''

        self._create_autoprocess_system()
        self.create_signals()

    def create_signals(self):
        # File signals
        self.connect_click_function(self.widget.load_data_file_btn, self.load_data_file)
        self.widget.load_next_data_file_btn.clicked.connect(self.model.load_next_data_image)
        self.widget.load_previous_data_file_btn.clicked.connect(self.model.load_previous_data_image)
        self.widget.load_next_frame_btn.clicked.connect(self.model.load_next_img_frame)
        self.widget.load_previous_frame_btn.clicked.connect(self.model.load_previous_img_frame)
        self.widget.autoprocess_cb.toggled.connect(self.auto_process_cb_toggled)

        self.connect_click_function(self.widget.save_data_btn, self.save_data_btn_clicked)
        self.connect_click_function(self.widget.save_graph_btn, self.save_graph_btn_clicked)

        # Calibration signals
        self.connect_click_function(self.widget.load_ds_calibration_file_btn, self.load_ds_calibration_file)
        self.connect_click_function(self.widget.load_us_calibration_file_btn, self.load_us_calibration_file)

        self.widget.ds_etalon_rb.toggled.connect(self.model.set_ds_calibration_modus)
        self.widget.us_etalon_rb.toggled.connect(self.model.set_us_calibration_modus)

        self.connect_click_function(self.widget.ds_load_etalon_file_btn, self.load_ds_etalon_file)
        self.connect_click_function(self.widget.us_load_etalon_file_btn, self.load_us_etalon_file)

        self.widget.ds_temperature_txt.editingFinished.connect(self.ds_temperature_txt_changed)
        self.widget.us_temperature_txt.editingFinished.connect(self.us_temperature_txt_changed)

        # Setting signals
        self.connect_click_function(self.widget.load_setting_btn, self.load_setting_file)
        self.connect_click_function(self.widget.save_setting_btn, self.save_setting_file)
        self.widget.settings_cb.currentIndexChanged.connect(self.settings_cb_changed)

        # model signals
        self.model.data_changed.connect(self.data_changed)
        self.model.ds_calculations_changed.connect(self.ds_calculations_changed)
        self.model.us_calculations_changed.connect(self.us_calculations_changed)

        self.model.data_changed.connect(self.update_time_lapse)
        self.model.ds_calculations_changed.connect(self.update_time_lapse)
        self.model.us_calculations_changed.connect(self.update_time_lapse)

        self.widget.roi_widget.rois_changed.connect(self.widget_rois_changed)

        # mouse moved signals
        self.widget.graph_widget.mouse_moved.connect(self.graph_mouse_moved)
        self.widget.roi_widget.img_widget.mouse_moved.connect(self.roi_mouse_moved)

    def connect_click_function(self, emitter, function):
        emitter.clicked.connect(function)

    def load_data_file(self, filename=None):
        if filename is None or filename is False:
            filename = open_file_dialog(self.widget, caption="Load Experiment SPE",
                                        directory=self._exp_working_dir)

        if filename is not '':
            self._exp_working_dir = os.path.dirname(str(filename))
            self.model.load_data_image(str(filename))
            self._directory_watcher.path = self._exp_working_dir

    def load_ds_calibration_file(self, filename=None):
        if filename is None or filename is False:
            filename = open_file_dialog(self.widget, caption="Load Downstream Calibration SPE",
                                        directory=self._exp_working_dir)

        if filename is not '':
            self._exp_working_dir = os.path.dirname(filename)
            self.model.load_ds_calibration_image(filename)

    def load_us_calibration_file(self, filename=None):
        if filename is None or filename is False:
            filename = open_file_dialog(self.widget, caption="Load Upstream Calibration SPE",
                                        directory=self._exp_working_dir)

        if filename is not '':
            self._exp_working_dir = os.path.dirname(filename)
            self.model.load_us_calibration_image(filename)

    def ds_temperature_txt_changed(self):
        new_temperature = float(str(self.widget.ds_temperature_txt.text()))
        self.model.set_ds_calibration_temperature(new_temperature)

    def us_temperature_txt_changed(self):
        new_temperature = float(str(self.widget.us_temperature_txt.text()))
        self.model.set_us_calibration_temperature(new_temperature)

    def load_ds_etalon_file(self, filename=None):
        if filename is None or filename is False:
            filename = open_file_dialog(self.widget, caption="Load Downstream Etalon Spectrum",
                                        directory=self._exp_working_dir)

        if filename is not '':
            self._exp_working_dir = os.path.dirname(filename)
            self.model.load_ds_etalon_spectrum(filename)

    def load_us_etalon_file(self, filename=None):
        if filename is None or filename is False:
            filename = open_file_dialog(self.widget, caption="Load Upstream Etalon Spectrum",
                                        directory=self._exp_working_dir)

        if filename is not '':
            self._exp_working_dir = os.path.dirname(filename)
            self.model.load_us_etalon_spectrum(filename)

    def save_setting_file(self, filename=None):
        if filename is None or filename is False:
            filename = save_file_dialog(self.widget, caption="Save setting file",
                                        directory=self._setting_working_dir)

        if filename is not '':
            self._setting_working_dir = os.path.dirname(filename)
            self.model.save_setting(filename)
            self.update_setting_combobox()

    def load_setting_file(self, filename=None):
        if filename is None or filename is False:
            filename = open_file_dialog(self.widget, caption="Load setting file",
                                        directory=self._setting_working_dir)

        if filename is not '':
            self._setting_working_dir = os.path.dirname(filename)
            self.model.load_setting(filename)
            self.update_setting_combobox()

    def save_data_btn_clicked(self, filename=None):
        if filename is None or filename is False:
            filename = save_file_dialog(
                self.widget,
                caption="Save data in tabulated text format",
                directory=os.path.join(self._exp_working_dir,
                                       '.'.join(self.model.data_img_file.filename.split(".")[:-1]) + ".txt")
            )
        if filename is not '':
            self.model.save_txt(filename)

    def save_graph_btn_clicked(self, filename=None):
        if filename is None or filename is False:
            filename = save_file_dialog(
                self.widget,
                caption="Save displayed graph as vector graphics or image",
                directory=os.path.join(self._exp_working_dir,
                                       '.'.join(self.model.data_img_file.filename.split(".")[:-1]) + ".svg"),
                filter='Vector Graphics (*.svg);; Image (*.png)'
            )
        filename = str(filename)

        if filename is not '':
            self.widget.graph_widget.save_graph(filename)

    def update_setting_combobox(self):
        self._settings_files_list = []
        self._settings_file_names_list = []
        try:
            for file in os.listdir(self._setting_working_dir):
                if file.endswith('.trs'):
                    self._settings_files_list.append(file)
                    self._settings_file_names_list.append(file.split('.')[:-1][0])
        except:
            pass
        self.widget.settings_cb.blockSignals(True)
        self.widget.settings_cb.clear()
        self.widget.settings_cb.addItems(self._settings_file_names_list)
        self.widget.settings_cb.blockSignals(False)

    def settings_cb_changed(self):
        current_index = self.widget.settings_cb.currentIndex()
        new_file_name = os.path.join(self._setting_working_dir,
                                     self._settings_files_list[current_index])  # therefore also one has to be deleted
        self.load_setting_file(new_file_name)
        self.widget.settings_cb.blockSignals(True)
        self.widget.settings_cb.setCurrentIndex(current_index)
        self.widget.settings_cb.blockSignals(False)

    def data_changed(self):
        self.widget.roi_widget.plot_img(self.model.data_img)
        self.widget.roi_widget.set_rois(self.model.get_roi_data_list())

        # update exp data widget
        #####################################

        if self.model.data_img_file is not None:
            self.widget.filename_lbl.setText(os.path.basename(self.model.data_img_file.filename))
            dirname = os.path.sep.join(os.path.dirname(self.model.data_img_file.filename).split(os.path.sep)[-2:])
            self.widget.dirname_lbl.setText(dirname)
            if self.model.data_img_file.num_frames > 1:
                self.widget.frame_widget.setVisible(True)
                self.widget.graph_widget.show_time_lapse_plot(True)
            else:
                self.widget.frame_widget.setVisible(False)
                self.widget.graph_widget.show_time_lapse_plot(False)
            self.widget.frame_num_txt.setText(str(self.model.current_frame + 1))
            self.widget.graph_info_lbl.setText(self.model.file_info)
        else:
            self.widget.filename_lbl.setText('Select File...')
            self.widget.dirname_lbl.setText('')
            self.widget.frame_widget.setVisible(False)
            self.widget.graph_widget.show_time_lapse_plot(False)

        self.ds_calculations_changed()
        self.us_calculations_changed()

    def ds_calculations_changed(self):
        if self.model.ds_calibration_filename is not None:
            self.widget.ds_calibration_filename_lbl.setText(str(os.path.basename(self.model.ds_calibration_filename)))
        else:
            self.widget.ds_calibration_filename_lbl.setText('Select File...')

        self.widget.ds_etalon_filename_lbl.setText(str(os.path.basename(self.model.ds_etalon_filename)))
        self.widget.ds_etalon_rb.setChecked(self.model.ds_temperature_model.calibration_parameter.modus)
        self.widget.ds_temperature_txt.setText(str(self.model.ds_temperature_model.calibration_parameter.temperature))

        if len(self.model.ds_corrected_spectrum):
            ds_plot_spectrum = self.model.ds_corrected_spectrum
        else:
            ds_plot_spectrum = self.model.ds_data_spectrum

        self.widget.graph_widget.plot_ds_data(*ds_plot_spectrum.data)
        self.widget.graph_widget.plot_ds_fit(*self.model.ds_fit_spectrum.data)

        self.widget.graph_widget.update_ds_temperature_txt(self.model.ds_temperature,
                                                           self.model.ds_temperature_error)
        self.widget.graph_widget.update_ds_roi_max_txt(self.model.ds_temperature_model.data_roi_max)

        if self.widget.connect_to_epics_cb.isChecked():
            if epics is not None:
                epics.caput("13IDD:ds_las_temp", self.model.ds_temperature)
                epics.caput("13IDD:dn_t_int", str(self.model.ds_roi_max))

    def us_calculations_changed(self):
        if self.model.us_calibration_filename is not None:
            self.widget.us_calibration_filename_lbl.setText(str(os.path.basename(self.model.us_calibration_filename)))
        else:
            self.widget.us_calibration_filename_lbl.setText('Select File...')

        self.widget.us_etalon_filename_lbl.setText(str(os.path.basename(self.model.us_etalon_filename)))
        self.widget.us_etalon_rb.setChecked(self.model.us_temperature_model.calibration_parameter.modus)
        self.widget.us_temperature_txt.setText(str(self.model.us_temperature_model.calibration_parameter.temperature))

        if len(self.model.us_corrected_spectrum):
            us_plot_spectrum = self.model.us_corrected_spectrum
        else:
            us_plot_spectrum = self.model.us_data_spectrum

        self.widget.graph_widget.plot_us_data(*us_plot_spectrum.data)
        self.widget.graph_widget.plot_us_fit(*self.model.us_fit_spectrum.data)
        self.widget.graph_widget.update_us_temperature_txt(self.model.us_temperature,
                                                           self.model.us_temperature_error)
        self.widget.graph_widget.update_us_roi_max_txt(self.model.us_temperature_model.data_roi_max)

        if self.widget.connect_to_epics_cb.isChecked():
            if epics is not None:
                epics.caput("13IDD:us_las_temp", self.model.us_temperature)
                epics.caput("13IDD:up_t_int", str(self.model.us_roi_max))

    def update_time_lapse(self):
        us_temperature, us_temperature_error, ds_temperature, ds_temperature_error = self.model.fit_all_frames()
        self.widget.graph_widget.plot_ds_time_lapse(range(0, len(ds_temperature)), ds_temperature)
        self.widget.graph_widget.plot_us_time_lapse(range(0, len(us_temperature)), us_temperature)

        self.widget.graph_widget.update_time_lapse_ds_temperature_txt(np.mean(ds_temperature),
                                                                      np.std(ds_temperature))

        self.widget.graph_widget.update_time_lapse_us_temperature_txt(np.mean(us_temperature),
                                                                      np.std(us_temperature))

        self.widget.graph_widget.update_time_lapse_combined_temperature_txt(
            np.mean(ds_temperature + us_temperature),
            np.std(ds_temperature + us_temperature)
        )

    def widget_rois_changed(self, roi_list):
        if self.model.has_data():
            self.model.set_rois(roi_list[0], roi_list[1])

    def graph_mouse_moved(self, x, y):
        self.widget.graph_mouse_pos_lbl.setText("X: {:8.2f}  Y: {:8.2f}".format(x, y))

    def roi_mouse_moved(self, x, y):
        x = np.floor(x)
        y = np.floor(y)
        try:
            self.widget.roi_widget.pos_lbl.setText("X: {:5.0f}  Y: {:5.0f}    Int: {:6.0f}    lambda: {:5.2f} nm".
                                                   format(x, y,
                                                          self.model.data_img[int(y), int(x)],
                                                          self.model.data_img_file.x_calibration[int(x)]))
        except (IndexError, TypeError):
            pass

    def save_settings(self, settings):
        if self.model.data_img_file:
            settings.setValue("temperature data file", self.model.data_img_file.filename)
        settings.setValue("temperature settings directory", self._setting_working_dir)
        settings.setValue("temperature settings file", str(self.widget.settings_cb.currentText()))

        settings.setValue("temperature autoprocessing",
                          self.widget.autoprocess_cb.isChecked())

        settings.setValue("temperature epics connected",
                          self.widget.connect_to_epics_cb.isChecked())

    def load_settings(self, settings):
        temperature_data_path = str(settings.value("temperature data file"))
        if os.path.exists(temperature_data_path):
            self.load_data_file(temperature_data_path)

        settings_file_path = os.path.join(str(settings.value("temperature settings directory")),
                                          str(settings.value("temperature settings file")) + ".trs")
        if os.path.exists(settings_file_path):
            self.load_setting_file(settings_file_path)

        temperature_autoprocessing = settings.value("temperature autoprocessing") == 'true'
        if temperature_autoprocessing:
            self.widget.autoprocess_cb.setChecked(True)

        self.widget.connect_to_epics_cb.setChecked(
            settings.value("temperature epics connected") == 'true'
        )

    def auto_process_cb_toggled(self):
        if self.widget.autoprocess_cb.isChecked():
            print('activate')
            self._directory_watcher.activate()
        else:
            self._directory_watcher.deactivate()

    def _create_autoprocess_system(self):
        self._directory_watcher = NewFileInDirectoryWatcher(file_types=['.spe'])
        self._directory_watcher.file_added.connect(self.load_data_file)
