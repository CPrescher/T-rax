# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtCore, QtGui
from .RoiWidget import RoiWidget
from .SpectrumWidget import SpectrumWidget
from .Widgets import FileGroupBox


class RamanWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(RamanWidget, self).__init__(*args, **kwargs)
        self._main_layout = QtGui.QVBoxLayout()
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        self._main_splitter = QtGui.QSplitter(QtCore.Qt.Vertical)

        self._graph_control_widget = QtGui.QWidget()
        self._graph_control_layout = QtGui.QHBoxLayout()
        self._graph_control_layout.setContentsMargins(0, 0, 0, 0)

        self.graph_widget = SpectrumWidget()
        self.control_widget = ControlWidget()
        self.roi_widget = RoiWidget(1, roi_colors=[(255, 255, 255)])

        self._graph_control_layout.addWidget(self.graph_widget)
        self._graph_control_layout.addWidget(self.control_widget)

        self._graph_control_layout.setStretch(0, 1)
        self._graph_control_layout.setStretch(1, 0)

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
        self.control_widget.setMinimumWidth(250)
        self.control_widget.setMaximumWidth(250)

    def create_shortcuts(self):
        self.load_file_btn = self.control_widget._file_gb.load_file_btn
        self.load_next_file_btn = self.control_widget._file_gb.load_next_file_btn
        self.load_previous_file_btn = self.control_widget._file_gb.load_previous_file_btn

        self.filename_lbl = self.control_widget._file_gb.filename_lbl
        self.dirname_lbl = self.control_widget._file_gb.dirname_lbl

class ControlWidget(QtGui.QWidget):
    def __init__(self):
        super(ControlWidget, self).__init__()
        self._layout = QtGui.QVBoxLayout()
        self._file_gb = FileGroupBox()

        self._layout.addWidget(self._file_gb)
        self._layout.addSpacerItem(QtGui.QSpacerItem(QtGui.QSpacerItem(10, 10,
                                                                       QtGui.QSizePolicy.Fixed,
                                                                       QtGui.QSizePolicy.Expanding)))
        self.setLayout(self._layout)


if __name__ == '__main__':
    app = QtGui.QApplication([])
    widget = RamanWidget()
    widget.show()
    widget.raise_()
    app.exec_()