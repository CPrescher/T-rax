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

import numpy as np
from qtpy import QtWidgets

from widget.RoiWidget import RoiWidget


class TestNewRoiView(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QtWidgets.QApplication([])

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        cls.app.deleteLater()

    def setUp(self):
        self.roi_widget = RoiWidget()
        self.img_roi = self.roi_widget.img_widget.rois[0]
        self.roi_gb = self.roi_widget.roi_gbs[0]


    def test_changing_the_img_roi_changes_the_text_fields(self):
        self.img_roi.setPos(100, 100)

        x_min_gb = np.round(float(str(self.roi_gb.x_min_txt.text())))
        y_min_gb = np.round(float(str(self.roi_gb.y_min_txt.text())))

        self.assertEqual(x_min_gb, 100)
        self.assertEqual(y_min_gb, 100)

        self.img_roi.setSize((100, 100))

        x_max_gb = np.round(float(str(self.roi_gb.x_max_txt.text())))
        y_max_gb = np.round(float(str(self.roi_gb.y_max_txt.text())))

        self.assertEqual(x_max_gb, 200)
        self.assertEqual(y_max_gb, 200)

    def test_changing_text_field_changes_img_rois(self):
        self.roi_gb.x_min_txt.setText('10')
        self.roi_gb.y_min_txt.setText('13')

        self.roi_gb.roi_txt_changed.emit([10, 200, 13, 200])

        rounded_roi_pos = np.round(self.img_roi.pos())
        self.assertEqual(rounded_roi_pos[0], 10)
        self.assertEqual(rounded_roi_pos[1], 13)

    def test_set_rois(self):
        # the set rois function should not emit any signal to avoid circular feedback loops:

        self.counter = 0

        def incr_counter():
            self.counter += 1

        self.roi_widget.rois_changed.connect(incr_counter)
        self.roi_widget.set_rois([[10, 100, 11, 101]])

        self.assertEqual(self.counter, 0)

        x_min_gb = np.round(float(str(self.roi_gb.x_min_txt.text())))
        x_max_gb = np.round(float(str(self.roi_gb.x_max_txt.text())))
        y_min_gb = np.round(float(str(self.roi_gb.y_min_txt.text())))
        y_max_gb = np.round(float(str(self.roi_gb.y_max_txt.text())))

        self.assertEqual(x_min_gb, 10)
        self.assertEqual(x_max_gb, 100)
        self.assertEqual(y_min_gb, 11)
        self.assertEqual(y_max_gb, 101)

        rounded_roi_pos = np.round(self.img_roi.pos())
        rounded_roi_size = np.round(self.img_roi.size())

        x_min_img_roi = rounded_roi_pos[0]
        x_max_img_roi = rounded_roi_pos[0] + rounded_roi_size[0]
        y_min_img_roi = rounded_roi_pos[1]
        y_max_img_roi = rounded_roi_pos[1] + rounded_roi_size[1]

        self.assertEqual(x_min_img_roi, 10)
        self.assertEqual(x_max_img_roi, 100)
        self.assertEqual(y_min_img_roi, 11)
        self.assertEqual(y_max_img_roi, 101)
