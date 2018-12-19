# -*- coding: utf-8 -*-
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

from qtpy import QtCore, QtWidgets, QtGui

from .TemperatureSpectrumWidget import TemperatureSpectrumWidget
from .RoiWidget import RoiWidget
from .Widgets import TemperatureFileGroupBox as FileGroupBox
from .Widgets import OutputGroupBox, StatusBar


class TemperatureWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(TemperatureWidget, self).__init__(*args, **kwargs)
        self._main_layout = QtWidgets.QVBoxLayout()
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        self._main_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)

        self._graph_control_widget = QtWidgets.QWidget()
        self._graph_control_layout = QtWidgets.QGridLayout()
        self._graph_control_layout.setContentsMargins(0, 0, 0, 0)

        self.graph_widget = TemperatureSpectrumWidget()
        self.control_widget = TemperatureControlWidget()
        self.graph_status_bar = StatusBar()
        self.roi_widget = RoiWidget(2, ['Downstream', 'Upstream'],
                                    roi_colors=[(255, 255, 0), (255, 140, 0)])

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
        self.control_widget.setMinimumWidth(250)
        self.control_widget.setMaximumWidth(250)

    def create_shortcuts(self):
        self.load_data_file_btn = self.control_widget.experiment_tab.file_gb.load_file_btn
        self.load_next_data_file_btn = self.control_widget.experiment_tab.file_gb.load_next_file_btn
        self.load_previous_data_file_btn = self.control_widget.experiment_tab.file_gb.load_previous_file_btn

        self.load_next_frame_btn = self.control_widget.experiment_tab.file_gb.load_next_frame_btn
        self.load_previous_frame_btn = self.control_widget.experiment_tab.file_gb.load_previous_frame_btn
        self.frame_num_txt = self.control_widget.experiment_tab.file_gb.frame_txt
        self.frame_widget = self.control_widget.experiment_tab.file_gb.frame_control_widget

        self.autoprocess_cb = self.control_widget.experiment_tab.file_gb.autoprocess_cb
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

        self.save_data_btn = self.control_widget.experiment_tab.output_gb.save_data_btn
        self.save_graph_btn = self.control_widget.experiment_tab.output_gb.save_graph_btn

        self.settings_cb = self.control_widget.experiment_tab.settings_gb.settings_cb

        self.roi_img_item = self.roi_widget.img_widget.pg_img_item
        self.time_lapse_layout = self.graph_widget._pg_time_lapse_layout

        self.graph_mouse_pos_lbl = self.graph_status_bar.left_lbl
        self.graph_info_lbl = self.graph_status_bar.right_lbl

        self.connect_to_epics_cb = self.control_widget.experiment_tab.connect_to_epics_cb


class TemperatureControlWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(TemperatureControlWidget, self).__init__(*args, **kwargs)

        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self.tab_widget = QtWidgets.QTabWidget()
        self.experiment_tab = TemperatureExperimentTab()
        self.calibration_tab = TemperatureCalibrationTab()

        self.tab_widget.addTab(self.experiment_tab, 'Experiment')
        self.tab_widget.addTab(self.calibration_tab, 'Calibration')
        self._layout.addWidget(self.tab_widget)
        self.setLayout(self._layout)


class TemperatureExperimentTab(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(TemperatureExperimentTab, self).__init__(*args, **kwargs)
        self._layout = QtWidgets.QVBoxLayout()
        self.file_gb = FileGroupBox()
        self.output_gb = OutputGroupBox()
        self.settings_gb = SettingsGroupBox()
        self.connect_to_epics_cb = QtWidgets.QCheckBox("Connect to Epics")
        self.connect_to_epics_cb.setLayoutDirection(QtCore.Qt.RightToLeft)

        self._layout.addWidget(self.file_gb)
        self._layout.addWidget(self.output_gb)
        self._layout.addWidget(self.settings_gb)
        self._layout.addWidget(self.connect_to_epics_cb)
        self._layout.addSpacerItem(QtWidgets.QSpacerItem(10, 10,
                                                     QtWidgets.QSizePolicy.Fixed,
                                                     QtWidgets.QSizePolicy.Expanding))

        self.setLayout(self._layout)


class SettingsGroupBox(QtWidgets.QGroupBox):
    def __init__(self, *args, **kwargs):
        super(SettingsGroupBox, self).__init__('Settings')

        self._layout = QtWidgets.QGridLayout()
        self._layout.setVerticalSpacing(8)
        self._layout.setHorizontalSpacing(8)

        self.settings_cb = QtWidgets.QComboBox()
        self.load_setting_btn = QtWidgets.QPushButton('Load')
        self.save_setting_btn = QtWidgets.QPushButton('Save')

        self._layout.addWidget(self.settings_cb, 0, 0, 1, 2)
        self._layout.addWidget(self.load_setting_btn, 1, 0)
        self._layout.addWidget(self.save_setting_btn, 1, 1)

        self.style_widgets()

        self.setLayout(self._layout)

    def style_widgets(self):
        self.load_setting_btn.setFlat(True)
        self.save_setting_btn.setFlat(True)

        cleanlooks = QtWidgets.QStyleFactory.create('plastique')
        self.settings_cb.setStyle(cleanlooks)
        self.settings_cb.view().setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)


class TemperatureCalibrationTab(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(TemperatureCalibrationTab, self).__init__(*args, **kwargs)
        self._layout = QtWidgets.QVBoxLayout()

        self.downstream_gb = CalibrationGB('Downstream', 'rgba(255, 255, 0, 255)')
        self.upstream_gb = CalibrationGB('Upstream', 'rgba(255, 140, 0, 255)')

        self._layout.addWidget(self.downstream_gb)
        self._layout.addWidget(self.upstream_gb)

        self._layout.addSpacerItem(QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed,
                                                     QtWidgets.QSizePolicy.Expanding))
        self.setLayout(self._layout)


class CalibrationGB(QtWidgets.QGroupBox):
    def __init__(self, title, color):
        super(CalibrationGB, self).__init__(title)

        self.color = color
        self._layout = QtWidgets.QGridLayout()
        self._layout.setVerticalSpacing(8)
        self._layout.setHorizontalSpacing(8)

        self.load_file_btn = QtWidgets.QPushButton('Load File')
        self.file_lbl = QtWidgets.QLabel('Select File...')

        self.temperature_txt = QtWidgets.QLineEdit('2000')
        self.temperature_unit_lbl = QtWidgets.QLabel('K')

        self.temperature_rb = QtWidgets.QRadioButton('Temperature')
        self.etalon_rb = QtWidgets.QRadioButton('Etalon Spectrum')
        self.load_etalon_btn = QtWidgets.QPushButton('...')
        self.etalon_file_lbl = QtWidgets.QLabel('Select File...')

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
