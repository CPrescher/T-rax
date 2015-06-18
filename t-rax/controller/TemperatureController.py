# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import os

from PyQt4 import QtGui, QtCore

from widget.TemperatureWidget import TemperatureWidget
from model.TemperatureModel import TemperatureModel
import numpy as np


class TemperatureController(QtCore.QObject):
    def __init__(self, temperature_widget):
        """
        :param temperature_widget: reference to the temperature widget
        :type temperature_widget: TemperatureWidget
        :return:
        """
        super(TemperatureController, self).__init__()
        self.widget = temperature_widget
        self.model = TemperatureModel()

        self.create_signals()

        self._exp_working_dir = ''
        self._setting_working_dir = ''

    def create_signals(self):
        # File signals
        self.connect_click_function(self.widget.load_data_file_btn, self.load_data_file)
        self.widget.load_next_data_file_btn.clicked.connect(self.model.load_next_data_image)
        self.widget.load_previous_data_file_btn.clicked.connect(self.model.load_previous_data_image)
        self.widget.load_next_frame_btn.clicked.connect(self.model.load_next_img_frame)
        self.widget.load_previous_frame_btn.clicked.connect(self.model.load_previous_img_frame)

        self.connect_click_function(self.widget.save_data_btn, self.save_data_file)

        # Calibration signals
        self.connect_click_function(self.widget.load_ds_calibration_file_btn, self.load_ds_calibration_file)
        self.connect_click_function(self.widget.load_us_calibration_file_btn, self.load_us_calibration_file)

        self.widget.ds_etalon_rb.toggled.connect(self.model.set_ds_calibration_modus)
        self.widget.us_etalon_rb.toggled.connect(self.model.set_us_calibration_modus)

        self.connect_click_function(self.widget.ds_load_etalon_file_btn, self.load_ds_etalon_file)
        self.connect_click_function(self.widget.us_load_etalon_file_btn, self.load_us_etalon_file)

        self.widget.ds_temperature_txt.editingFinished.connect(self.ds_temperature_txt_changed)
        self.widget.us_temperature_txt.editingFinished.connect(self.us_temperature_txt_changed)

        #Setting signals
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



    def connect_click_function(self, emitter, function):
        self.widget.connect(emitter, QtCore.SIGNAL('clicked()'), function)

    def load_data_file(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.widget, caption="Load Experiment SPE",
                                                             directory=self._exp_working_dir))

        if filename is not '':
            self._exp_working_dir = os.path.dirname(filename)
            self.model.load_data_image(filename)

    def load_ds_calibration_file(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.widget, caption="Load Downstream Calibration SPE",
                                                             directory=self._exp_working_dir))

        if filename is not '':
            self._exp_working_dir = os.path.dirname(filename)
            self.model.load_ds_calibration_image(filename)

    def load_us_calibration_file(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.widget, caption="Load Upstream Calibration SPE",
                                                             directory=self._exp_working_dir))

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
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.widget, caption="Load Downstream Etalon Spectrum",
                                                             directory=self._exp_working_dir))

        if filename is not '':
            self._exp_working_dir = os.path.dirname(filename)
            self.model.load_ds_etalon_spectrum(filename)

    def load_us_etalon_file(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.widget, caption="Load Upstream Etalon Spectrum",
                                                             directory=self._exp_working_dir))

        if filename is not '':
            self._exp_working_dir = os.path.dirname(filename)
            self.model.load_us_etalon_spectrum(filename)

    def save_setting_file(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getSaveFileName(self.widget, caption="Save setting file",
                                                             directory=self._setting_working_dir))

        if filename is not '':
            self._setting_working_dir = os.path.dirname(filename)
            self.model.save_setting(filename)
            self.update_setting_combobox()

    def load_setting_file(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.widget, caption="Load setting file",
                                                             directory=self._setting_working_dir))

        if filename is not '':
            self._setting_working_dir = os.path.dirname(filename)
            self.model.load_setting(filename)
            self.update_setting_combobox()

    def save_data_file(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getSaveFileName(
                parent=self.widget,
                caption="Save data in tabulated text format",
                directory=os.path.join(self._exp_working_dir,
                                       '.'.join(self.model.data_img_file.filename.split(".")[:-1]) + ".txt"))
            )
        if filename is not '':
            self.model.save_txt(filename)

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
        new_file_name = os.path.join(self._setting_working_dir, self._settings_files_list[current_index])# therefore also one has to be deleted
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
            self.widget.frame_num_txt.setText(str(self.model.current_frame+1))
        else:
            self.widget.filename_lbl.setText('Select File...')
            self.widget.dirname_lbl.setText('')
            self.widget.frame_widget.setVisible(False)
            self.widget.graph_widget.show_time_lapse_plot(False)

        self.ds_calculations_changed()
        self.us_calculations_changed()


    def ds_calculations_changed(self):
        if self.model.ds_calibration_filename is not None:
            self.widget.ds_calibration_filename_lbl.setText(os.path.basename(self.model.ds_calibration_filename))
        else:
            self.widget.ds_calibration_filename_lbl.setText('Select File...')


        self.widget.ds_etalon_filename_lbl.setText(os.path.basename(self.model.ds_etalon_filename))
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

    def us_calculations_changed(self):
        if self.model.us_calibration_filename is not None:
            self.widget.us_calibration_filename_lbl.setText(os.path.basename(self.model.us_calibration_filename))
        else:
            self.widget.us_calibration_filename_lbl.setText('Select File...')

        self.widget.us_etalon_filename_lbl.setText(os.path.basename(self.model.us_etalon_filename))
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


if __name__ == '__main__':
    app = QtGui.QApplication([])
    widget = TemperatureWidget()
    controller = TemperatureController(widget)
    widget.show()
    widget.raise_()
    app.exec_()
