# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import sys

from PyQt4 import QtGui

from controller.MainController import MainController

from sys import platform

app = QtGui.QApplication(sys.argv)
if platform != "darwin":
    app.setStyle('plastique')
controller = MainController()
controller.show_window()
app.exec_()
