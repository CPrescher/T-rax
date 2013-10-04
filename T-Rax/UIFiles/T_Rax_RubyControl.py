# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'T_Rax_RubyControl.ui'
#
# Created: Fri Oct 04 11:33:07 2013
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

class Ui_ruby_control_widget(object):
    def setupUi(self, ruby_control_widget):
        ruby_control_widget.setObjectName(_fromUtf8("ruby_control_widget"))
        ruby_control_widget.resize(263, 393)
        ruby_control_widget.setMaximumSize(QtCore.QSize(263, 16777215))
        ruby_control_widget.setStyleSheet(_fromUtf8(" #ruby_control_widget, #temperature_control_widget, #diamond_control_widget, QTabWidget::pane, QTabWidget::tab-bar,  \n"
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
"QComboBox {\n"
"    background: #2D2D30;\n"
"    border-radius:5px;\n"
"    font-weight: normal;\n"
"    padding: 4px;\n"
"    padding-left: 8px;\n"
"    text-align: right;\n"
"    margin:3px;\n"
"}\n"
"\n"
" QLineEdit{  \n"
"     border-radius: 5px;  \n"
"     background: #F1F1F1;  \n"
"     color: black;  \n"
" }  \n"
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
" }  \n"
""))
        self.verticalLayout_2 = QtGui.QVBoxLayout(ruby_control_widget)
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(ruby_control_widget)
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
        self.roi_setup_btn = QtGui.QPushButton(ruby_control_widget)
        self.roi_setup_btn.setObjectName(_fromUtf8("roi_setup_btn"))
        self.verticalLayout_2.addWidget(self.roi_setup_btn)
        self.groupBox_2 = QtGui.QGroupBox(ruby_control_widget)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formLayout.setItem(0, QtGui.QFormLayout.LabelRole, spacerItem)
        self.conditions_cb = QtGui.QComboBox(self.groupBox_2)
        self.conditions_cb.setMinimumSize(QtCore.QSize(0, 26))
        self.conditions_cb.setMaximumSize(QtCore.QSize(250, 16777215))
        self.conditions_cb.setObjectName(_fromUtf8("conditions_cb"))
        self.conditions_cb.addItem(_fromUtf8(""))
        self.conditions_cb.addItem(_fromUtf8(""))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.conditions_cb)
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(7)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.reference_pos_txt = QtGui.QLineEdit(self.groupBox_2)
        self.reference_pos_txt.setMaximumSize(QtCore.QSize(80, 16777215))
        self.reference_pos_txt.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.reference_pos_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.reference_pos_txt.setObjectName(_fromUtf8("reference_pos_txt"))
        self.horizontalLayout_4.addWidget(self.reference_pos_txt)
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setMinimumSize(QtCore.QSize(30, 0))
        self.label_5.setMaximumSize(QtCore.QSize(30, 18))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_4.addWidget(self.label_5)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.temperature_txt = QtGui.QLineEdit(self.groupBox_2)
        self.temperature_txt.setMaximumSize(QtCore.QSize(80, 16777215))
        self.temperature_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.temperature_txt.setObjectName(_fromUtf8("temperature_txt"))
        self.horizontalLayout_6.addWidget(self.temperature_txt)
        self.label_7 = QtGui.QLabel(self.groupBox_2)
        self.label_7.setMinimumSize(QtCore.QSize(30, 0))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_6.addWidget(self.label_7)
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout_6)
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.measured_pos_lbl = QtGui.QLabel(self.groupBox_2)
        self.measured_pos_lbl.setMinimumSize(QtCore.QSize(0, 18))
        self.measured_pos_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.measured_pos_lbl.setObjectName(_fromUtf8("measured_pos_lbl"))
        self.horizontalLayout_3.addWidget(self.measured_pos_lbl)
        self.label_8 = QtGui.QLabel(self.groupBox_2)
        self.label_8.setMinimumSize(QtCore.QSize(30, 0))
        self.label_8.setMaximumSize(QtCore.QSize(30, 18))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.horizontalLayout_3.addWidget(self.label_8)
        self.formLayout.setLayout(3, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(7)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.pressure_lbl = QtGui.QLabel(self.groupBox_2)
        self.pressure_lbl.setMinimumSize(QtCore.QSize(0, 18))
        self.pressure_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pressure_lbl.setObjectName(_fromUtf8("pressure_lbl"))
        self.horizontalLayout_5.addWidget(self.pressure_lbl)
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setMaximumSize(QtCore.QSize(30, 16777215))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_5.addWidget(self.label_6)
        self.formLayout.setLayout(4, QtGui.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.verticalLayout.addLayout(self.formLayout)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.fit_ruby_btn = QtGui.QPushButton(ruby_control_widget)
        self.fit_ruby_btn.setMaximumSize(QtCore.QSize(250, 16777215))
        self.fit_ruby_btn.setObjectName(_fromUtf8("fit_ruby_btn"))
        self.verticalLayout_2.addWidget(self.fit_ruby_btn)
        spacerItem3 = QtGui.QSpacerItem(20, 49, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)

        self.retranslateUi(ruby_control_widget)
        QtCore.QMetaObject.connectSlotsByName(ruby_control_widget)

    def retranslateUi(self, ruby_control_widget):
        ruby_control_widget.setWindowTitle(_translate("ruby_control_widget", "Form", None))
        self.groupBox.setTitle(_translate("ruby_control_widget", "Experiment", None))
        self.load_exp_data_btn.setText(_translate("ruby_control_widget", "Load Data", None))
        self.load_previous_exp_data_btn.setText(_translate("ruby_control_widget", "<--", None))
        self.load_next_exp_data_btn.setText(_translate("ruby_control_widget", "-->", None))
        self.auto_process_cb.setText(_translate("ruby_control_widget", "autoprocess", None))
        self.roi_setup_btn.setText(_translate("ruby_control_widget", "ROI Setup", None))
        self.groupBox_2.setTitle(_translate("ruby_control_widget", "Pressure", None))
        self.conditions_cb.setItemText(0, _translate("ruby_control_widget", "hydrostatic", None))
        self.conditions_cb.setItemText(1, _translate("ruby_control_widget", "non-hydrostatic", None))
        self.label.setText(_translate("ruby_control_widget", "Reference:", None))
        self.reference_pos_txt.setText(_translate("ruby_control_widget", "694.15", None))
        self.label_5.setText(_translate("ruby_control_widget", "nm", None))
        self.label_4.setText(_translate("ruby_control_widget", "Temperature:", None))
        self.temperature_txt.setText(_translate("ruby_control_widget", "300", None))
        self.label_7.setText(_translate("ruby_control_widget", "K", None))
        self.label_2.setText(_translate("ruby_control_widget", "Measured:", None))
        self.measured_pos_lbl.setText(_translate("ruby_control_widget", "705", None))
        self.label_8.setText(_translate("ruby_control_widget", "nm", None))
        self.label_3.setText(_translate("ruby_control_widget", "Pressure:", None))
        self.pressure_lbl.setText(_translate("ruby_control_widget", "150", None))
        self.label_6.setText(_translate("ruby_control_widget", "GPa", None))
        self.fit_ruby_btn.setText(_translate("ruby_control_widget", "Fit Ruby", None))

