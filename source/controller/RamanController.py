# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtCore
from model.RamanModel import RamanModel


class RamanController(QtCore.QObject):
    def __init__(self, raman_widget):
        super(RamanController, self).__init__()

        self.widget = raman_widget
        self.model = RamanModel()

    def create_signals(self):
        self.connect_click_function(self.widget.load_data_file_btn, self.load_data_file)
        self.widget.load_next_data_file_btn.clicked.connect(self.model.load_next_data_image)
        self.widget.load_previous_data_file_btn.clicked.connect(self.model.load_previous_data_image)