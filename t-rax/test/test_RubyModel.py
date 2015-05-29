import unittest
import os

from PyQt4 import QtGui

from model.RubyModel import RubyModel

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, 'test_files')
test_file = os.path.join(unittest_files_path, 'temper_009.spe')


class RubyModelTest(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.model = RubyModel()

    def tearDown(self):
        del self.app

    def test_get_pressure(self):
        self.assertAlmostEqual(self.model.get_ruby_pressure(), 0)

    def test_changing_sample_position(self):
        self.model.sample_position = 700
        self.assertGreater(self.model.get_ruby_pressure(), 0)

    def test_changing_reference_position(self):
        self.model.sample_position = 700
        p1 = self.model.get_ruby_pressure()

        self.model.reference_position = 694.22
        self.assertGreater(self.model.get_ruby_pressure(), p1)

    def test_changing_sample_temperature(self):
        self.model.sample_position = 700
        p1 = self.model.get_ruby_pressure()

        self.model.sample_temperature = 1500
        self.assertLess(self.model.get_ruby_pressure(), p1)

    def test_changing_reference_temperature(self):
        self.model.sample_position = 700
        p1 = self.model.get_ruby_pressure()

        self.model.reference_temperature = 800
        self.assertGreater(self.model.get_ruby_pressure(), p1)

    def test_changing_ruby_scale(self):
        self.model.sample_position = 700
        p1 = self.model.get_ruby_pressure()

        self.model.ruby_scale = RubyModel.HYDROSTATIC_SCALE
        self.assertNotEqual(self.model.get_ruby_pressure(), p1)

        self.model.ruby_scale = RubyModel.NONHYDROSTATIC_SCALE
        self.assertNotEqual(self.model.get_ruby_pressure(), p1)
