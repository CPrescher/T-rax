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

import numpy as np
import os
from qtpy import QtCore
from copy import deepcopy


from .BaseModel import SingleSpectrumModel
RAMAN_LOG_FILE = 'Raman_export_log.txt'
LOG_HEADER = '# File\tPath\tExposure Time [sec]\tCentral WL\tx-units\tROI [x_min, x_max] [y_min, y_max]\tDetector\n'

class RamanModel(SingleSpectrumModel, object):
    REVERSE_CM_MODE = 0
    WAVELENGTH_MODE = 1

    overlay_changed = QtCore.Signal(int)
    overlay_added = QtCore.Signal()
    overlay_removed = QtCore.Signal(int)

    def __init__(self):
        super(RamanModel, self).__init__()
        self._laser_line = 532
        self._mode = RamanModel.REVERSE_CM_MODE
        self.log_file = None
        self.overlays = []

    def load_file(self, filename):
        super(RamanModel, self).load_file(filename)
        if not self.log_file or not os.path.dirname(self.filename) == os.path.dirname(filename):
            self.create_log_file(os.path.dirname(filename))
        self.write_to_log_file()

    def create_log_file(self, file_path):
        self.log_file = open(os.path.join(file_path, RAMAN_LOG_FILE), 'a')
        self.log_file.write(LOG_HEADER)
        return self.log_file

    def write_to_log_file(self):
        filename = os.path.normpath(self.filename)
        if self.mode:
            units = 'nm'
        else:
            units = 'cm^-1'
        print(self.roi.x_min, self.roi.x_max, self.roi.y_min, self.roi.y_max)
        roi = '[' + str(int(self.roi.x_min)) + ', ' + str(int(self.roi.x_max)) + '] [' + str(int(self.roi.y_min)) + \
              ', ' + str(int(self.roi.y_max)) + ']'
        log_data = (os.path.basename(filename), os.path.dirname(filename), str(self.spe_file.exposure_time),
                    str(self.laser_line), units, roi, self.spe_file.detector)
        self.log_file.write('\t'.join(log_data) + '\n')
        self.log_file.flush()

    @property
    def spectrum(self):
        spec = super(RamanModel, self).spectrum
        if self._mode is RamanModel.REVERSE_CM_MODE:
            spec._x = convert_wavelength_to_reverse_cm(spec.x, self.laser_line)
        return spec

    @property
    def laser_line(self):
        return self._laser_line

    @laser_line.setter
    def laser_line(self, value):
        self._laser_line = value
        if self.spe_file is not None:
            self.spectrum_changed.emit(*self.spectrum.data)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value
        if self.spe_file is not None:
            self.spectrum_changed.emit(*self.spectrum.data)

    def add_overlay(self):
        self.overlays.append(deepcopy(self.spectrum))
        # self.overlays[-1].load(filename)
        self.overlay_added.emit()

    def remove_overlay(self, ind):
        if ind >= 0:
            del self.overlays[ind]
            self.overlay_removed.emit(ind)

    def set_overlay_scaling(self, ind, scaling):
        """
        Sets the scaling of the specified overlay
        :param ind: index of the overlay
        :param scaling: new scaling value
        """
        self.overlays[ind].scaling = scaling
        self.overlay_changed.emit(ind)

    def get_overlay_scaling(self, ind):
        """
        Returns the scaling of the specified overlay
        :param ind: index of the overlay
        :return: scaling value
        """
        return self.overlays[ind].scaling

    def set_overlay_offset(self, ind, offset):
        """
        Sets the offset of the specified overlay
        :param ind: index of the overlay
        :param offset: new offset value
        """
        self.overlays[ind].offset = offset
        self.overlay_changed.emit(ind)

    def get_overlay_offset(self, ind):
        """
        Return the offset of the specified overlay
        :param ind: index of the overlay
        :return: overlay value
        """
        return self.overlays[ind].offset

    # @staticmethod
    # def calculate_color(self, ind):
    #     s = 0.8
    #     v = 0.8
    #     h = (0.19 * (ind + 2)) % 1
    #     return np.array(hsv_to_rgb(h, s, v)) * 255


def convert_wavelength_to_reverse_cm(wavelength, laser_line):
    return (1.0 / laser_line - 1 / np.array(wavelength)) * 1.0e7
