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

import numpy as np
from qtpy import QtCore

from scipy.ndimage import gaussian_filter1d

from .RamanModel import RamanModel
from .Spectrum import Spectrum


class DiamondModel(RamanModel):
    pressure_changed = QtCore.Signal(float)

    def __init__(self):
        super(DiamondModel, self).__init__()

        self._reference_position = 1334.
        self._sample_position = 1334.

    def get_pressure(self):
        K = 547
        Kp = 3.75

        P = (K * (self.sample_position - self.reference_position) / self.reference_position) * \
            (1 + 0.5 * (Kp - 1) * (self.sample_position - self.reference_position) / self.reference_position)
        return P

    def calculate_derivative_spectrum(self, smoothing):
        if self.spe_file is None:
            return None
        original_spectrum = self.spectrum
        derivative_spectrum = Spectrum(np.copy(original_spectrum.x), np.gradient(original_spectrum.y))
        derivative_spectrum._y = gaussian_filter1d(derivative_spectrum.y, smoothing)
        derivative_spectrum._y = float((max(original_spectrum.y) - min(original_spectrum.y))) / (
            max(derivative_spectrum.y) - min(derivative_spectrum.y)) * derivative_spectrum.y
        derivative_spectrum._y = derivative_spectrum.y + min(original_spectrum.y) - min(derivative_spectrum.y)
        return derivative_spectrum

    @property
    def reference_position(self):
        return self._reference_position

    @reference_position.setter
    def reference_position(self, value):
        self._reference_position = value
        self.pressure_changed.emit(self.get_pressure())

    @property
    def sample_position(self):
        return self._sample_position

    @sample_position.setter
    def sample_position(self, value):
        self._sample_position = value
        self.pressure_changed.emit(self.get_pressure())
