# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtCore, QtGui
from PyQt4.QtTest import QTest
import unittest
import os
import numpy as np

from controller.MainController import TRaxMainController

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, 'unittest files')

class TestNewTemperatureController(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.main_controller = TRaxMainController()
        self.controller = self.main_controller.temperature_controller
        self.model = self.controller.data
        self.widget = self.main_controller.main_view.temperature_control_widget

    def tearDown(self):
        del self.app

    def array_almost_equal(self, array1, array2):
        self.assertAlmostEqual(np.sum(array1 - array2), 0)

    def array_not_almost_equal(self, array1, array2):
        self.assertNotAlmostEqual(np.sum(array1 - array2), 0)

    def test_loading_data(self):
        self.controller.load_exp_data(
            os.path.join(unittest_files_path, 'temper_009.spe')
        )

        self.assertGreater(len(self.model.ds_data_spectrum), 0)
        self.assertGreater(len(self.model.us_data_spectrum), 0)

        ds_x, ds_y = self.model.ds_data_spectrum.data
        us_x, us_y = self.model.us_data_spectrum.data

        QTest.mouseClick(self.widget.load_next_exp_data_btn, QtCore.Qt.LeftButton)

        ds_x_1, ds_y_1 = self.model.ds_data_spectrum.data
        us_x_1, us_y_1 = self.model.us_data_spectrum.data

        self.array_almost_equal(ds_x, ds_x_1)
        self.array_not_almost_equal(ds_y, ds_y_1)

        self.array_almost_equal(us_x, us_x_1)
        self.array_not_almost_equal(us_y, us_y_1)

        QTest.mouseClick(self.widget.load_previous_exp_data_btn, QtCore.Qt.LeftButton)

        ds_x_2, ds_y_2 = self.model.ds_data_spectrum.data
        us_x_2, us_y_2 = self.model.us_data_spectrum.data

        self.array_almost_equal(ds_x, ds_x_2)
        self.array_almost_equal(ds_y, ds_y_2)
        self.array_almost_equal(us_x, us_x_2)
        self.array_almost_equal(us_y, us_y_2)

    def test_temperature_fitting(self):
        temperature_fitting_path = os.path.join(
            unittest_files_path, 'temperature fitting')
        self.controller.load_exp_data(os.path.join(
            temperature_fitting_path,
            'test_measurement_multiple.spe'))

        self.controller.load_ds_calibration_data(os.path.join(temperature_fitting_path, 'ds_calibration.spe'))
        self.controller.load_us_calibration_data(os.path.join(temperature_fitting_path, 'us_calibration.spe'))

        self.controller.load_ds_etalon_data(os.path.join(temperature_fitting_path, '15A_lamp.txt'))
        self.controller.load_us_etalon_data(os.path.join(temperature_fitting_path, '15A_lamp.txt'))

        QTest.mouseClick(self.widget.ds_etalon_rb, QtCore.Qt.LeftButton)
        QTest.mouseClick(self.widget.us_etalon_rb, QtCore.Qt.LeftButton)


