# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest
import os
import numpy as np

from PyQt4 import QtGui, QtCore
from PyQt4.QtTest import QTest

from model.RamanModel import RamanModel
from widget.RamanWidget import RamanWidget
from controller.RamanController import RamanController

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, 'test_files')
test_file = os.path.join(unittest_files_path, 'temper_009.spe')


class RamanControllerTest(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.model = RamanModel()
        self.widget = RamanWidget(None)
        self.controller = RamanController(self.model, self.widget)
        self.model.load_file(test_file)

    def tearDown(self):
        del self.app

    def click_checkbox(self, checkbox):
        QTest.mouseClick(checkbox, QtCore.Qt.LeftButton, pos=QtCore.QPoint(2, checkbox.height() / 2))

    def test_laser_line(self):
        x, y = self.widget.graph_widget.get_data()
        self.widget.laser_line_txt.setText('')
        QTest.keyClicks(self.widget.laser_line_txt, "415")
        QTest.keyClick(self.widget.laser_line_txt, QtCore.Qt.Key_Enter)
        new_x, new_y = self.widget.graph_widget.get_data()

        self.assertFalse(np.array_equal(new_x, x))
        self.assertTrue(np.array_equal(new_y, y))

    def test_change_mode(self):
        x, y = self.widget.graph_widget.get_data()
        self.click_checkbox(self.widget.nanometer_cb)
        new_x, new_y = self.widget.graph_widget.get_data()
        self.assertFalse(np.array_equal(new_x, x))
        self.assertTrue(np.array_equal(new_y, y))
