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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.import unittest

import unittest
import os

from qtpy import QtWidgets

from ...model.DiamondModel import DiamondModel

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, '..', 'test_files')
test_file = os.path.join(unittest_files_path, 'temper_009.spe')


class DiamondModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QtWidgets.QApplication([])

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        cls.app.deleteLater()

    def setUp(self):
        self.model = DiamondModel()

    def test_get_pressure(self):
        self.model.reference_position = 1334.
        self.model.sample_position = 1335.
        self.assertGreater(self.model.get_pressure(), 0)

    def test_change_reference_position(self):
        self.model.sample_position = 1350
        p1 = self.model.get_pressure()
        self.model.reference_position = 1338
        self.assertLess(self.model.get_pressure(), p1)
