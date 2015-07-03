# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import sys
import os

from PyQt4 import QtGui, QtCore

from model.TemperatureModel import TemperatureModel
from model.RubyModel import RubyModel
from model.DiamondModel import DiamondModel
from model.RamanModel import RamanModel
from widget.MainWidget import MainWidget
from controller.TemperatureController import TemperatureController
from controller.RubyController import RubyController
from controller.DiamondController import DiamondController
from controller.RamanController import RamanController

from . import versioneer

versioneer.VCS = 'git'
versioneer.versionfile_source = ''
versioneer.versionfile_build = ''
versioneer.tag_prefix = ''
versioneer.parentdir_prefix = ''


def get_version():
    version = versioneer.get_version()
    if version not in __name__:
        write_version_file(version)
        return version
    else:
        import _version
        return _version.__version__


def write_version_file(version_str):
    path = os.path.dirname(__file__)
    with open(os.path.join(path, '_version.py'), 'w') as f:
        f.write('__version__="{}"'.format(version_str))

__version__ = get_version()

class MainController(object):
    def __init__(self, version=None):
        self.main_widget = MainWidget()

        if version is not None:
            self.main_widget.setWindowTitle('T-Rax ' + get_version())

        self.create_signals()
        self.create_data_models()
        self.create_sub_controller()
        self.settings = QtCore.QSettings("T-Rax", "T-Rax")
        self.load_settings()

    def show_window(self):
        self.main_widget.show()
        self.main_widget.setWindowState(
            self.main_widget.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.main_widget.activateWindow()
        self.main_widget.raise_()

    def create_data_models(self):
        self.temperature_model = TemperatureModel()
        self.ruby_model = RubyModel()
        self.diamond_model = DiamondModel()
        self.raman_model = RamanModel()

    def create_sub_controller(self):
        self.temperature_controller = TemperatureController(self.main_widget.temperature_widget, self.temperature_model)
        self.ruby_controller = RubyController(self.ruby_model, self.main_widget.ruby_widget)
        self.diamond_controller = DiamondController(self.diamond_model, self.main_widget.diamond_widget)
        self.raman_controller = RamanController(self.raman_model, self.main_widget.raman_widget)

    def load_settings(self):
        self.temperature_controller.load_settings(self.settings)
        self.ruby_controller.load_settings(self.settings)
        self.diamond_controller.load_settings(self.settings)
        self.raman_controller.load_settings(self.settings)

    def save_settings(self):
        self.temperature_controller.save_settings(self.settings)
        self.ruby_controller.save_settings(self.settings)
        self.diamond_controller.save_settings(self.settings)
        self.raman_controller.save_settings(self.settings)

    def create_signals(self):
        self.main_widget.closeEvent = self.closeEvent

        self.main_widget.navigation_widget.temperature_btn.clicked.connect(
            self.navigation_temperature_btn_clicked)
        self.main_widget.navigation_widget.ruby_btn.clicked.connect(
            self.navigation_ruby_btn_clicked)
        self.main_widget.navigation_widget.diamond_btn.clicked.connect(
            self.navigation_diamond_btn_clicked
        )
        self.main_widget.navigation_widget.raman_btn.clicked.connect(
            self.navigation_raman_btn_clicked)

    def navigation_ruby_btn_clicked(self):
        self.hide_module_widgets()
        self.main_widget.ruby_widget.show()

    def navigation_diamond_btn_clicked(self):
        self.hide_module_widgets()
        self.main_widget.diamond_widget.show()

    def navigation_raman_btn_clicked(self):
        self.hide_module_widgets()
        self.main_widget.raman_widget.show()

    def navigation_temperature_btn_clicked(self):
        self.hide_module_widgets()
        self.main_widget.temperature_widget.show()

    def hide_module_widgets(self):
        self.main_widget.temperature_widget.hide()
        self.main_widget.ruby_widget.hide()
        self.main_widget.diamond_widget.hide()
        self.main_widget.raman_widget.hide()

    def closeEvent(self, event):
        self.save_settings()
        try:
            self.temperature_controller.roi_controller.view.close()
        except:
            pass
        self.main_widget.close()
        event.accept()