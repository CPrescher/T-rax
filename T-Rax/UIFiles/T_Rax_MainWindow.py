# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'T_Rax_MainWindow.ui'
#
# Created: Mon Oct 14 23:43:41 2013
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

class Ui_T_Rax_MainWindow(object):
    def setupUi(self, T_Rax_MainWindow):
        T_Rax_MainWindow.setObjectName(_fromUtf8("T_Rax_MainWindow"))
        T_Rax_MainWindow.resize(850, 530)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(T_Rax_MainWindow.sizePolicy().hasHeightForWidth())
        T_Rax_MainWindow.setSizePolicy(sizePolicy)
        T_Rax_MainWindow.setMinimumSize(QtCore.QSize(850, 530))
        T_Rax_MainWindow.setStyleSheet(_fromUtf8("QMainWindow, #T_Rax_MainWindow{\n"
"    background: rgb(44, 43, 43)\n"
"}\n"
"#centralwidget{\n"
"    background: rgb(30, 30, 30)\n"
"}\n"
"#status_bar {\n"
"    background: rgb(44, 43, 43);\n"
"\n"
"}\n"
"\n"
"QLabel ,QGroupBox{\n"
"    color: #F1F1F1;\n"
"    font-weight: bold;\n"
"    font-size: 12px;\n"
"}\n"
"\n"
"\n"
"#navigation_frame {\n"
"    border: none;\n"
"    background: qlineargradient(spread:reflect, x1:0, y1:0.5, x2:0, y2:0, stop:0.114428 rgba(21, 134, 31, 255), stop:0.467662 rgba(12, 80, 18, 255), \n"
"    stop:0.726368 rgba(9, 60, 13, 255), stop:1 rgb(30, 30, 30))\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton{\n"
"    color:white;\n"
"    border-color: black;\n"
"    border: 2px solid #F1F1F1;\n"
"    border-radius: 11px;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"    border:3px solid #fff;\n"
"    margin: 0.5px;\n"
"}\n"
"\n"
"QPushPutton::press{\n"
"   border: 3px solid #fff;\n"
"margin: 2px;\n"
"}\n"
"\n"
"\n"
"#navigation_frame QPushButton{\n"
"    min-width: 104px;\n"
"    min-height: 20px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"#temperature_btn {\n"
"    background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.20398 rgba(221, 124, 40, 180), stop:1 rgba(0, 0, 0, 255))\n"
"}\n"
"#ruby_btn {\n"
"    background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.20398 rgba(197, 0, 3, 255), stop:1 rgba(0, 0, 0, 255))\n"
"}\n"
"\n"
"#diamond_btn {\n"
"    background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.20398 rgba(27, 0, 134, 255), stop:1 rgba(0, 0, 0, 255))\n"
"}\n"
"#raman_btn {\n"
"    background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.20398 rgba(21, 134, 31, 255), stop:1 rgba(0, 0, 0, 255))\n"
"}\n"
"\n"
"#status_ds_calib_filename_lbl{  \n"
"    color: #F1F1F1;  \n"
" }  \n"
" #status_us_calib_filename_lbl{  \n"
"    color: #F1F1F1;\n"
"}"))
        self.centralwidget = QtGui.QWidget(T_Rax_MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.navigation_frame = QtGui.QFrame(self.centralwidget)
        self.navigation_frame.setMinimumSize(QtCore.QSize(0, 60))
        self.navigation_frame.setMaximumSize(QtCore.QSize(16777215, 100))
        self.navigation_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.navigation_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.navigation_frame.setObjectName(_fromUtf8("navigation_frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.navigation_frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.temperature_btn = QtGui.QPushButton(self.navigation_frame)
        self.temperature_btn.setObjectName(_fromUtf8("temperature_btn"))
        self.horizontalLayout.addWidget(self.temperature_btn)
        self.ruby_btn = QtGui.QPushButton(self.navigation_frame)
        self.ruby_btn.setObjectName(_fromUtf8("ruby_btn"))
        self.horizontalLayout.addWidget(self.ruby_btn)
        self.diamond_btn = QtGui.QPushButton(self.navigation_frame)
        self.diamond_btn.setObjectName(_fromUtf8("diamond_btn"))
        self.horizontalLayout.addWidget(self.diamond_btn)
        self.raman_btn = QtGui.QPushButton(self.navigation_frame)
        self.raman_btn.setObjectName(_fromUtf8("raman_btn"))
        self.horizontalLayout.addWidget(self.raman_btn)
        spacerItem = QtGui.QSpacerItem(248, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.navigation_frame)
        self.main_frame = QtGui.QFrame(self.centralwidget)
        self.main_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.main_frame.setObjectName(_fromUtf8("main_frame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.main_frame)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.figure3_frame = QtGui.QFrame(self.main_frame)
        self.figure3_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.figure3_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.figure3_frame.setObjectName(_fromUtf8("figure3_frame"))
        self.horizontalLayout_2.addWidget(self.figure3_frame)
        self.figure1_frame = QtGui.QFrame(self.main_frame)
        self.figure1_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.figure1_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.figure1_frame.setObjectName(_fromUtf8("figure1_frame"))
        self.horizontalLayout_2.addWidget(self.figure1_frame)
        self.figure2_frame = QtGui.QFrame(self.main_frame)
        self.figure2_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.figure2_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.figure2_frame.setObjectName(_fromUtf8("figure2_frame"))
        self.horizontalLayout_2.addWidget(self.figure2_frame)
        self.verticalLayout.addWidget(self.main_frame)
        self.status_bar = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status_bar.sizePolicy().hasHeightForWidth())
        self.status_bar.setSizePolicy(sizePolicy)
        self.status_bar.setMaximumSize(QtCore.QSize(16777215, 25))
        self.status_bar.setFrameShape(QtGui.QFrame.StyledPanel)
        self.status_bar.setFrameShadow(QtGui.QFrame.Raised)
        self.status_bar.setObjectName(_fromUtf8("status_bar"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.status_bar)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setContentsMargins(5, 0, 5, 0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.status_coord_lbl = QtGui.QLabel(self.status_bar)
        self.status_coord_lbl.setText(_fromUtf8(""))
        self.status_coord_lbl.setObjectName(_fromUtf8("status_coord_lbl"))
        self.horizontalLayout_3.addWidget(self.status_coord_lbl)
        spacerItem1 = QtGui.QSpacerItem(743, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.status_file_information_lbl = QtGui.QLabel(self.status_bar)
        self.status_file_information_lbl.setText(_fromUtf8(""))
        self.status_file_information_lbl.setObjectName(_fromUtf8("status_file_information_lbl"))
        self.horizontalLayout_3.addWidget(self.status_file_information_lbl)
        self.verticalLayout.addWidget(self.status_bar)
        T_Rax_MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(T_Rax_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(T_Rax_MainWindow)

    def retranslateUi(self, T_Rax_MainWindow):
        T_Rax_MainWindow.setWindowTitle(_translate("T_Rax_MainWindow", "T-Rax ver 0.2", None))
        self.temperature_btn.setText(_translate("T_Rax_MainWindow", "Temperature", None))
        self.ruby_btn.setText(_translate("T_Rax_MainWindow", "Ruby", None))
        self.diamond_btn.setText(_translate("T_Rax_MainWindow", "Diamond", None))
        self.raman_btn.setText(_translate("T_Rax_MainWindow", "Raman", None))

