__author__ = 'Clemens Prescher'

import sys

from PyQt4 import QtCore, QtGui

from Views.UIFiles.ROI_Selector import Ui_roi_selector_main_widget
from ImgView import ImgView


class RoiView(QtGui.QWidget, Ui_roi_selector_main_widget):
    def __init__(self):
        super(RoiView, self).__init__()
        self.setupUi(self)
        self.setValidator()
        self.create_graphics()

    def setValidator(self):
        self.ds_x_min_txt.setValidator(QtGui.QIntValidator())
        self.ds_x_max_txt.setValidator(QtGui.QIntValidator())
        self.ds_y_min_txt.setValidator(QtGui.QIntValidator())
        self.ds_y_max_txt.setValidator(QtGui.QIntValidator())
        self.us_x_min_txt.setValidator(QtGui.QIntValidator())
        self.us_x_max_txt.setValidator(QtGui.QIntValidator())
        self.us_y_min_txt.setValidator(QtGui.QIntValidator())
        self.us_y_max_txt.setValidator(QtGui.QIntValidator())
        self.fit_from_txt.setValidator(QtGui.QIntValidator())
        self.fit_to_txt.setValidator(QtGui.QIntValidator())

    def create_graphics(self):
        self.img_view = ImgView(self.img_view)

    def raise_window(self):
        self.show()
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.activateWindow()
        self.raise_()


if __name__ == '__main__':
    from Model.SpeFile import SpeFile

    app = QtGui.QApplication(sys.argv)
    roi_view = RoiView()
    roi_view.raise_window()
    img_file = SpeFile('../sample files/Leonid spe files/Pt_42.SPE')
    roi_view.img_view.plot_image(img_file.img, True)
    app.exec_()