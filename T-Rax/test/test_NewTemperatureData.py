# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest
import os

import numpy as np

from model.TemperatureModel import TemperatureModel


unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, 'unittest files')


class TestTemperatureModel(unittest.TestCase):
    def setUp(self):
        self.model = TemperatureModel()

    def tearDown(self):
        pass

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

    def test_loading_upstream_img_and_retrieve_uptream_spectrum(self):
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
        _, ds_data_y = self.model.ds_data_spectrum.data

        _, us_calibration_y = self.model.us_calibration_spectrum.data
        _, ds_calibration_y = self.model.ds_calibration_spectrum.data

        self.model.set_us_roi([123, 900, 30, 50])

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

    def test_changing_ds_roi_values(self):
        self.model.load_data_image(os.path.join(unittest_files_path, 'temper_009.spe'))
        self.model.load_us_calibration_image(os.path.join(unittest_files_path, 'temper_011.spe'))
        self.model.load_ds_calibration_image(os.path.join(unittest_files_path, 'temper_010.spe'))

        _, us_data_y = self.model.us_data_spectrum.data
        _, ds_data_y = self.model.ds_data_spectrum.data

        _, us_calibration_y = self.model.us_calibration_spectrum.data
        _, ds_calibration_y = self.model.ds_calibration_spectrum.data

        self.model.set_ds_roi([123, 900, 30, 50])

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
        temperature_fitting_path = os.path.join(
            unittest_files_path, 'temperature fitting')
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
        self.model.ds_calibration_parameter.set_modus(1)
        self.model.us_calibration_parameter.set_modus(1)

        # set the correct roi
        x_limits_wavelength = [666, 836]
        x_limits_ind = self.model.data_img_file.get_index_from(x_limits_wavelength)

        self.model.set_rois([x_limits_ind[0], x_limits_ind[1], 152, 163],
                            [x_limits_ind[0], x_limits_ind[1], 99, 110])

        self.model.fit_data()

        self.assertEqual(np.round(self.model.ds_temperature), 1047)
        self.assertEqual(np.round(self.model.us_temperature), 1414)

    def test_multiple_frame_spe_file(self):
        temperature_fitting_path = os.path.join(
            unittest_files_path, 'temperature fitting')
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
            unittest_files_path, 'temperature fitting')
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
            unittest_files_path, 'temperature fitting')
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
        self.model.ds_calibration_parameter.set_modus(1)
        self.model.us_calibration_parameter.set_modus(1)

        self.model.fit_data()
        us_temperature1 = self.model.us_temperature
        ds_temperature1 = self.model.ds_temperature

        self.model.load_next_img_frame()
        self.model.fit_data()

        us_temperature2 = self.model.us_temperature
        ds_temperature2 = self.model.ds_temperature

        self.assertNotAlmostEqual(us_temperature1, us_temperature2)
        self.assertNotAlmostEqual(ds_temperature1, ds_temperature2)

    def test_batch_fitting_of_multiple_frame_spe_file(self):
        temperature_fitting_path = os.path.join(
            unittest_files_path, 'temperature fitting')
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


        self.model.ds_calibration_parameter.set_modus(1)
        self.model.us_calibration_parameter.set_modus(1)

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


