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

    def test_fitting_temperature(self):
        # loading files
        temperature_fitting_path = os.path.join(
            unittest_files_path,'temperature fitting')
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

        # set the correct roi
        x_limits_wavelength = [666, 836]
        x_limits_ind = self.model.data_img_file.get_index_from(x_limits_wavelength)

        print x_limits_ind

        self.model.set_rois([x_limits_ind[0], x_limits_ind[1], 152, 163],
                            [x_limits_ind[0], x_limits_ind[1], 99, 110])

        self.model.fit_data()
