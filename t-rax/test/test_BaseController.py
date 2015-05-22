# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest
from mock import patch
import os
from numpy import array_equal

from PyQt4 import QtGui, QtCore
from PyQt4.QtTest import QTest

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, 'test_files')

from model.BaseModel import SingleSpectrumModel
from widget.BaseWidget import BaseWidget
from controller.BaseController import BaseController


class BaseControllerTest(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.widget = BaseWidget()
        self.model = SingleSpectrumModel()
        self.controller = BaseController(self.model, self.widget)
        self.model = self.controller.model

    def tearDown(self):
        del self.app

    @patch('PyQt4.QtGui.QFileDialog.getOpenFileName')
    def test_loading_files(self, filedialog):
        in_path = os.path.join(unittest_files_path, 'temper_009.spe')
        filedialog.return_value = in_path
        QTest.mouseClick(self.widget.load_file_btn, QtCore.Qt.LeftButton)

        self.assertIsNotNone(self.model.spectrum)
        self.assertEqual(str(self.widget.filename_lbl.text()), 'temper_009.spe')
        self.assertEqual(str(self.widget.dirname_lbl.text()), 'test/test_files')

        self.assertIsNotNone(self.widget.graph_widget._data_item.xData)
        self.assertIsNotNone(self.widget.graph_widget._data_item.yData)

        self.assertIsNotNone(self.widget.roi_widget.img_widget.img_data)
        self.assertNotEqual(str(self.widget.roi_widget.roi_gbs[0].x_min_txt.text()), "0")
        self.assertNotEqual(str(self.widget.roi_widget.roi_gbs[0].y_min_txt.text()), "0")
        self.assertNotEqual(str(self.widget.roi_widget.roi_gbs[0].x_max_txt.text()), "0")
        self.assertNotEqual(str(self.widget.roi_widget.roi_gbs[0].y_max_txt.text()), "0")

    def test_load_multiple_frame_file(self):
        self.controller.load_data_file(os.path.join(unittest_files_path,
                                                    'temperature_fitting',
                                                    'test_measurement_multiple.spe'))

        self.assertEqual(float(str(self.widget.frame_txt.text())), self.model.current_frame)

        img_data = self.widget.roi_widget.img_widget.img_data
        QTest.mouseClick(self.widget.load_next_frame_btn, QtCore.Qt.LeftButton)
        img_data2 = self.widget.roi_widget.img_widget.img_data
        self.assertFalse(array_equal(img_data, img_data2))
        QTest.mouseClick(self.widget.load_previous_frame_btn, QtCore.Qt.LeftButton)
        img_data3 = self.widget.roi_widget.img_widget.img_data
        self.assertTrue(array_equal(img_data, img_data3))


    def test_changing_roi(self):
        self.controller.load_data_file(os.path.join(unittest_files_path, 'temper_009.spe'))

        x, y = self.model.spectrum.data
        self.widget.roi_widget.roi_gbs[0].x_min_txt.setText("")
        QTest.keyClicks(self.widget.roi_widget.roi_gbs[0].x_min_txt, "0")
        QTest.keyPress(self.widget.roi_widget.roi_gbs[0].x_min_txt, QtCore.Qt.Key_Enter)

        new_x, new_y = self.model.spectrum.data
        self.assertNotEqual(len(x), len(new_x))
