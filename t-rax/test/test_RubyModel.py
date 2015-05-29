import unittest
import os

import numpy as np

from model.RubyModel import RubyModel, HYDROSTATIC_SCALE, NONHYDROSTATIC_SCALE

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, 'test_files')
test_file = os.path.join(unittest_files_path, 'temper_009.spe')


class RubyModelTest(unittest.TestCase):
    def setUp(self):
        self.model = RubyModel()

    def test_get_pressure(self):
        self.model._temperature = 0
        self.model._reference_pos = 694.35

        self.assertAlmostEqual(self.model.get_ruby_pressure(694.35), 0)
        self.assertGreater(self.model.get_ruby_pressure(700), 0)
