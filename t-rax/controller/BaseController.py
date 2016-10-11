# -*- coding: utf8 -*-
# T-Rax - GUI program for analysis of spectroscopy data during
# diamond anvil cell experiments
# Copyright (C) 2016 Clemens Prescher (clemens.prescher@gmail.com)
# Institute for Geology and Mineralogy, University of Cologne
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import numpy as np

from qtpy import QtCore, QtWidgets

from model.BaseModel import SingleSpectrumModel
from widget.BaseWidget import BaseWidget
from widget.Widgets import open_file_dialog, save_file_dialog

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

        self.connect_signals()

    def connect_signals(self):
        self.connect_click_function(self.widget.load_file_btn, self.load_data_file)
        self.widget.load_next_file_btn.clicked.connect(self.model.load_next_file)
        self.widget.load_previous_file_btn.clicked.connect(self.model.load_previous_file)
        self.widget.load_next_frame_btn.clicked.connect(self.model.load_next_frame)
        self.widget.load_previous_frame_btn.clicked.connect(self.model.load_previous_frame)

        self.connect_click_function(self.widget.save_data_btn, self.save_data_btn_clicked)
        self.connect_click_function(self.widget.save_graph_btn, self.save_graph_btn_clicked)

        self.model.data_changed.connect(self.data_changed)
        self.model.spectrum_changed.connect(self.widget.graph_widget.plot_data)
        self.widget.roi_widget.rois_changed.connect(self.rois_changed)
        self.widget.autoprocess_cb.toggled.connect(self.auto_process_cb_toggled)

        self.widget.graph_widget.mouse_moved.connect(self.graph_mouse_moved)
        self.widget.roi_widget.img_widget.mouse_moved.connect(self.img_mouse_moved)

    def connect_click_function(self, emitter, function):
        emitter.clicked.connect(function)

    def load_data_file(self):
        filename = open_file_dialog(self.widget, caption="Load Experiment SPE",
                                    directory=self._working_dir)
        filename = str(filename)
        if filename is not '':
            self.model.load_file(filename)
            self._working_dir = os.path.dirname(filename)
            self._directory_watcher.path = self._working_dir

    def save_data_btn_clicked(self, filename=None):
        if filename is None:
            filename = save_file_dialog(
                self.widget,
                caption="Save data in tabulated text format",
                directory=os.path.join(self._working_dir, '.'.join(self.model.filename.split(".")[:-1]) + ".txt")
            )

            if filename is not '':
                self.model.save_txt(filename)

    def save_graph_btn_clicked(self, filename=None):
        if filename is None:
            filename = save_file_dialog(
                self.widget,
                caption="Save displayed graph as vector graphics or image",
                directory=os.path.join(self._working_dir, '.'.join(self.model.filename.split(".")[:-1]) + ".svg"),
                filter='Vector Graphics (*.svg);; Image (*.png)'
            )
        filename = str(filename)

        if filename is not '':
            self.widget.graph_widget.save_graph(filename)

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

        self.widget.graph_info_lbl.setText(self.model.file_info)

    def rois_changed(self):
        """
        called when the roi is changed in the roi Widget, will recalculate the spectrum and then plot the new updated
        one.
        """
        self.model.roi = self.widget.roi_widget.get_rois()[0]

    def graph_mouse_moved(self, x, y):
        self.widget.graph_mouse_pos_lbl.setText("X: {:8.2f}  Y: {:8.2f}".format(x, y))

    def img_mouse_moved(self, x, y):
        x = np.floor(x)
        y = np.floor(y)
        try:
            self.widget.roi_widget.pos_lbl.setText("X: {:5.0f}  Y: {:5.0f}    Int: {:6.0f}    lambda: {:5.2f} nm".
                                                   format(x, y,
                                                          self.model.data_img[y, x],
                                                          self.model._data_img_x_calibration[x]))

        except (IndexError, AttributeError, TypeError):
            pass

    def auto_process_cb_toggled(self):
        if self.widget.autoprocess_cb.isChecked():
            self._directory_watcher.activate()
        else:
            self._directory_watcher.deactivate()

    def _create_autoprocess_system(self):
        self._directory_watcher = NewFileInDirectoryWatcher(file_types=['.spe'])
        self._directory_watcher.file_added.connect(self.load_data_file)
