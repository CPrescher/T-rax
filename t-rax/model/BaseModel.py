# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtCore
import numpy as np

from .SpeFile import SpeFile
from .RoiData import RoiDataManager, Roi
from .Spectrum import Spectrum
from .helper import FileNameIterator


class SingleSpectrumModel(QtCore.QObject, object):
    data_changed = QtCore.pyqtSignal()
    spectrum_changed = QtCore.pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self):
        super(SingleSpectrumModel, self).__init__()

        self.spe_file = None
        self.filename = None

        self._data_img = None
        self._data_img_dimension = None
        self._data_img_x_calibration = None

        self.current_frame = None

        self._spectrum = None

        self._filename_iterator = FileNameIterator()
        self.roi_manager = RoiDataManager(1)
        self.data_spectrum = Spectrum([], [])

    def load_file(self, filename):
        self.spe_file = SpeFile(filename)
        self.filename = filename

        self._data_img = self.spe_file.img
        self._data_img_x_calibration = self.spe_file.x_calibration

        if self.spe_file.num_frames > 1:
            self._data_img = self.spe_file.img[0]
            self.current_frame = 0
        else:
            self._data_img = self.spe_file.img
        self._data_img_dimension = (self._data_img.shape[1], self._data_img.shape[0])
        self._filename_iterator.update_filename(filename)
        self.data_changed.emit()
        self.spectrum_changed.emit(*self.spectrum.data)

    def load_next_file(self):
        new_filename = self._filename_iterator.get_next_filename()
        if new_filename is not None:
            self.load_file(new_filename)

    def load_previous_file(self):
        new_filename = self._filename_iterator.get_previous_filename()
        if new_filename is not None:
            self.load_file(new_filename)

    def load_next_frame(self):
        return self.set_frame_number(self.current_frame + 1)

    def load_previous_frame(self):
        return self.set_frame_number(self.current_frame - 1)

    def set_frame_number(self, frame_number):
        if frame_number < 0 or frame_number >= self.spe_file.num_frames:
            return False
        self.current_frame = frame_number
        self._data_img = self.spe_file.img[frame_number]
        self.data_changed.emit()
        return True

    def save_txt(self, filename):
        self.spectrum.save(filename)

    @property
    def spectrum(self):
        if self.spe_file is not None:
            roi = self.roi_manager.get_roi(0, self._data_img_dimension)
            self._validate_roi(roi)
            data_x = self._data_img_x_calibration[roi.x_min:roi.x_max + 1]
            data_y = self._get_roi_sum(self.data_img, roi)
            self.data_roi_max = self._get_roi_max(self.data_img, roi)
            self.data_spectrum.data = data_x, data_y
            return self.data_spectrum
        return None

    def _validate_roi(self, roi):
        roi.x_min, roi.x_max = (roi.x_min, roi.x_max) if roi.x_max > roi.x_min else (roi.x_max, roi.x_min)
        roi.y_min, roi.y_max = (roi.y_min, roi.y_max) if roi.y_max > roi.y_min else (roi.y_max, roi.y_min)
        roi.x_min = roi.x_min if roi.x_min > 0 else 0
        roi.y_min = roi.y_min if roi.y_min > 0 else 0
        return roi

    def _get_roi_sum(self, img, roi):
        roi_img = img[roi.y_min: roi.y_max + 1, roi.x_min:roi.x_max + 1]
        return np.sum(roi_img, 0) / np.float(np.size(roi_img, 0))

    def _get_roi_max(self, img, roi):
        roi_img = img[roi.y_min: roi.y_max + 1, roi.x_min:roi.x_max + 1]
        return np.max(roi_img)

    @property
    def roi(self):
        try:
            return self.roi_manager.get_roi(0, self._data_img_dimension)
        except AttributeError:
            return Roi([0, 0, 0, 0])

    @roi.setter
    def roi(self, roi):
        if self._data_img is not None:
            self.roi_manager.set_roi(0, self._data_img_dimension, roi)
            self.spectrum_changed.emit(*self.spectrum.data)

    @property
    def data_img(self):
        return self._data_img

    def has_frames(self):
        return self.spe_file.num_frames > 1

    @property
    def num_frames(self):
        return self.spe_file.num_frames

    @property
    def file_info(self):
        return "Exp. Time: {}s | Grating: {} | Detector: {}".format(self.spe_file.exposure_time,
                                                                    self.spe_file.grating,
                                                                    self.spe_file.detector)
