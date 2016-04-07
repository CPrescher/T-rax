# -*- coding: utf8 -*-
# T-Rax - GUI program for analysis of spectroscopy data during
# diamond anvil cell experiments
# Copyright (C) 2016 Clemens Prescher (clemens.prescher@gmail.com)
# Institute for Geology and Mineralogy, University of Cologne
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
from mock import patch
import os
import sys

from PyQt4 import QtCore, QtGui
from PyQt4.QtTest import QTest
import numpy as np

from model.TemperatureModel import TemperatureModel
from controller.TemperatureController import TemperatureController
from widget.TemperatureWidget import TemperatureWidget

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, '..', 'test_files')
temperature_fitting_path = os.path.join(unittest_files_path, 'temperature_fitting')


class TestTemperatureController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QtGui.QApplication([])

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        cls.app.deleteLater()

    def setUp(self):
        self.widget = TemperatureWidget()
        self.model = TemperatureModel()
        self.controller = TemperatureController(self.widget, self.model)

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
                         pos=QtCore.QPoint(2, self.widget.ds_etalon_rb.height() / 2))
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
                         pos=QtCore.QPoint(2, self.widget.us_etalon_rb.height() / 2))
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

        self.assertNotEqual(self.widget.graph_widget._us_temperature_txt_item.text, u'')
        self.array_almost_equal(np.array(self.widget.graph_widget._ds_fit_item.getData()),
                                np.array(self.model.ds_fit_spectrum.data))

    def test_us_temperature_fitting_is_shown_in_graph(self):
        data_filename = os.path.join(temperature_fitting_path, 'test_measurement_multiple.spe')
        calibration_filename = os.path.join(temperature_fitting_path, 'us_calibration.spe')
        self.controller.load_data_file(data_filename)
        self.controller.load_us_calibration_file(calibration_filename)

        self.assertNotEqual(self.widget.graph_widget._us_temperature_txt_item.text, u'')
        self.array_almost_equal(np.array(self.widget.graph_widget._us_fit_item.getData()),
                                np.array(self.model.us_fit_spectrum.data))

    def test_loading_settings(self):
        self.load_pimax_example_and_setting()

        self.assertEqual(self.widget.graph_widget._ds_temperature_txt_item.text,
                         '1047 K &plusmn; 15')
        self.assertEqual(self.widget.graph_widget._us_temperature_txt_item.text,
                         '1414 K &plusmn; 2')

        self.assertEqual(self.widget.ds_calibration_filename_lbl.text(),
                         'ds_calibration.spe')
        self.assertEqual(self.widget.us_calibration_filename_lbl.text(),
                         'us_calibration.spe')

        self.assertEqual(self.widget.ds_etalon_filename_lbl.text(),
                         '15A_lamp.txt')
        self.assertEqual(self.widget.us_etalon_filename_lbl.text(),
                         '15A_lamp.txt')

        self.assertEqual(self.widget.ds_temperature_txt.text(), '2500')
        self.assertEqual(self.widget.us_temperature_txt.text(), '2300')

        self.assertEqual(self.widget.settings_cb.count(), 1)

    def load_single_frame_file_and_calibration(self):
        temperature_fitting_path = os.path.join(
            unittest_files_path, 'temperature_fitting')
        self.model.load_data_image(os.path.join(
            temperature_fitting_path,
            'test_measurement.spe'))
        self.model.load_us_calibration_image(os.path.join(
            temperature_fitting_path,
            'us_calibration.spe'))
        self.model.load_ds_calibration_image(os.path.join(
            temperature_fitting_path,
            'ds_calibration.spe'))
        # load correct etalon files:
        self.model.load_us_etalon_spectrum(os.path.join(
            temperature_fitting_path,
            '15A_lamp.txt'
        ))
        self.model.load_ds_etalon_spectrum(os.path.join(
            temperature_fitting_path,
            '15A_lamp.txt'
        ))
        self.model.set_ds_calibration_modus(1)
        self.model.set_us_calibration_modus(1)
        # set the correct roi
        x_limits_wavelength = [666, 836]
        x_limits_ind = self.model.data_img_file.get_index_from(x_limits_wavelength)
        self.model.set_rois([x_limits_ind[0], x_limits_ind[1], 152, 163],
                            [x_limits_ind[0], x_limits_ind[1], 99, 110])

    def load_pimax_example_and_setting(self):
        filename = os.path.join(temperature_fitting_path, 'test_measurement.spe')
        self.controller.load_data_file(filename)
        setting_filename = os.path.join(temperature_fitting_path, 'PiMax.trs')
        self.controller.load_setting_file(setting_filename)

    @patch('PyQt4.QtGui.QFileDialog.getSaveFileName')
    def test_saving_data_as_txt(self, filedialog):
        self.load_single_frame_file_and_calibration()
        out_path = os.path.join(unittest_files_path, 'data.txt')
        filedialog.return_value = out_path
        QTest.mouseClick(self.widget.save_data_btn, QtCore.Qt.LeftButton)

        self.assertTrue(os.path.exists(out_path))
        os.remove(out_path)

    @patch('PyQt4.QtGui.QFileDialog.getSaveFileName')
    def test_saving_graph_image(self, filedialog):
        self.load_single_frame_file_and_calibration()

        out_path = os.path.join(unittest_files_path, 'data.png')
        filedialog.return_value = out_path
        QTest.mouseClick(self.widget.save_graph_btn, QtCore.Qt.LeftButton)

        self.assertTrue(os.path.exists(out_path))
        os.remove(out_path)

        out_path = os.path.join(unittest_files_path, 'data.svg')
        filedialog.return_value = out_path
        QTest.mouseClick(self.widget.save_graph_btn, QtCore.Qt.LeftButton)

        self.assertTrue(os.path.exists(out_path))
        os.remove(out_path)

    def test_graph_status_bar_shows_file_info(self):
        self.controller.load_data_file(os.path.join(unittest_files_path, 'temper_009.spe'))
        self.assertEqual(str(self.widget.graph_info_lbl.text()), self.model.file_info)

    def test_graph_status_bar_shows_mouse_position(self):
        self.widget.graph_widget._ds_plot.mouse_moved.emit(102, 104)

        self.assertIn("102", str(self.widget.graph_mouse_pos_lbl.text()))
        self.assertIn("104", str(self.widget.graph_mouse_pos_lbl.text()))

        self.widget.graph_widget._us_plot.mouse_moved.emit(106, 154)

        self.assertIn("106", str(self.widget.graph_mouse_pos_lbl.text()))
        self.assertIn("154", str(self.widget.graph_mouse_pos_lbl.text()))

        self.widget.graph_widget._time_lapse_plot.mouse_moved.emit(200, 300)

        self.assertIn("200", str(self.widget.graph_mouse_pos_lbl.text()))
        self.assertIn("300", str(self.widget.graph_mouse_pos_lbl.text()))

    def test_roi_status_bar_shows_mouse_position_intensity_and_wavelength(self):
        self.controller.load_data_file(os.path.join(unittest_files_path, 'temper_009.spe'))
        self.widget.roi_widget.img_widget.mouse_moved.emit(130, 20)

        self.assertIn("20", self.widget.roi_widget.pos_lbl.text())
        self.assertIn("130", self.widget.roi_widget.pos_lbl.text())
        self.assertIn("{:.0f}".format(self.model.data_img[20, 130]), self.widget.roi_widget.pos_lbl.text())
        self.assertIn("{:.2f}".format(self.model.data_img_file.x_calibration[130]),
                      self.widget.roi_widget.pos_lbl.text())

    def test_pyepics_connection_is_working(self):
        try:
            import epics
        except ImportError:
            return
        QTest.mouseClick(self.widget.connect_to_epics_cb, QtCore.Qt.LeftButton,
                         pos=QtCore.QPoint(self.widget.connect_to_epics_cb.width() - 2,
                                           self.widget.connect_to_epics_cb.height() / 2))

        self.load_pimax_example_and_setting()

        self.assertAlmostEqual(self.model.ds_temperature, epics.caget('13IDD:ds_las_temp.VAL'))
        self.assertAlmostEqual(self.model.us_temperature, epics.caget('13IDD:us_las_temp.VAL'))

        self.assertAlmostEqual(self.model.ds_roi_max, float(epics.caget('13IDD:dn_t_int.VAL')))
        self.assertAlmostEqual(self.model.us_roi_max, float(epics.caget('13IDD:up_t_int.VAL')))

        self.load_single_frame_file_and_calibration()

        self.assertAlmostEqual(self.model.ds_temperature, epics.caget('13IDD:ds_las_temp.VAL'))
        self.assertAlmostEqual(self.model.us_temperature, epics.caget('13IDD:us_las_temp.VAL'))

        self.assertAlmostEqual(self.model.ds_roi_max, float(epics.caget('13IDD:dn_t_int.VAL')))
        self.assertAlmostEqual(self.model.us_roi_max, float(epics.caget('13IDD:up_t_int.VAL')))
