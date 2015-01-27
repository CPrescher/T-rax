# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'T_Rax_MainWindow.ui'
#
# Created: Wed Jul  9 08:08:07 2014
#      by: PyQt4 UI code generator 4.10.4
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
        T_Rax_MainWindow.resize(888, 654)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(T_Rax_MainWindow.sizePolicy().hasHeightForWidth())
        T_Rax_MainWindow.setSizePolicy(sizePolicy)
        T_Rax_MainWindow.setMinimumSize(QtCore.QSize(850, 530))
        T_Rax_MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        T_Rax_MainWindow.setStyleSheet(_fromUtf8("QTabWidget, QTabWidget::tab-bar,  QTabWidget::panel, QWidget{  \n"
"     background: rgba(30, 30, 30, 255);      \n"
" }  \n"
"   \n"
" QLabel , QCheckBox, QGroupBox, QRadioButton, QComboBox  {  \n"
"    background: rgba(0,0,0,0);\n"
"     color: #F1F1F1;  \n"
" }  \n"
"\n"
"\n"
"QTabWidget::tab-bar{ \n"
"    alignment: center;\n"
"}\n"
"\n"
"QWidget{\n"
"    color: #F1F1F1;\n"
"}\n"
"\n"
"\n"
"QTabBar::tab:left, QTabBar::tab:right {  \n"
"     background: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 rgba(30, 30, 30, 255), stop:1 #505050);\n"
"     border: 1px solid  #5B5B5B;  \n"
"    font: normal 14px;\n"
"    color: #F1F1F1;\n"
"     border-radius:2px;\n"
"    \n"
"    padding: 0px;\n"
"     width: 20px;  \n"
"    min-height:140px;\n"
" }  \n"
"\n"
"\n"
"QTabBar::tab::top, QTabBar::tab::bottom {  \n"
"     background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(30, 30, 30, 255), stop:1 #505050);\n"
"     border: 1px solid  #5B5B5B;  \n"
"    border-right: 0px solid white;\n"
"      color: #F1F1F1; \n"
"    font: normal 11px;\n"
"     border-radius:2px;\n"
"     min-width: 80px;  \n"
"    height: 19px;\n"
"    padding: 0px;\n"
"     margin-top: 1px ;\n"
"    margin-right: 1px;\n"
" }  \n"
"QTabBar::tab::left:last, QTabBar::tab::right:last{\n"
"    border-bottom-left-radius: 2px;\n"
"    border-bottom-right-radius: 2px;\n"
"}\n"
"QTabBar::tab:left:first, QTabBar::tab:right:first{\n"
"    border-top-left-radius: 2px;\n"
"    border-top-right-radius: 2px;\n"
"}\n"
"\n"
"QTabWidget, QTabWidget::tab-bar,  QTabWidget::panel, QWidget{  \n"
"     background: rgba(30, 30, 30, 255);      \n"
" }  \n"
"\n"
"QTabWidget::tab-bar {\n"
"    alignment: center;\n"
"}\n"
"\n"
" QTabBar::tab:hover {  \n"
"     border: 1px solid #ADADAD;  \n"
" }  \n"
"   \n"
" QTabBar:tab:selected{  \n"
"\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 1, \n"
"        x2: 0, y2: 0,\n"
"        stop: 0 #727272, \n"
"        stop: 1 #444444\n"
"    );\n"
"     border:1px solid  rgb(255, 120,00);/*#ADADAD; */ \n"
"}\n"
"\n"
"QTabBar::tab:bottom:last, QTabBar::tab:top:last{\n"
"    border-top-right-radius: 2px;\n"
"    border-bottom-right-radius: 2px;\n"
"}\n"
"QTabBar::tab:bottom:first, QTabBar::tab:top:first{\n"
"    border-top-left-radius: 2px;\n"
"    border-bottom-left-radius: 2px;\n"
"}\n"
" QTabBar::tab:top:!selected {  \n"
"    margin-top: 1px;\n"
"    padding-top:1px;\n"
" }  \n"
"QTabBar::tab:bottom:!selected{\n"
"    margin-bottom: 1px;\n"
"    padding-bottom:1px;\n"
"}\n"
"\n"
"QGraphicsView {\n"
"    border-style: none;\n"
"}\n"
"\n"
" QLabel , QCheckBox, QGroupBox, QRadioButton, QListWidget::item, QPushButton, QToolBox::tab, QSpinBox, QDoubleSpinBox , QComboBox{  \n"
"     color: #F1F1F1; \n"
"    font-size: 12px;\n"
" }  \n"
" QCheckBox{  \n"
"     border-radius: 5px;  \n"
" }  \n"
" QRadioButton, QCheckBox {  \n"
"     font-weight: normal;  \n"
"    height: 15px;\n"
" }  \n"
" \n"
" QLineEdit  {  \n"
"     border-radius: 2px;  \n"
"     background: #F1F1F1;  \n"
"     color: black;  \n"
"    height: 18 px;\n"
" }  \n"
"\n"
"QLineEdit::focus{\n"
"    border-style: none;\n"
"     border-radius: 2px;  \n"
"     background: #F1F1F1;  \n"
"     color: black;  \n"
"}\n"
"QSpinBox, QDoubleSpinBox {\n"
"    background-color:  #F1F1F1; \n"
"    color: black;\n"
"    margin-left: -15px;\n"
"    margin-right: -2px;\n"
"    height: 30px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item { \n"
"    min-height: 40px; \n"
"    min-width: 60px; \n"
"}\n"
"QComboBox QAbstractItemView{\n"
"    background: rgba(35, 35, 35, 255);\n"
"    color: #F1F1F1;\n"
"    min-height: 50px;\n"
"    selection-background-color: rgba(221, 124, 40, 120);\n"
"    border-radius: 5px;\n"
"\n"
"}\n"
"\n"
"QComboBox:!editable {\n"
"    margin-left: 1px;\n"
"    padding-left: 10px;\n"
"    height: 23px;\n"
"    background-color: rgba(35, 35, 35, 255);\n"
"}\n"
"\n"
"QComboBox::item{\n"
"    background-color: rgba(35, 35, 35, 255);\n"
"}\n"
"\n"
"QComboBox::item::selected {\n"
"    background-color: #505050;\n"
"}\n"
"\n"
"\n"
"QToolBox::tab:QToolButton{\n"
"    background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(30, 30, 30, 255), stop:1 #505050);\n"
"     border: 1px solid  #5B5B5B;  \n"
"\n"
"     border-radius:2px;\n"
"     padding-right: 10px;  \n"
"    \n"
"      color: #F1F1F1; \n"
"    font-size: 12px;\n"
"    padding: 3px;\n"
"}\n"
"QToolBox::tab:QToolButton{\n"
"    background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(30, 30, 30, 255), stop:1 #505050);\n"
"     border: 1px solid  #5B5B5B;  \n"
"\n"
"     border-radius:2px;\n"
"     padding-right: 10px;  \n"
"    \n"
"      color: #F1F1F1; \n"
"    font-size: 12px;\n"
"    padding: 3px;\n"
"}\n"
"  \n"
"QPushButton{  \n"
"     color: #F1F1F1;\n"
"     background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop:1 #505050);\n"
"     border: 1px solid #5B5B5B;\n"
"     border-radius: 5px; \n"
"     padding-left: 8px;\n"
"height: 18px;\n"
"    padding-right: 8px;   \n"
" }  \n"
"QPushButton:pressed{\n"
"        margin-top: 2,px;\n"
"        margin-left: 2px;   \n"
"}\n"
"QPushButton::disabled{\n"
"}\n"
"\n"
"QPushButton::hover{  \n"
"     border:1px solid #ADADAD; \n"
" }  \n"
" \n"
"\n"
"QPushButton::checked{\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 1, \n"
"        x2: 0, y2: 0,\n"
"        stop: 0 #727272, \n"
"        stop: 1 #444444\n"
"    );\n"
"     border:1px solid  rgb(255, 120,00);\n"
"}\n"
"\n"
"QPushButton::focus {\n"
"    outline: None;\n"
"}\n"
" QGroupBox {  \n"
"     border: 1px solid #ADADAD;  \n"
"     border-radius: 4px;  \n"
"     margin-top: 7px;\n"
"     padding: 0px  \n"
" }  \n"
" QGroupBox::title {  \n"
"      subcontrol-origin: margin;  \n"
"      left: 20px  \n"
"  }\n"
"\n"
"QSplitter::handle:hover {\n"
"    background: rgba(30, 30, 30, 255);\n"
" }\n"
"\n"
"\n"
"QGraphicsView{\n"
"    border-style: none;\n"
"}\n"
"\n"
" QScrollBar:vertical {\n"
"      border: 2px solid rgba(30, 30, 30, 255);\n"
"      background: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 #323232, stop:1 #505050);\n"
"      width: 12px;\n"
"      margin: 0px 0px 0px 0px;\n"
"  }\n"
"  QScrollBar::handle:vertical {\n"
"      background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #969696, stop:1 #CACACA);\n"
"     border-radius: 3px;\n"
"      min-height: 20px;\n"
"    padding: 15px;\n"
"  }\n"
"  QScrollBar::add-line:vertical {\n"
"      border: 0px solid grey;\n"
"      height: 0px;\n"
"  }\n"
"\n"
"  QScrollBar::sub-line:vertical {\n"
"      border: 0px solid grey;\n"
"      height: 0px;\n"
"  }\n"
"  QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"      background: none;\n"
"  }\n"
"\n"
"\n"
"\n"
"#navigation_frame {\n"
"    border: none;\n"
"    background: qlineargradient(spread:reflect, x1:0, y1:0.5, x2:0, y2:0, stop:0.114428 rgba(21, 134, 31, 255), stop:0.467662 rgba(12, 80, 18, 255), \n"
"    stop:0.726368 rgba(9, 60, 13, 255), stop:1 rgba(0, 0, 0, 255))\n"
"}\n"
"\n"
"\n"
"\n"
"#navigation_frame QPushButton{\n"
"    min-width: 104px;\n"
"    min-height: 20px;\n"
"    font-size: 12px;\n"
"    padding: 2px;\n"
"    font-weight: bold;\n"
"    border-radius: 10px;\n"
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
""))
        T_Rax_MainWindow.setAnimated(False)
        self.centralwidget = QtGui.QWidget(T_Rax_MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.navigation_frame = QtGui.QFrame(self.centralwidget)
        self.navigation_frame.setMinimumSize(QtCore.QSize(0, 60))
        self.navigation_frame.setMaximumSize(QtCore.QSize(16777215, 100))
        self.navigation_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.navigation_frame.setFrameShadow(QtGui.QFrame.Plain)
        self.navigation_frame.setLineWidth(0)
        self.navigation_frame.setObjectName(_fromUtf8("navigation_frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.navigation_frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.temperature_btn = QtGui.QPushButton(self.navigation_frame)
        self.temperature_btn.setDefault(False)
        self.temperature_btn.setFlat(True)
        self.temperature_btn.setObjectName(_fromUtf8("temperature_btn"))
        self.horizontalLayout.addWidget(self.temperature_btn)
        self.ruby_btn = QtGui.QPushButton(self.navigation_frame)
        self.ruby_btn.setDefault(False)
        self.ruby_btn.setFlat(True)
        self.ruby_btn.setObjectName(_fromUtf8("ruby_btn"))
        self.horizontalLayout.addWidget(self.ruby_btn)
        self.diamond_btn = QtGui.QPushButton(self.navigation_frame)
        self.diamond_btn.setDefault(False)
        self.diamond_btn.setFlat(True)
        self.diamond_btn.setObjectName(_fromUtf8("diamond_btn"))
        self.horizontalLayout.addWidget(self.diamond_btn)
        self.raman_btn = QtGui.QPushButton(self.navigation_frame)
        self.raman_btn.setDefault(False)
        self.raman_btn.setFlat(True)
        self.raman_btn.setObjectName(_fromUtf8("raman_btn"))
        self.horizontalLayout.addWidget(self.raman_btn)
        spacerItem = QtGui.QSpacerItem(248, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_2 = QtGui.QLabel(self.navigation_frame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_3.addWidget(self.label_2)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout.addWidget(self.navigation_frame)
        self.axes_frame = QtGui.QFrame(self.centralwidget)
        self.axes_frame.setStyleSheet(_fromUtf8(""))
        self.axes_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.axes_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.axes_frame.setObjectName(_fromUtf8("axes_frame"))
        self.verticalLayout.addWidget(self.axes_frame)
        self.main_frame = QtGui.QFrame(self.centralwidget)
        self.main_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.main_frame.setFrameShadow(QtGui.QFrame.Plain)
        self.main_frame.setLineWidth(0)
        self.main_frame.setObjectName(_fromUtf8("main_frame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.main_frame)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.figure1_frame = QtGui.QFrame(self.main_frame)
        self.figure1_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.figure1_frame.setFrameShadow(QtGui.QFrame.Plain)
        self.figure1_frame.setLineWidth(0)
        self.figure1_frame.setObjectName(_fromUtf8("figure1_frame"))
        self.horizontalLayout_2.addWidget(self.figure1_frame)
        self.figure2_frame = QtGui.QFrame(self.main_frame)
        self.figure2_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.figure2_frame.setFrameShadow(QtGui.QFrame.Plain)
        self.figure2_frame.setLineWidth(0)
        self.figure2_frame.setObjectName(_fromUtf8("figure2_frame"))
        self.horizontalLayout_2.addWidget(self.figure2_frame)
        self.figure3_frame = QtGui.QFrame(self.main_frame)
        self.figure3_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.figure3_frame.setFrameShadow(QtGui.QFrame.Plain)
        self.figure3_frame.setLineWidth(0)
        self.figure3_frame.setObjectName(_fromUtf8("figure3_frame"))
        self.horizontalLayout_2.addWidget(self.figure3_frame)
        self.verticalLayout.addWidget(self.main_frame)
        self.status_bar = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status_bar.sizePolicy().hasHeightForWidth())
        self.status_bar.setSizePolicy(sizePolicy)
        self.status_bar.setMaximumSize(QtCore.QSize(16777215, 25))
        self.status_bar.setFrameShape(QtGui.QFrame.NoFrame)
        self.status_bar.setFrameShadow(QtGui.QFrame.Plain)
        self.status_bar.setLineWidth(0)
        self.status_bar.setObjectName(_fromUtf8("status_bar"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.status_bar)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setContentsMargins(5, 0, 5, 0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.status_coord_lbl = QtGui.QLabel(self.status_bar)
        self.status_coord_lbl.setText(_fromUtf8(""))
        self.status_coord_lbl.setObjectName(_fromUtf8("status_coord_lbl"))
        self.horizontalLayout_3.addWidget(self.status_coord_lbl)
        self.progress_bar = QtGui.QProgressBar(self.status_bar)
        self.progress_bar.setMinimumSize(QtCore.QSize(0, 20))
        self.progress_bar.setMaximumSize(QtCore.QSize(16777215, 18))
        self.progress_bar.setStyleSheet(_fromUtf8("color: white"))
        self.progress_bar.setProperty("value", 24)
        self.progress_bar.setObjectName(_fromUtf8("progress_bar"))
        self.horizontalLayout_3.addWidget(self.progress_bar)
        spacerItem2 = QtGui.QSpacerItem(743, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.status_file_information_lbl = QtGui.QLabel(self.status_bar)
        self.status_file_information_lbl.setText(_fromUtf8(""))
        self.status_file_information_lbl.setObjectName(_fromUtf8("status_file_information_lbl"))
        self.horizontalLayout_3.addWidget(self.status_file_information_lbl)
        self.verticalLayout.addWidget(self.status_bar)
        T_Rax_MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(T_Rax_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(T_Rax_MainWindow)

    def retranslateUi(self, T_Rax_MainWindow):
        T_Rax_MainWindow.setWindowTitle(_translate("T_Rax_MainWindow", "T-Rax ver 0.203", None))
        self.temperature_btn.setText(_translate("T_Rax_MainWindow", "Temperature", None))
        self.ruby_btn.setText(_translate("T_Rax_MainWindow", "Ruby", None))
        self.diamond_btn.setText(_translate("T_Rax_MainWindow", "Diamond", None))
        self.raman_btn.setText(_translate("T_Rax_MainWindow", "Raman", None))
        self.label_2.setText(_translate("T_Rax_MainWindow", "written by C. Prescher, GSECARS, UofC", None))

