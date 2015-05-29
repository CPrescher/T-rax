# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'
import unittest
import os
from PyQt4 import QtGui

import numpy as np

from model.RamanModel import RamanModel

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, 'test_files')
test_file = os.path.join(unittest_files_path, 'temper_009.spe')


class RamanModelTest(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.model = RamanModel()

    def tearDown(self):
        del self.app

    def test_changing_laser_line(self):
        self.model.load_file(test_file)

        x, y = self.model.spectrum.data

        self.model.laser_line = 600

        x_new, y_new = self.model.spectrum.data

        self.assertFalse(np.array_equal(x, x_new))
        self.assertTrue(np.array_equal(y, y_new))

    def test_changing_mode(self):
        self.model.load_file(test_file)

        x, y = self.model.spectrum.data
        self.model._mode = RamanModel.WAVELENGTH_MODE
        x_new, y_new = self.model.spectrum.data
        self.assertFalse(np.array_equal(x, x_new))
        self.assertTrue(np.array_equal(y, y_new))
