# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import os

from PyQt4 import QtGui, QtCore

from view.new.TemperatureWidget import TemperatureWidget
from model.new.TemperatureModel import TemperatureModel


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

    def create_signals(self):
        # File signals
        self.connect_click_function(self.widget.load_data_file_btn, self.load_data_file)
        self.widget.load_next_data_file_btn.clicked.connect(self.model.load_next_data_image)
        self.widget.load_previous_data_file_btn.clicked.connect(self.model.load_previous_data_image)
        self.widget.load_next_frame_btn.clicked.connect(self.model.load_next_img_frame)
        self.widget.load_previous_frame_btn.clicked.connect(self.model.load_previous_img_frame)

        # Calibration signals
        self.connect_click_function(self.widget.load_ds_calibration_file_btn, self.load_ds_calibration_file)
        self.connect_click_function(self.widget.load_us_calibration_file_btn, self.load_us_calibration_file)

        self.widget.ds_etalon_rb.toggled.connect(self.model.set_ds_calibration_modus)
        self.widget.us_etalon_rb.toggled.connect(self.model.set_us_calibration_modus)

        self.connect_click_function(self.widget.ds_load_etalon_file_btn, self.load_ds_etalon_file)
        self.connect_click_function(self.widget.us_load_etalon_file_btn, self.load_us_etalon_file)

        self.widget.ds_temperature_txt.editingFinished.connect(self.ds_temperature_txt_changed)
        self.widget.us_temperature_txt.editingFinished.connect(self.us_temperature_txt_changed)


        # model signals
        self.model.data_changed.connect(self.data_changed)
        self.model.ds_calculations_changed.connect(self.calculations_changed)
        self.model.us_calculations_changed.connect(self.calculations_changed)

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
            else:
                self.widget.frame_widget.setVisible(False)
            self.widget.frame_num_txt.setText(str(self.model.current_frame+1))
        else:
            self.widget.filename_lbl.setText('Select File...')
            self.widget.dirname_lbl.setText('')
            self.widget.frame_widget.setVisible(False)

        self.ds_calculations_changed()
        self.us_calculations_changed()


    def ds_calculations_changed(self):
        try:
            ds_calibration_filename_str = os.path.basename(self.model.ds_calibration_img_file.filename)
        except AttributeError as e:
            ds_calibration_filename_str = 'Select File...'

        self.widget.ds_calibration_filename_lbl.setText(ds_calibration_filename_str)
        self.widget.ds_etalon_filename_lbl.setText(os.path.basename(self.model.ds_etalon_filename))


        ds_data_roi_max = self.model.ds_temperature_model.data_roi_max
        us_data_roi_max = self.model.us_temperature_model.data_roi_max

        if len(self.model.ds_corrected_spectrum):
            ds_plot_spectrum = self.model.ds_corrected_spectrum
        else:
            ds_plot_spectrum = self.model.ds_data_spectrum

        if len(self.model.us_corrected_spectrum):
            us_plot_spectrum = self.model.us_corrected_spectrum
        else:
            us_plot_spectrum = self.model.us_data_spectrum


        self.widget.graph_widget.update_graph(ds_plot_spectrum, us_plot_spectrum,
                                              ds_data_roi_max, us_data_roi_max,
                                              '', '')

        self.widget.graph_widget.plot_ds_temperature_fit(
            self.model.ds_temperature,
            self.model.ds_temperature_error,
            self.model.ds_fit_spectrum
        )

    def us_calculations_changed(self):
        try:
            us_calibration_filename_str = os.path.basename(self.model.us_calibration_img_file.filename)
        except AttributeError as e:
            us_calibration_filename_str = 'Select File...'

        self.widget.us_calibration_filename_lbl.setText(us_calibration_filename_str)
        self.widget.us_etalon_filename_lbl.setText(os.path.basename(self.model.us_etalon_filename))


        ds_data_roi_max = self.model.ds_temperature_model.data_roi_max
        us_data_roi_max = self.model.us_temperature_model.data_roi_max

        if len(self.model.ds_corrected_spectrum):
            ds_plot_spectrum = self.model.ds_corrected_spectrum
        else:
            ds_plot_spectrum = self.model.ds_data_spectrum

        if len(self.model.us_corrected_spectrum):
            us_plot_spectrum = self.model.us_corrected_spectrum
        else:
            us_plot_spectrum = self.model.us_data_spectrum


        self.widget.graph_widget.update_graph(ds_plot_spectrum, us_plot_spectrum,
                                              ds_data_roi_max, us_data_roi_max,
                                              '', '')

        self.widget.graph_widget.plot_us_temperature_fit(
            self.model.us_temperature,
            self.model.us_temperature_error,
            self.model.us_fit_spectrum
        )

    def calculations_changed(self):
        self.us_calculations_changed()
        self.ds_calculations_changed()
        self.widget.graph_widget.redraw_figure()

    def widget_rois_changed(self, roi_list):
        self.model.set_rois(roi_list[0], roi_list[1])


if __name__ == '__main__':
    app = QtGui.QApplication([])
    widget = TemperatureWidget()
    controller = TemperatureController(widget)
    widget.show()
    widget.raise_()
    app.exec_()
