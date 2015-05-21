# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtCore, QtGui
from model.BaseModel import SingleSpectrumModel
from widget.RamanWidget import RamanWidget
import os

class RamanController(QtCore.QObject):
    def __init__(self, raman_widget):
        """
        :type raman_widget: RamanWidget
        """
        super(RamanController, self).__init__()

        self.widget = raman_widget
        self.model = SingleSpectrumModel()
        self._working_dir = ''
        self.create_signals()

    def create_signals(self):
        self.connect_click_function(self.widget.load_file_btn, self.load_data_file)
        self.widget.load_next_file_btn.clicked.connect(self.model.load_next_file)
        self.widget.load_previous_file_btn.clicked.connect(self.model.load_previous_file)

        self.model.data_changed.connect(self.data_changed)

    def connect_click_function(self, emitter, function):
        self.widget.connect(emitter, QtCore.SIGNAL('clicked()'), function)

    def load_data_file(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.widget, caption="Load Experiment SPE",
                                                             directory=self._working_dir))

        if filename is not '':
            self.model.load_file(filename)

    def data_changed(self):
        """
        Updates the interface everytime the RamanModel sends the data_changed signal
        """
        self.widget.filename_lbl.setText(os.path.basename(self.model.filename))
        self.widget.dirname_lbl.setText(os.path.sep.join(os.path.dirname(self.model.filename).split(os.sep)[-2:]))

        self.widget.graph_widget.plot_data(*self.model.spectrum.data)
        self.widget.roi_widget.img_widget.plot_image(self.model.data_img)

        self.widget.roi_widget.set_rois([self.model.roi.as_list()])
