from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
from PyQt4 import QtGui, QtCore
import sys

from controller.T_Rax_ROISelectorTemperatureController import TRaxROITemperatureController
from data.T_Rax_TemperatureData import TraxTemperatureData

app = QtGui.QApplication(sys.argv)
data=TraxTemperatureData()
roi_controller = TRaxROITemperatureController(data)
roi_controller.show()
app.exec_()