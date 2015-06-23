# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtCore, QtGui

from .RoiWidget import RoiWidget
from .SpectrumWidget import SpectrumWidget
from .Widgets import FileGroupBox, OutputGroupBox, StatusBar


class BaseWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(BaseWidget, self).__init__(*args, **kwargs)
        self._main_layout = QtGui.QVBoxLayout()
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        self._main_splitter = QtGui.QSplitter(QtCore.Qt.Vertical)

        self._graph_control_widget = QtGui.QWidget()
        self._graph_control_layout = QtGui.QGridLayout()
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


class ControlWidget(QtGui.QWidget):
    def __init__(self):
        super(ControlWidget, self).__init__()
        self._layout = QtGui.QVBoxLayout()
        self._file_gb = FileGroupBox()
        self._output_gb = OutputGroupBox()

        self._layout.addWidget(self._file_gb)
        self._layout.addWidget(self._output_gb)
        self._layout.addSpacerItem(QtGui.QSpacerItem(QtGui.QSpacerItem(10, 10,
                                                                       QtGui.QSizePolicy.Fixed,
                                                                       QtGui.QSizePolicy.Expanding)))
        self.setLayout(self._layout)


if __name__ == '__main__':
    app = QtGui.QApplication([])
    widget = BaseWidget()
    widget.show()
    widget.raise_()
    app.exec_()
