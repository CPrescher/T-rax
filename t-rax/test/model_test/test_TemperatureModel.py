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

from model.TemperatureModel import TemperatureModel

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, '..', 'test_files')


class TestTemperatureModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QtGui.QApplication([])

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        cls.app.deleteLater()

    def setUp(self):
        self.model = TemperatureModel()

    def tearDown(self):
        self.delete_if_exists('complete.trs')
        self.delete_if_exists('empty.trs')

    def delete_if_exists(self, file_name):
        if os.path.exists(os.path.join(unittest_files_path, file_name)):
            os.remove(os.path.join(unittest_files_path, file_name))

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

    def test_file_browsing(self):
        self.model.load_data_image(os.path.join(unittest_files_path, 'temper_009.spe'))

        us_data_x_1, us_data_y_1 = self.model.us_data_spectrum.data
        ds_data_x_1, ds_data_y_1 = self.model.ds_data_spectrum.data
        self.model.load_next_data_image()

        us_data_x_2, us_data_y_2 = self.model.us_data_spectrum.data
        ds_data_x_2, ds_data_y_2 = self.model.ds_data_spectrum.data

        self.array_almost_equal(us_data_x_1, us_data_x_2)
        self.array_almost_equal(ds_data_x_1, ds_data_x_2)

        self.array_not_almost_equal(ds_data_y_1, ds_data_y_2)
        self.array_not_almost_equal(us_data_y_1, us_data_y_2)

        self.model.load_previous_data_image()

        us_data_x_3, us_data_y_3 = self.model.us_data_spectrum.data
        ds_data_x_3, ds_data_y_3 = self.model.ds_data_spectrum.data

        self.array_almost_equal(us_data_x_1, us_data_x_3)
        self.array_almost_equal(ds_data_x_1, ds_data_x_3)
        self.array_almost_equal(ds_data_y_1, ds_data_y_3)
        self.array_almost_equal(us_data_y_1, us_data_y_3)

    def test_loading_data_img_and_retrieve_upstream_and_down_stream_spectrum(self):
        self.model.load_data_image(os.path.join(unittest_files_path, 'temper_009.spe'))
        self.assertGreater(len(self.model.us_data_spectrum._x), 0)
        self.assertGreater(len(self.model.ds_data_spectrum._x), 0)

    def test_loading_upstream_img_and_retrieve_upstream_spectrum(self):
        self.model.load_us_calibration_image(os.path.join(unittest_files_path, 'temper_009.spe'))
        self.assertGreater(len(self.model.us_calibration_spectrum._x), 0)

    def test_loading_downstream_img_and_retrieve_downstream_spectrum(self):
        self.model.load_ds_calibration_image(os.path.join(unittest_files_path, 'temper_009.spe'))
        self.assertGreater(len(self.model.ds_calibration_spectrum._x), 0)

    def test_loading_images_for_data_downstream_and_upstream_all_should_be_different(self):
        self.model.load_data_image(os.path.join(unittest_files_path, 'temper_009.spe'))
        self.model.load_us_calibration_image(os.path.join(unittest_files_path, 'temper_011.spe'))
        self.model.load_ds_calibration_image(os.path.join(unittest_files_path, 'temper_010.spe'))

        us_data_x, us_data_y = self.model.us_data_spectrum.data
        ds_data_x, ds_data_y = self.model.ds_data_spectrum.data

        us_calibration_x, us_calibration_y = self.model.us_calibration_spectrum.data
        ds_calibration_x, ds_calibration_y = self.model.ds_calibration_spectrum.data

        self.array_not_almost_equal(us_data_y, ds_data_y)
        self.array_not_almost_equal(us_data_y, us_calibration_y)
        self.array_not_almost_equal(us_data_y, ds_calibration_y)

        self.array_not_almost_equal(ds_data_y, us_calibration_y)
        self.array_not_almost_equal(ds_data_y, ds_calibration_y)

        self.array_not_almost_equal(us_calibration_y, ds_calibration_y)

    def test_changing_us_roi_values(self):
        self.model.load_data_image(os.path.join(unittest_files_path, 'temper_009.spe'))
        self.model.load_us_calibration_image(os.path.join(unittest_files_path, 'temper_011.spe'))
        self.model.load_ds_calibration_image(os.path.join(unittest_files_path, 'temper_010.spe'))

        _, us_data_y = self.model.us_data_spectrum.data
        _, us_calibration_y = self.model.us_calibration_spectrum.data

        self.model.us_roi = [123, 900, 30, 50]

        _, after_us_data_y = self.model.us_data_spectrum.data
        _, after_us_calibration_y = self.model.us_calibration_spectrum.data

        self.assertNotEqual(len(us_data_y), len(after_us_data_y))
        self.assertNotEqual(len(us_calibration_y), len(after_us_calibration_y))
        self.assertEqual(len(after_us_data_y), len(after_us_calibration_y))

    def test_changing_ds_roi_values(self):
        self.model.load_data_image(os.path.join(unittest_files_path, 'temper_009.spe'))
        self.model.load_us_calibration_image(os.path.join(unittest_files_path, 'temper_011.spe'))
        self.model.load_ds_calibration_image(os.path.join(unittest_files_path, 'temper_010.spe'))

        _, ds_data_y = self.model.ds_data_spectrum.data
        _, ds_calibration_y = self.model.ds_calibration_spectrum.data

        self.model.ds_roi = [123, 900, 30, 50]

        _, after_ds_data_y = self.model.ds_data_spectrum.data
        _, after_ds_calibration_y = self.model.ds_calibration_spectrum.data

        self.assertNotEqual(len(ds_data_y), len(after_ds_data_y))
        self.assertNotEqual(len(ds_calibration_y), len(after_ds_calibration_y))

    def test_changing_aggregate_roi_values(self):
        self.model.load_data_image(os.path.join(unittest_files_path, 'temper_009.spe'))
        self.model.load_us_calibration_image(os.path.join(unittest_files_path, 'temper_011.spe'))
        self.model.load_ds_calibration_image(os.path.join(unittest_files_path, 'temper_010.spe'))

        _, us_data_y = self.model.us_data_spectrum.data
        _, ds_data_y = self.model.ds_data_spectrum.data

        _, us_calibration_y = self.model.us_calibration_spectrum.data
        _, ds_calibration_y = self.model.ds_calibration_spectrum.data

        self.model.set_rois([123, 500, 30, 40], [123, 500, 60, 90])

        _, after_us_data_y = self.model.us_data_spectrum.data
        _, after_ds_data_y = self.model.ds_data_spectrum.data

        _, after_us_calibration_y = self.model.us_calibration_spectrum.data
        _, after_ds_calibration_y = self.model.ds_calibration_spectrum.data

        self.assertNotEqual(len(us_data_y), len(after_us_data_y))
        self.assertNotEqual(len(ds_data_y), len(after_ds_data_y))
        self.assertNotEqual(len(us_calibration_y), len(after_us_calibration_y))
        self.assertNotEqual(len(ds_calibration_y), len(after_ds_calibration_y))

        self.assertEqual(len(after_us_data_y), len(after_ds_data_y))
        self.assertEqual(len(after_us_data_y), len(after_ds_calibration_y))
        self.assertEqual(len(after_us_data_y), len(after_us_calibration_y))

    def test_changing_the_sum_with_roi_settings(self):
        self.model.load_data_image(os.path.join(unittest_files_path, 'temper_009.spe'))
        self.model.load_us_calibration_image(os.path.join(unittest_files_path, 'temper_011.spe'))
        self.model.load_ds_calibration_image(os.path.join(unittest_files_path, 'temper_010.spe'))

        self.model.set_rois([123, 500, 30, 40], [123, 500, 60, 90])

        _, us_data_y = self.model.us_data_spectrum.data
        _, ds_data_y = self.model.ds_data_spectrum.data

        _, us_calibration_y = self.model.us_calibration_spectrum.data
        _, ds_calibration_y = self.model.ds_calibration_spectrum.data

        _, us_corrected_y = self.model.us_corrected_spectrum.data
        _, ds_corrected_y = self.model.ds_corrected_spectrum.data

        self.model.set_rois([123, 500, 30, 50], [123, 500, 55, 120])

        _, after_us_data_y = self.model.us_data_spectrum.data
        _, after_ds_data_y = self.model.ds_data_spectrum.data

        _, after_us_calibration_y = self.model.us_calibration_spectrum.data
        _, after_ds_calibration_y = self.model.ds_calibration_spectrum.data

        _, after_us_corrected_y = self.model.us_corrected_spectrum.data
        _, after_ds_corrected_y = self.model.ds_corrected_spectrum.data

        self.array_not_almost_equal(us_data_y, after_us_data_y)
        self.array_not_almost_equal(ds_data_y, after_ds_data_y)
        self.array_not_almost_equal(us_calibration_y, after_us_calibration_y)
        self.array_not_almost_equal(ds_calibration_y, after_ds_calibration_y)
        self.array_not_almost_equal(us_corrected_y, after_us_corrected_y)
        self.array_not_almost_equal(ds_corrected_y, after_ds_corrected_y)

    def test_fitting_temperature(self):
        # loading files
        self.load_single_frame_file_and_calibration()

        self.assertEqual(np.round(self.model.ds_temperature), 1047)
        self.assertEqual(np.round(self.model.us_temperature), 1414)

    def test_multiple_frame_spe_file(self):
        temperature_fitting_path = os.path.join(
            unittest_files_path, 'temperature_fitting')
        self.model.load_data_image(os.path.join(
            temperature_fitting_path,
            'test_measurement_multiple.spe'))

        self.assertGreater(len(self.model.us_data_spectrum), 0)
        self.assertGreater(len(self.model.ds_data_spectrum), 0)

        _, us_y = self.model.us_data_spectrum.data
        _, ds_y = self.model.ds_data_spectrum.data

        self.model.load_next_img_frame()

        _, us_y_1 = self.model.us_data_spectrum.data
        _, ds_y_1 = self.model.ds_data_spectrum.data

        self.array_not_almost_equal(us_y, us_y_1)
        self.array_not_almost_equal(ds_y, ds_y_1)

        self.model.load_previous_img_frame()

        _, us_y_2 = self.model.us_data_spectrum.data
        _, ds_y_2 = self.model.ds_data_spectrum.data

        self.array_almost_equal(us_y, us_y_2)
        self.array_almost_equal(ds_y, ds_y_2)

    def test_multiple_frame_spe_file_on_limits(self):
        temperature_fitting_path = os.path.join(
            unittest_files_path, 'temperature_fitting')
        self.model.load_data_image(os.path.join(
            temperature_fitting_path,
            'test_measurement_multiple.spe'))

        _, us_y = self.model.us_data_spectrum.data
        _, ds_y = self.model.ds_data_spectrum.data

        self.model.load_previous_img_frame()

        _, us_y_1 = self.model.us_data_spectrum.data
        _, ds_y_1 = self.model.ds_data_spectrum.data

        self.array_almost_equal(us_y, us_y_1)
        self.array_almost_equal(ds_y, ds_y_1)
        self.assertEqual(self.model.current_frame, 0)

        self.model.set_img_frame_number_to(9)

        _, us_y = self.model.us_data_spectrum.data
        _, ds_y = self.model.ds_data_spectrum.data

        self.model.load_next_img_frame()

        _, us_y_1 = self.model.us_data_spectrum.data
        _, ds_y_1 = self.model.ds_data_spectrum.data

        self.array_almost_equal(us_y, us_y_1)
        self.array_almost_equal(ds_y, ds_y_1)
        self.assertEqual(self.model.current_frame, 9)

    def test_temperature_fitting_of_multiple_frame_spe_file(self):
        temperature_fitting_path = os.path.join(
            unittest_files_path, 'temperature_fitting')
        self.model.load_data_image(os.path.join(
            temperature_fitting_path,
            'test_measurement_multiple.spe'))

        self.model.load_us_calibration_image(os.path.join(
            temperature_fitting_path,
            'us_calibration.spe'))
        self.model.load_ds_calibration_image(os.path.join(
            temperature_fitting_path,
            'ds_calibration.spe'))

        # load correct etalon files:
        self.model.load_us_etalon_spectrum(os.path.join(
            temperature_fitting_path,
            '15A_lamp.txt'
        ))

        self.model.load_ds_etalon_spectrum(os.path.join(
            temperature_fitting_path,
            '15A_lamp.txt'
        ))
        self.model.set_us_calibration_modus(1)
        self.model.set_ds_calibration_modus(1)

        us_temperature1 = self.model.us_temperature
        ds_temperature1 = self.model.ds_temperature

        self.model.load_next_img_frame()

        us_temperature2 = self.model.us_temperature
        ds_temperature2 = self.model.ds_temperature

        self.assertNotAlmostEqual(us_temperature1, us_temperature2)
        self.assertNotAlmostEqual(ds_temperature1, ds_temperature2)

    def test_batch_fitting_of_multiple_frame_spe_file(self):
        temperature_fitting_path = os.path.join(
            unittest_files_path, 'temperature_fitting')
        self.model.load_data_image(os.path.join(
            temperature_fitting_path,
            'test_measurement_multiple.spe'))

        self.model.load_us_calibration_image(os.path.join(
            temperature_fitting_path,
            'us_calibration.spe'))
        self.model.load_ds_calibration_image(os.path.join(
            temperature_fitting_path,
            'ds_calibration.spe'))

        # load correct etalon files:
        self.model.load_us_etalon_spectrum(os.path.join(
            temperature_fitting_path,
            '15A_lamp.txt'
        ))

        self.model.load_ds_etalon_spectrum(os.path.join(
            temperature_fitting_path,
            '15A_lamp.txt'
        ))

        self.model.set_ds_calibration_modus(1)
        self.model.set_us_calibration_modus(1)

        # set the correct roi
        x_limits_wavelength = [666, 836]
        x_limits_ind = self.model.data_img_file.get_index_from(x_limits_wavelength)

        self.model.set_rois([x_limits_ind[0], x_limits_ind[1], 152, 163],
                            [x_limits_ind[0], x_limits_ind[1], 99, 110])

        us_temperature, us_temperature_error, ds_temperature, ds_temperature_error = self.model.fit_all_frames()

        self.assertEqual(len(us_temperature), 10)
        self.assertEqual(len(ds_temperature), 10)
        self.assertEqual(len(us_temperature_error), 10)
        self.assertEqual(len(ds_temperature_error), 10)

        self.array_not_almost_equal(np.array(us_temperature), np.array(ds_temperature))
        self.array_not_almost_equal(np.array(us_temperature_error), np.array(ds_temperature_error))

    def test_saving_and_loading_empty_settings(self):
        filename = os.path.join(unittest_files_path, 'empty.trs')

        self.model.save_setting(filename)

        temperature_fitting_path = os.path.join(
            unittest_files_path, 'temperature_fitting')
        self.model.load_data_image(os.path.join(
            temperature_fitting_path,
            'test_measurement_multiple.spe'))

        self.model.load_us_calibration_image(os.path.join(
            temperature_fitting_path,
            'us_calibration.spe'))
        self.model.load_ds_calibration_image(os.path.join(
            temperature_fitting_path,
            'ds_calibration.spe'))

        # load correct etalon files:
        self.model.load_us_etalon_spectrum(os.path.join(
            temperature_fitting_path,
            '15A_lamp.txt'
        ))

        self.model.load_ds_etalon_spectrum(os.path.join(
            temperature_fitting_path,
            '15A_lamp.txt'
        ))

        self.model.set_ds_calibration_temperature(2500)
        self.model.set_us_calibration_temperature(2300)
        self.model.set_ds_calibration_modus(1)
        self.model.set_us_calibration_modus(1)

        self.model.load_setting(filename)

        self.assertEqual(self.model.ds_calibration_filename, None)
        self.assertEqual(self.model.us_calibration_filename, None)
        self.assertEqual(self.model.ds_temperature_model.calibration_parameter.temperature, 2000)
        self.assertEqual(self.model.us_temperature_model.calibration_parameter.temperature, 2000)
        self.assertEqual(self.model.ds_temperature_model.calibration_parameter.modus, 0)
        self.assertEqual(self.model.us_temperature_model.calibration_parameter.modus, 0)

        self.assertTrue(self.model.ds_temperature is np.NaN)
        self.assertTrue(self.model.ds_temperature_error is np.NaN)
        self.assertTrue(self.model.us_temperature is np.NaN)
        self.assertTrue(self.model.us_temperature_error is np.NaN)

        self.assertEqual(self.model.ds_roi.as_list(), [0, 0, 0, 0])
        self.assertEqual(self.model.us_roi.as_list(), [0, 0, 0, 0])

    def test_saving_and_loading_a_complete_setting(self):
        setting_filename = os.path.join(unittest_files_path, 'complete.trs')

        temperature_fitting_path = os.path.join(
            unittest_files_path, 'temperature_fitting')
        self.model.load_data_image(os.path.join(
            temperature_fitting_path,
            'test_measurement.spe'))

        self.model.load_us_calibration_image(os.path.join(
            temperature_fitting_path,
            'us_calibration.spe'))
        self.model.load_ds_calibration_image(os.path.join(
            temperature_fitting_path,
            'ds_calibration.spe'))

        # load correct etalon files:
        self.model.load_us_etalon_spectrum(os.path.join(
            temperature_fitting_path,
            '15A_lamp.txt'
        ))

        self.model.load_ds_etalon_spectrum(os.path.join(
            temperature_fitting_path,
            '15A_lamp.txt'
        ))

        self.model.set_ds_calibration_temperature(2500)
        self.model.set_us_calibration_temperature(2300)
        self.model.set_ds_calibration_modus(1)
        self.model.set_us_calibration_modus(1)

        # set the correct roi
        x_limits_wavelength = [666, 836]
        x_limits_ind = self.model.data_img_file.get_index_from(x_limits_wavelength)

        ds_roi_limits = [x_limits_ind[0], x_limits_ind[1], 152, 163]
        us_roi_limits = [x_limits_ind[0], x_limits_ind[1], 99, 110]

        self.model.set_rois(ds_roi_limits, us_roi_limits)

        self.model.save_setting(setting_filename)

        self.model2 = TemperatureModel()
        self.model2.load_data_image(os.path.join(
            temperature_fitting_path,
            'test_measurement.spe'))

        self.model2.load_setting(setting_filename)

        print self.model.ds_roi.as_list()
        print self.model2.ds_roi.as_list()
        self.assertEqual(self.model.ds_temperature, self.model2.ds_temperature)
        self.assertEqual(self.model.us_temperature, self.model2.us_temperature)

    def load_single_frame_file_and_calibration(self):
        temperature_fitting_path = os.path.join(
            unittest_files_path, 'temperature_fitting')
        self.model.load_data_image(os.path.join(
            temperature_fitting_path,
            'test_measurement.spe'))
        self.model.load_us_calibration_image(os.path.join(
            temperature_fitting_path,
            'us_calibration.spe'))
        self.model.load_ds_calibration_image(os.path.join(
            temperature_fitting_path,
            'ds_calibration.spe'))
        # load correct etalon files:
        self.model.load_us_etalon_spectrum(os.path.join(
            temperature_fitting_path,
            '15A_lamp.txt'
        ))
        self.model.load_ds_etalon_spectrum(os.path.join(
            temperature_fitting_path,
            '15A_lamp.txt'
        ))
        self.model.set_ds_calibration_modus(1)
        self.model.set_us_calibration_modus(1)
        # set the correct roi
        x_limits_wavelength = [666, 836]
        x_limits_ind = self.model.data_img_file.get_index_from(x_limits_wavelength)
        self.model.set_rois([x_limits_ind[0], x_limits_ind[1], 152, 163],
                            [x_limits_ind[0], x_limits_ind[1], 99, 110])

    def test_saving_data_as_text_from_a_single_frame(self):
        self.load_single_frame_file_and_calibration()

        out_path = os.path.join(unittest_files_path, 'data.txt')
        self.model.save_txt(out_path)

        file = open(out_path)
        lines = file.readlines()

        self.assertEqual(lines[0], "# Fitted Temperatures:\n")
        self.assertEqual(lines[1], "# Downstream (K): 1046.9	14.7\n")
        self.assertEqual(lines[2], "# Upstream (K): 1413.6	2.1\n")
        self.assertEqual(lines[3], "# \n")
        self.assertEqual(lines[4], "# Datacolumns:\n")
        self.assertEqual(lines[5], "# lambda(nm)	DS_data	DS_fit	US_data	US_fit\n")

        file.close()
        os.remove(out_path)
