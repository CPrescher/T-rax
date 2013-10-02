# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'T_Rax_TemperatureControl.ui'
#
# Created: Wed Oct 02 15:30:19 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_temperature_control_widget(object):
    def setupUi(self, temperature_control_widget):
        temperature_control_widget.setObjectName(_fromUtf8("temperature_control_widget"))
        temperature_control_widget.resize(269, 444)
        temperature_control_widget.setMaximumSize(QtCore.QSize(269, 16777215))
        temperature_control_widget.setStyleSheet(_fromUtf8("   \n"
" #ruby_control_widget, #temperature_control_widget, #diamond_control_widget, QTabWidget::pane, QTabWidget::tab-bar,  \n"
" #experiment_tab, #calibration_tab{  \n"
"     background: #1E1E1E;      \n"
" }  \n"
"   \n"
" #temperature_control_widget {  \n"
"     padding-left: 5px;  \n"
" }  \n"
"   \n"
" QLabel , QCheckBox, QGroupBox, QRadioButton, QComboBox  {  \n"
"     color: #F1F1F1;  \n"
"     font-weight: bold;  \n"
" }  \n"
" QCheckBox{  \n"
"     border-radius: 5px;  \n"
" }  \n"
" QRadioButton {  \n"
"     font-weight: normal;  \n"
" }  \n"
"   \n"
" QLineEdit{  \n"
"     border-radius: 5px;  \n"
"     background: #F1F1F1;  \n"
"     color: black;  \n"
" }  \n"
"\n"
"\n"
"QComboBox {\n"
"    background: #2D2D30;\n"
"    border-radius:5px;\n"
"    font-weight: normal;\n"
"    padding: 4px;\n"
"    padding-left: 8px;\n"
"    text-align: right;\n"
"    margin:3px;\n"
"}\n"
"   \n"
" QPushButton{  \n"
"     color:white;  \n"
"     border-color: black;  \n"
"     border: 2px solid #F1F1F1;  \n"
"     border-radius: 11px;  \n"
"     font-weight: bold;  \n"
"     padding: 5px;  \n"
" }  \n"
" #temperature_control_widget QPushButton {  \n"
"     background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.20398 rgba(221, 124, 40, 180), stop:1 rgba(0, 0, 0, 255))  \n"
" }  \n"
"   \n"
" #ruby_control_widget QPushButton {  \n"
"     background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.20398 rgba(197, 0, 3, 255), stop:1 rgba(0, 0, 0, 255))  \n"
" }  \n"
"   \n"
" #diamond_control_widget QPushButton{  \n"
"     background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.20398 rgba(27, 0, 134, 255), stop:1 rgba(0, 0, 0, 255))  \n"
" }  \n"
"   \n"
" QPushButton::hover{  \n"
"     border:2px solid #fff;  \n"
"     margin: 0.5px;  \n"
" }  \n"
"   \n"
" QPushPutton::press{  \n"
"    border:2px solid #fff;  \n"
"     margin: 2px;  \n"
" }  \n"
"   \n"
" QGroupBox {  \n"
"     border: 2px solid #F1F1F1;  \n"
"     border-radius: 5px;  \n"
"     margin-top: 7px;  \n"
"     padding: 0px  \n"
" }  \n"
" QGroupBox::title {  \n"
"      subcontrol-origin: margin;  \n"
"      left: 20px  \n"
"  }  \n"
"    \n"
" QTabBar::tab {  \n"
"     background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.20398 rgba(221, 124, 40, 180), stop:1 #1E1E1E);  \n"
"     border: 2px solid  #F1F1F1;  \n"
"     border-top-left-radius: 4px;  \n"
"     border-top-right-radius: 10px;  \n"
"     padding: 5px;  \n"
"     padding-right: 10px;  \n"
"     color: #FFF;  \n"
"     font-weight: bold;  \n"
"     width:85px;  \n"
"     margin-left: 7px  \n"
" }  \n"
"   \n"
" QTabBar::tab:hover {  \n"
"     border-color: #fff;  \n"
" }  \n"
"   \n"
" QTabBar::tab:selected {  \n"
"   \n"
"     border:3px solid  #FFF;  \n"
"     border-bottom-color: #1E1E1E;  \n"
" }  \n"
"   \n"
" QTabBar::tab:!selected {  \n"
"     margin-top: 2px;  \n"
" }  \n"
"   \n"
" #downstream_calib_box{  \n"
"     color:  rgba(255,255,0,255);  \n"
"     border: 2px solid rgba(255,255,0,255);  \n"
" }  \n"
" #upstream_calib_box {  \n"
"     color: rgba(255,140,0,255);  \n"
"     border: 2px solid rgba(255,140,0,255);  \n"
" }  \n"
"   \n"
" #upstream_calib_box QPushButton, #downstream_calib_box QPushButton {  \n"
"     background:qconicalgradient(cx:0.5, cy:0.5, angle:0, stop:0 rgba(30, 30, 30, 255), stop:1 rgba(60, 60, 64, 255))  \n"
" }  "))
        self.verticalLayout_4 = QtGui.QVBoxLayout(temperature_control_widget)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.tab_control = QtGui.QTabWidget(temperature_control_widget)
        self.tab_control.setObjectName(_fromUtf8("tab_control"))
        self.experiment_tab = QtGui.QWidget()
        self.experiment_tab.setObjectName(_fromUtf8("experiment_tab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.experiment_tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(self.experiment_tab)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.load_exp_data_btn = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_exp_data_btn.sizePolicy().hasHeightForWidth())
        self.load_exp_data_btn.setSizePolicy(sizePolicy)
        self.load_exp_data_btn.setMinimumSize(QtCore.QSize(90, 0))
        self.load_exp_data_btn.setObjectName(_fromUtf8("load_exp_data_btn"))
        self.gridLayout.addWidget(self.load_exp_data_btn, 0, 0, 1, 1)
        self.exp_filename_lbl = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exp_filename_lbl.sizePolicy().hasHeightForWidth())
        self.exp_filename_lbl.setSizePolicy(sizePolicy)
        self.exp_filename_lbl.setText(_fromUtf8(""))
        self.exp_filename_lbl.setObjectName(_fromUtf8("exp_filename_lbl"))
        self.gridLayout.addWidget(self.exp_filename_lbl, 0, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.load_previous_exp_data_btn = QtGui.QPushButton(self.groupBox)
        self.load_previous_exp_data_btn.setMaximumSize(QtCore.QSize(40, 24))
        self.load_previous_exp_data_btn.setObjectName(_fromUtf8("load_previous_exp_data_btn"))
        self.horizontalLayout.addWidget(self.load_previous_exp_data_btn)
        self.load_next_exp_data_btn = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_next_exp_data_btn.sizePolicy().hasHeightForWidth())
        self.load_next_exp_data_btn.setSizePolicy(sizePolicy)
        self.load_next_exp_data_btn.setMaximumSize(QtCore.QSize(40, 24))
        self.load_next_exp_data_btn.setObjectName(_fromUtf8("load_next_exp_data_btn"))
        self.horizontalLayout.addWidget(self.load_next_exp_data_btn)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.auto_process_cb = QtGui.QCheckBox(self.groupBox)
        self.auto_process_cb.setObjectName(_fromUtf8("auto_process_cb"))
        self.gridLayout.addWidget(self.auto_process_cb, 1, 1, 1, 1)
        self.exp_folder_name_lbl = QtGui.QLabel(self.groupBox)
        self.exp_folder_name_lbl.setText(_fromUtf8(""))
        self.exp_folder_name_lbl.setObjectName(_fromUtf8("exp_folder_name_lbl"))
        self.gridLayout.addWidget(self.exp_folder_name_lbl, 2, 0, 1, 2)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.roi_setup_btn = QtGui.QPushButton(self.experiment_tab)
        self.roi_setup_btn.setObjectName(_fromUtf8("roi_setup_btn"))
        self.verticalLayout_2.addWidget(self.roi_setup_btn)
        self.groupBox_2 = QtGui.QGroupBox(self.experiment_tab)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 0, 1, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(7)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.fit_from_txt = QtGui.QLineEdit(self.groupBox_2)
        self.fit_from_txt.setMaximumSize(QtCore.QSize(800, 16777215))
        self.fit_from_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fit_from_txt.setObjectName(_fromUtf8("fit_from_txt"))
        self.horizontalLayout_4.addWidget(self.fit_from_txt)
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_4.addWidget(self.label_5)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.fit_to_txt = QtGui.QLineEdit(self.groupBox_2)
        self.fit_to_txt.setMaximumSize(QtCore.QSize(800, 16777215))
        self.fit_to_txt.setBaseSize(QtCore.QSize(50, 0))
        self.fit_to_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fit_to_txt.setObjectName(_fromUtf8("fit_to_txt"))
        self.horizontalLayout_3.addWidget(self.fit_to_txt)
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_3.addWidget(self.label_6)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.groupBox_3 = QtGui.QGroupBox(self.experiment_tab)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.settings_cb = QtGui.QComboBox(self.groupBox_3)
        self.settings_cb.setObjectName(_fromUtf8("settings_cb"))
        self.settings_cb.addItem(_fromUtf8(""))
        self.verticalLayout_7.addWidget(self.settings_cb)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.load_settings_btn = QtGui.QPushButton(self.groupBox_3)
        self.load_settings_btn.setMaximumSize(QtCore.QSize(16777215, 30))
        self.load_settings_btn.setObjectName(_fromUtf8("load_settings_btn"))
        self.horizontalLayout_9.addWidget(self.load_settings_btn)
        self.save_settings_btn = QtGui.QPushButton(self.groupBox_3)
        self.save_settings_btn.setMaximumSize(QtCore.QSize(16777215, 30))
        self.save_settings_btn.setObjectName(_fromUtf8("save_settings_btn"))
        self.horizontalLayout_9.addWidget(self.save_settings_btn)
        self.verticalLayout_7.addLayout(self.horizontalLayout_9)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        spacerItem = QtGui.QSpacerItem(20, 118, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.epics_connection_cb = QtGui.QCheckBox(self.experiment_tab)
        self.epics_connection_cb.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.epics_connection_cb.setObjectName(_fromUtf8("epics_connection_cb"))
        self.verticalLayout_2.addWidget(self.epics_connection_cb)
        self.tab_control.addTab(self.experiment_tab, _fromUtf8(""))
        self.calibration_tab = QtGui.QWidget()
        self.calibration_tab.setObjectName(_fromUtf8("calibration_tab"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.calibration_tab)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.upstream_calib_box = QtGui.QGroupBox(self.calibration_tab)
        self.upstream_calib_box.setObjectName(_fromUtf8("upstream_calib_box"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.upstream_calib_box)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.us_calib_filename_lbl = QtGui.QLabel(self.upstream_calib_box)
        self.us_calib_filename_lbl.setObjectName(_fromUtf8("us_calib_filename_lbl"))
        self.gridLayout_3.addWidget(self.us_calib_filename_lbl, 0, 1, 1, 1)
        self.line = QtGui.QFrame(self.upstream_calib_box)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_3.addWidget(self.line, 1, 0, 1, 2)
        self.load_us_calib_data_btn = QtGui.QPushButton(self.upstream_calib_box)
        self.load_us_calib_data_btn.setObjectName(_fromUtf8("load_us_calib_data_btn"))
        self.gridLayout_3.addWidget(self.load_us_calib_data_btn, 0, 0, 1, 1)
        self.us_temperature_rb = QtGui.QRadioButton(self.upstream_calib_box)
        self.us_temperature_rb.setObjectName(_fromUtf8("us_temperature_rb"))
        self.gridLayout_3.addWidget(self.us_temperature_rb, 2, 1, 1, 1)
        self.us_etalon_lbl = QtGui.QLabel(self.upstream_calib_box)
        self.us_etalon_lbl.setObjectName(_fromUtf8("us_etalon_lbl"))
        self.gridLayout_3.addWidget(self.us_etalon_lbl, 4, 1, 1, 1)
        self.us_etalon_rb = QtGui.QRadioButton(self.upstream_calib_box)
        self.us_etalon_rb.setObjectName(_fromUtf8("us_etalon_rb"))
        self.gridLayout_3.addWidget(self.us_etalon_rb, 3, 1, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.us_temperature_txt = QtGui.QLineEdit(self.upstream_calib_box)
        self.us_temperature_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.us_temperature_txt.setObjectName(_fromUtf8("us_temperature_txt"))
        self.horizontalLayout_5.addWidget(self.us_temperature_txt)
        self.label_9 = QtGui.QLabel(self.upstream_calib_box)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_5.addWidget(self.label_9)
        self.gridLayout_3.addLayout(self.horizontalLayout_5, 2, 0, 1, 1)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.us_etalon_btn = QtGui.QPushButton(self.upstream_calib_box)
        self.us_etalon_btn.setMaximumSize(QtCore.QSize(50, 16777215))
        self.us_etalon_btn.setObjectName(_fromUtf8("us_etalon_btn"))
        self.horizontalLayout_6.addWidget(self.us_etalon_btn)
        self.gridLayout_3.addLayout(self.horizontalLayout_6, 3, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_3)
        self.verticalLayout_6.addWidget(self.upstream_calib_box)
        self.downstream_calib_box = QtGui.QGroupBox(self.calibration_tab)
        self.downstream_calib_box.setObjectName(_fromUtf8("downstream_calib_box"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.downstream_calib_box)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.ds_calib_filename_lbl = QtGui.QLabel(self.downstream_calib_box)
        self.ds_calib_filename_lbl.setObjectName(_fromUtf8("ds_calib_filename_lbl"))
        self.gridLayout_4.addWidget(self.ds_calib_filename_lbl, 0, 1, 1, 1)
        self.line_2 = QtGui.QFrame(self.downstream_calib_box)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout_4.addWidget(self.line_2, 1, 0, 1, 2)
        self.load_ds_calib_data_btn = QtGui.QPushButton(self.downstream_calib_box)
        self.load_ds_calib_data_btn.setObjectName(_fromUtf8("load_ds_calib_data_btn"))
        self.gridLayout_4.addWidget(self.load_ds_calib_data_btn, 0, 0, 1, 1)
        self.ds_temperature_rb = QtGui.QRadioButton(self.downstream_calib_box)
        self.ds_temperature_rb.setObjectName(_fromUtf8("ds_temperature_rb"))
        self.gridLayout_4.addWidget(self.ds_temperature_rb, 2, 1, 1, 1)
        self.ds_etalon_lbl = QtGui.QLabel(self.downstream_calib_box)
        self.ds_etalon_lbl.setObjectName(_fromUtf8("ds_etalon_lbl"))
        self.gridLayout_4.addWidget(self.ds_etalon_lbl, 4, 1, 1, 1)
        self.ds_etalon_rb = QtGui.QRadioButton(self.downstream_calib_box)
        self.ds_etalon_rb.setObjectName(_fromUtf8("ds_etalon_rb"))
        self.gridLayout_4.addWidget(self.ds_etalon_rb, 3, 1, 1, 1)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.ds_temperature_txt = QtGui.QLineEdit(self.downstream_calib_box)
        self.ds_temperature_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ds_temperature_txt.setObjectName(_fromUtf8("ds_temperature_txt"))
        self.horizontalLayout_7.addWidget(self.ds_temperature_txt)
        self.label_11 = QtGui.QLabel(self.downstream_calib_box)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayout_7.addWidget(self.label_11)
        self.gridLayout_4.addLayout(self.horizontalLayout_7, 2, 0, 1, 1)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem2)
        self.ds_etalon_btn = QtGui.QPushButton(self.downstream_calib_box)
        self.ds_etalon_btn.setMaximumSize(QtCore.QSize(50, 16777215))
        self.ds_etalon_btn.setObjectName(_fromUtf8("ds_etalon_btn"))
        self.horizontalLayout_8.addWidget(self.ds_etalon_btn)
        self.gridLayout_4.addLayout(self.horizontalLayout_8, 3, 0, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_4)
        self.verticalLayout_6.addWidget(self.downstream_calib_box)
        spacerItem3 = QtGui.QSpacerItem(20, 26, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem3)
        self.tab_control.addTab(self.calibration_tab, _fromUtf8(""))
        self.verticalLayout_4.addWidget(self.tab_control)

        self.retranslateUi(temperature_control_widget)
        self.tab_control.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(temperature_control_widget)

    def retranslateUi(self, temperature_control_widget):
        temperature_control_widget.setWindowTitle(_translate("temperature_control_widget", "Form", None))
        self.groupBox.setTitle(_translate("temperature_control_widget", "Experiment", None))
        self.load_exp_data_btn.setText(_translate("temperature_control_widget", "Load Data", None))
        self.load_previous_exp_data_btn.setText(_translate("temperature_control_widget", "<--", None))
        self.load_next_exp_data_btn.setText(_translate("temperature_control_widget", "-->", None))
        self.auto_process_cb.setText(_translate("temperature_control_widget", "autoprocess", None))
        self.roi_setup_btn.setText(_translate("temperature_control_widget", "ROI Setup", None))
        self.groupBox_2.setTitle(_translate("temperature_control_widget", "Fit Limits", None))
        self.label_3.setText(_translate("temperature_control_widget", "From", None))
        self.label_4.setText(_translate("temperature_control_widget", "To", None))
        self.label_5.setText(_translate("temperature_control_widget", "nm", None))
        self.label_6.setText(_translate("temperature_control_widget", "nm", None))
        self.groupBox_3.setTitle(_translate("temperature_control_widget", "Settings", None))
        self.settings_cb.setItemText(0, _translate("temperature_control_widget", "user_specified", None))
        self.load_settings_btn.setText(_translate("temperature_control_widget", "Load", None))
        self.save_settings_btn.setText(_translate("temperature_control_widget", "Save", None))
        self.epics_connection_cb.setText(_translate("temperature_control_widget", "Connected to Epics", None))
        self.tab_control.setTabText(self.tab_control.indexOf(self.experiment_tab), _translate("temperature_control_widget", "Experiment", None))
        self.upstream_calib_box.setTitle(_translate("temperature_control_widget", "Upstream", None))
        self.us_calib_filename_lbl.setText(_translate("temperature_control_widget", "Select File...", None))
        self.load_us_calib_data_btn.setText(_translate("temperature_control_widget", "Load Data", None))
        self.us_temperature_rb.setText(_translate("temperature_control_widget", "Temperature", None))
        self.us_etalon_lbl.setText(_translate("temperature_control_widget", "15A Lamp", None))
        self.us_etalon_rb.setText(_translate("temperature_control_widget", "Etalon Spectrum", None))
        self.us_temperature_txt.setText(_translate("temperature_control_widget", "2000", None))
        self.label_9.setText(_translate("temperature_control_widget", "K", None))
        self.us_etalon_btn.setText(_translate("temperature_control_widget", "...", None))
        self.downstream_calib_box.setTitle(_translate("temperature_control_widget", "Downstream", None))
        self.ds_calib_filename_lbl.setText(_translate("temperature_control_widget", "Select File...", None))
        self.load_ds_calib_data_btn.setText(_translate("temperature_control_widget", "Load Data", None))
        self.ds_temperature_rb.setText(_translate("temperature_control_widget", "Temperature", None))
        self.ds_etalon_lbl.setText(_translate("temperature_control_widget", "15A Lamp", None))
        self.ds_etalon_rb.setText(_translate("temperature_control_widget", "Etalon Spectrum", None))
        self.ds_temperature_txt.setText(_translate("temperature_control_widget", "2000", None))
        self.label_11.setText(_translate("temperature_control_widget", "K", None))
        self.ds_etalon_btn.setText(_translate("temperature_control_widget", "...", None))
        self.tab_control.setTabText(self.tab_control.indexOf(self.calibration_tab), _translate("temperature_control_widget", "Calibration", None))

