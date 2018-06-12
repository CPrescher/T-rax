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

from qtpy import QtCore, QtWidgets

from .RoiWidget import RoiWidget
from .SpectrumWidget import SpectrumWidget
from .Widgets import FileGroupBox, OutputGroupBox, StatusBar


class BaseWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(BaseWidget, self).__init__(*args, **kwargs)
        self._main_layout = QtWidgets.QVBoxLayout()
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        self._main_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)

        self._graph_control_widget = QtWidgets.QWidget()
        self._graph_control_layout = QtWidgets.QGridLayout()
        self._graph_control_layout.setContentsMargins(0, 0, 0, 0)

        self.graph_widget = SpectrumWidget()
        self.control_widget = ControlWidget()
        self.graph_status_bar = StatusBar()
        self.roi_widget = RoiWidget(1, roi_colors=[(255, 255, 255)])

        self._graph_control_layout.addWidget(self.graph_widget, 0, 0)
        self._graph_control_layout.addWidget(self.control_widget, 0, 1)
        self._graph_control_layout.addWidget(self.graph_status_bar, 1, 0, 1, 2)

        self._graph_control_widget.setLayout(self._graph_control_layout)

        self._main_splitter.addWidget(self._graph_control_widget)
        self._main_splitter.addWidget(self.roi_widget)

        self._main_layout.addWidget(self._main_splitter)

        self._main_splitter.setStretchFactor(0, 3)
        self._main_splitter.setStretchFactor(1, 2)

        self.setLayout(self._main_layout)

        self.style_widgets()
        self.create_shortcuts()

    def style_widgets(self):
        self._graph_control_layout.setSpacing(0)
        self._graph_control_layout.setContentsMargins(0, 0, 0, 0)
        self._main_splitter.setContentsMargins(0, 0, 0, 0)

        self.control_widget.setMinimumWidth(250)
        self.control_widget.setMaximumWidth(250)

    def create_shortcuts(self):
        self.load_file_btn = self.control_widget._file_gb.load_file_btn
        self.load_next_file_btn = self.control_widget._file_gb.load_next_file_btn
        self.load_previous_file_btn = self.control_widget._file_gb.load_previous_file_btn

        self.autoprocess_cb = self.control_widget._file_gb.autoprocess_cb

        self.filename_lbl = self.control_widget._file_gb.filename_lbl
        self.dirname_lbl = self.control_widget._file_gb.dirname_lbl

        self.frame_widget = self.control_widget._file_gb.frame_control_widget
        self.frame_txt = self.control_widget._file_gb.frame_txt
        self.load_next_frame_btn = self.control_widget._file_gb.load_next_frame_btn
        self.load_previous_frame_btn = self.control_widget._file_gb.load_previous_frame_btn

        self.save_data_btn = self.control_widget._output_gb.save_data_btn
        self.save_graph_btn = self.control_widget._output_gb.save_graph_btn

        self.graph_info_lbl = self.graph_status_bar.right_lbl
        self.graph_mouse_pos_lbl = self.graph_status_bar.left_lbl

    def add_control_widget(self, widget):
        self.control_widget._layout.insertWidget(self.control_widget._layout.count() - 1, widget)


class ControlWidget(QtWidgets.QWidget):
    def __init__(self):
        super(ControlWidget, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._file_gb = FileGroupBox()
        self._output_gb = OutputGroupBox()

        self._layout.addWidget(self._file_gb)
        self._layout.addWidget(self._output_gb)
        self._layout.addSpacerItem(QtWidgets.QSpacerItem(QtWidgets.QSpacerItem(10, 10,
                                                                       QtWidgets.QSizePolicy.Fixed,
                                                                       QtWidgets.QSizePolicy.Expanding)))
        self.setLayout(self._layout)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = BaseWidget()
    widget.show()
    widget.raise_()
    app.exec_()
