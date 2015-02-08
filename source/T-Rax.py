import sys
from datetime import datetime

from PyQt4 import QtGui

from controller.MainController import MainController
import model

# legacy issues
sys.modules['data'] = model
sys.modules['Model'] = model

__version__ = 0.24


class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

# redirect output:
sys.stdout = Logger()
sys.stderr = Logger()

print ('*********************************************************\n' +
       'T-Rax has been started at {time}\n' +
       '*********************************************************'). \
    format(time=str(datetime.now()))

from sys import platform as _platform

app = QtGui.QApplication(sys.argv)
if _platform == "linux" or _platform == "linux2":
    app.setStyle('plastique')
elif _platform == "win32" or _platform == 'cygwin':
    app.setStyle('plastique')
controller = MainController(__version__)
controller.show_window()
app.exec_()