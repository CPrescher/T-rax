import unittest
import datetime
import os

from model.SpeFile import SpeFile
unittest_folder = os.path.join(os.path.dirname(__file__), 'unittest files')


class TestSPEModule(unittest.TestCase):
    def setUp(self):
        self.vers2_spe_file = SpeFile(os.path.join(unittest_folder, 'SPE_v2_PIXIS.SPE'))
        self.vers2_converted_spe_file = SpeFile(os.path.join(unittest_folder, 'SPE_v2_converted.SPE'))
        self.vers3_spe_file = SpeFile(os.path.join(unittest_folder, 'SPE_v3_PIMAX.spe'))
        self.vers3_spe_pimax_file = SpeFile(os.path.join(unittest_folder, 'Fe7C3_150_152.spe'))

    def test_calibration(self):
        self.assertGreater(len(self.vers2_spe_file.x_calibration), 0)
        self.assertGreater(len(self.vers3_spe_file.x_calibration), 0)
        self.assertGreater(len(self.vers2_converted_spe_file.x_calibration), 0)

    def test_time(self):
        self.assertEqual(self.vers2_spe_file.date_time, datetime.datetime(2013, 7, 13, 19, 42, 23))
        self.assertEqual(self.vers3_spe_file.date_time, datetime.datetime(2013, 9, 6, 16, 50, 39, 445678,
                                                                          self.vers3_spe_file.date_time.tzinfo))
        self.assertEqual(self.vers2_converted_spe_file.date_time,
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

    def test_roi(self):
        self.assertEqual(self.vers3_spe_file.roi_modus, 'CustomRegions')
        self.assertEqual(self.vers3_spe_file.get_roi(), [0, 1023, 0, 99])

        self.vers3_spe_file_custom_region = SpeFile(os.path.join(unittest_folder, 'SPE_v3_CustomRegions.spe'))
        self.assertEqual(self.vers3_spe_file_custom_region.roi_modus, 'CustomRegions')
        self.assertEqual(self.vers3_spe_file_custom_region.get_roi(), [100, 599, 10, 59])
        self.assertEqual(len(self.vers3_spe_file_custom_region.x_calibration),
                         self.vers3_spe_file_custom_region.get_dimension()[0])

        self.vers3_spe_file_full_sensor = SpeFile(os.path.join(unittest_folder, 'SPE_v3_FullSensor.spe'))
        self.assertEqual(self.vers3_spe_file_full_sensor.roi_modus, 'FullSensor')
        dimensions = self.vers3_spe_file_full_sensor.get_dimension()
        self.assertEqual(self.vers3_spe_file_full_sensor.get_roi(),
                         [0, dimensions[0] - 1, 0, dimensions[1] - 1])

    def test_multiple_frames(self):
        self.spe3_2frames_file = SpeFile(os.path.join(unittest_folder, 'SPE_v3_PIMAX_2frames.spe'))

