# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import os

from PyQt4 import QtGui, QtCore

from view.new.TemperatureWidget import TemperatureWidget
from model.new import TemperatureModel


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

        # model signals
        self.model.data_changed.connect(self.data_changed)

    def connect_click_function(self, emitter, function):
        self.widget.connect(emitter, QtCore.SIGNAL('clicked()'), function)

    def load_data_file(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.main_view, caption="Load Experiment SPE",
                                                             directory=self._exp_working_dir))

        if filename is not '':
            self._exp_working_dir = os.path.dirname(filename)
            self.model.load_data_image(filename)

    def data_changed(self):
        self.widget.roi_widget.plot_img(self.model.data_img)
        self.widget.roi_widget.set_rois(self.model.get_roi_data_list())

        self.model.fit_data()

        self.main_view.temperature_axes.update_graph(self.data.ds_corrected_spectrum, self.data.us_corrected_spectrum,
                                                     self.data.ds_data_roi_max, self.data.us_data_roi_max,
                                                     ds_calibration_filename_str, us_calibration_filename_str)
