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
import numpy as np

from qtpy import QtWidgets, QtCore
from qtpy.QtTest import QTest

from model.DiamondModel import DiamondModel
from widget.DiamondWidget import DiamondWidget
from controller.DiamondController import DiamondController

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, '..', 'test_files')
test_file = os.path.join(unittest_files_path, 'temper_009.spe')


class DiamondControllerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QtWidgets.QApplication([])

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        cls.app.deleteLater()


    def setUp(self):
        self.model = DiamondModel()
        self.widget = DiamondWidget(None)
        self.controller = DiamondController(self.model, self.widget)
        self.model.load_file(test_file)

    def input_txt_into_text_field(self, text_field, text):
        text_field.setText("")
        QTest.keyClicks(text_field, str(text))
        QTest.keyClick(text_field, QtCore.Qt.Key_Enter)

    def get_numeric_value_from_text_field(self, text_field):
        return float(str(text_field.text()))

    def test_derivative_is_shown_in_graph_widget(self):
        x_der, y_der = self.widget._derivative_item.getData()
        x, y = self.widget.graph_widget.get_data()
        self.assertTrue(np.array_equal(x, x_der))

    def test_changing_derivative_smoothing(self):
        _, y_der = self.widget._derivative_item.getData()
        self.widget.derivative_sb.setValue(10)
        _, y_der2 = self.widget._derivative_item.getData()
        self.assertFalse(np.array_equal(y_der, y_der2))

    def test_diamond_position_text_field(self):
        self.input_txt_into_text_field(self.widget.sample_position_txt, "1340")
        self.assertAlmostEqual(self.get_numeric_value_from_text_field(self.widget.pressure_lbl), 2.48)
        self.assertEqual(self.widget.get_diamond_line_pos(), 1340)

    def test_diamond_reference_text_field(self):
        self.input_txt_into_text_field(self.widget.reference_position_txt, "1332")
        self.assertNotEqual(float(str(self.widget.pressure_lbl.text())), 0)

    def test_clicking_in_graph_widget(self):
        self.widget.graph_widget.mouse_left_clicked.emit(1400, 100)
        self.assertEqual(self.get_numeric_value_from_text_field(self.widget.sample_position_txt), 1400)
        self.assertAlmostEqual(self.get_numeric_value_from_text_field(self.widget.pressure_lbl), 28.9)
        self.assertAlmostEqual(self.widget.get_diamond_line_pos(), 1400)

    def test_change_laser_line(self):
        x, y = self.widget.graph_widget.get_data()
        self.widget.laser_line_txt.setText('')
        self.input_txt_into_text_field(self.widget.laser_line_txt, 415)
        new_x, new_y = self.widget.graph_widget.get_data()

        self.assertFalse(np.array_equal(new_x, x))
        self.assertTrue(np.array_equal(new_y, y))
