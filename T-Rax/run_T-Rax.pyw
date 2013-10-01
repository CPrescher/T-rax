from T_Rax_QtController import TRaxMainController
from PyQt4 import QtGui
import sys

app = QtGui.QApplication(sys.argv)
controller = TRaxMainController()
controller.main_view.show()
app.exec_()