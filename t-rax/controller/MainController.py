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


class MainController(object):
    def __init__(self, version=None):
        self.main_widget = MainWidget()

        if version is not None:
            self.main_widget.setWindowTitle('T-Rax v' + str(version))

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
        ## temperature module:
        temperature_data_path = str(self.settings.value("temperature data file").toString())
        if os.path.exists(temperature_data_path):
            self.temperature_controller.load_data_file(temperature_data_path)

        settings_file_path = os.path.join(str(self.settings.value("temperature settings directory").toString()),
                                          str(self.settings.value("temperature settings file").toString()) + ".trs")
        if os.path.exists(settings_file_path):
            self.temperature_controller.load_setting_file(settings_file_path)

        temperature_autoprocessing = self.settings.value("temperature autoprocessing").toBool()
        if temperature_autoprocessing:
            self.main_widget.temperature_widget.autoprocess_cb.setChecked(True)

        self.main_widget.temperature_widget.connect_to_epics_cb.setChecked(
            self.settings.value("temperature epics connected").toBool()
        )

        ## Ruby Module:
        ruby_data_path = str(self.settings.value("ruby data file").toString())
        if os.path.exists(ruby_data_path):
            self.ruby_controller.base_controller.load_data_file(ruby_data_path)

        ruby_autoprocessing = self.settings.value("ruby autoprocessing").toBool()
        if ruby_autoprocessing:
            self.main_widget.ruby_widget.autoprocess_cb.setChecked(True)

        self.ruby_model.blockSignals(True)
        value = self.settings.value("ruby scale").toInt()
        self.ruby_model.ruby_scale = value[0] if value[1] else self.ruby_model.ruby_scale

        value = self.settings.value("ruby reference position").toFloat()
        self.ruby_model.reference_position = value[0] if value[1] else self.ruby_model.reference_position

        value = self.settings.value("ruby reference temperature").toFloat()
        self.ruby_model.reference_temperature = value[0] if value[1] else self.ruby_model.reference_temperature

        value = self.settings.value("ruby sample position").toFloat()
        self.ruby_model.sample_position = value[0] if value[1] else self.ruby_model.sample_position

        self.ruby_model.blockSignals(False)
        value = self.settings.value("ruby sample temperature").toFloat()
        self.ruby_model.sample_temperature = value[0] if value[1] else self.ruby_model.sample_temperature

        ruby_roi_str = str(self.settings.value("ruby roi").toString())
        if ruby_roi_str is not "":
            ruby_roi = [float(e) for e in ruby_roi_str.split()]
            self.ruby_model.roi = ruby_roi
            self.main_widget.ruby_widget.roi_widget.set_rois([ruby_roi])

        ## Diamond Module:
        diamond_data_path = str(self.settings.value("diamond data file").toString())
        if os.path.exists(ruby_data_path):
            self.diamond_controller.base_controller.load_data_file(diamond_data_path)

        diamond_autoprocessing = self.settings.value("diamond autoprocessing").toBool()
        if diamond_autoprocessing:
            self.main_widget.diamond_widget.autoprocess_cb.setChecked(True)

        value = self.settings.value("diamond laser line").toFloat()
        self.diamond_model.laser_line = value[0] if value[1] else self.diamond_model.laser_line

        value = self.settings.value("diamond derivative").toInt()
        self.main_widget.diamond_widget.derivative_sb.setValue(value[0])

        value = self.settings.value("diamond reference position").toFloat()
        self.diamond_model.reference_position = value[0] if value[1] else self.diamond_model.reference_position

        value = self.settings.value("diamond sample position").toFloat()
        self.diamond_model.sample_position = value[0] if value[1] else self.diamond_model.sample_position

        self.diamond_controller.update_widget_parameter()

        diamond_roi_str = str(self.settings.value("diamond roi").toString())
        if diamond_roi_str != "":
            diamond_roi = [float(e) for e in diamond_roi_str.split()]
            self.diamond_model.roi = diamond_roi
            self.main_widget.diamond_widget.roi_widget.set_rois([diamond_roi])


    def save_settings(self):
        # temperature
        self.settings.setValue("temperature data file", self.temperature_model.data_img_file.filename)
        self.settings.setValue("temperature settings directory", self.temperature_controller._setting_working_dir)
        self.settings.setValue("temperature settings file",
                               str(self.main_widget.temperature_widget.settings_cb.currentText()))

        self.settings.setValue("temperature autoprocessing",
                               self.main_widget.temperature_widget.autoprocess_cb.isChecked())

        self.settings.setValue("temperature epics connected",
                               self.main_widget.temperature_widget.connect_to_epics_cb.isChecked())

        # ruby
        self.settings.setValue("ruby data file", self.ruby_model.filename)
        self.settings.setValue("ruby autoprocessing",
                               self.main_widget.ruby_widget.autoprocess_cb.isChecked())
        self.settings.setValue("ruby reference position", self.ruby_model.reference_position)
        self.settings.setValue("ruby reference temperature", self.ruby_model.reference_temperature)
        self.settings.setValue("ruby sample position", self.ruby_model.sample_position)
        self.settings.setValue("ruby sample temperature", self.ruby_model.sample_temperature)
        self.settings.setValue("ruby scale", self.ruby_model.ruby_scale)
        self.settings.setValue("ruby roi", " ".join(str(e) for e in self.ruby_model.roi.as_list()))

        # diamond
        self.settings.setValue("diamond data file", self.diamond_model.filename)
        self.settings.setValue("diamond autoprocessing", self.main_widget.diamond_widget.autoprocess_cb.isChecked())
        self.settings.setValue("diamond laser line", self.diamond_model.laser_line)
        self.settings.setValue("diamond derivative", self.main_widget.diamond_widget.derivative_sb.value())
        self.settings.setValue("diamond reference position", self.diamond_model.reference_position)
        self.settings.setValue("diamond sample position", self.diamond_model.sample_position)
        self.settings.setValue("diamond roi", " ".join(str(e) for e in self.diamond_model.roi.as_list()))

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


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    controller = MainController()
    controller.show_window()
    app.exec_()
