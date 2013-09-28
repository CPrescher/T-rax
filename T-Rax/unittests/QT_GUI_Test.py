import unittest
import sys
import numpy as np
from PyQt4 import QtGui
from T_Rax_QtController import TRaxMainController


class Test_QT_GUI_Test(unittest.TestCase):
    def setUp(self):
        self.app=QtGui.QApplication(sys.argv)
        self.controller = TRaxMainController()

    def test_load_exp_data(self):
        filename1='D:/Programming/VS Projects/T-Rax/T-Rax/sample files/Test 2013-09-24/temper_010.spe'
        self.controller.load_exp_data(filename1)
        self.assertGreater(len(self.controller.data.exp_data.get_img_data()),0)
        self.controller.load_next_exp_data()
        filename2='D:/Programming/VS Projects/T-Rax/T-Rax/sample files/Test 2013-09-24/temper_011.spe'
        self.assertEqual(self.controller.data.exp_data.filename,filename2)
        self.controller.load_previous_exp_data()
        self.assertEqual(self.controller.data.exp_data.filename, filename1)
        
        self.assertEqual(str(self.controller.main_view.temperature_control_widget.exp_filename_lbl.text()),
                         filename1.split('/')[-1])
        self.assertEqual(str(self.controller.main_view.ruby_control_widget.exp_filename_lbl.text()),
                         filename1.split('/')[-1])
        self.assertEqual(str(self.controller.main_view.diamond_control_widget.exp_filename_lbl.text()),
                         filename1.split('/')[-1])

        self.assertEqual(str(self.controller.main_view.temperature_control_widget.exp_folder_name_lbl.text()),
                         '/'.join(filename1.split('/')[-3:-1]))
        self.assertEqual(str(self.controller.main_view.ruby_control_widget.exp_folder_name_lbl.text()),
                         '/'.join(filename1.split('/')[-3:-1]))
        self.assertEqual(str(self.controller.main_view.diamond_control_widget.exp_folder_name_lbl.text()),
                         '/'.join(filename1.split('/')[-3:-1]))


    def test_load_roi_selector_view(self):
        self.controller.load_roi_view()
        new_ds_roi=[80,90,100,900]
        self.controller.data.roi_data.set_ds_roi(new_ds_roi)        
        new_ds_roi[:2]=np.round(self.controller.data.calculate_wavelength(new_ds_roi[:2]))
        self.assertEqual(self.controller.roi_controller.view.get_ds_roi(),
                         new_ds_roi)
        self.assertEqual(self.controller.roi_controller.view.get_us_roi()[:2],
                         new_ds_roi[:2])
        self.assertEqual(self.controller.roi_controller.view.get_fit_x_limits(),
                         new_ds_roi[:2])

        new_us_roi=[7,13,120,850]
        self.controller.data.roi_data.set_us_roi(new_ds_roi)        
        new_ds_roi[:2]=np.round(self.controller.data.calculate_wavelength(new_ds_roi[:2]))
        self.assertEqual(self.controller.roi_controller.view.get_us_roi(),
                         new_ds_roi)
        self.assertEqual(self.controller.roi_controller.view.get_ds_roi()[:2],
                         new_ds_roi[:2])
        self.assertEqual(self.controller.roi_controller.view.get_fit_x_limits(),
                         new_ds_roi[:2])

if __name__ == '__main__':
    unittest.main()
