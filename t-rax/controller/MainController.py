import sys
import os

from PyQt4 import QtGui, QtCore

from model.RamanModel import RamanModel
from widget.MainWidget import MainWidget
from controller.TemperatureController import TemperatureController
from controller.RamanController import RamanController


class MainController(object):
    def __init__(self, version=None):
        self.main_widget = MainWidget()

        if version is not None:
            self.main_widget.setWindowTitle('T-Rax v' + str(version))

        self.create_signals()
        self.create_data_models()
        self.create_sub_controller()
        self.load_directories()

    def show_window(self):
        self.main_widget.show()
        self.main_widget.setWindowState(
            self.main_widget.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.main_widget.activateWindow()
        self.main_widget.raise_()

    def create_data_models(self):
        self.raman_model = RamanModel()

    def create_sub_controller(self):
        self.temperature_controller = TemperatureController(self.main_widget.temperature_widget)
        self.raman_controller = RamanController(self.raman_model, self.main_widget.raman_widget)

    def load_directories(self):
        try:
            fid = open('parameters.txt', 'r')
            self.temperature_controller._exp_working_dir = ':'.join(fid.readline().split(':')[1::])[1:-1]
            self.temperature_controller._calibration_working_dir = ':'.join(fid.readline().split(':')[1::])[1:-1]
            self.temperature_controller._setting_working_dir = ':'.join(fid.readline().split(':')[1::])[1:-1]
            fid.close()
        except IOError:
            self.temperature_controller._exp_working_dir = os.getcwd()
            self.temperature_controller._calibration_working_dir = os.getcwd()
            self.temperature_controller._settings_working_dir = os.getcwd()
        self.temperature_controller.update_setting_combobox()

    def create_signals(self):
        self.main_widget.closeEvent = self.closeEvent

        self.main_widget.navigation_widget.temperature_btn.clicked.connect(
            self.navigation_temperature_btn_clicked)
        self.main_widget.navigation_widget.raman_btn.clicked.connect(
            self.navigation_raman_btn_clicked)

    def navigation_raman_btn_clicked(self):
        self.main_widget.temperature_widget.hide()
        self.main_widget.raman_widget.show()

    def navigation_temperature_btn_clicked(self):
        self.main_widget.raman_widget.hide()
        self.main_widget.temperature_widget.show()


    def save_directories(self):
        fid = open('parameters.txt', 'w')
        output_str = \
            'Temperature Working directory: ' + self.temperature_controller._exp_working_dir + '\n' + \
            'Temperature Calibration directory: ' + self.temperature_controller._calibration_working_dir + '\n' + \
            'Temperature Settings directory: ' + self.temperature_controller._setting_working_dir + '\n'
        fid.write(output_str)
        fid.close()

    def closeEvent(self, event):
        self.save_directories()
        try:
            self.temperature_controller.roi_controller.view.close()
        except:
            pass
        self.main_widget.close()
        event.accept()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    controller = MainController()
    controller.show_window()
    app.exec_()
