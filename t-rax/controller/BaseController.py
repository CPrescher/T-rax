# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import os

from PyQt4 import QtCore, QtGui

from model.BaseModel import SingleSpectrumModel
from widget.BaseWidget import BaseWidget


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
        self._file_system_watcher = QtCore.QFileSystemWatcher()
        self._file_system_watcher.addPath(os.getcwd())
        self._file_system_watcher.directoryChanged.connect(self.new_file_in_directory)
        self._file_system_watcher.blockSignals(True)
        self._file_update_timer = QtCore.QTimer()
        self._file_update_timer.setSingleShot(True)
        self._file_update_timer.timeout.connect(self.new_file_in_directory)
        self._files_in_working_dir = []

        self.create_signals()

    def create_signals(self):
        self.connect_click_function(self.widget.load_file_btn, self.load_data_file)
        self.widget.load_next_file_btn.clicked.connect(self.model.load_next_file)
        self.widget.load_previous_file_btn.clicked.connect(self.model.load_previous_file)
        self.widget.load_next_frame_btn.clicked.connect(self.model.load_next_frame)
        self.widget.load_previous_frame_btn.clicked.connect(self.model.load_previous_frame)

        self.model.data_changed.connect(self.data_changed)
        self.model.spectrum_changed.connect(self.widget.graph_widget.plot_data)
        self.widget.roi_widget.rois_changed.connect(self.rois_changed)
        self.widget.autoprocess_cb.toggled.connect(self.auto_process_cb_toggled)

    def connect_click_function(self, emitter, function):
        self.widget.connect(emitter, QtCore.SIGNAL('clicked()'), function)

    def load_data_file(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.widget, caption="Load Experiment SPE",
                                                             directory=self._working_dir))

        if filename is not '':
            self.model.load_file(filename)
            self._file_system_watcher.removePath(self._file_system_watcher.directories()[0])
            self._working_dir = os.path.dirname(filename)
            self._file_system_watcher.addPath(self._working_dir)
            self._files_in_working_dir = os.listdir(self._working_dir)

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
            self._file_system_watcher.blockSignals(False)
        else:
            self._file_system_watcher.blockSignals(True)

    def new_file_in_directory(self):
        files_now = os.listdir(self._working_dir)
        files_added = [f for f in files_now if not f in self._files_in_working_dir]
        if len(files_added) > 0:
            new_file_path = os.path.join(str(self._working_dir), files_added[-1])
            if new_file_path.endswith(self.model.filename.split('.')[-1]):
                file_info = os.stat(new_file_path)
                if file_info.st_size > 1000:
                    try:
                        self.load_data_file(new_file_path)
                    except IOError:
                        self._file_update_timer.start(5)
                        return
                else:
                    self._file_update_timer.start(5)
                    return
            self._files_in_working_dir = files_now
