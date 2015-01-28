# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest
from model.RoiData import RoiDataManager

class TestRoiDataManager(unittest.TestCase):
    def setUp(self):
        self.roi_data_manager = RoiDataManager()

    def tearDown(self):
        pass

    def test_initializing_roi_from_empty_roi_data_manager(self):
        roi_data = self.roi_data_manager.get_roi_data([1000, 200])
        self.assertEqual(roi_data.get_ds_roi(), [249, 749, 159, 179])
        self.assertEqual(roi_data.get_us_roi(), [249, 749, 19, 39])

    def test_setting_a_different_roi_for_a_specific_img_dimension(self):
        ds_limits = [150, 850, 120, 500]
        us_limits = [140, 963, 1400, 1800]
        self.roi_data_manager.set_roi_data([1000, 2000], ds_limits, us_limits)
        roi_data = self.roi_data_manager.get_roi_data([1000,2000])
        self.assertEqual(roi_data.get_ds_roi(),ds_limits )
        self.assertEqual(roi_data.get_us_roi(),us_limits )
