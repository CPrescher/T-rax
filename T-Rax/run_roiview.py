from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
from PyQt4 import QtGui, QtCore
import sys

from Controller.RoiSelectorTemperatureController import TRaxROITemperatureController
from Model.TemperatureData import TemperatureData

app = QtGui.QApplication(sys.argv)
data=TemperatureData()
roi_controller = TRaxROITemperatureController(data)
roi_controller.show()
app.exec_()