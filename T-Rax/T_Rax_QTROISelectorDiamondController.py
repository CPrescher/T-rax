from PyQt4.QtCore import SIGNAL
from PyQt4 import QtCore, QtGui
import sys
from wx.lib.pubsub import pub

from views.T_Rax_ROIViewDiamond import TRaxROIViewDiamond
from T_Rax_Data import TraxData

class TRaxROIControllerDiamond(object):
    def __init__(self, data, parent=None):
        self.parent=parent
        self.view = TRaxROIViewDiamond(data,parent)
        self.data = data
        self.create_signals()
        self.view.update_txt_roi()
        self.save_roi_data()

    def create_signals(self):
        self.create_btn_signals()
        self.create_txt_signals()
        self.create_pub_signals()

    def create_btn_signals(self):
        self.view.save_btn.clicked.connect(self.save_btn_click)
        self.view.cancel_btn.clicked.connect(self.cancel_btn_click)

    def create_txt_signals(self):
        self.view.x_min_txt.editingFinished.connect(self.roi_txt_changed)
        self.view.x_max_txt.editingFinished.connect(self.roi_txt_changed)
        self.view.y_min_txt.editingFinished.connect(self.roi_txt_changed)
        self.view.y_max_txt.editingFinished.connect(self.roi_txt_changed)

    def create_pub_signals(self):
        pub.subscribe(self.roi_graph_changed, "DIAMOND ROI GRAPH CHANGED")
        pub.subscribe(self.roi_changed, "DIAMOND ROI CHANGED")
        pub.subscribe(self.exp_data_changed, "EXP DIAMOND DATA CHANGED")

    def roi_txt_changed(self):
        roi=self.view.get_roi()
        roi[:2] = self.data.calculate_ind(roi[:2])  
        self.data.roi.set_roi(roi)
        pub.sendMessage("DIAMOND ROI CHANGED")

    def roi_changed(self):
        self.view.update_graph_roi()
        self.view.update_txt_roi()

    def roi_graph_changed(self, data):
        self.data.roi.set_roi(data)
        pub.sendMessage("DIAMOND ROI CHANGED")


    def exp_data_changed(self):
        self.view.update_img()

    def save_btn_click(self):
        self.shut_down_window()

    def cancel_btn_click(self):
        self.reset_roi_data()
        self.shut_down_window()

    def reset_roi_data(self):
        self.data.roi.set_roi(self.initial_roi)

    def save_roi_data(self):
        self.initial_roi = self.data.roi.get_roi_as_list()

    def shut_down_window(self):
        self.view.close()

    def show(self):
        self.save_roi_data()
        self.view.show()
        self.view.activateWindow()
        self.view.move(self.parent.x(), 
                       self.parent.y()+self.parent.height()+50)
        self.view.resize(self.parent.size().width(),self.view.size().height())


if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    data=TraxData()
    controller=TRaxROIController(data)
    controller.view.show()
    app.exec_()