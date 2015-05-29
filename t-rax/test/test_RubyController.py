# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest
import os

from PyQt4 import QtGui, QtCore

from PyQt4.QtTest import QTest

from model.RubyModel import RubyModel
from widget.RubyWidget import RubyWidget
from controller.RubyController import RubyController

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, 'test_files')
test_file = os.path.join(unittest_files_path, 'temper_009.spe')


class RubyControllerTest(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.model = RubyModel()
        self.widget = RubyWidget(None)
        self.controller = RubyController(self.model, self.widget)
        self.model.load_file(test_file)

    def tearDown(self):
        del self.app

    def input_txt_into_text_field(self, text_field, str):
        text_field.setText("")
        QTest.keyClicks(text_field, str)
        QTest.keyClick(text_field, QtCore.Qt.Key_Enter)

    def test_set_ruby_position_textfield_and_retrieve_pressure(self):
        self.input_txt_into_text_field(self.widget.sample_position_txt, "700")
        self.assertNotEqual(float(str(self.widget.pressure_lbl.text())), 0)

    def test_set_ruby_reference_position_text_and_retrieve_pressure(self):
        self.input_txt_into_text_field(self.widget.reference_position_txt, "694.15")
        self.assertNotEqual(float(str(self.widget.pressure_lbl.text())), 0)

    def test_set_sample_temperature_text_and_retrieve_pressure(self):
        self.input_txt_into_text_field(self.widget.sample_position_txt, "700")
        p1 = float(str(self.widget.pressure_lbl.text()))
        self.input_txt_into_text_field(self.widget.sample_temperature_txt, "1500")
        self.assertLess(float(str(self.widget.pressure_lbl.text())), p1)

    def test_set_ruby_reference_temperature_text_and_retrieve_pressure(self):
        self.input_txt_into_text_field(self.widget.sample_position_txt, "700")
        p1 = float(str(self.widget.pressure_lbl.text()))
        self.input_txt_into_text_field(self.widget.reference_temperature_txt, "600")
        self.assertGreater(float(str(self.widget.pressure_lbl.text())), p1)
