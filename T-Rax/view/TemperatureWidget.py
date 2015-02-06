# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtCore, QtGui

from view.SpectrumWidget import SpectrumWidget
from view.RoiWidget import RoiWidget


class TemperatureWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(TemperatureWidget, self).__init__(*args, **kwargs)
        self._main_layout = QtGui.QVBoxLayout()
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        self._main_splitter = QtGui.QSplitter(QtCore.Qt.Vertical)

        self._graph_control_widget = QtGui.QWidget()
        self._graph_control_layout = QtGui.QHBoxLayout()
        self._graph_control_layout.setContentsMargins(0, 0, 0, 0)

        self.graph_widget = SpectrumWidget()
        self.control_widget = ControlWidget()
        self.roi_widget = RoiWidget(2, ['Downstream', 'Upstream'],
                                       roi_colors=[(255, 255, 0), (255, 140, 0)])

        self._graph_control_layout.addWidget(self.graph_widget)
        self._graph_control_layout.addWidget(self.control_widget)

        self._graph_control_layout.setStretch(0, 1)
        self._graph_control_layout.setStretch(1, 0)

        self._graph_control_widget.setLayout(self._graph_control_layout)

        self._main_splitter.addWidget(self._graph_control_widget)
        self._main_splitter.addWidget(self.roi_widget)

        self._main_layout.addWidget(self._main_splitter)

        self.setLayout(self._main_layout)

        self.create_shortcuts()

    def create_shortcuts(self):
        self.load_data_file_btn = self.control_widget.experiment_tab.file_gb.load_file_btn
        self.load_next_data_file_btn = self.control_widget.experiment_tab.file_gb.load_next_file_btn
        self.load_previous_data_file_btn = self.control_widget.experiment_tab.file_gb.load_previous_file_btn

        self.load_next_frame_btn = self.control_widget.experiment_tab.file_gb.load_next_frame_btn
        self.load_previous_frame_btn = self.control_widget.experiment_tab.file_gb.load_previous_frame_btn
        self.frame_num_txt = self.control_widget.experiment_tab.file_gb.frame_txt
        self.frame_widget = self.control_widget.experiment_tab.file_gb.frame_control_widget

        self.auto_process_cb = self.control_widget.experiment_tab.file_gb.autoprocess_cb
        self.filename_lbl = self.control_widget.experiment_tab.file_gb.filename_lbl
        self.dirname_lbl = self.control_widget.experiment_tab.file_gb.dirname_lbl

        self.load_ds_calibration_file_btn = self.control_widget.calibration_tab.downstream_gb.load_file_btn
        self.load_us_calibration_file_btn = self.control_widget.calibration_tab.upstream_gb.load_file_btn
        self.ds_calibration_filename_lbl = self.control_widget.calibration_tab.downstream_gb.file_lbl
        self.us_calibration_filename_lbl = self.control_widget.calibration_tab.upstream_gb.file_lbl

        self.ds_temperature_rb = self.control_widget.calibration_tab.downstream_gb.temperature_rb
        self.us_temperature_rb = self.control_widget.calibration_tab.upstream_gb.temperature_rb
        self.ds_etalon_rb = self.control_widget.calibration_tab.downstream_gb.etalon_rb
        self.us_etalon_rb = self.control_widget.calibration_tab.upstream_gb.etalon_rb
        self.ds_load_etalon_file_btn = self.control_widget.calibration_tab.downstream_gb.load_etalon_btn
        self.us_load_etalon_file_btn = self.control_widget.calibration_tab.upstream_gb.load_etalon_btn
        self.ds_etalon_filename_lbl = self.control_widget.calibration_tab.downstream_gb.etalon_file_lbl
        self.us_etalon_filename_lbl = self.control_widget.calibration_tab.upstream_gb.etalon_file_lbl
        self.ds_temperature_txt = self.control_widget.calibration_tab.downstream_gb.temperature_txt
        self.us_temperature_txt = self.control_widget.calibration_tab.upstream_gb.temperature_txt

        self.load_setting_btn = self.control_widget.experiment_tab.settings_gb.load_setting_btn
        self.save_setting_btn = self.control_widget.experiment_tab.settings_gb.save_setting_btn

        self.settings_cb = self.control_widget.experiment_tab.settings_gb.settings_cb

        self.roi_img_item = self.roi_widget.img_widget.pg_img_item


class ControlWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(ControlWidget, self).__init__(*args, **kwargs)

        self._layout = QtGui.QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self.tab_widget = QtGui.QTabWidget()
        self.experiment_tab = ExperimentTab()
        self.calibration_tab = CalibrationTab()

        self.tab_widget.addTab(self.experiment_tab, 'Experiment')
        self.tab_widget.addTab(self.calibration_tab, 'Calibration')
        self._layout.addWidget(self.tab_widget)
        self.setLayout(self._layout)


class ExperimentTab(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(ExperimentTab, self).__init__(*args, **kwargs)
        self._layout = QtGui.QVBoxLayout()
        self.file_gb = FileGroupBox()
        self.settings_gb = SettingsGroupBox()

        self._layout.addWidget(self.file_gb)
        self._layout.addWidget(self.settings_gb)
        self._layout.addSpacerItem(QtGui.QSpacerItem(10, 10,
                                                     QtGui.QSizePolicy.Fixed,
                                                     QtGui.QSizePolicy.Expanding))
        self.setLayout(self._layout)


class FileGroupBox(QtGui.QGroupBox):
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

        self._file_control_layout.addWidget(self.load_file_btn, 0, 0)
        self._file_control_layout.addWidget(self.load_previous_file_btn, 0, 1)
        self._file_control_layout.addWidget(self.load_next_file_btn, 0, 2)
        self._file_control_layout.addWidget(self.autoprocess_cb, 0, 3)
        self._file_control_layout.addWidget(self.filename_lbl, 1, 0, 1, 4)
        self._file_control_layout.addWidget(self.dirname_lbl, 2, 0, 1, 4)
        self.file_control_widget.setLayout(self._file_control_layout)

    def create_frame_control_widget(self):
        self.frame_control_widget = QtGui.QWidget()

        self._frame_control_layout = QtGui.QHBoxLayout()
        self._frame_control_layout.setContentsMargins(0, 0, 0, 0)
        self._frame_control_layout.setSpacing(5)

        self.load_previous_frame_btn = QtGui.QPushButton('<')
        self.load_next_frame_btn = QtGui.QPushButton('>')
        self.frame_txt = QtGui.QLineEdit('100')
        self.timelapse_btn = QtGui.QPushButton('Time Lapse')

        self._frame_control_layout.addWidget(self.load_previous_frame_btn)
        self._frame_control_layout.addWidget(self.frame_txt)
        self._frame_control_layout.addWidget(self.load_next_frame_btn)
        self._frame_control_layout.addWidget(self.timelapse_btn)
        self.frame_control_widget.setLayout(self._frame_control_layout)

    def style_widgets(self):
        self.load_previous_file_btn.setMaximumWidth(25)
        self.load_next_file_btn.setMaximumWidth(25)
        self.load_previous_frame_btn.setMaximumWidth(25)
        self.load_next_frame_btn.setMaximumWidth(25)

        self.frame_txt.setMaximumWidth(50)

        self.load_previous_file_btn.setFlat(True)
        self.load_next_file_btn.setFlat(True)
        self.load_previous_frame_btn.setFlat(True)
        self.load_next_frame_btn.setFlat(True)
        self.load_file_btn.setFlat(True)
        self.timelapse_btn.setFlat(True)

        self.frame_txt.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.frame_txt.setValidator(QtGui.QIntValidator())


class SettingsGroupBox(QtGui.QGroupBox):
    def __init__(self, *args, **kwargs):
        super(SettingsGroupBox, self).__init__('Settings')

        self._layout = QtGui.QGridLayout()
        self._layout.setVerticalSpacing(8)
        self._layout.setHorizontalSpacing(8)

        self.settings_cb = QtGui.QComboBox()
        self.load_setting_btn = QtGui.QPushButton('Load')
        self.save_setting_btn = QtGui.QPushButton('Save')

        self._layout.addWidget(self.settings_cb, 0, 0, 1, 2)
        self._layout.addWidget(self.load_setting_btn, 1, 0)
        self._layout.addWidget(self.save_setting_btn, 1, 1)

        self.style_widgets()

        self.setLayout(self._layout)

    def style_widgets(self):
        self.load_setting_btn.setFlat(True)
        self.save_setting_btn.setFlat(True)

        cleanlooks = QtGui.QStyleFactory.create('plastique')
        self.settings_cb.setStyle(cleanlooks)
        self.settings_cb.view().setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)


class CalibrationTab(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(CalibrationTab, self).__init__(*args, **kwargs)
        self._layout = QtGui.QVBoxLayout()

        self.downstream_gb = CalibrationGB('Downstream', 'rgba(255, 255, 0, 255)')
        self.upstream_gb = CalibrationGB('Upstream', 'rgba(255, 140, 0, 255)')

        self._layout.addWidget(self.downstream_gb)
        self._layout.addWidget(self.upstream_gb)

        self._layout.addSpacerItem(QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Fixed,
                                                     QtGui.QSizePolicy.Expanding))
        self.setLayout(self._layout)


class CalibrationGB(QtGui.QGroupBox):
    def __init__(self, title, color):
        super(CalibrationGB, self).__init__(title)

        self.color = color
        self._layout = QtGui.QGridLayout()
        self._layout.setVerticalSpacing(8)
        self._layout.setHorizontalSpacing(8)

        self.load_file_btn = QtGui.QPushButton('Load File')
        self.file_lbl = QtGui.QLabel('Select File...')

        self.temperature_txt = QtGui.QLineEdit('2000')
        self.temperature_unit_lbl = QtGui.QLabel('K')

        self.temperature_rb = QtGui.QRadioButton('Temperature')
        self.etalon_rb = QtGui.QRadioButton('Etalon Spectrum')
        self.load_etalon_btn = QtGui.QPushButton('...')
        self.etalon_file_lbl = QtGui.QLabel('Select File...')

        self._layout.addWidget(self.load_file_btn, 0, 0, 1, 3)
        self._layout.addWidget(self.file_lbl, 0, 3)
        self._layout.addWidget(self.temperature_txt, 1, 0, 1, 2)
        self._layout.addWidget(self.temperature_unit_lbl, 1, 2)
        self._layout.addWidget(self.temperature_rb, 1, 3)
        self._layout.addWidget(self.load_etalon_btn, 2, 1, 1, 2)
        self._layout.addWidget(self.etalon_rb, 2, 3)
        self._layout.addWidget(self.etalon_file_lbl, 3, 3)

        self.setLayout(self._layout)
        self.style_widgets()
        self.set_stylesheet()

    def style_widgets(self):
        self.load_file_btn.setFlat(True)
        self.load_etalon_btn.setFlat(True)

        self.temperature_txt.setValidator(QtGui.QDoubleValidator())
        self.temperature_txt.setAlignment(QtCore.Qt.AlignRight)

        self.temperature_rb.toggle()

    def set_stylesheet(self):
        style_str = "QGroupBox { color: %s; border: 1px solid %s}" % (self.color, self.color)
        self.setStyleSheet(style_str)



