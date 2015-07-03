# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtGui, QtCore


class FileGroupBox(QtGui.QGroupBox, object):
    def __init__(self, *args):
        super(FileGroupBox, self).__init__(*args)
        self.setTitle('File')
        self._main_layout = QtGui.QVBoxLayout()
        self._main_layout.setContentsMargins(8, 8, 8, 8)
        self._main_layout.setSpacing(8)

        self.create_file_control_widget()
        self.create_frame_control_widget()

        self.style_widgets()

        self._main_layout.addWidget(self.file_control_widget)
        self._main_layout.addWidget(self.frame_control_widget)
        self.frame_control_widget.hide()
        self.setLayout(self._main_layout)

    def create_file_control_widget(self):
        self.file_control_widget = QtGui.QWidget()

        self._file_control_layout = QtGui.QGridLayout()
        self._file_control_layout.setContentsMargins(0, 0, 0, 0)
        self._file_control_layout.setHorizontalSpacing(5)
        self._file_control_layout.setVerticalSpacing(8)

        self.load_file_btn = QtGui.QPushButton('Load')
        self.load_next_file_btn = QtGui.QPushButton('>')
        self.load_previous_file_btn = QtGui.QPushButton('<')
        self.autoprocess_cb = QtGui.QCheckBox('auto')
        self.filename_lbl = QtGui.QLabel('file')
        self.dirname_lbl = QtGui.QLabel('folder')

        self._file_control_layout.addWidget(self.load_file_btn, 0, 0, 1, 2)
        self._file_control_layout.addWidget(self.load_previous_file_btn, 1, 0)
        self._file_control_layout.addWidget(self.load_next_file_btn, 1, 1)
        self._file_control_layout.addWidget(self.autoprocess_cb, 0, 2)
        self._file_control_layout.addWidget(self.filename_lbl, 2, 0, 1, 4)
        self._file_control_layout.addWidget(self.dirname_lbl, 3, 0, 1, 4)
        self.file_control_widget.setLayout(self._file_control_layout)

    def create_frame_control_widget(self):
        self.frame_control_widget = QtGui.QWidget()

        self._frame_control_layout = QtGui.QHBoxLayout()
        self._frame_control_layout.setContentsMargins(0, 0, 0, 0)
        self._frame_control_layout.setSpacing(5)

        self.load_previous_frame_btn = QtGui.QPushButton('<')
        self.load_next_frame_btn = QtGui.QPushButton('>')
        self.frame_txt = QtGui.QLineEdit('100')

        self._frame_control_layout.addWidget(self.load_previous_frame_btn)
        self._frame_control_layout.addWidget(self.frame_txt)
        self._frame_control_layout.addWidget(self.load_next_frame_btn)
        self._frame_control_layout.addSpacerItem(QtGui.QSpacerItem(QtGui.QSpacerItem(10, 10,
                                                                                     QtGui.QSizePolicy.Expanding,
                                                                                     QtGui.QSizePolicy.Fixed)))
        self.frame_control_widget.setLayout(self._frame_control_layout)

    def style_widgets(self):
        self.frame_txt.setMaximumWidth(50)

        self.load_previous_file_btn.setFlat(True)
        self.load_next_file_btn.setFlat(True)
        self.load_previous_frame_btn.setFlat(True)
        self.load_next_frame_btn.setFlat(True)
        self.load_file_btn.setFlat(True)

        self.frame_txt.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.frame_txt.setValidator(QtGui.QIntValidator())


class TemperatureFileGroupBox(FileGroupBox):
    def __init__(self, *args, **kwargs):
        super(TemperatureFileGroupBox, self).__init__()
        self.timelapse_btn = QtGui.QPushButton('Time Lapse')
        self.timelapse_btn.setFlat(True)
        self._frame_control_layout.addWidget(self.timelapse_btn)

        self.load_previous_frame_btn.setMaximumWidth(25)
        self.load_next_frame_btn.setMaximumWidth(25)


class OutputGroupBox(QtGui.QGroupBox, object):
    def __init__(self, *args, **kwargs):
        super(OutputGroupBox, self).__init__("Output", *args, **kwargs)

        self.create_widgets()
        self.create_layout()
        self.style_widgets()

    def create_widgets(self):
        self.save_data_btn = QtGui.QPushButton("Save Data")
        self.save_graph_btn = QtGui.QPushButton("Save Graph")

    def create_layout(self):
        self._layout = QtGui.QHBoxLayout()

        self._layout.addWidget(self.save_data_btn)
        self._layout.addWidget(self.save_graph_btn)
        self.setLayout(self._layout)

    def style_widgets(self):
        self.save_data_btn.setFlat(True)
        self.save_graph_btn.setFlat(True)


class StatusBar(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(StatusBar, self).__init__(*args, **kwargs)

        self.create_widgets()
        self.create_layout()
        self.style_widgets()

    def create_widgets(self):
        self.left_lbl = QtGui.QLabel()
        self.right_lbl = QtGui.QLabel()

    def create_layout(self):
        self._layout = QtGui.QHBoxLayout()
        self._layout.addWidget(self.left_lbl)
        self._layout.addSpacerItem(QtGui.QSpacerItem(QtGui.QSpacerItem(10, 10,
                                                                       QtGui.QSizePolicy.Expanding,
                                                                       QtGui.QSizePolicy.Fixed)))
        self._layout.addWidget(self.right_lbl)

        self.setLayout(self._layout)

    def style_widgets(self):
        self._layout.setContentsMargins(8, 0, 8, 0)
