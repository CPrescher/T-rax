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

from model.TemperatureModel import SingleTemperatureModel
from model.RoiData import RoiDataManager
from model.SpeFile import SpeFile

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, '..', 'test_files')


class TestSingleTemperatureModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QtGui.QApplication([])

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        cls.app.deleteLater()

    def setUp(self):
        self.roi_manager = RoiDataManager(1)
        self.model = SingleTemperatureModel(0, self.roi_manager)

    def array_almost_equal(self, array1, array2):
        self.assertAlmostEqual(np.sum(array1 - array2), 0)

    def array_not_almost_equal(self, array1, array2):
        self.assertNotAlmostEqual(np.sum(array1 - array2), 0)

    def spectrum_almost_equal(self, spectrum1, spectrum2):
        x1, y1 = spectrum1.data
        x2, y2 = spectrum2.data

        self.array_almost_equal(x1, x2)
        self.array_almost_equal(y1, y2)

    def spectrum_not_almost_equal(self, spectrum1, spectrum2):
        x1, y1 = spectrum1.data
        x2, y2 = spectrum2.data

        self.array_almost_equal(x1, x2)
        self.array_not_almost_equal(y1, y2)

    def test_setting_data_and_retrieving_spectrum(self):
        spe_file = SpeFile(os.path.join(unittest_files_path, 'temper_009.spe'))
        self.model.set_data(spe_file.img, spe_file.x_calibration)
        self.assertGreater(len(self.model.data_spectrum), 0)

        self.assertEqual(len(self.model.calibration_spectrum), 0)
        self.assertEqual(len(self.model.corrected_spectrum), 0)
        self.assertEqual(len(self.model.fit_spectrum), 0)

    def test_setting_calibration_data_and_retrieving_spectrum(self):
        spe_file = SpeFile(os.path.join(unittest_files_path, 'temper_009.spe'))
        self.model.set_calibration_data(spe_file.img, spe_file.x_calibration)

        self.assertGreater(len(self.model.calibration_spectrum), 0)

        self.assertEqual(len(self.model.data_spectrum), 0)
        self.assertEqual(len(self.model.corrected_spectrum), 0)
        self.assertEqual(len(self.model.fit_spectrum), 0)

    def test_setting_calibration_and_experimental_data_retrieving_spectra(self):
        temperature_fitting_path = os.path.join(
            unittest_files_path, 'temperature_fitting')
        data_file = SpeFile(os.path.join(temperature_fitting_path, 'test_measurement.spe'))
        calibration_file = SpeFile(os.path.join(temperature_fitting_path, 'us_calibration.spe'))

        self.model.set_data(data_file.img, data_file.x_calibration)
        self.model.set_calibration_data(calibration_file.img, calibration_file.x_calibration)

        self.assertGreater(len(self.model.calibration_spectrum), 0)
        self.assertGreater(len(self.model.data_spectrum), 0)
        self.assertGreater(len(self.model.corrected_spectrum), 0)
        self.assertGreater(len(self.model.fit_spectrum), 0)

    def test_temperature_fitting(self):
        # loading files
        temperature_fitting_path = os.path.join(unittest_files_path, 'temperature_fitting')
        data_file = SpeFile(os.path.join(temperature_fitting_path, 'test_measurement.spe'))
        calibration_file = SpeFile(os.path.join(temperature_fitting_path, 'ds_calibration.spe'))

        self.model.set_data(data_file.img, data_file.x_calibration)
        self.model.set_calibration_data(calibration_file.img, calibration_file.x_calibration)

        self.model.load_etalon_spectrum(os.path.join(temperature_fitting_path,
                                                     '15A_lamp.txt'))
        self.model.set_calibration_modus(1)

        # set the correct roi
        x_limits_wavelength = [666, 836]
        x_limits_ind = data_file.get_index_from(x_limits_wavelength)

        self.roi_manager.set_roi(0, data_file.get_dimension(),
                                 [x_limits_ind[0], x_limits_ind[1], 152, 163])

        self.model._update_all_spectra()
        self.model.fit_data()

        self.assertEqual(np.round(self.model.temperature), 1047)
