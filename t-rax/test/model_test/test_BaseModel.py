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
import os
from PyQt4 import QtGui

import numpy as np

from model.BaseModel import SingleSpectrumModel

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, '..', 'test_files')


class TestSingleSpectrumModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QtGui.QApplication([])

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        cls.app.deleteLater()


    def setUp(self):
        self.model = SingleSpectrumModel()

    def array_almost_equal(self, array1, array2):
        self.assertAlmostEqual(np.sum(array1 - array2), 0)

    def array_not_almost_equal(self, array1, array2):
        self.assertNotAlmostEqual(np.sum(array1 - array2), 0)

    def test_load_image_data(self):
        filename = os.path.join(unittest_files_path, 'temper_009.spe')

        self.assertEqual(self.model.spectrum, None)
        self.model.load_file(filename)
        self.assertEqual(self.model.spe_file.filename, filename)
        self.assertNotEqual(self.model.spectrum, None)

        self.assertEqual(len(self.model.spectrum.x), len(self.model.spectrum.y))

    def test_file_browsing(self):
        self.model.load_file(os.path.join(unittest_files_path, 'temper_009.spe'))

        x1, y1 = self.model.spectrum.data
        self.model.load_next_file()
        x2, y2 = self.model.spectrum.data

        self.array_not_almost_equal(y1, y2)

        self.model.load_previous_file()
        x3, y3 = self.model.spectrum.data

        self.array_almost_equal(y1, y3)

    def test_frame_browsing(self):
        self.model.load_file(os.path.join(unittest_files_path, 'SPE_v3_PIMAX_2frames.spe'))

        y1 = self.model.spectrum.y
        self.model.load_next_frame()

        y2 = self.model.spectrum.y
        self.array_not_almost_equal(y1, y2)

        self.model.load_next_frame()
        y3 = self.model.spectrum.y
        self.array_almost_equal(y3, y2)

    def test_changing_roi(self):
        filename = os.path.join(unittest_files_path, 'temper_009.spe')
        self.model.load_file(filename)

        y1 = self.model.spectrum.y
        self.model.roi = [123, 900, 30, 50]
        y2 = self.model.spectrum.y

        self.assertNotEqual(len(y1), len(y2))
