import unittest
import os

import numpy as np
from PyQt4 import QtGui

from controller.MainController import TRaxMainController


class TestGui(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.main_controller = TRaxMainController()
        self.temperature_controller = self.main_controller.temperature_controller
        self.ruby_controller = self.main_controller.ruby_controller
        self.diamond_controller = self.main_controller.diamond_controller

    def tearDown(self):
        del self.app

    def test_temperature_load_exp_data(self):
        filename1 = 'unittest files/temper_010.spe'
        filename2 = 'unittest files/temper_011.spe'

        self.temperature_controller.load_exp_data(filename1)
        self.assertGreater(len(self.temperature_controller.data.exp_data.get_img_data()), 0)
        self.temperature_controller.load_next_exp_data()
        self.assertEqual(self.temperature_controller.data.exp_data.filename, filename2)
        self.temperature_controller.load_previous_exp_data()
        self.assertEqual(self.temperature_controller.data.exp_data.filename, filename1)

        self.assertEqual(str(self.temperature_controller.main_view.temperature_control_widget.exp_filename_lbl.text()),
                         filename1.replace('\\', '/').split('/')[-1])
        self.assertEqual(
            str(self.temperature_controller.main_view.temperature_control_widget.exp_folder_name_lbl.text()),
            '/'.join(filename1.replace('\\', '/').split('/')[-3:-1]))

    def test_ruby_load_exp_data(self):
        filename1 = 'unittest files/temper_010.spe'
        filename2 = 'unittest files/temper_011.spe'

        self.ruby_controller.load_exp_data(filename1)
        self.assertGreater(len(self.ruby_controller.data.exp_data.get_img_data()), 0)
        self.ruby_controller.load_next_exp_data()
        self.assertEqual(self.ruby_controller.data.exp_data.filename, filename2)
        self.ruby_controller.load_previous_exp_data()
        self.assertEqual(self.ruby_controller.data.exp_data.filename, filename1)

        self.assertEqual(str(self.ruby_controller.main_view.ruby_control_widget.exp_filename_lbl.text()),
                         filename1.replace('\\', '/').split('/')[-1])
        self.assertEqual(str(self.ruby_controller.main_view.ruby_control_widget.exp_folder_name_lbl.text()),
                         '/'.join(filename1.replace('\\', '/').split('/')[-3:-1]))

    def test_diamond_load_exp_data(self):
        filename1 = 'unittest files/temper_010.spe'
        filename2 = 'unittest files/temper_011.spe'

        self.diamond_controller.load_exp_data(filename1)
        self.assertGreater(len(self.diamond_controller.data.exp_data.get_img_data()), 0)
        self.diamond_controller.load_next_exp_data()
        self.assertEqual(self.diamond_controller.data.exp_data.filename, filename2)
        self.diamond_controller.load_previous_exp_data()
        self.assertEqual(self.diamond_controller.data.exp_data.filename, filename1)

        self.assertEqual(str(self.diamond_controller.main_view.diamond_control_widget.exp_filename_lbl.text()),
                         filename1.replace('\\', '/').split('/')[-1])
        self.assertEqual(str(self.diamond_controller.main_view.diamond_control_widget.exp_folder_name_lbl.text()),
                         '/'.join(filename1.replace('\\', '/').split('/')[-3:-1]))

    def test_temperature_roi_selector(self):
        self.temperature_controller.load_roi_view()
        new_ds_roi = [100, 900, 80, 90]
        self.temperature_controller.data.roi_data.set_ds_roi(new_ds_roi)
        new_ds_roi[:2] = np.round(self.temperature_controller.data.get_wavelength_from(new_ds_roi[:2]))
        self.assertEqual(self.temperature_controller.roi_controller.view.get_ds_roi(),
                         new_ds_roi)
        self.assertEqual(self.temperature_controller.roi_controller.view.get_us_roi()[:2],
                         new_ds_roi[:2])
        self.assertEqual(self.temperature_controller.roi_controller.view.get_fit_x_limits(),
                         new_ds_roi[:2])

        new_us_roi = [120, 850, 7, 13]
        self.temperature_controller.data.roi_data.set_us_roi(new_ds_roi)
        new_ds_roi[:2] = np.round(self.temperature_controller.data.get_wavelength_from(new_ds_roi[:2]))
        self.assertEqual(self.temperature_controller.roi_controller.view.get_us_roi(),
                         new_ds_roi)
        self.assertEqual(self.temperature_controller.roi_controller.view.get_ds_roi()[:2],
                         new_ds_roi[:2])
        self.assertEqual(self.temperature_controller.roi_controller.view.get_fit_x_limits(),
                         new_ds_roi[:2])

        new_ds_roi = [650, 750, 12, 20]
        self.temperature_controller.roi_controller.view.set_ds_txt_roi(new_ds_roi)
        self.temperature_controller.roi_controller.ds_roi_txt_changed()
        data_ds_roi = self.temperature_controller.data.get_roi_data().get_ds_roi()
        data_ds_roi[:2] = np.round(self.temperature_controller.data.get_wavelength_from(data_ds_roi[:2]))
        self.assertEqual(data_ds_roi, new_ds_roi)
        self.assertEqual(self.temperature_controller.data.get_roi_data().get_ds_roi()[:2],
                         self.temperature_controller.data.get_roi_data().get_us_roi()[:2])

        new_us_roi = [659, 788, 80, 90]
        self.temperature_controller.roi_controller.view.set_us_txt_roi(new_us_roi)
        self.temperature_controller.roi_controller.us_roi_txt_changed()
        data_us_roi = self.temperature_controller.data.get_roi_data().get_us_roi()
        data_us_roi[:2] = np.round(self.temperature_controller.data.get_wavelength_from(data_us_roi[:2]))
        self.assertEqual(data_us_roi, new_us_roi)
        self.assertEqual(self.temperature_controller.data.get_roi_data().get_us_roi()[:2],
                         self.temperature_controller.data.get_roi_data().get_ds_roi()[:2])

    def test_temperature_calibration_tab(self):
        self.temperature_controller.load_ds_calib_data('unittest files/dn_15.SPE')
        self.temperature_controller.load_us_calib_data('unittest files/up_15.SPE')
        self.assertEqual(self.temperature_controller.main_view.temperature_control_widget.ds_calib_filename_lbl.text(),
                         'dn_15.SPE')
        self.assertEqual(self.temperature_controller.main_view.temperature_control_widget.us_calib_filename_lbl.text(),
                         'up_15.SPE')
        self.temperature_controller.load_ds_etalon_data('unittest files/15A_lamp.txt')
        self.temperature_controller.load_us_etalon_data('unittest files/15A_lamp.txt')
        self.assertEqual(self.temperature_controller.main_view.temperature_control_widget.ds_etalon_lbl.text(),
                         '15A_lamp.txt')
        self.assertEqual(self.temperature_controller.main_view.temperature_control_widget.us_etalon_lbl.text(),
                         '15A_lamp.txt')

    def test_settings(self):
        self.temperature_controller.save_settings_btn_click('unittest files/setting1.trs')
        self.temperature_controller.load_settings_btn_click('unittest files/setting1.trs')
        self.temperature_controller.load_ds_calib_data('unittest files/dn_15.SPE')
        self.temperature_controller.load_us_calib_data('unittest files/up_15.SPE')
        self.temperature_controller.save_settings_btn_click('unittest files/setting2.trs')
        self.temperature_controller.load_settings_btn_click('unittest files/setting1.trs')
        self.assertEqual(
            str(self.temperature_controller.main_view.temperature_control_widget.ds_calib_filename_lbl.text()),
            'Select File...')

        self.temperature_controller.load_settings_btn_click(os.getcwd() + '/unittest files/setting2.trs')
        self.assertEqual(
            str(self.temperature_controller.main_view.temperature_control_widget.ds_calib_filename_lbl.text()),
            'dn_15.SPE')
