# -*- coding: utf8 -*-
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
import os, sys
import numpy as np

from ..ehook import excepthook
from qtpy import QtWidgets, QtCore
from qtpy.QtTest import QTest

from model.RamanModel import RamanModel
from widget.RamanWidget import RamanWidget
from controller.RamanController import RamanController
from controller.BaseController import BaseController

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, '..', 'test_files')
test_file = os.path.join(unittest_files_path, 'test.spe')


class RamanControllerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QtWidgets.QApplication([])

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        cls.app.deleteLater()

    def setUp(self):
        self.model = RamanModel()
        self.widget = RamanWidget(None)
        self.controller = RamanController(self.model, self.widget)
        self.base_controller = BaseController(self.model, self.widget)
        self.model.load_file(test_file)

    def click_checkbox(self, checkbox):
        QTest.mouseClick(checkbox, QtCore.Qt.LeftButton, pos=QtCore.QPoint(2, checkbox.height() / 2))

    def click_button(widget):
        QTest.mouseClick(widget, QtCore.Qt.LeftButton)

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

########Testing Overlays########

class RamanOverlayControllerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QtWidgets.QApplication([])

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        cls.app.deleteLater()

    def setUp(self):
        self.widget = RamanWidget(None)
        self.model = RamanModel()
        # self.model.working_directories['overlay'] = unittest_files_path
        self.raman_controller = RamanController(self.model, self.widget)
        self.base_controller = BaseController(self.model, self.widget)
        # self.overlay_tw = self.widget.overlay_tw
        self.model.load_file(test_file)

    def tearDown(self):
        del self.raman_controller
        # del self.overlay_tw
        del self.widget
        del self.model
        # gc.collect()

    def test_add_overlay(self):
        sys.excepthook = excepthook
        self.widget.overlay_gb.overlay_add_btn.click()
        self.assertEqual(len(self.model.overlays), 1)
        self.assertEqual(self.widget.overlay_tw.rowCount(), 1)

    def test_remove_overlay(self):
        sys.excepthook = excepthook
        self.widget.overlay_gb.overlay_add_btn.click()
        self.widget.select_overlay(0)
        self.assertEqual(len(self.model.overlays), 1)

        self.widget.overlay_gb.overlay_remove_btn.click()
        self.assertEqual(len(self.model.overlays), 0)
        self.assertEqual(self.widget.overlay_tw.rowCount(), 0)