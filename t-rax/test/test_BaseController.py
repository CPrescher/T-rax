# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest
from mock import patch
import os
import shutil
from numpy import array_equal

from PyQt4 import QtGui, QtCore
from PyQt4.QtTest import QTest

unittest_path = os.path.dirname(__file__)
unittest_files_path = os.path.join(unittest_path, 'test_files')

from model.BaseModel import SingleSpectrumModel
from widget.BaseWidget import BaseWidget
from controller.BaseController import BaseController


class BaseControllerTest(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.widget = BaseWidget()
        self.model = SingleSpectrumModel()
        self.controller = BaseController(self.model, self.widget)
        self.model = self.controller.model

    def tearDown(self):
        del self.app
        self.delete_file_if_exists(os.path.join(unittest_files_path, 'temp.spe'))
        self.delete_file_if_exists(os.path.join(unittest_files_path, 'output.txt'))
        self.delete_file_if_exists(os.path.join(unittest_files_path, 'output.png'))
        self.delete_file_if_exists(os.path.join(unittest_files_path, 'output.svq'))

    def delete_file_if_exists(self, path):
        if os.path.exists(path):
            os.remove(path)

    @patch('PyQt4.QtGui.QFileDialog.getOpenFileName')
    def test_loading_files(self, filedialog):
        in_path = os.path.join(unittest_files_path, 'temper_009.spe')
        filedialog.return_value = in_path
        QTest.mouseClick(self.widget.load_file_btn, QtCore.Qt.LeftButton)

        self.assertIsNotNone(self.model.spectrum)
        self.assertEqual(str(self.widget.filename_lbl.text()), 'temper_009.spe')
        self.assertEqual(str(self.widget.dirname_lbl.text()), 'test/test_files')

        self.assertIsNotNone(self.widget.graph_widget._data_item.xData)
        self.assertIsNotNone(self.widget.graph_widget._data_item.yData)

        self.assertIsNotNone(self.widget.roi_widget.img_widget.img_data)
        self.assertNotEqual(str(self.widget.roi_widget.roi_gbs[0].x_min_txt.text()), "0")
        self.assertNotEqual(str(self.widget.roi_widget.roi_gbs[0].y_min_txt.text()), "0")
        self.assertNotEqual(str(self.widget.roi_widget.roi_gbs[0].x_max_txt.text()), "0")
        self.assertNotEqual(str(self.widget.roi_widget.roi_gbs[0].y_max_txt.text()), "0")

    @patch('PyQt4.QtGui.QFileDialog.getSaveFileName')
    def test_saving_data(self, filedialog):
        # load a file:
        self.controller.load_data_file(
            os.path.join(unittest_files_path, 'temper_009.spe')
        )
        # Monkey patch
        out_path = os.path.join(unittest_files_path, 'output.txt')
        filedialog.return_value = out_path

        # initiate the saving process
        QTest.mouseClick(self.widget.save_data_btn, QtCore.Qt.LeftButton)
        self.assertTrue(os.path.exists(out_path))

    @patch('PyQt4.QtGui.QFileDialog.getSaveFileName')
    def test_saving_graph(self, filedialog):
        # load a file:
        self.controller.load_data_file(
            os.path.join(unittest_files_path, 'temper_009.spe')
        )

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
        self.controller.load_data_file(os.path.join(unittest_files_path,
                                                    'temperature_fitting',
                                                    'test_measurement_multiple.spe'))

        self.assertEqual(float(str(self.widget.frame_txt.text())), self.model.current_frame)

        img_data = self.widget.roi_widget.img_widget.img_data
        QTest.mouseClick(self.widget.load_next_frame_btn, QtCore.Qt.LeftButton)
        img_data2 = self.widget.roi_widget.img_widget.img_data
        self.assertFalse(array_equal(img_data, img_data2))
        QTest.mouseClick(self.widget.load_previous_frame_btn, QtCore.Qt.LeftButton)
        img_data3 = self.widget.roi_widget.img_widget.img_data
        self.assertTrue(array_equal(img_data, img_data3))

    def test_changing_roi(self):
        self.controller.load_data_file(os.path.join(unittest_files_path, 'temper_009.spe'))

        x, y = self.model.spectrum.data
        self.widget.roi_widget.roi_gbs[0].x_min_txt.setText("")
        QTest.keyClicks(self.widget.roi_widget.roi_gbs[0].x_min_txt, "0")
        QTest.keyPress(self.widget.roi_widget.roi_gbs[0].x_min_txt, QtCore.Qt.Key_Enter)

        new_x, new_y = self.model.spectrum.data
        self.assertNotEqual(len(x), len(new_x))

    def test_using_auto_load_function(self):
        self.controller.load_data_file(os.path.join(unittest_files_path, 'temper_009.spe'))

        QTest.mouseClick(self.widget.autoprocess_cb, QtCore.Qt.LeftButton,
                         pos=QtCore.QPoint(2, self.widget.autoprocess_cb.height() / 2))
        shutil.copy2(os.path.join(unittest_files_path, 'temper_009.spe'),
                     os.path.join(unittest_files_path, 'temp.spe'))
        # apparently the file system watcher signal has to be send manually that when using unittests....
        self.controller._directory_watcher._file_system_watcher.directoryChanged.emit(unittest_files_path)

        self.assertEqual(str(self.widget.filename_lbl.text()), 'temp.spe')

    def test_graph_status_bar_shows_file_info(self):
        self.controller.load_data_file(os.path.join(unittest_files_path, 'temper_009.spe'))
        self.assertEqual(str(self.widget.graph_info_lbl.text()), self.model.file_info)

    def test_graph_status_bar_shows_mouse_position(self):
        self.widget.graph_widget._plot_item.mouse_moved.emit(102, 104)

        self.assertIn("102", str(self.widget.graph_mouse_pos_lbl.text()))
        self.assertIn("104", str(self.widget.graph_mouse_pos_lbl.text()))

    def test_roi_status_bar_shows_mouse_position_intensity_and_wavelength(self):
        self.controller.load_data_file(os.path.join(unittest_files_path, 'temper_009.spe'))
        self.widget.roi_widget.img_widget.mouse_moved.emit(130, 20)

        self.assertIn("20", self.widget.roi_widget.pos_lbl.text())
        self.assertIn("130", self.widget.roi_widget.pos_lbl.text())
        self.assertIn("{:.0f}".format(self.model.data_img[20, 130]), self.widget.roi_widget.pos_lbl.text())
        self.assertIn("{:.2f}".format(self.model._data_img_x_calibration[130]), self.widget.roi_widget.pos_lbl.text())
