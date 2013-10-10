from T_Rax_QtController import TRaxMainController
from PyQt4 import QtGui
import sys
from datetime import datetime


class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

#redirect output:
sys.stdout = Logger()
sys.stderr = Logger()

print ('*********************************************************\n'+
       'T-Rax has been started at {time}\n'+
       '*********************************************************').\
       format(time = str(datetime.now()))

app = QtGui.QApplication(sys.argv)
controller = TRaxMainController()
controller.main_view.show()
app.exec_()