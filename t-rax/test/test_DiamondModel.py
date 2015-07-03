import unittest
import os

from PyQt4 import QtGui

from model.DiamondModel import DiamondModel

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, 'test_files')
test_file = os.path.join(unittest_files_path, 'temper_009.spe')


class DiamondModelTest(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.model = DiamondModel()

    def tearDown(self):
        del self.app

    def test_get_pressure(self):
        self.model.reference_position = 1334.
        self.model.sample_position = 1335.
        self.assertGreater(self.model.get_pressure(), 0)

    def test_change_reference_position(self):
        self.model.sample_position = 1350
        p1 = self.model.get_pressure()
        self.model.reference_position = 1338
        self.assertLess(self.model.get_pressure(), p1)
