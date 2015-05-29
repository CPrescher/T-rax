# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtCore

from .RamanModel import RamanModel


class DiamondModel(RamanModel):
    pressure_changed = QtCore.pyqtSignal(float)

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
