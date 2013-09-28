from PyQt4 import QtGui
from UIFiles.T_Rax_TemperatureControl import Ui_temperature_control_widget
from UIFiles.T_Rax_RubyControl import Ui_ruby_control_widget
from UIFiles.T_Rax_DiamondControl import Ui_diamond_control_widget


class TemperatureControlWidget(QtGui.QWidget, Ui_temperature_control_widget):
    def __init__(self, parent = None):
        super(TemperatureControlWidget, self).__init__(parent)
        self.setupUi(self)

class RubyControlWidget(QtGui.QWidget, Ui_ruby_control_widget):
    def __init__(self, parent = None):
        super(RubyControlWidget, self).__init__(parent)
        self.setupUi(self)

class DiamondControlWidget(QtGui.QWidget, Ui_diamond_control_widget):
    def __init__(self, parent = None):
        super(DiamondControlWidget, self).__init__(parent)
        self.setupUi(self)