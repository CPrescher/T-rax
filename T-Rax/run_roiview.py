import sys

from PyQt4 import QtGui

from controller.RoiSelectorTemperatureController import TRaxROITemperatureController
from Model.TemperatureData import TemperatureData


app = QtGui.QApplication(sys.argv)
data = TemperatureData()
roi_controller = TRaxROITemperatureController(data)
roi_controller.show()
app.exec_()