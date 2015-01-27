# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import random

from wx.lib.pubsub import pub
import numpy as np

class Roi():
    def __init__(self, limits):
        self.x_min = limits[0]
        self.x_max = limits[1]
        self.y_min = limits[2]
        self.y_max = limits[3]

    def set_x_limit(self, x_limit):
        self.x_min = x_limit[0]
        self.x_max = x_limit[1]

    def set_y_limit(self, y_limit):
        self.y_max = y_limit[0]
        self.y_max = y_limit[1]

    def set_x_max(self, x_max):
        if self.x_max > x_max:
            self.x_max = x_max
        if self.x_min >= x_max:
            self.x_min = 0

    def set_y_max(self, y_max):
        if self.y_max > y_max:
            self.y_max = y_max
        if self.y_min >= y_max:
            self.y_min = y_max - 1

    def get_width(self):
        return self.x_max - self.x_min

    def get_height(self):
        return self.y_max - self.y_min

    def get_x_limits(self):
        return [self.x_min, self.x_max]

    def get_y_limits(self):
        return [self.y_min, self.y_max]

    def get_roi_as_list(self):
        return [self.x_min, self.x_max, self.y_min, self.y_max]

    def set_roi(self, limits):
        self.x_min = limits[0]
        self.x_max = limits[1]
        self.y_min = limits[2]
        self.y_max = limits[3]


class RoiDataManager():
    def __init__(self):
        self._img_dimensions_list = []
        self._roi_data_list = []
        self._num = 0
        self._current = None

    def _exists(self, dimension):
        if self._get_dimension_ind(dimension) is not None:
            return True
        else:
            return False

    def _add(self, img_dimension, roi_data):
        if self._exists(img_dimension):
            ind = self._get_dimension_ind(img_dimension)
            self._roi_data_list[ind] = roi_data
        else:
            self._img_dimensions_list.append(img_dimension)
            self._roi_data_list.append(roi_data)
            self._num += 1

    def _get_dimension_ind(self, img_dimension):
        for ind in range(self._num):
            if self._img_dimensions_list[ind] == img_dimension:
                self._current = ind
                return ind
        self._current = None
        return None

    def get_roi_data(self, img_dimension):
        if self._exists(img_dimension):
            return self._roi_data_list[self._get_dimension_ind(img_dimension)]
        else:
            ds_limits = np.array([0.25 * (img_dimension[0] - 1), 0.75 * (img_dimension[0] - 1),
                                  0.8 * (img_dimension[1] - 1), 0.9 * (img_dimension[1] - 1)])
            us_limits = np.array([0.25 * (img_dimension[0] - 1), 0.75 * (img_dimension[0] - 1),
                                  0.1 * (img_dimension[1] - 1), 0.2 * (img_dimension[1] - 1)])
            ds_limits = np.round(ds_limits)
            us_limits = np.round(us_limits)

            self._add(img_dimension, RoiData(ds_limits, us_limits))
            return self._roi_data_list[self._get_dimension_ind(img_dimension)]

    def get_current_roi(self):
        return self._roi_data_list[self._current]


class RoiData():
    def __init__(self, ds_limits, us_limits):
        self.ds_roi = Roi(ds_limits)
        self.us_roi = Roi(us_limits)

    def get_roi_data(self):
        data = [self.ds_roi.get_roi_as_list(), self.us_roi.get_roi_as_list()]
        return data

    def get_ds_roi(self):
        return self.ds_roi.get_roi_as_list()

    def get_us_roi(self):
        return self.us_roi.get_roi_as_list()

    def set_ds_roi(self, ds_limits):
        if self.roi_is_valid(Roi(ds_limits)):
            self.ds_roi = Roi(ds_limits)
            self.us_roi.set_x_limit(ds_limits[:2])
        else:
            pub.sendMessage("ROI ERROR")
        pub.sendMessage("ROI CHANGED")

    def set_us_roi(self, us_limits):
        if self.roi_is_valid(Roi(us_limits)):
            self.us_roi = Roi(us_limits)
            self.ds_roi.set_x_limit(us_limits[:2])
        else:
            pub.sendMessage("ROI ERROR")
        pub.sendMessage("ROI CHANGED")

    def set_max_x_limits(self, x_max):
        self.ds_roi.set_x_max(x_max)
        self.us_roi.set_x_max(x_max)

    def set_max_y_limits(self, y_max):
        self.ds_roi.set_y_max(y_max)
        self.us_roi.set_y_max(y_max)

    def set_max_limits(self, x_max, y_max):
        self.set_max_x_limits(x_max)
        self.set_max_y_limits(y_max)

    def set_x_limits(self, x_limits):
        if x_limits[0] < x_limits[1]:
            self.set_x_min(x_limits[0])
            self.set_x_max(x_limits[1])
        else:
            pub.sendMessage("ROI ERROR")
            pub.sendMessage("ROI CHANGED")

    def get_x_limits(self):
        return [self.ds_roi.x_min, self.ds_roi.x_max]

    def set_x_min(self, x_min):
        self.ds_roi.x_min = x_min
        self.us_roi.x_min = x_min
        pub.sendMessage("ROI CHANGED")

    def set_x_max(self, x_max):
        self.ds_roi.x_max = x_max
        self.us_roi.x_max = x_max
        pub.sendMessage("ROI CHANGED")

    @staticmethod
    def roi_is_valid(roi):
        if roi.x_min > roi.x_max:
            return False
        elif roi.y_min > roi.y_max:
            return False
        return True
