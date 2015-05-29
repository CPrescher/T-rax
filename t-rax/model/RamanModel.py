# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import numpy as np

from .BaseModel import SingleSpectrumModel


class RamanModel(SingleSpectrumModel, object):
    REVERSE_CM_MODE = 0
    WAVELENGTH_MODE = 1

    def __init__(self):
        super(RamanModel, self).__init__()
        self._laser_line = 532
        self._mode = RamanModel.REVERSE_CM_MODE

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
        self.spectrum_changed.emit(*self.spectrum.data)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value
        self.spectrum_changed.emit(*self.spectrum.data)


def convert_wavelength_to_reverse_cm(wavelength, laser_line):
    return (1.0 / laser_line - 1 / np.array(wavelength)) * 1.0e7
