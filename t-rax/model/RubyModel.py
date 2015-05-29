# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtCore
from BaseModel import SingleSpectrumModel

HYDROSTATIC_SCALE = 0
NONHYDROSTATIC_SCALE = 1
DEWAELE_SCALE = 2


class RubyModel(SingleSpectrumModel):
    pressure_changed = QtCore.pyqtSignal(float)

    HYDROSTATIC_SCALE = 0
    NONHYDROSTATIC_SCALE = 1
    DEWAELE_SCALE = 2

    def __init__(self):
        super(RubyModel, self).__init__()
        self._reference_position = 694.35
        self._reference_temperature = 298

        self._sample_position = 694.35
        self._sample_temperature = 298

        self._ruby_scale = DEWAELE_SCALE

    def get_ruby_pressure(self):
        line_pos = self._sample_position
        temperature = self._sample_temperature
        k = 0.46299
        l = 0.0060823
        m = 0.0000010264
        reftemp = self._reference_temperature
        if temperature is None:
            temp = reftemp
        else:
            temp = temperature
        lam0 = self.reference_position
        lam = line_pos

        if self._ruby_scale == DEWAELE_SCALE:
            B = 9.61
            A = 1920
        elif self._ruby_scale == HYDROSTATIC_SCALE:
            B = 7.665
            A = 1904
        elif self._ruby_scale == NONHYDROSTATIC_SCALE:
            B = 5
            A = 1904

        Acorr = A + (k * (temp - reftemp))
        lam0corr = lam0 + (l * (temp - reftemp)) + (m * ((temp - reftemp) * (temp - reftemp)))

        if temp <= 80:
            lam0corr = lam0
            Acorr = A
            lam = lam + 0.92
        elif temp > 80 and temp < 298:
            lam0corr = lam0
            Acorr = A
            deltaT = temp - 298
            corr3 = deltaT ** 3 * -0.0000000337
            corr2 = deltaT ** 2 * 0.0000046231
            corr1 = deltaT * 0.0068259498
            lam = lam + 0.00003547 - corr1 - corr2 - corr3

        rat = (lam / lam0corr) ** B
        P = (Acorr / B) * rat - (Acorr / B)
        P = (P * 100) / 100.
        return P

    @property
    def sample_temperature(self):
        return self._sample_temperature

    @sample_temperature.setter
    def sample_temperature(self, value):
        self._sample_temperature = value
        self.pressure_changed.emit(self.get_ruby_pressure())

    @property
    def sample_position(self):
        return self._sample_position

    @sample_position.setter
    def sample_position(self, value):
        self._sample_position = value
        self.pressure_changed.emit(self.get_ruby_pressure())

    @property
    def reference_temperature(self):
        return self._reference_temperature

    @reference_temperature.setter
    def reference_temperature(self, value):
        self._reference_temperature = value
        self.pressure_changed.emit(self.get_ruby_pressure())

    @property
    def reference_position(self):
        return self._reference_position

    @reference_position.setter
    def reference_position(self, value):
        self._reference_position = value
        self.pressure_changed.emit(self.get_ruby_pressure())

    @property
    def ruby_scale(self):
        return self._ruby_scale

    @ruby_scale.setter
    def ruby_scale(self, value):
        self._ruby_scale = value
        self.pressure_changed.emit(self.get_ruby_pressure())
