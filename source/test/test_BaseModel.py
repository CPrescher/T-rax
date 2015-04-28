# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'
import unittest
import os

import numpy as np

from model.BaseModel import SingleSpectrumModel


unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, 'test_files')


class TestRamanModel(unittest.TestCase):
    def setUp(self):
        self.model = SingleSpectrumModel()

    def tearDown(self):
        pass

    def array_almost_equal(self, array1, array2):
        self.assertAlmostEqual(np.sum(array1 - array2), 0)

    def array_not_almost_equal(self, array1, array2):
        self.assertNotAlmostEqual(np.sum(array1 - array2), 0)


    def test_load_image_data(self):
        filename = os.path.join(unittest_files_path, 'temper_009.spe')

        self.assertEqual(self.model.spectrum, None)
        self.model.load_file(filename)
        self.assertEqual(self.model.spe_file.filename, filename)
        self.assertNotEqual(self.model.spectrum, None)

        self.assertEqual(len(self.model.spectrum.x), len(self.model.spectrum.y))

    def test_file_browsing(self):
        self.model.load_file(os.path.join(unittest_files_path, 'temper_009.spe'))

        x1, y1 = self.model.spectrum.data
        self.model.load_next_file()
        x2, y2 = self.model.spectrum.data

        self.array_not_almost_equal(y1, y2)

        self.model.load_previous_file()
        x3, y3 = self.model.spectrum.data

        self.array_almost_equal(y1, y3)

    def test_frame_browsing(self):
        self.model.load_file(os.path.join(unittest_files_path, 'SPE_v3_PIMAX_2frames.spe'))

        y1 = self.model.spectrum.y
        self.model.load_next_frame()

        y2 = self.model.spectrum.y
        self.array_not_almost_equal(y1, y2)

        self.model.load_next_frame()
        y3 = self.model.spectrum.y
        self.array_almost_equal(y3, y2)

    def test_changing_roi(self):
        filename = os.path.join(unittest_files_path, 'temper_009.spe')
        self.model.load_file(filename)

        y1 = self.model.spectrum.y
        self.model.roi = [123, 900, 30, 50]
        y2 = self.model.spectrum.y

        self.assertNotEqual(len(y1), len(y2))

