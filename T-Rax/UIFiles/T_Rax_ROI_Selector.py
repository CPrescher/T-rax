# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'T_Rax_ROI_Selector.ui'
#
# Created: Sat Sep 28 09:19:18 2013
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

class Ui_roi_selector_main_widget(object):
    def setupUi(self, roi_selector_main_widget):
        roi_selector_main_widget.setObjectName(_fromUtf8("roi_selector_main_widget"))
        roi_selector_main_widget.resize(945, 484)
        roi_selector_main_widget.setStyleSheet(_fromUtf8("#roi_selector_main_widget{\n"
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
"    border: 2px solid #F1F1F1;\n"
"    border-radius: 11px;\n"
"    font-weight: bold;\n"
"    padding: 5px;\n"
"    background:qconicalgradient(cx:0.5, cy:0.5, angle:0, stop:0 rgba(30, 30, 30, 255), stop:1 rgba(60, 60, 64, 255))\n"
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
"     left: 20px;\n"
"}\n"
"\n"
"#upstream_roi_box{\n"
"    color:  rgba(255,255,0,255);\n"
"    border: 2px solid rgba(255,255,0,255);\n"
"}\n"
"#downstream_roi_box {\n"
"    color: rgba(255,140,0,255);\n"
"    border: 2px solid rgba(255,140,0,255);\n"
"}\n"
""))
        self.horizontalLayout = QtGui.QHBoxLayout(roi_selector_main_widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.axes_frame = QtGui.QFrame(roi_selector_main_widget)
        self.axes_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.axes_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.axes_frame.setObjectName(_fromUtf8("axes_frame"))
        self.horizontalLayout.addWidget(self.axes_frame)
        self.frame = QtGui.QFrame(roi_selector_main_widget)
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
        self.upstream_roi_box = QtGui.QGroupBox(self.frame)
        self.upstream_roi_box.setMinimumSize(QtCore.QSize(180, 0))
        self.upstream_roi_box.setMaximumSize(QtCore.QSize(180, 16777215))
        self.upstream_roi_box.setObjectName(_fromUtf8("upstream_roi_box"))
        self.verticalLayout = QtGui.QVBoxLayout(self.upstream_roi_box)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.upstream_roi_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 16))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.upstream_roi_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(60, 16))
        self.label_2.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.upstream_roi_box)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.us_x_min_txt = QtGui.QLineEdit(self.upstream_roi_box)
        self.us_x_min_txt.setMinimumSize(QtCore.QSize(60, 22))
        self.us_x_min_txt.setMaximumSize(QtCore.QSize(60, 16777215))
        self.us_x_min_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.us_x_min_txt.setObjectName(_fromUtf8("us_x_min_txt"))
        self.gridLayout.addWidget(self.us_x_min_txt, 1, 1, 1, 1)
        self.us_x_max_txt = QtGui.QLineEdit(self.upstream_roi_box)
        self.us_x_max_txt.setMinimumSize(QtCore.QSize(60, 22))
        self.us_x_max_txt.setMaximumSize(QtCore.QSize(60, 16777215))
        self.us_x_max_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.us_x_max_txt.setObjectName(_fromUtf8("us_x_max_txt"))
        self.gridLayout.addWidget(self.us_x_max_txt, 1, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.upstream_roi_box)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.us_y_min_txt = QtGui.QLineEdit(self.upstream_roi_box)
        self.us_y_min_txt.setMinimumSize(QtCore.QSize(60, 22))
        self.us_y_min_txt.setMaximumSize(QtCore.QSize(60, 16777215))
        self.us_y_min_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.us_y_min_txt.setObjectName(_fromUtf8("us_y_min_txt"))
        self.gridLayout.addWidget(self.us_y_min_txt, 2, 1, 1, 1)
        self.us_y_max_txt = QtGui.QLineEdit(self.upstream_roi_box)
        self.us_y_max_txt.setMinimumSize(QtCore.QSize(60, 22))
        self.us_y_max_txt.setMaximumSize(QtCore.QSize(60, 16777215))
        self.us_y_max_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.us_y_max_txt.setObjectName(_fromUtf8("us_y_max_txt"))
        self.gridLayout.addWidget(self.us_y_max_txt, 2, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout_3.addWidget(self.upstream_roi_box)
        self.downstream_roi_box = QtGui.QGroupBox(self.frame)
        self.downstream_roi_box.setMinimumSize(QtCore.QSize(180, 0))
        self.downstream_roi_box.setMaximumSize(QtCore.QSize(180, 16777215))
        self.downstream_roi_box.setObjectName(_fromUtf8("downstream_roi_box"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.downstream_roi_box)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_5 = QtGui.QLabel(self.downstream_roi_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(0, 16))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 0, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.downstream_roi_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(60, 16))
        self.label_6.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 0, 2, 1, 1)
        self.label_7 = QtGui.QLabel(self.downstream_roi_box)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 1)
        self.ds_x_min_txt = QtGui.QLineEdit(self.downstream_roi_box)
        self.ds_x_min_txt.setMinimumSize(QtCore.QSize(60, 22))
        self.ds_x_min_txt.setMaximumSize(QtCore.QSize(60, 16777215))
        self.ds_x_min_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ds_x_min_txt.setObjectName(_fromUtf8("ds_x_min_txt"))
        self.gridLayout_2.addWidget(self.ds_x_min_txt, 1, 1, 1, 1)
        self.ds_x_max_txt = QtGui.QLineEdit(self.downstream_roi_box)
        self.ds_x_max_txt.setMinimumSize(QtCore.QSize(60, 22))
        self.ds_x_max_txt.setMaximumSize(QtCore.QSize(60, 16777215))
        self.ds_x_max_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ds_x_max_txt.setObjectName(_fromUtf8("ds_x_max_txt"))
        self.gridLayout_2.addWidget(self.ds_x_max_txt, 1, 2, 1, 1)
        self.label_8 = QtGui.QLabel(self.downstream_roi_box)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 2, 0, 1, 1)
        self.ds_y_min_txt = QtGui.QLineEdit(self.downstream_roi_box)
        self.ds_y_min_txt.setMinimumSize(QtCore.QSize(60, 22))
        self.ds_y_min_txt.setMaximumSize(QtCore.QSize(60, 16777215))
        self.ds_y_min_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ds_y_min_txt.setObjectName(_fromUtf8("ds_y_min_txt"))
        self.gridLayout_2.addWidget(self.ds_y_min_txt, 2, 1, 1, 1)
        self.ds_y_max_txt = QtGui.QLineEdit(self.downstream_roi_box)
        self.ds_y_max_txt.setMinimumSize(QtCore.QSize(60, 22))
        self.ds_y_max_txt.setMaximumSize(QtCore.QSize(60, 16777215))
        self.ds_y_max_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ds_y_max_txt.setObjectName(_fromUtf8("ds_y_max_txt"))
        self.gridLayout_2.addWidget(self.ds_y_max_txt, 2, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.verticalLayout_3.addWidget(self.downstream_roi_box)
        self.fitting_param_roi = QtGui.QGroupBox(self.frame)
        self.fitting_param_roi.setMinimumSize(QtCore.QSize(180, 0))
        self.fitting_param_roi.setMaximumSize(QtCore.QSize(180, 16777215))
        self.fitting_param_roi.setObjectName(_fromUtf8("fitting_param_roi"))
        self.gridLayout_4 = QtGui.QGridLayout(self.fitting_param_roi)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_9 = QtGui.QLabel(self.fitting_param_roi)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_3.addWidget(self.label_9, 0, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.fitting_param_roi)
        self.label_10.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_3.addWidget(self.label_10, 0, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.fit_from_txt = QtGui.QLineEdit(self.fitting_param_roi)
        self.fit_from_txt.setMinimumSize(QtCore.QSize(0, 22))
        self.fit_from_txt.setSizeIncrement(QtCore.QSize(0, 0))
        self.fit_from_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fit_from_txt.setObjectName(_fromUtf8("fit_from_txt"))
        self.horizontalLayout_2.addWidget(self.fit_from_txt)
        self.label_11 = QtGui.QLabel(self.fitting_param_roi)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayout_2.addWidget(self.label_11)
        self.gridLayout_5.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.fit_to_txt = QtGui.QLineEdit(self.fitting_param_roi)
        self.fit_to_txt.setMinimumSize(QtCore.QSize(0, 22))
        self.fit_to_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fit_to_txt.setObjectName(_fromUtf8("fit_to_txt"))
        self.horizontalLayout_3.addWidget(self.fit_to_txt)
        self.label_12 = QtGui.QLabel(self.fitting_param_roi)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.horizontalLayout_3.addWidget(self.label_12)
        self.gridLayout_5.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_5, 1, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.fitting_param_roi)
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

        self.retranslateUi(roi_selector_main_widget)
        QtCore.QMetaObject.connectSlotsByName(roi_selector_main_widget)

    def retranslateUi(self, roi_selector_main_widget):
        roi_selector_main_widget.setWindowTitle(_translate("roi_selector_main_widget", "Form", None))
        self.upstream_roi_box.setTitle(_translate("roi_selector_main_widget", "Upstream ROI", None))
        self.label.setText(_translate("roi_selector_main_widget", "Min", None))
        self.label_2.setText(_translate("roi_selector_main_widget", "Max", None))
        self.label_3.setText(_translate("roi_selector_main_widget", "X:", None))
        self.us_x_min_txt.setText(_translate("roi_selector_main_widget", "5", None))
        self.us_x_max_txt.setText(_translate("roi_selector_main_widget", "100", None))
        self.label_4.setText(_translate("roi_selector_main_widget", "Y:", None))
        self.us_y_min_txt.setText(_translate("roi_selector_main_widget", "20", None))
        self.us_y_max_txt.setText(_translate("roi_selector_main_widget", "30", None))
        self.downstream_roi_box.setTitle(_translate("roi_selector_main_widget", "Downstream ROI", None))
        self.label_5.setText(_translate("roi_selector_main_widget", "Min", None))
        self.label_6.setText(_translate("roi_selector_main_widget", "Max", None))
        self.label_7.setText(_translate("roi_selector_main_widget", "X:", None))
        self.ds_x_min_txt.setText(_translate("roi_selector_main_widget", "5", None))
        self.ds_x_max_txt.setText(_translate("roi_selector_main_widget", "100", None))
        self.label_8.setText(_translate("roi_selector_main_widget", "Y:", None))
        self.ds_y_min_txt.setText(_translate("roi_selector_main_widget", "20", None))
        self.ds_y_max_txt.setText(_translate("roi_selector_main_widget", "30", None))
        self.fitting_param_roi.setTitle(_translate("roi_selector_main_widget", "Fitting Parameters", None))
        self.label_9.setText(_translate("roi_selector_main_widget", "From", None))
        self.label_10.setText(_translate("roi_selector_main_widget", "To", None))
        self.label_11.setText(_translate("roi_selector_main_widget", "nm", None))
        self.label_12.setText(_translate("roi_selector_main_widget", "nm", None))
        self.save_btn.setText(_translate("roi_selector_main_widget", "Save", None))
        self.cancel_btn.setText(_translate("roi_selector_main_widget", "Cancel", None))

