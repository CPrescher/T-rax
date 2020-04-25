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

from qtpy import QtWidgets

from t_rax.model.RubyModel import RubyModel

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, '..', 'test_files')
test_file = os.path.join(unittest_files_path, 'temper_009.spe')
ruby_file = os.path.join(unittest_files_path, 'ruby_fitting', 'Ruby.spe')


class RubyModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QtWidgets.QApplication([])

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        cls.app.deleteLater()

    def setUp(self):
        self.model = RubyModel()

    def test_get_pressure(self):
        self.assertAlmostEqual(self.model.get_ruby_pressure(), 0)

    def test_changing_sample_position(self):
        self.model.sample_position = 700
        self.assertGreater(self.model.get_ruby_pressure(), 0)

    def test_changing_reference_position(self):
        self.model.sample_position = 700
        p1 = self.model.get_ruby_pressure()

        self.model.reference_position = 694.22
        self.assertGreater(self.model.get_ruby_pressure(), p1)

    def test_changing_sample_temperature(self):
        self.model.sample_position = 700
        p1 = self.model.get_ruby_pressure()

        self.model.sample_temperature = 1500
        self.assertLess(self.model.get_ruby_pressure(), p1)

    def test_changing_reference_temperature(self):
        self.model.sample_position = 700
        p1 = self.model.get_ruby_pressure()

        self.model.reference_temperature = 800
        self.assertGreater(self.model.get_ruby_pressure(), p1)

    def test_changing_ruby_scale(self):
        self.model.sample_position = 700
        p1 = self.model.get_ruby_pressure()

        self.model.ruby_scale = RubyModel.HYDROSTATIC_SCALE
        self.assertNotEqual(self.model.get_ruby_pressure(), p1)

        self.model.ruby_scale = RubyModel.NONHYDROSTATIC_SCALE
        self.assertNotEqual(self.model.get_ruby_pressure(), p1)

    def test_fit_ruby_peak(self):
        self.model.load_file(ruby_file)
        self.model.roi = [82, 752, 11, 24]
        self.model.sample_position = 694.33
        self.model.fit_ruby_peaks()

        self.assertAlmostEqual(self.model.sample_position, 694.318, places=2)
        self.assertGreater(len(self.model.fitted_spectrum.y), 0)
        self.assertLess(
            np.sum((self.model.fitted_spectrum.y - self.model.spectrum.y) ** 2) / len(self.model.spectrum.y),
            10)

    def test_fit_ruby_peak_automatic(self):
        self.model.load_file(ruby_file)
        self.model.sample_position = 694.33
        self.model.roi = [82, 752, 11, 24]
        self.model.set_fit_automatic(True)
        self.model.load_file(ruby_file)
        self.assertAlmostEqual(self.model.sample_position, 694.318, places=2)
