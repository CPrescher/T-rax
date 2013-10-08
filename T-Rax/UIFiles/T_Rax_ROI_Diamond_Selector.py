# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'T_Rax_ROI_Diamond_Selector.ui'
#
# Created: Tue Oct 08 10:28:47 2013
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

class Ui_roi_selector_diamond_widget(object):
    def setupUi(self, roi_selector_diamond_widget):
        roi_selector_diamond_widget.setObjectName(_fromUtf8("roi_selector_diamond_widget"))
        roi_selector_diamond_widget.resize(945, 484)
        roi_selector_diamond_widget.setStyleSheet(_fromUtf8("#roi_selector_diamond_widget{\n"
"    background: #1E1E1E;    \n"
"}\n"
"\n"
"QLabel ,QGroupBox{\n"
"    color: #F1F1F1;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QLineEdit{\n"
"    border-radius:5px;\n"
"    background: #F1F1F1;\n"
"    color: black;\n"
"}\n"
"\n"
"QPushButton{\n"
"    color:white;\n"
"    border-color: black;\n"
"    border: 1px solid #F1F1F1;\n"
"    border-radius: 11px;\n"
"    font-weight: bold;\n"
"    padding: 5px;\n"
"    background:qconicalgradient(cx:0.5, cy:0.5, angle:0, stop:0 rgba(30, 30, 30, 255), stop:1 rgba(60, 60, 64, 255))\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"    border:1px solid #fff;\n"
"    margin: 0.5px;\n"
"}\n"
"\n"
"QPushPutton::pressed{\n"
"   border:1px solid #fff;\n"
"    margin: 2px;\n"
"}\n"
"\n"
"QGroupBox {\n"
"    border: 1px solid #F1F1F1;\n"
"    border-radius: 5px;\n"
"    margin-top: 7px;\n"
"    padding: 0px\n"
"}\n"
"QGroupBox::title {\n"
"     subcontrol-origin: margin;\n"
"     left: 20px;\n"
"}\n"
"\n"
"#roi_box{\n"
"    color: rgba(0, 127, 255, 255);\n"
"    border: 1px solid rgba(0, 127, 255, 255);\n"
"}\n"
""))
        self.horizontalLayout = QtGui.QHBoxLayout(roi_selector_diamond_widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.axes_frame = QtGui.QFrame(roi_selector_diamond_widget)
        self.axes_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.axes_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.axes_frame.setObjectName(_fromUtf8("axes_frame"))
        self.horizontalLayout.addWidget(self.axes_frame)
        self.frame = QtGui.QFrame(roi_selector_diamond_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.roi_box = QtGui.QGroupBox(self.frame)
        self.roi_box.setMinimumSize(QtCore.QSize(180, 0))
        self.roi_box.setMaximumSize(QtCore.QSize(180, 16777215))
        self.roi_box.setObjectName(_fromUtf8("roi_box"))
        self.verticalLayout = QtGui.QVBoxLayout(self.roi_box)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(self.roi_box)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.x_min_txt = QtGui.QLineEdit(self.roi_box)
        self.x_min_txt.setMinimumSize(QtCore.QSize(60, 22))
        self.x_min_txt.setMaximumSize(QtCore.QSize(60, 16777215))
        self.x_min_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.x_min_txt.setObjectName(_fromUtf8("x_min_txt"))
        self.gridLayout.addWidget(self.x_min_txt, 0, 1, 1, 1)
        self.x_max_txt = QtGui.QLineEdit(self.roi_box)
        self.x_max_txt.setMinimumSize(QtCore.QSize(60, 22))
        self.x_max_txt.setMaximumSize(QtCore.QSize(60, 16777215))
        self.x_max_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.x_max_txt.setObjectName(_fromUtf8("x_max_txt"))
        self.gridLayout.addWidget(self.x_max_txt, 0, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.roi_box)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.y_min_txt = QtGui.QLineEdit(self.roi_box)
        self.y_min_txt.setMinimumSize(QtCore.QSize(60, 22))
        self.y_min_txt.setMaximumSize(QtCore.QSize(60, 16777215))
        self.y_min_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.y_min_txt.setObjectName(_fromUtf8("y_min_txt"))
        self.gridLayout.addWidget(self.y_min_txt, 1, 1, 1, 1)
        self.y_max_txt = QtGui.QLineEdit(self.roi_box)
        self.y_max_txt.setMinimumSize(QtCore.QSize(60, 22))
        self.y_max_txt.setMaximumSize(QtCore.QSize(60, 16777215))
        self.y_max_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.y_max_txt.setObjectName(_fromUtf8("y_max_txt"))
        self.gridLayout.addWidget(self.y_max_txt, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout_3.addWidget(self.roi_box)
        self.frame_2 = QtGui.QFrame(self.frame)
        self.frame_2.setMinimumSize(QtCore.QSize(180, 0))
        self.frame_2.setMaximumSize(QtCore.QSize(180, 16777215))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.save_btn = QtGui.QPushButton(self.frame_2)
        self.save_btn.setMaximumSize(QtCore.QSize(80, 16777215))
        self.save_btn.setObjectName(_fromUtf8("save_btn"))
        self.horizontalLayout_5.addWidget(self.save_btn)
        self.cancel_btn = QtGui.QPushButton(self.frame_2)
        self.cancel_btn.setMaximumSize(QtCore.QSize(80, 16777215))
        self.cancel_btn.setObjectName(_fromUtf8("cancel_btn"))
        self.horizontalLayout_5.addWidget(self.cancel_btn)
        self.verticalLayout_3.addWidget(self.frame_2)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(roi_selector_diamond_widget)
        QtCore.QMetaObject.connectSlotsByName(roi_selector_diamond_widget)

    def retranslateUi(self, roi_selector_diamond_widget):
        roi_selector_diamond_widget.setWindowTitle(_translate("roi_selector_diamond_widget", "Form", None))
        self.roi_box.setTitle(_translate("roi_selector_diamond_widget", "ROI Limits", None))
        self.label_3.setText(_translate("roi_selector_diamond_widget", "X:", None))
        self.x_min_txt.setText(_translate("roi_selector_diamond_widget", "5", None))
        self.x_max_txt.setText(_translate("roi_selector_diamond_widget", "100", None))
        self.label_4.setText(_translate("roi_selector_diamond_widget", "Y:", None))
        self.y_min_txt.setText(_translate("roi_selector_diamond_widget", "20", None))
        self.y_max_txt.setText(_translate("roi_selector_diamond_widget", "30", None))
        self.save_btn.setText(_translate("roi_selector_diamond_widget", "Save", None))
        self.cancel_btn.setText(_translate("roi_selector_diamond_widget", "Cancel", None))

