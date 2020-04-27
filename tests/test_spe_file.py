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
import datetime
import os

from t_rax.model.SpeFile import SpeFile
from tests.utility import QtTest

unittest_folder = os.path.join(os.path.dirname(__file__), 'test_files')


class TestSPEModule(QtTest):
    def read_default(self):
        self.vers2_spe_file = SpeFile(os.path.join(unittest_folder, 'SPE_v2_PIXIS.SPE'))
        self.vers2_converted_spe_file = SpeFile(os.path.join(unittest_folder, 'SPE_v2_converted.SPE'))
        self.vers3_spe_file = SpeFile(os.path.join(unittest_folder, 'SPE_v3_PIMAX.spe'))

    def test_calibration(self):
        self.read_default()
        self.assertGreater(len(self.vers2_spe_file.x_calibration), 0)
        self.assertGreater(len(self.vers3_spe_file.x_calibration), 0)
        self.assertGreater(len(self.vers2_converted_spe_file.x_calibration), 0)

    def test_time(self):
        self.read_default()
        self.assertEqual(self.vers2_spe_file.date_time, datetime.datetime(2013, 7, 13, 19, 42, 23))
        self.assertEqual(self.vers3_spe_file.date_time, datetime.datetime(2013, 9, 6, 16, 50, 39, 445678,
                                                                          self.vers3_spe_file.date_time.tzinfo))
        self.assertEqual(self.vers2_converted_spe_file.date_time,
                         datetime.datetime(2013, 5, 10, 10, 34, 27, 0,
                                           self.vers2_converted_spe_file.date_time.tzinfo))

    def test_exposure_time(self):
        self.read_default()
        self.assertEqual(self.vers2_spe_file.exposure_time, 0.5)
        self.assertEqual(self.vers3_spe_file.exposure_time, 0.1)
        self.assertEqual(self.vers2_converted_spe_file.exposure_time, 0.18)

    def test_detector(self):
        self.read_default()
        self.assertEqual(self.vers2_spe_file.detector, 'unspecified')
        self.assertEqual(self.vers3_spe_file.detector, "PIXIS: 100BR")
        self.assertEqual(self.vers2_converted_spe_file.detector, 'unspecified')

    def test_grating(self):
        self.read_default()
        self.assertEqual(self.vers2_spe_file.grating, '300.0')
        self.assertEqual(self.vers3_spe_file.grating, '860nm 300')
        self.assertEqual(self.vers2_converted_spe_file.grating, '300.0')

    def test_center_wavelength(self):
        self.read_default()
        self.assertEqual(self.vers2_spe_file.center_wavelength, 750)
        self.assertEqual(self.vers3_spe_file.center_wavelength, 500)
        self.assertEqual(self.vers2_converted_spe_file.center_wavelength, 750)

    def test_roi(self):
        self.read_default()
        self.assertEqual(self.vers3_spe_file.roi_modus, 'CustomRegions')
        self.assertEqual(self.vers3_spe_file.get_roi(), [0, 1023, 0, 99])

        self.vers3_spe_file_custom_region = SpeFile(os.path.join(unittest_folder, 'SPE_v3_CustomRegions.spe'))
        self.assertEqual(self.vers3_spe_file_custom_region.roi_modus, 'CustomRegions')
        self.assertEqual(self.vers3_spe_file_custom_region.get_roi(), [100, 599, 10, 59])
        self.assertEqual(len(self.vers3_spe_file_custom_region.x_calibration),
                         self.vers3_spe_file_custom_region.get_dimension()[0])

        self.vers3_spe_file_full_sensor = SpeFile(os.path.join(unittest_folder, 'SPE_v3_FullSensor.spe'))
        self.assertEqual(self.vers3_spe_file_full_sensor.roi_modus, 'FullSensor')
        dimensions = self.vers3_spe_file_full_sensor.get_dimension()
        self.assertEqual(self.vers3_spe_file_full_sensor.get_roi(),
                         [0, dimensions[0] - 1, 0, dimensions[1] - 1])

    def test_reading_files_with_asian_characters(self):
        self.spe_file = SpeFile(os.path.join(unittest_folder, 'asian character.spe'))

    def test_multiple_frames(self):
        self.spe3_2frames_file = SpeFile(os.path.join(unittest_folder, 'SPE_v3_PIMAX_2frames.spe'))

    def test_reading_image_with_glue_and_spectroscopy_mode(self):
        self.spe_file = SpeFile(os.path.join(unittest_folder, 'spectroscopy_glue.spe'))
        self.assertEqual(len(self.spe_file.x_calibration), self.spe_file.img.shape[1])
