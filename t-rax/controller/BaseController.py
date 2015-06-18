# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import os

from PyQt4 import QtCore, QtGui

from model.BaseModel import SingleSpectrumModel
from widget.BaseWidget import BaseWidget

from .NewFileInDirectoryWatcher import NewFileInDirectoryWatcher


class BaseController(QtCore.QObject):
    def __init__(self, model, widget):
        """
        :type widget: BaseWidget
        :type model: SingleSpectrumModel
        """
        super(BaseController, self).__init__()

        self.widget = widget
        self.model = model

        self._working_dir = ''
        self._create_autoprocess_system()

        self.create_signals()

    def create_signals(self):
        self.connect_click_function(self.widget.load_file_btn, self.load_data_file)
        self.widget.load_next_file_btn.clicked.connect(self.model.load_next_file)
        self.widget.load_previous_file_btn.clicked.connect(self.model.load_previous_file)
        self.widget.load_next_frame_btn.clicked.connect(self.model.load_next_frame)
        self.widget.load_previous_frame_btn.clicked.connect(self.model.load_previous_frame)

        self.connect_click_function(self.widget.save_data_btn, self.save_data_btn_clicked)

        self.model.data_changed.connect(self.data_changed)
        self.model.spectrum_changed.connect(self.widget.graph_widget.plot_data)
        self.widget.roi_widget.rois_changed.connect(self.rois_changed)
        self.widget.autoprocess_cb.toggled.connect(self.auto_process_cb_toggled)

    def connect_click_function(self, emitter, function):
        self.widget.connect(emitter, QtCore.SIGNAL('clicked()'), function)

    def load_data_file(self, filename=None):
        if filename is None:
            filename = QtGui.QFileDialog.getOpenFileName(self.widget, caption="Load Experiment SPE",
                                                         directory=self._working_dir)
        filename = str(filename)
        if filename is not '':
            self.model.load_file(filename)
            self._working_dir = os.path.dirname(filename)
            self._directory_watcher.path = self._working_dir

    def save_data_btn_clicked(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getSaveFileName(
                parent=self.widget,
                caption="Save data in tabulated text format",
                directory=os.path.join(self._working_dir, '.'.join(self.model.filename.split(".")[:-1]) + ".txt"))
            )

        if filename is not '':
            self.model.save_txt(filename)

    def data_changed(self):
        """
        Updates the interface everytime the BaseModel sends the data_changed signal
        """
        self.widget.filename_lbl.setText(os.path.basename(self.model.filename))
        self.widget.dirname_lbl.setText(os.path.sep.join(os.path.dirname(self.model.filename).split(os.sep)[-2:]))

        self.widget.roi_widget.plot_img(self.model.data_img)

        self.widget.roi_widget.set_rois([self.model.roi.as_list()])

        if self.model.has_frames():
            self.widget.frame_widget.setVisible(True)
            self.widget.frame_txt.setText(str(self.model.current_frame))
        else:
            self.widget.frame_widget.setVisible(False)

    def rois_changed(self):
        """
        called when the roi is changed in the roi Widget, will recalculate the spectrum and then plot the new updated
        one.
        """
        self.model.roi = self.widget.roi_widget.get_rois()[0]

    def auto_process_cb_toggled(self):
        if self.widget.autoprocess_cb.isChecked():
            self._directory_watcher.activate()
        else:
            self._directory_watcher.deactivate()

    def _create_autoprocess_system(self):
        self._directory_watcher = NewFileInDirectoryWatcher(file_types=['.spe'])
        self._directory_watcher.file_added.connect(self.load_data_file)
