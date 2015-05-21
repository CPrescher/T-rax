# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest
from mock import patch
import os

from PyQt4 import QtGui, QtCore
from PyQt4.QtTest import QTest

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, 'test_files')

from widget.RamanWidget import RamanWidget
from controller.RamanController import RamanController


class RamanControllerTest(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.widget = RamanWidget()
        self.controller = RamanController(self.widget)
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

    def test_changing_roi(self):
        self.controller.load_data_file(os.path.join(unittest_files_path, 'temper_009.spe'))
