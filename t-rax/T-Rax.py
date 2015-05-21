import sys
from datetime import datetime

from PyQt4 import QtGui

from controller.MainController import MainController


__version__ = 0.24

from sys import platform

app = QtGui.QApplication(sys.argv)
if platform != "darwin":
    app.setStyle('plastique')
controller = MainController(__version__)
controller.show_window()
app.exec_()