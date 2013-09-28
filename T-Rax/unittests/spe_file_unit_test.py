import unittest
import datetime

import os

from SPE_module import SPE_File


class TestSPEModule(unittest.TestCase):
    def setUp(self):
        self.vers2_spe_file = SPE_File(os.getcwd()+'\\unittest files\\SPE_v2_PIXIS.SPE')
        self.vers3_spe_file = SPE_File(os.getcwd()+'\\unittest files\\SPE_v3_PIMAX.spe')
        self.vers2_converted_spe_file = SPE_File(os.getcwd()+ '\\unittest files\\SPE_v2_converted.SPE')

    def test_calibration(self):
        self.assertGreater(len(self.vers2_spe_file.x_calibration),0)
        self.assertGreater(len(self.vers3_spe_file.x_calibration),0)
        self.assertGreater(len(self.vers2_converted_spe_file.x_calibration),0)

    def test_time(self):
        self.assertEqual(self.vers2_spe_file.date_time, \
                         datetime.datetime(2013, 7, 13, 19, 42, 23))
        self.assertEqual(self.vers3_spe_file.date_time,\
                         datetime.datetime(2013, 9,6, 16, 50, 39, 445678, 
                                           self.vers3_spe_file.date_time.tzinfo))
        self.assertEqual(self.vers2_converted_spe_file.date_time,\
                         datetime.datetime(2013, 5, 10, 10, 34, 27, 0, 
                                           self.vers2_converted_spe_file.date_time.tzinfo))

    def test_exposure_time(self):
        self.assertEqual(self.vers2_spe_file.exposure_time, 0.5)
        self.assertEqual(self.vers3_spe_file.exposure_time, 0.1)
        self.assertEqual(self.vers2_converted_spe_file.exposure_time, 0.18)

    def test_detector(self):
        self.assertEqual(self.vers2_spe_file.detector, 'unspecified')
        self.assertEqual(self.vers3_spe_file.detector, "PIXIS: 100BR")
        self.assertEqual(self.vers2_converted_spe_file.detector, 'unspecified')

    def test_grating(self):
        self.assertEqual(self.vers2_spe_file.grating, '300.0')
        self.assertEqual(self.vers3_spe_file.grating, '860nm 300')
        self.assertEqual(self.vers2_converted_spe_file.grating, '300.0')

    def test_center_wavelength(self):
        self.assertEqual(self.vers2_spe_file.center_wavelength, 750)
        self.assertEqual(self.vers3_spe_file.center_wavelength, 500)
        self.assertEqual(self.vers2_converted_spe_file.center_wavelength, 750)

if __name__ == '__main__':
    unittest.main()
