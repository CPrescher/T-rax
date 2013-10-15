# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'T_Rax_OutputGraphWidget.ui'
#
# Created: Tue Oct 15 08:38:01 2013
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

class Ui_output_graph_widget(object):
    def setupUi(self, output_graph_widget):
        output_graph_widget.setObjectName(_fromUtf8("output_graph_widget"))
        output_graph_widget.resize(1014, 634)
        self.horizontalLayout = QtGui.QHBoxLayout(output_graph_widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.graph_frame = QtGui.QFrame(output_graph_widget)
        self.graph_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.graph_frame.setFrameShadow(QtGui.QFrame.Plain)
        self.graph_frame.setObjectName(_fromUtf8("graph_frame"))
        self.horizontalLayout.addWidget(self.graph_frame)

        self.retranslateUi(output_graph_widget)
        QtCore.QMetaObject.connectSlotsByName(output_graph_widget)

    def retranslateUi(self, output_graph_widget):
        output_graph_widget.setWindowTitle(_translate("output_graph_widget", "Form", None))

