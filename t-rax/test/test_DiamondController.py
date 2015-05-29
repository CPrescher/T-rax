# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest
import os
import numpy as np

from PyQt4 import QtGui, QtCore
from PyQt4.QtTest import QTest

from model.DiamondModel import DiamondModel
from widget.DiamondWidget import DiamondWidget
from controller.DiamondController import DiamondController

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, 'test_files')
test_file = os.path.join(unittest_files_path, 'temper_009.spe')


class DiamondControllerTest(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.model = DiamondModel()
        self.widget = DiamondWidget(None)
        self.controller = DiamondController(self.model, self.widget)
        self.model.load_file(test_file)

    def tearDown(self):
        del self.app

    def input_txt_into_text_field(self, text_field, text):
        text_field.setText("")
        QTest.keyClicks(text_field, str(text))
        QTest.keyClick(text_field, QtCore.Qt.Key_Enter)

    def test_diamond_position_text_field(self):
        self.input_txt_into_text_field(self.widget.sample_pos_txt, "1340")
        self.assertNotEqual(float(str(self.widget.pressure_lbl.text())), 0)

    def test_diamond_reference_text_field(self):
        self.input_txt_into_text_field(self.widget.reference_pos_txt, "1332")
        self.assertNotEqual(float(str(self.widget.pressure_lbl.text())), 0)

    def test_change_laser_line(self):
        x, y = self.widget.graph_widget.get_data()
        self.widget.laser_line_txt.setText('')
        self.input_txt_into_text_field(self.widget.laser_line_txt, 415)
        new_x, new_y = self.widget.graph_widget.get_data()

        self.assertFalse(np.array_equal(new_x, x))
        self.assertTrue(np.array_equal(new_y, y))
