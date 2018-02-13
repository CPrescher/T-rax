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
from qtpy import QtWidgets

import numpy as np

from model.RamanModel import RamanModel, RAMAN_LOG_FILE, LOG_HEADER

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

    def test_logging_of_single_raman_spectrum(self):
        raman_export_path = os.path.join(
            unittest_files_path, 'raman_data')

        log_path = os.path.join(raman_export_path, RAMAN_LOG_FILE)
        self.delete_if_exists(log_path)

        self.model.load_file(test_file)
        self.model.write_to_log_file()

        self.assertTrue(os.path.isfile(log_path))
        self.model.log_file.close()

        file = open(log_path)
        lines = file.readlines()

        self.assertEqual(lines[0], LOG_HEADER)
        line2 = lines[1].split('\t')

        self.assertEqual(line2[0], os.path.basename(self.model.filename))
        self.assertEqual(line2[1], os.path.dirname(self.model.filename))
        file.close()

        self.delete_if_exists(log_path)

    def delete_if_exists(self, file_name):
        if os.path.exists(os.path.join(unittest_files_path, file_name)):
            os.remove(os.path.join(unittest_files_path, file_name))
