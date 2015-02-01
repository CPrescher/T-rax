# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtCore, QtGui
from PyQt4.QtTest import QTest
import unittest
import os
import numpy as np

from controller.new.TemperatureController import TemperatureController
from view.new.TemperatureWidget import TemperatureWidget

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, 'unittest files')

class TestNewTemperatureController(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.widget = TemperatureWidget()
        self.controller = TemperatureController(self.widget)
        self.model = self.controller.model

    def tearDown(self):
        del self.model
        del self.widget
        del self.controller
        del self.app

    def array_almost_equal(self, array1, array2):
        self.assertAlmostEqual(np.sum(array1 - array2), 0)

    def array_not_almost_equal(self, array1, array2):
        self.assertNotAlmostEqual(np.sum(array1 - array2), 0)


    def test_gui_to_model_connection(self):
        self.controller.load_data_file(
            os.path.join(unittest_files_path, 'temper_009.spe')
        )

        self.assertGreater(len(self.model.ds_data_spectrum), 0)
        self.assertGreater(len(self.model.us_data_spectrum), 0)

        ds_x, ds_y = self.model.ds_data_spectrum.data
        us_x, us_y = self.model.us_data_spectrum.data

        QTest.mouseClick(self.widget.load_next_data_file_btn, QtCore.Qt.LeftButton)

        ds_x_1, ds_y_1 = self.model.ds_data_spectrum.data
        us_x_1, us_y_1 = self.model.us_data_spectrum.data

        self.array_almost_equal(ds_x, ds_x_1)
        self.array_not_almost_equal(ds_y, ds_y_1)

        self.array_almost_equal(us_x, us_x_1)
        self.array_not_almost_equal(us_y, us_y_1)

        QTest.mouseClick(self.widget.load_previous_data_file_btn, QtCore.Qt.LeftButton)

        ds_x_2, ds_y_2 = self.model.ds_data_spectrum.data
        us_x_2, us_y_2 = self.model.us_data_spectrum.data

        self.array_almost_equal(ds_x, ds_x_2)
        self.array_almost_equal(ds_y, ds_y_2)
        self.array_almost_equal(us_x, us_x_2)
        self.array_almost_equal(us_y, us_y_2)

    def test_model_to_gui_connection(self):
        self.controller.load_data_file(
            os.path.join(unittest_files_path, 'temper_009.spe')
        )

        self.array_almost_equal(self.widget.roi_img_item.image, self.model.data_img)

        self.assertEqual(self.widget.roi_widget.get_rois(),
                         self.model.get_roi_data_list())



