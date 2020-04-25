# -*- coding: utf-8 -*-
# T-Rax - GUI program for analysis of spectroscopy data during
# diamond anvil cell experiments
# Copyright (C) 2016 Clemens Prescher (clemens.prescher@gmail.com)
# Institute for Geology and Mineralogy, University of Cologne
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import os

from qtpy import QtWidgets, QtCore

from qtpy.QtTest import QTest

from ...model.RubyModel import RubyModel
from ...widget.RubyWidget import RubyWidget
from ...controller.RubyController import RubyController

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, '..', 'test_files')
test_file = os.path.join(unittest_files_path, 'temper_009.spe')


class RubyControllerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QtWidgets.QApplication([])

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        cls.app.deleteLater()

    def setUp(self):
        self.model = RubyModel()
        self.widget = RubyWidget(None)
        self.controller = RubyController(self.model, self.widget)
        self.model.load_file(test_file)


    def input_txt_into_text_field(self, text_field, str):
        text_field.setText("")
        QTest.keyClicks(text_field, str)
        QTest.keyClick(text_field, QtCore.Qt.Key_Enter)

    def test_set_ruby_position_textfield_retrieve_pressure_and_set_line_pos(self):
        self.input_txt_into_text_field(self.widget.sample_position_txt, "700")
        self.assertNotEqual(float(str(self.widget.pressure_lbl.text())), 0)
        self.assertAlmostEqual(self.widget.get_ruby_line_pos(), 700)

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

    def test_change_ruby_equation_of_state_and_retrieve_pressure(self):
        self.input_txt_into_text_field(self.widget.sample_position_txt, "702")
        p1 = float(str(self.widget.pressure_lbl.text()))
        self.widget.ruby_scale_cb.setCurrentIndex(1)
        self.assertNotAlmostEqual(float(str(self.widget.pressure_lbl.text())), p1)

        self.widget.ruby_scale_cb.setCurrentIndex(2)
        self.assertNotAlmostEqual(float(str(self.widget.pressure_lbl.text())), p1)
