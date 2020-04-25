# -*- coding: utf-8 -*-
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
from mock import patch, MagicMock
import time
import os
import shutil
from numpy import array_equal

from qtpy import QtWidgets, QtCore
from qtpy.QtTest import QTest

from tests.utility import QtTest

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, '..', 'test_files')

from t_rax.model.BaseModel import SingleSpectrumModel
from t_rax.widget.BaseWidget import BaseWidget
from t_rax.controller.BaseController import BaseController


class BaseControllerTest(QtTest):
    def setUp(self):
        self.widget = BaseWidget()
        self.model = SingleSpectrumModel()
        self.controller = BaseController(self.model, self.widget)
        self.model = self.controller.model

        QtWidgets.QFileDialog.getOpenFileName = MagicMock(
            return_value=os.path.abspath(os.path.join(unittest_files_path, 'temper_009.spe')))
        QtWidgets.QFileDialog.getOpenFileNames = MagicMock(
            return_value=[os.path.abspath(os.path.join(unittest_files_path, 'temper_009.spe'))])

    def tearDown(self):
        self.delete_file_if_exists(os.path.join(unittest_files_path, 'temp.spe'))
        self.delete_file_if_exists(os.path.join(unittest_files_path, 'output.txt'))
        self.delete_file_if_exists(os.path.join(unittest_files_path, 'output.png'))
        self.delete_file_if_exists(os.path.join(unittest_files_path, 'output.svg'))

    def delete_file_if_exists(self, path):
        if os.path.exists(path):
            os.remove(path)

    def test_loading_files(self):
        QTest.mouseClick(self.widget.load_file_btn, QtCore.Qt.LeftButton)

        self.assertIsNotNone(self.model.spectrum)
        self.assertEqual(str(self.widget.filename_lbl.text()), 'temper_009.spe')
        self.assertEqual(str(self.widget.dirname_lbl.text()), os.path.join('tests', 'test_files'))

        self.assertIsNotNone(self.widget.graph_widget._data_item.xData)
        self.assertIsNotNone(self.widget.graph_widget._data_item.yData)

        self.assertIsNotNone(self.widget.roi_widget.img_widget.img_data)
        self.assertNotEqual(str(self.widget.roi_widget.roi_gbs[0].x_min_txt.text()), "0")
        self.assertNotEqual(str(self.widget.roi_widget.roi_gbs[0].y_min_txt.text()), "0")
        self.assertNotEqual(str(self.widget.roi_widget.roi_gbs[0].x_max_txt.text()), "0")
        self.assertNotEqual(str(self.widget.roi_widget.roi_gbs[0].y_max_txt.text()), "0")

    def test_saving_data(self):
        # load a file:
        self.controller.load_file_btn_clicked()
        # Monkey patch
        out_path = os.path.join(unittest_files_path, 'output.txt')
        QtWidgets.QFileDialog.getSaveFileName = MagicMock(return_value=out_path)

        # initiate the saving process
        QTest.mouseClick(self.widget.save_data_btn, QtCore.Qt.LeftButton)
        self.assertTrue(os.path.exists(out_path))

    @patch('qtpy.QtWidgets.QFileDialog.getSaveFileName')
    def test_saving_graph(self, filedialog):
        # load a file:
        self.controller.load_file_btn_clicked()

        # Monkey patch
        out_path = os.path.join(unittest_files_path, 'output.svg')
        filedialog.return_value = out_path

        QTest.mouseClick(self.widget.save_graph_btn, QtCore.Qt.LeftButton)
        self.assertTrue(os.path.exists(out_path))

        # do the same for png
        # Monkey patch
        out_path = os.path.join(unittest_files_path, 'output.png')
        filedialog.return_value = out_path

        QTest.mouseClick(self.widget.save_graph_btn, QtCore.Qt.LeftButton)
        self.assertTrue(os.path.exists(out_path))

    def test_load_multiple_frame_file(self):
        QtWidgets.QFileDialog.getOpenFileNames = MagicMock(
            return_value=[os.path.join(unittest_files_path,
                                       'temperature_fitting',
                                       'test_measurement_multiple.spe')])
        self.controller.load_file_btn_clicked()

        self.assertEqual(float(str(self.widget.frame_txt.text())), self.model.current_frame)

        img_data = self.widget.roi_widget.img_widget.img_data
        QTest.mouseClick(self.widget.load_next_frame_btn, QtCore.Qt.LeftButton)
        img_data2 = self.widget.roi_widget.img_widget.img_data
        self.assertFalse(array_equal(img_data, img_data2))
        QTest.mouseClick(self.widget.load_previous_frame_btn, QtCore.Qt.LeftButton)
        img_data3 = self.widget.roi_widget.img_widget.img_data
        self.assertTrue(array_equal(img_data, img_data3))

    def test_changing_roi(self):
        self.controller.load_file_btn_clicked()

        x, y = self.model.spectrum.data
        self.widget.roi_widget.roi_gbs[0].x_min_txt.setText("")
        QTest.keyClicks(self.widget.roi_widget.roi_gbs[0].x_min_txt, "0")
        QTest.keyPress(self.widget.roi_widget.roi_gbs[0].x_min_txt, QtCore.Qt.Key_Enter)

        new_x, new_y = self.model.spectrum.data
        self.assertNotEqual(len(x), len(new_x))

    def test_using_auto_load_function(self):
        self.controller.load_file_btn_clicked()

        QTest.mouseClick(self.widget.autoprocess_cb, QtCore.Qt.LeftButton,
                         pos=QtCore.QPoint(2, self.widget.autoprocess_cb.height() / 2))
        self.assertTrue(self.widget.autoprocess_cb.isChecked())
        shutil.copy2(os.path.join(unittest_files_path, 'temper_009.spe'),
                     os.path.join(unittest_files_path, 'temp.spe'))

        time.sleep(0.1)  # need to wait until file_watcher updates the path correctly
        QtWidgets.QApplication.processEvents()
        self.assertEqual(str(self.widget.filename_lbl.text()), 'temp.spe')

    def test_graph_status_bar_shows_file_info(self):
        self.controller.load_file_btn_clicked()
        self.assertEqual(str(self.widget.graph_info_lbl.text()), self.model.file_info)

    def test_graph_status_bar_shows_mouse_position(self):
        self.widget.graph_widget._plot_item.mouse_moved.emit(102, 104)

        self.assertIn("102", str(self.widget.graph_mouse_pos_lbl.text()))
        self.assertIn("104", str(self.widget.graph_mouse_pos_lbl.text()))

    def test_roi_status_bar_shows_mouse_position_intensity_and_wavelength(self):
        self.controller.load_file_btn_clicked()
        self.widget.roi_widget.img_widget.mouse_moved.emit(130, 20)

        self.app.processEvents()

        self.assertIn("20", self.widget.roi_widget.pos_lbl.text())
        self.assertIn("130", self.widget.roi_widget.pos_lbl.text())
        self.assertIn("{:.0f}".format(self.model.data_img[20, 130]), self.widget.roi_widget.pos_lbl.text())
        self.assertIn("{:.2f}".format(self.model._data_img_x_calibration[130]), self.widget.roi_widget.pos_lbl.text())
