# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'
import unittest
import os

import numpy as np

from model.RamanModel import RamanModel


unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, 'test_files')


class TestRamanModel(unittest.TestCase):
    def setUp(self):
        self.model = RamanModel()

    def array_almost_equal(self, array1, array2):
        self.assertAlmostEqual(np.sum(array1 - array2), 0)

    def array_not_almost_equal(self, array1, array2):
        self.assertNotAlmostEqual(np.sum(array1 - array2), 0)

    def test_changing_unit(self):
        self.model.load_file(os.path.join(unittest_files_path, 'temper_009.spe'))

