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
from qtpy import QtWidgets

import numpy as np

from model.RamanModel import RamanModel

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, '..', 'test_files')
test_file = os.path.join(unittest_files_path, 'temper_009.spe')


class RamanModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QtWidgets.QApplication([])

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        cls.app.deleteLater()

    def setUp(self):
        self.model = RamanModel()

    def test_changing_laser_line(self):
        self.model.load_file(test_file)

        x, y = self.model.spectrum.data

        self.model.laser_line = 600

        x_new, y_new = self.model.spectrum.data

        self.assertFalse(np.array_equal(x, x_new))
        self.assertTrue(np.array_equal(y, y_new))

    def test_changing_mode(self):
        self.model.load_file(test_file)

        x, y = self.model.spectrum.data
        self.model._mode = RamanModel.WAVELENGTH_MODE
        x_new, y_new = self.model.spectrum.data
        self.assertFalse(np.array_equal(x, x_new))
        self.assertTrue(np.array_equal(y, y_new))
