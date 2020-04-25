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
from qtpy import QtWidgets

from t_rax.model.RoiData import RoiDataManager


class TestNewRoiData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QtWidgets.QApplication([])

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        cls.app.deleteLater()


    def test_single_roi_get_and_set_methods(self):
        roi_data_manager = RoiDataManager(1)

        roi_list = roi_data_manager.get_rois((1000, 1000))[0].as_list()
        self.assertEqual(roi_list, [249, 749, 332, 666])

        new_roi = [140, 850, 300, 600]
        roi_data_manager.set_roi(0, (1000, 1000), new_roi)

        roi_list = roi_data_manager.get_rois((1000, 1000))[0].as_list()
        self.assertEqual(roi_list, new_roi)

        roi_list = roi_data_manager.get_roi(0, (1000, 1000)).as_list()
        self.assertEqual(roi_list, new_roi)

        roi_list = roi_data_manager.get_roi(0, (600, 600)).as_list()
        self.assertEqual(roi_list, [149, 449, 199, 399])

        new_roi = [100, 200, 250, 280]
        roi_data_manager.set_roi(0, (300, 300), new_roi)
        roi_list = roi_data_manager.get_roi(0, (300, 300)).as_list()
        self.assertEqual(roi_list, new_roi)

    def test_multiple_roi_get_and_set_methods(self):
        roi_data_manager = RoiDataManager(10)

        rois_list_1 = roi_data_manager.get_rois((1000, 1000))
        heights = []
        for roi in rois_list_1:
            heights.append(roi.as_list()[3] - roi.as_list()[2])

        self.assertAlmostEqual(heights[0], heights[1], delta=1)
        self.assertAlmostEqual(heights[1], heights[2], delta=1)
        self.assertAlmostEqual(heights[2], heights[3], delta=1)
        self.assertAlmostEqual(heights[3], heights[4], delta=1)
        self.assertAlmostEqual(heights[4], heights[5], delta=1)
        self.assertAlmostEqual(heights[5], heights[6], delta=1)
        self.assertAlmostEqual(heights[6], heights[7], delta=1)
        self.assertAlmostEqual(heights[7], heights[8], delta=1)
        self.assertAlmostEqual(heights[8], heights[9], delta=1)

        new_roi = [20, 300, 150, 200]
        roi_data_manager.set_roi(7, (1000, 1000), new_roi)
        self.assertEqual(new_roi, roi_data_manager.get_roi(7, (1000, 1000)).as_list())

        # tests if setting a ROI in a empty data manager also correctly initializes all the other ROIS
        roi_data_manager_2 = RoiDataManager(10)
        roi_data_manager_2.set_roi(7, (1000, 1000), new_roi)

        for ind in range(10):
            self.assertEqual(roi_data_manager.get_roi(ind, (1000, 1000)).as_list(),
                             roi_data_manager_2.get_roi(ind, (1000, 1000)).as_list())
