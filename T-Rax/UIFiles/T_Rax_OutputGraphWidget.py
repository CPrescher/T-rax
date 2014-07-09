# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'T_Rax_OutputGraphWidget.ui'
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

class Ui_output_graph_widget(object):
    def setupUi(self, output_graph_widget):
        output_graph_widget.setObjectName(_fromUtf8("output_graph_widget"))
        output_graph_widget.resize(1014, 585)
        output_graph_widget.setStyleSheet(_fromUtf8(" #output_graph_widget, #information_frame{  \n"
"     background: #1E1E1E;      \n"
" }  \n"
"   \n"
" QLabel  {  \n"
"     color: #F1F1F1;  \n"
"     font: bold 16px;  \n"
" }  \n"
"   \n"
" #ds_lbl{  \n"
"     color:  rgba(255,255,0,255);  \n"
"     font-weight: bold;\n"
" }  \n"
" #us_lbl {  \n"
"     color: rgba(255,140,0,255);  \n"
"     font-weight: bold;\n"
" }  \n"
"  \n"
"#combined_lbl{\n"
"    color: rgba(255, 197,0,255)\n"
"\n"
"}"))
        self.verticalLayout = QtGui.QVBoxLayout(output_graph_widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.information_frame = QtGui.QFrame(output_graph_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.information_frame.sizePolicy().hasHeightForWidth())
        self.information_frame.setSizePolicy(sizePolicy)
        self.information_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.information_frame.setFrameShadow(QtGui.QFrame.Plain)
        self.information_frame.setLineWidth(0)
        self.information_frame.setObjectName(_fromUtf8("information_frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.information_frame)
        self.horizontalLayout.setContentsMargins(5, 12, 5, 0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(93, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.ds_lbl = QtGui.QLabel(self.information_frame)
        self.ds_lbl.setObjectName(_fromUtf8("ds_lbl"))
        self.horizontalLayout.addWidget(self.ds_lbl)
        self.ds_temperature_lbl = QtGui.QLabel(self.information_frame)
        self.ds_temperature_lbl.setObjectName(_fromUtf8("ds_temperature_lbl"))
        self.horizontalLayout.addWidget(self.ds_temperature_lbl)
        spacerItem1 = QtGui.QSpacerItem(95, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.us_lbl = QtGui.QLabel(self.information_frame)
        self.us_lbl.setObjectName(_fromUtf8("us_lbl"))
        self.horizontalLayout.addWidget(self.us_lbl)
        self.us_temperature_lbl = QtGui.QLabel(self.information_frame)
        self.us_temperature_lbl.setObjectName(_fromUtf8("us_temperature_lbl"))
        self.horizontalLayout.addWidget(self.us_temperature_lbl)
        spacerItem2 = QtGui.QSpacerItem(93, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.combined_lbl = QtGui.QLabel(self.information_frame)
        self.combined_lbl.setObjectName(_fromUtf8("combined_lbl"))
        self.horizontalLayout.addWidget(self.combined_lbl)
        self.combined_temperature_lbl = QtGui.QLabel(self.information_frame)
        self.combined_temperature_lbl.setObjectName(_fromUtf8("combined_temperature_lbl"))
        self.horizontalLayout.addWidget(self.combined_temperature_lbl)
        spacerItem3 = QtGui.QSpacerItem(94, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout.addWidget(self.information_frame)
        self.graph_frame = QtGui.QFrame(output_graph_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graph_frame.sizePolicy().hasHeightForWidth())
        self.graph_frame.setSizePolicy(sizePolicy)
        self.graph_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.graph_frame.setFrameShadow(QtGui.QFrame.Plain)
        self.graph_frame.setLineWidth(0)
        self.graph_frame.setObjectName(_fromUtf8("graph_frame"))
        self.verticalLayout.addWidget(self.graph_frame)

        self.retranslateUi(output_graph_widget)
        QtCore.QMetaObject.connectSlotsByName(output_graph_widget)

    def retranslateUi(self, output_graph_widget):
        output_graph_widget.setWindowTitle(_translate("output_graph_widget", "Form", None))
        self.ds_lbl.setText(_translate("output_graph_widget", "Downstream:", None))
        self.ds_temperature_lbl.setText(_translate("output_graph_widget", "1500+-13K", None))
        self.us_lbl.setText(_translate("output_graph_widget", "Upstream:", None))
        self.us_temperature_lbl.setText(_translate("output_graph_widget", "1500+-13K", None))
        self.combined_lbl.setText(_translate("output_graph_widget", "Combined:", None))
        self.combined_temperature_lbl.setText(_translate("output_graph_widget", "1500+-13K", None))

