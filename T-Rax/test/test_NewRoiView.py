# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest

import numpy as np
from PyQt4 import QtGui

from view.New import RoiWidget


class TestNewRoiView(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.view = RoiWidget()
        self.img_roi = self.view.img_widget.rois[0]
        self.roi_gb = self.view.roi_gbs[0]

    def tearDown(self):
        del self.app


    def test_changing_the_img_roi_changes_the_text_fields(self):
        self.img_roi.setPos(100,100)

        x_min_gb = np.round(float(str(self.roi_gb.x_min_txt.text())))
        y_min_gb = np.round(float(str(self.roi_gb.y_min_txt.text())))

        self.assertEqual(x_min_gb, 100)
        self.assertEqual(y_min_gb, 100)

        self.img_roi.setSize(100,100)

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
        self.view.widget_rois_changed.connect(incr_counter)
        self.view.set_rois([[10,100,11,101]])

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


