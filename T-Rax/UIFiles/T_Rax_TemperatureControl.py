# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'T_Rax_TemperatureControl.ui'
#
# Created: Fri Sep 27 22:01:06 2013
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
        temperature_control_widget.resize(250, 472)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(temperature_control_widget.sizePolicy().hasHeightForWidth())
        temperature_control_widget.setSizePolicy(sizePolicy)
        temperature_control_widget.setMinimumSize(QtCore.QSize(250, 0))
        temperature_control_widget.setMaximumSize(QtCore.QSize(250, 16777215))
        temperature_control_widget.setStyleSheet(_fromUtf8("\n"
"#ruby_control_widget, #temperature_control_widget, #diamond_control_widget, QTabWidget::pane, QTabWidget::tab-bar,\n"
"#experiment_tab, #calibration_tab{\n"
"    background: #1E1E1E;    \n"
"}\n"
"\n"
"#temperature_control_widget {\n"
"    padding-left: 5px;\n"
"}\n"
"\n"
"QLabel , QCheckBox, QGroupBox, QRadioButton  {\n"
"    color: #F1F1F1;\n"
"    font-weight: bold;\n"
"}\n"
"QCheckBox{\n"
"    border-radius: 5px;\n"
"}\n"
"QRadioButton {\n"
"    font-weight: normal;\n"
"}\n"
"\n"
"QLineEdit{\n"
"    border-radius: 5px;\n"
"    background: #F1F1F1;\n"
"    color: black;\n"
"}\n"
"\n"
"QPushButton{\n"
"    color:white;\n"
"    border-color: black;\n"
"    border: 2px solid #F1F1F1;\n"
"    border-radius: 11px;\n"
"    font-weight: bold;\n"
"    padding: 5px;\n"
"}\n"
"#temperature_control_widget QPushButton {\n"
"    background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.20398 rgba(221, 124, 40, 180), stop:1 rgba(0, 0, 0, 255))\n"
"}\n"
"\n"
"#ruby_control_widget QPushButton {\n"
"    background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.20398 rgba(197, 0, 3, 255), stop:1 rgba(0, 0, 0, 255))\n"
"}\n"
"\n"
"#diamond_control_widget QPushButton{\n"
"    background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.20398 rgba(27, 0, 134, 255), stop:1 rgba(0, 0, 0, 255))\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"    border:2px solid #fff;\n"
"    margin: 0.5px;\n"
"}\n"
"\n"
"QPushPutton::press{\n"
"   border:2px solid #fff;\n"
"    margin: 2px;\n"
"}\n"
"\n"
"QGroupBox {\n"
"    border: 2px solid #F1F1F1;\n"
"    border-radius: 5px;\n"
"    margin-top: 7px;\n"
"    padding: 0px\n"
"}\n"
"QGroupBox::title {\n"
"     subcontrol-origin: margin;\n"
"     left: 20px\n"
" }\n"
" \n"
"QTabBar::tab {\n"
"    background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.20398 rgba(221, 124, 40, 180), stop:1 #1E1E1E);\n"
"    border: 2px solid  #F1F1F1;\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 10px;\n"
"    padding: 5px;\n"
"    padding-right: 10px;\n"
"    color: #FFF;\n"
"    font-weight: bold;\n"
"    width:85px;\n"
"    margin-left: 7px\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"    border-color: #fff;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"\n"
"    border:3px solid  #FFF;\n"
"    border-bottom-color: #1E1E1E;\n"
"}\n"
"\n"
"QTabBar::tab:!selected {\n"
"    margin-top: 2px;\n"
"}\n"
"\n"
"#downstream_calib_box{\n"
"    color:  rgba(255,255,0,255);\n"
"    border: 2px solid rgba(255,255,0,255);\n"
"}\n"
"#upstream_calib_box {\n"
"    color: rgba(255,140,0,255);\n"
"    border: 2px solid rgba(255,140,0,255);\n"
"}\n"
"\n"
"#upstream_calib_box QPushButton, #downstream_calib_box QPushButton {\n"
"    background:qconicalgradient(cx:0.5, cy:0.5, angle:0, stop:0 rgba(30, 30, 30, 255), stop:1 rgba(60, 60, 64, 255))\n"
"}\n"
""))
        self.verticalLayout_3 = QtGui.QVBoxLayout(temperature_control_widget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.tab_control = QtGui.QTabWidget(temperature_control_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_control.sizePolicy().hasHeightForWidth())
        self.tab_control.setSizePolicy(sizePolicy)
        self.tab_control.setMinimumSize(QtCore.QSize(255, 0))
        self.tab_control.setMaximumSize(QtCore.QSize(255, 16777215))
        self.tab_control.setObjectName(_fromUtf8("tab_control"))
        self.experiment_tab = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.experiment_tab.sizePolicy().hasHeightForWidth())
        self.experiment_tab.setSizePolicy(sizePolicy)
        self.experiment_tab.setObjectName(_fromUtf8("experiment_tab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.experiment_tab)
        self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(self.experiment_tab)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_5.setContentsMargins(11, -1, -1, 11)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.load_exp_data_btn = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_exp_data_btn.sizePolicy().hasHeightForWidth())
        self.load_exp_data_btn.setSizePolicy(sizePolicy)
        self.load_exp_data_btn.setMinimumSize(QtCore.QSize(90, 0))
        self.load_exp_data_btn.setObjectName(_fromUtf8("load_exp_data_btn"))
        self.gridLayout.addWidget(self.load_exp_data_btn, 0, 0, 1, 1)
        self.exp_filename_lbl = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exp_filename_lbl.sizePolicy().hasHeightForWidth())
        self.exp_filename_lbl.setSizePolicy(sizePolicy)
        self.exp_filename_lbl.setObjectName(_fromUtf8("exp_filename_lbl"))
        self.gridLayout.addWidget(self.exp_filename_lbl, 0, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.load_previous_exp_data_btn = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_previous_exp_data_btn.sizePolicy().hasHeightForWidth())
        self.load_previous_exp_data_btn.setSizePolicy(sizePolicy)
        self.load_previous_exp_data_btn.setMaximumSize(QtCore.QSize(40, 24))
        self.load_previous_exp_data_btn.setObjectName(_fromUtf8("load_previous_exp_data_btn"))
        self.horizontalLayout.addWidget(self.load_previous_exp_data_btn)
        self.load_next_exp_data_btn = QtGui.QPushButton(self.groupBox)
        self.load_next_exp_data_btn.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_next_exp_data_btn.sizePolicy().hasHeightForWidth())
        self.load_next_exp_data_btn.setSizePolicy(sizePolicy)
        self.load_next_exp_data_btn.setMaximumSize(QtCore.QSize(40, 24))
        self.load_next_exp_data_btn.setObjectName(_fromUtf8("load_next_exp_data_btn"))
        self.horizontalLayout.addWidget(self.load_next_exp_data_btn)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.exp_folder_name_lbl = QtGui.QLabel(self.groupBox)
        self.exp_folder_name_lbl.setObjectName(_fromUtf8("exp_folder_name_lbl"))
        self.gridLayout.addWidget(self.exp_folder_name_lbl, 2, 0, 1, 2)
        self.auto_process_cb = QtGui.QCheckBox(self.groupBox)
        self.auto_process_cb.setObjectName(_fromUtf8("auto_process_cb"))
        self.gridLayout.addWidget(self.auto_process_cb, 1, 1, 1, 1)
        self.horizontalLayout_5.addLayout(self.gridLayout)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.roi_setup_btn = QtGui.QPushButton(self.experiment_tab)
        self.roi_setup_btn.setObjectName(_fromUtf8("roi_setup_btn"))
        self.verticalLayout_2.addWidget(self.roi_setup_btn)
        self.groupBox_2 = QtGui.QGroupBox(self.experiment_tab)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_3.addWidget(self.label_4, 0, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit.setSizeIncrement(QtCore.QSize(0, 0))
        self.lineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.lineEdit_2 = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        self.label = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.tab_control.addTab(self.experiment_tab, _fromUtf8(""))
        self.calibration_tab = QtGui.QWidget()
        self.calibration_tab.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.calibration_tab.setObjectName(_fromUtf8("calibration_tab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.calibration_tab)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.upstream_calib_box = QtGui.QGroupBox(self.calibration_tab)
        self.upstream_calib_box.setObjectName(_fromUtf8("upstream_calib_box"))
        self.gridLayout_6 = QtGui.QGridLayout(self.upstream_calib_box)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.line_2 = QtGui.QFrame(self.upstream_calib_box)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout_6.addWidget(self.line_2, 1, 0, 1, 2)
        self.us_calib_filename_lbl = QtGui.QLabel(self.upstream_calib_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.us_calib_filename_lbl.sizePolicy().hasHeightForWidth())
        self.us_calib_filename_lbl.setSizePolicy(sizePolicy)
        self.us_calib_filename_lbl.setObjectName(_fromUtf8("us_calib_filename_lbl"))
        self.gridLayout_6.addWidget(self.us_calib_filename_lbl, 0, 1, 1, 2)
        self.pushButton_7 = QtGui.QPushButton(self.upstream_calib_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy)
        self.pushButton_7.setMinimumSize(QtCore.QSize(90, 0))
        self.pushButton_7.setMaximumSize(QtCore.QSize(90, 16777215))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.gridLayout_6.addWidget(self.pushButton_7, 0, 0, 1, 1)
        self.radioButton_3 = QtGui.QRadioButton(self.upstream_calib_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButton_3.sizePolicy().hasHeightForWidth())
        self.radioButton_3.setSizePolicy(sizePolicy)
        self.radioButton_3.setObjectName(_fromUtf8("radioButton_3"))
        self.gridLayout_6.addWidget(self.radioButton_3, 2, 1, 1, 2)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.lineEdit_4 = QtGui.QLineEdit(self.upstream_calib_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy)
        self.lineEdit_4.setMinimumSize(QtCore.QSize(70, 0))
        self.lineEdit_4.setMaximumSize(QtCore.QSize(70, 16777215))
        self.lineEdit_4.setStyleSheet(_fromUtf8("background-color:white"))
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.horizontalLayout_8.addWidget(self.lineEdit_4)
        self.label_12 = QtGui.QLabel(self.upstream_calib_box)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.horizontalLayout_8.addWidget(self.label_12)
        self.gridLayout_6.addLayout(self.horizontalLayout_8, 2, 0, 1, 1)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        spacerItem1 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem1)
        self.pushButton_8 = QtGui.QPushButton(self.upstream_calib_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy)
        self.pushButton_8.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButton_8.setMaximumSize(QtCore.QSize(50, 50))
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.horizontalLayout_9.addWidget(self.pushButton_8)
        self.gridLayout_6.addLayout(self.horizontalLayout_9, 3, 0, 1, 1)
        self.radioButton_4 = QtGui.QRadioButton(self.upstream_calib_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButton_4.sizePolicy().hasHeightForWidth())
        self.radioButton_4.setSizePolicy(sizePolicy)
        self.radioButton_4.setMinimumSize(QtCore.QSize(130, 0))
        self.radioButton_4.setObjectName(_fromUtf8("radioButton_4"))
        self.gridLayout_6.addWidget(self.radioButton_4, 3, 1, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem2, 4, 0, 1, 1)
        self.label_13 = QtGui.QLabel(self.upstream_calib_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_6.addWidget(self.label_13, 4, 1, 1, 1)
        self.verticalLayout.addWidget(self.upstream_calib_box)
        self.downstream_calib_box = QtGui.QGroupBox(self.calibration_tab)
        self.downstream_calib_box.setAutoFillBackground(False)
        self.downstream_calib_box.setObjectName(_fromUtf8("downstream_calib_box"))
        self.gridLayout_5 = QtGui.QGridLayout(self.downstream_calib_box)
        self.gridLayout_5.setMargin(11)
        self.gridLayout_5.setHorizontalSpacing(7)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.pushButton_5 = QtGui.QPushButton(self.downstream_calib_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)
        self.pushButton_5.setMinimumSize(QtCore.QSize(90, 0))
        self.pushButton_5.setMaximumSize(QtCore.QSize(90, 16777215))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.gridLayout_5.addWidget(self.pushButton_5, 0, 0, 1, 1)
        self.ds_calib_filename_lbl = QtGui.QLabel(self.downstream_calib_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ds_calib_filename_lbl.sizePolicy().hasHeightForWidth())
        self.ds_calib_filename_lbl.setSizePolicy(sizePolicy)
        self.ds_calib_filename_lbl.setObjectName(_fromUtf8("ds_calib_filename_lbl"))
        self.gridLayout_5.addWidget(self.ds_calib_filename_lbl, 0, 1, 1, 2)
        self.line = QtGui.QFrame(self.downstream_calib_box)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_5.addWidget(self.line, 1, 0, 1, 2)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.lineEdit_3 = QtGui.QLineEdit(self.downstream_calib_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(70, 0))
        self.lineEdit_3.setMaximumSize(QtCore.QSize(70, 16777215))
        self.lineEdit_3.setStyleSheet(_fromUtf8("background-color: white"))
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.horizontalLayout_6.addWidget(self.lineEdit_3)
        self.label_9 = QtGui.QLabel(self.downstream_calib_box)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_6.addWidget(self.label_9)
        self.gridLayout_5.addLayout(self.horizontalLayout_6, 2, 0, 1, 1)
        self.radioButton = QtGui.QRadioButton(self.downstream_calib_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButton.sizePolicy().hasHeightForWidth())
        self.radioButton.setSizePolicy(sizePolicy)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.gridLayout_5.addWidget(self.radioButton, 2, 1, 1, 2)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem3)
        self.pushButton_6 = QtGui.QPushButton(self.downstream_calib_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        self.pushButton_6.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButton_6.setMaximumSize(QtCore.QSize(50, 50))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.horizontalLayout_7.addWidget(self.pushButton_6)
        self.gridLayout_5.addLayout(self.horizontalLayout_7, 3, 0, 1, 1)
        self.radioButton_2 = QtGui.QRadioButton(self.downstream_calib_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButton_2.sizePolicy().hasHeightForWidth())
        self.radioButton_2.setSizePolicy(sizePolicy)
        self.radioButton_2.setMinimumSize(QtCore.QSize(130, 0))
        self.radioButton_2.setBaseSize(QtCore.QSize(500, 20))
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.gridLayout_5.addWidget(self.radioButton_2, 3, 1, 1, 2)
        spacerItem4 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem4, 4, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.downstream_calib_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_5.addWidget(self.label_10, 4, 1, 1, 1)
        self.verticalLayout.addWidget(self.downstream_calib_box)
        spacerItem5 = QtGui.QSpacerItem(20, 58, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.tab_control.addTab(self.calibration_tab, _fromUtf8(""))
        self.verticalLayout_3.addWidget(self.tab_control)

        self.retranslateUi(temperature_control_widget)
        self.tab_control.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(temperature_control_widget)

    def retranslateUi(self, temperature_control_widget):
        temperature_control_widget.setWindowTitle(_translate("temperature_control_widget", "Form", None))
        self.groupBox.setTitle(_translate("temperature_control_widget", "Experiment", None))
        self.load_exp_data_btn.setText(_translate("temperature_control_widget", "Load Data", None))
        self.exp_filename_lbl.setText(_translate("temperature_control_widget", "Pt_30.spe", None))
        self.load_previous_exp_data_btn.setText(_translate("temperature_control_widget", "<--", None))
        self.load_next_exp_data_btn.setText(_translate("temperature_control_widget", "-->", None))
        self.exp_folder_name_lbl.setText(_translate("temperature_control_widget", "TextLabel", None))
        self.auto_process_cb.setText(_translate("temperature_control_widget", "autoprocess", None))
        self.roi_setup_btn.setText(_translate("temperature_control_widget", "ROI Setup", None))
        self.groupBox_2.setTitle(_translate("temperature_control_widget", "Fitting Parameters", None))
        self.label_3.setText(_translate("temperature_control_widget", "From", None))
        self.label_4.setText(_translate("temperature_control_widget", "To", None))
        self.label_2.setText(_translate("temperature_control_widget", "nm", None))
        self.label.setText(_translate("temperature_control_widget", "nm", None))
        self.tab_control.setTabText(self.tab_control.indexOf(self.experiment_tab), _translate("temperature_control_widget", "Experiment", None))
        self.upstream_calib_box.setTitle(_translate("temperature_control_widget", "Upstream", None))
        self.us_calib_filename_lbl.setText(_translate("temperature_control_widget", "up_15.SPE", None))
        self.pushButton_7.setText(_translate("temperature_control_widget", "Load Data", None))
        self.radioButton_3.setText(_translate("temperature_control_widget", "Temperature", None))
        self.lineEdit_4.setText(_translate("temperature_control_widget", "2000", None))
        self.label_12.setText(_translate("temperature_control_widget", "K", None))
        self.pushButton_8.setText(_translate("temperature_control_widget", "...", None))
        self.radioButton_4.setText(_translate("temperature_control_widget", "Etalon Spectrum", None))
        self.label_13.setText(_translate("temperature_control_widget", "15A Lamp", None))
        self.downstream_calib_box.setTitle(_translate("temperature_control_widget", "Downstream", None))
        self.pushButton_5.setText(_translate("temperature_control_widget", "Load Data", None))
        self.ds_calib_filename_lbl.setText(_translate("temperature_control_widget", "up_15.SPE", None))
        self.lineEdit_3.setText(_translate("temperature_control_widget", "2000", None))
        self.label_9.setText(_translate("temperature_control_widget", "K", None))
        self.radioButton.setText(_translate("temperature_control_widget", "Temperature", None))
        self.pushButton_6.setText(_translate("temperature_control_widget", "...", None))
        self.radioButton_2.setText(_translate("temperature_control_widget", "Etalon Spectrum", None))
        self.label_10.setText(_translate("temperature_control_widget", "15A Lamp", None))
        self.tab_control.setTabText(self.tab_control.indexOf(self.calibration_tab), _translate("temperature_control_widget", "Calibration", None))

