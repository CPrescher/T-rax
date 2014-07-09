import sys
import os
import pickle
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL

import numpy as np

from Views.MainView import TRaxMainView

from Controller.TemperatureController import TRaxTemperatureController
from Controller.DiamondController import TRaxDiamondController
from Controller.RubyController import TRaxRubyController
from Controller.OutputGraphController import TRaxOutputGraphController
from Controller.RoiSelectorTemperatureController import TRaxROITemperatureController
from Controller.RoiSelectorRubyController import TRaxROIControllerRuby
from Controller.RoiSelectorDiamondController import TRaxROIControllerDiamond


class TRaxMainController(object):
    def __init__(self, version = None):
        self.main_view = TRaxMainView()

        if version is not None:
            self.main_view.setWindowTitle('T-Rax v'+str(version))
        
        self.create_signals()
        self.create_sub_controller()
        self.load_directories()
        self.temperature_btn_click()
        self.raise_window()

    def raise_window(self):
        self.main_view.show()
        self.main_view.setWindowState(self.main_view.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.main_view.activateWindow()
        self.main_view.raise_()

    def create_sub_controller(self):
        self.temperature_controller = TRaxTemperatureController(self,self.main_view)
        self.ruby_controller = TRaxRubyController(self, self.main_view)
        self.diamond_controller = TRaxDiamondController(self, self.main_view)
        self.output_graph_controller = TRaxOutputGraphController(self, self.main_view)
        
    def load_directories(self):
       try:
            fid = open('parameters.txt', 'r')
            self.temperature_controller._exp_working_dir = ':'.join(fid.readline().split(':')[1::])[1:-1]
            self.temperature_controller._calib_working_dir = ':'.join(fid.readline().split(':')[1::])[1:-1]
            self.temperature_controller._settings_working_dir = ':'.join(fid.readline().split(':')[1::])[1:-1]
            self.ruby_controller._exp_working_dir = ':'.join(fid.readline().split(':')[1::])[1:-1]            
            self.diamond_controller._exp_working_dir = ':'.join(fid.readline().split(':')[1::])[1:-1]
            fid.close()
       except IOError:
            self.temperature_controller._exp_working_dir = os.getcwd()
            self.temperature_controller._calib_working_dir = os.getcwd()
            self.temperature_controller._settings_working_dir = os.getcwd()
            self.ruby_controller._exp_working_dir = os.getcwd()
            self.diamond_controller._exp_working_dir = os.getcwd()
       self.temperature_controller.load_settings()
            
    def create_signals(self):
        self.create_navigation_signals()
        self.create_axes_listener()
        self.create_error_listener()
        self.create_progress_listener()
        self.main_view.closeEvent = self.closeEvent 

    def create_navigation_signals(self):
        self.main_view.connect(self.main_view.ruby_btn, SIGNAL('clicked()'), self.ruby_btn_click)
        self.main_view.connect(self.main_view.raman_btn, SIGNAL('clicked()'), self.raman_btn_click)
        self.main_view.connect(self.main_view.diamond_btn, SIGNAL('clicked()'), self.diamond_btn_click)
        self.main_view.connect(self.main_view.temperature_btn, SIGNAL('clicked()'), self.temperature_btn_click)
        self.main_view.main_frame.resizeEvent = self.main_view.resize_graphs

    def create_axes_listener(self):
        self.main_view.ruby_axes.canvas.mpl_connect('motion_notify_event', self.on_mouse_move_in_graph)
        self.main_view.temperature_axes.canvas.mpl_connect('motion_notify_event', self.on_mouse_move_in_graph)
        self.main_view.diamond_axes.canvas.mpl_connect('motion_notify_event', self.on_mouse_move_in_graph)

    def create_error_listener(self):
        pub.subscribe(self.interpolation_error, "INTERPOLATION RANGE ERROR")
        pub.subscribe(self.roi_error, "ROI ERROR")

    def create_progress_listener(self):
        pub.subscribe(self.progress_bar_change, "PROGRESS ONGOING")

    def connect_click_function(self, emitter, function):
        self.main_view.connect(emitter, SIGNAL('clicked()'), function)

    def temperature_btn_click(self):
        self.main_view.navigate_to('temperature_btn')
        self.main_view.status_file_information_lbl.setText(self.temperature_controller.data.exp_data.get_file_information())
        self.mode = "temperature"

    def ruby_btn_click(self):
        self.main_view.navigate_to('ruby_btn')
        self.main_view.status_file_information_lbl.setText(self.ruby_controller.data.exp_data.get_file_information())
        self.mode = "ruby"

    def diamond_btn_click(self):
        self.main_view.navigate_to('diamond_btn')
        self.main_view.status_file_information_lbl.setText(self.diamond_controller.data.exp_data.get_file_information())
        self.mode = "diamond"

    def raman_btn_click(self):
        self.main_view.update_navigation_bar('rgba(21, 134, 31, 255)', 'raman_btn')
        self.main_view.hide_control_widgets()

    def on_mouse_move_in_graph(self, event):
        x_coord, y_coord = event.xdata, event.ydata
        if x_coord <> None:
           self.main_view.status_coord_lbl.setText('x: %(x).3F y: %(y).3F' \
                              % {'x':x_coord, 'y':y_coord})
        else:
           self.main_view.status_coord_lbl.setText('')


    def interpolation_error(self):
        error_message = QtGui.QMessageBox.warning(None, 'Interpolation Error',
                                                'Etalon spectrum file has not the right range. Please select either standard temperature or load another etalon file.',
                                                QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton)

    def roi_error(self):
        error_message = QtGui.QMessageBox.warning(None, 'ROI Error',
                                                'Please enter valid limits for the regions of interest.',
                                                QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton)

    def progress_bar_change(self, progress):
        self.main_view.progress_bar.show()
        self.main_view.progress_bar.setValue(progress)
        if progress == 100:
            self.main_view.progress_bar.hide()

    def save_directories(self):
        fid = open('parameters.txt', 'w')
        output_str = \
            'Temperature Working directory: ' + self.temperature_controller._exp_working_dir + '\n' + \
            'Temperature Calibration directory: ' + self.temperature_controller._calib_working_dir + '\n' + \
            'Temperature Settings directory: ' + self.temperature_controller._settings_working_dir + '\n' + \
            'Ruby Working directory: ' + self.ruby_controller._exp_working_dir + '\n' + \
            'Diamond Working directory: ' + self.diamond_controller._exp_working_dir + ''
        fid.write(output_str)
        fid.close()

    def closeEvent(self, event):
        self.save_directories()
        try:
            self.temperature_controller.roi_controller.view.close()
        except:
            pass
        try:
            self.ruby_controller.roi_controller.view.close()
        except:
            pass

        try:
            self.output_graph_controller.view.close()
        except:
            pass

        self.main_view.close()
        event.accept()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    controller = TRaxMainController()
    controller.main_view.show()
    app.exec_()
