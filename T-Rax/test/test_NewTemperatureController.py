# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest
import os

from PyQt4 import QtCore, QtGui
from PyQt4.QtTest import QTest
import numpy as np

from controller.new.TemperatureController import TemperatureController
from view.new.TemperatureWidget import TemperatureWidget


unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, 'unittest files')
temperature_fitting_path = os.path.join(unittest_files_path, 'temperature fitting')


class TestNewTemperatureController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QtGui.QApplication([])

    def setUp(self):
        self.widget = TemperatureWidget()
        self.controller = TemperatureController(self.widget)
        self.model = self.controller.model

    def tearDown(self):
        pass

    def array_almost_equal(self, array1, array2):
        self.assertAlmostEqual(np.sum(array1 - array2), 0)

    def array_not_almost_equal(self, array1, array2):
        self.assertNotAlmostEqual(np.sum(array1 - array2), 0)


    def test_gui_to_model_connection(self):
        self.controller.load_data_file(
            os.path.join(unittest_files_path, 'temper_009.spe')
        )

        self.assertGreater(len(self.model.ds_data_spectrum), 0)
        self.assertGreater(len(self.model.us_data_spectrum), 0)

        ds_x, ds_y = self.model.ds_data_spectrum.data
        us_x, us_y = self.model.us_data_spectrum.data

        QTest.mouseClick(self.widget.load_next_data_file_btn, QtCore.Qt.LeftButton)

        ds_x_1, ds_y_1 = self.model.ds_data_spectrum.data
        us_x_1, us_y_1 = self.model.us_data_spectrum.data

        self.array_almost_equal(ds_x, ds_x_1)
        self.array_not_almost_equal(ds_y, ds_y_1)

        self.array_almost_equal(us_x, us_x_1)
        self.array_not_almost_equal(us_y, us_y_1)

        QTest.mouseClick(self.widget.load_previous_data_file_btn, QtCore.Qt.LeftButton)

        ds_x_2, ds_y_2 = self.model.ds_data_spectrum.data
        us_x_2, us_y_2 = self.model.us_data_spectrum.data

        self.array_almost_equal(ds_x, ds_x_2)
        self.array_almost_equal(ds_y, ds_y_2)
        self.array_almost_equal(us_x, us_x_2)
        self.array_almost_equal(us_y, us_y_2)

    def test_updating_gui_after_loading_single_frame_data(self):
        filename = os.path.join(temperature_fitting_path, 'test_measurement.spe')
        self.controller.load_data_file(filename)

        self.array_almost_equal(self.widget.roi_img_item.image,
                                np.rot90(self.model.data_img))
        self.assertEqual(self.widget.roi_widget.get_rois(),
                         self.model.get_roi_data_list())

        self.assertEqual(os.path.basename(filename), str(self.widget.filename_lbl.text()))

        dirname = os.path.sep.join(os.path.dirname(filename).split(os.path.sep)[-2:])
        self.assertEqual(dirname, str(self.widget.dirname_lbl.text()))

        self.assertFalse(self.widget.frame_widget.isVisible())

    def test_updating_gui_after_loading_multi_frame_data(self):
        filename = os.path.join(temperature_fitting_path, 'test_measurement_multiple.spe')

        self.controller.load_data_file(filename)

        self.array_almost_equal(self.widget.roi_img_item.image,
                                np.rot90(self.model.data_img))
        self.assertEqual(self.widget.roi_widget.get_rois(), self.model.get_roi_data_list())

        self.assertEqual(os.path.basename(filename), str(self.widget.filename_lbl.text()))

        dirname = os.path.sep.join(os.path.dirname(filename).split(os.path.sep)[-2:])
        self.assertEqual(dirname, str(self.widget.dirname_lbl.text()))

        self.assertEqual(1, int(str(self.widget.frame_num_txt.text())))

        # browsing frames changes the frame_num_txt
        QTest.mouseClick(self.widget.load_next_frame_btn, QtCore.Qt.LeftButton)
        self.assertEqual(2, int(str(self.widget.frame_num_txt.text())))

    def test_loading_downstream_calibration_img(self):
        filename = os.path.join(temperature_fitting_path, 'ds_calibration.spe')

        self.controller.load_ds_calibration_file(filename)
        self.assertGreater(len(self.model.ds_calibration_spectrum), 0)
        self.assertEqual(os.path.basename(filename),
                         str(self.widget.ds_calibration_filename_lbl.text()))


    def test_loading_upstream_calibration_img(self):
        filename = os.path.join(temperature_fitting_path, 'us_calibration.spe')

        self.controller.load_us_calibration_file(filename)
        self.assertGreater(len(self.model.us_calibration_spectrum), 0)
        self.assertEqual(os.path.basename(filename),
                         str(self.widget.us_calibration_filename_lbl.text()))

    def test_downstream_calibration_controls(self):
        QTest.mouseClick(self.widget.ds_etalon_rb, QtCore.Qt.LeftButton,
                         pos=QtCore.QPoint(2, self.widget.ds_etalon_rb.height() / 2))
        self.assertTrue(self.widget.ds_etalon_rb.isChecked())
        self.assertEqual(self.model.ds_temperature_model.calibration_parameter.modus, 1)
        QTest.mouseClick(self.widget.ds_temperature_rb, QtCore.Qt.LeftButton,
                         pos = QtCore.QPoint(2, self.widget.ds_etalon_rb.height() / 2))
        self.assertEqual(self.model.ds_temperature_model.calibration_parameter.modus, 0)


        self.widget.ds_temperature_txt.setText('')
        QTest.keyClicks(self.widget.ds_temperature_txt, '1800')
        QTest.keyPress(self.widget.ds_temperature_txt, QtCore.Qt.Key_Enter)
        self.assertEqual(self.model.ds_temperature_model.calibration_parameter.temperature, 1800)

        filename = os.path.join(temperature_fitting_path, '15A_lamp.txt')
        self.controller.load_ds_etalon_file(filename)
        self.assertEqual(self.model.ds_temperature_model.calibration_parameter.etalon_file_name, filename)
        self.assertEqual(str(self.widget.ds_etalon_filename_lbl.text()), os.path.basename(filename))

    def test_upstream_calibration_controls(self):
        QTest.mouseClick(self.widget.us_etalon_rb, QtCore.Qt.LeftButton,
                         pos=QtCore.QPoint(2, self.widget.us_etalon_rb.height() / 2))
        self.assertTrue(self.widget.us_etalon_rb.isChecked())
        self.assertEqual(self.model.us_temperature_model.calibration_parameter.modus, 1)
        QTest.mouseClick(self.widget.us_temperature_rb, QtCore.Qt.LeftButton,
                         pos = QtCore.QPoint(2, self.widget.us_etalon_rb.height() / 2))
        self.assertEqual(self.model.us_temperature_model.calibration_parameter.modus, 0)


        self.widget.us_temperature_txt.setText('')
        QTest.keyClicks(self.widget.us_temperature_txt, '1800')
        QTest.keyPress(self.widget.us_temperature_txt, QtCore.Qt.Key_Enter)
        self.assertEqual(self.model.us_temperature_model.calibration_parameter.temperature, 1800)

        filename = os.path.join(temperature_fitting_path, '15A_lamp.txt')
        self.controller.load_us_etalon_file(filename)
        self.assertEqual(self.model.us_temperature_model.calibration_parameter.etalon_file_name, filename)
        self.assertEqual(str(self.widget.us_etalon_filename_lbl.text()), os.path.basename(filename))

    def test_ds_temperature_fitting_is_shown_in_graph(self):
        data_filename = os.path.join(temperature_fitting_path, 'test_measurement_multiple.spe')
        calibration_filename = os.path.join(temperature_fitting_path, 'ds_calibration.spe')
        self.controller.load_data_file(data_filename)
        self.controller.load_ds_calibration_file(calibration_filename)

        # self.assertNotEqual(self.widget.graph_widget.ds_temp_txt.get_text(), u'')
        self.array_almost_equal(np.array(self.widget.graph_widget._ds_fit_item.getData()),
                                np.array(self.model.ds_fit_spectrum.data))

    def test_us_temperature_fitting_is_shown_in_graph(self):
        data_filename = os.path.join(temperature_fitting_path, 'test_measurement_multiple.spe')
        calibration_filename = os.path.join(temperature_fitting_path, 'us_calibration.spe')
        self.controller.load_data_file(data_filename)
        self.controller.load_us_calibration_file(calibration_filename)

        # self.assertNotEqual(self.widget.graph_widget.us_temp_txt.get_text(), u'')
        self.array_almost_equal(np.array(self.widget.graph_widget._us_fit_item.getData()),
                                np.array(self.model.us_fit_spectrum.data))


