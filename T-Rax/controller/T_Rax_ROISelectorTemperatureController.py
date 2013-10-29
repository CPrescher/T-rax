from PyQt4.QtCore import SIGNAL
from PyQt4 import QtCore, QtGui
import sys
from wx.lib.pubsub import pub

from views.T_Rax_ROIView import TRaxROIView

class TRaxROITemperatureController(object):
    def __init__(self, data, parent=None):
        self.parent=parent
        self.view = TRaxROIView(data,parent)
        self.data = data
        self.create_signals()
        self.view.update_txt_roi()
        self.save_roi_data()
        self.view.draw_image()

    def create_signals(self):
        self.create_btn_signals()
        self.create_ds_txt_signals()
        self.create_us_txt_signals()
        self.create_fit_txt_signals()
        self.create_key_signals()
        self.create_pub_signals()

    def create_btn_signals(self):
        self.view.save_btn.clicked.connect(self.save_btn_click)
        self.view.cancel_btn.clicked.connect(self.cancel_btn_click)

    def create_ds_txt_signals(self):
        self.view.ds_x_min_txt.editingFinished.connect(self.ds_roi_txt_changed)
        self.view.ds_x_max_txt.editingFinished.connect(self.ds_roi_txt_changed)
        self.view.ds_y_min_txt.editingFinished.connect(self.ds_roi_txt_changed)
        self.view.ds_y_max_txt.editingFinished.connect(self.ds_roi_txt_changed)
                                                            
    def create_us_txt_signals(self):                        
        self.view.us_x_min_txt.editingFinished.connect(self.us_roi_txt_changed)
        self.view.us_x_max_txt.editingFinished.connect(self.us_roi_txt_changed)
        self.view.us_y_min_txt.editingFinished.connect(self.us_roi_txt_changed)
        self.view.us_y_max_txt.editingFinished.connect(self.us_roi_txt_changed)

    def create_fit_txt_signals(self):
        self.view.fit_from_txt.editingFinished.connect(self.fit_txt_changed)
        self.view.fit_to_txt.editingFinished.connect(self.fit_txt_changed)     

    def create_key_signals(self):
        self.view.keyPressEvent = self.key_pressed

    def create_pub_signals(self):
        pub.subscribe(self.ds_roi_graph_changed, "DS ROI GRAPH CHANGED")
        pub.subscribe(self.us_roi_graph_changed, "US ROI GRAPH CHANGED")
        
        pub.subscribe(self.min_roi_line_changed, "MIN ROI LINE CHANGED")
        pub.subscribe(self.max_roi_line_changed, "MAX ROI LINE CHANGED")

        pub.subscribe(self.roi_changed, "ROI CHANGED")
        pub.subscribe(self.img_loaded, "IMG LOADED")
        pub.subscribe(self.graph_loaded, "GRAPH LOADED")
        pub.subscribe(self.exp_data_changed, "EXP DATA CHANGED")

    def us_roi_txt_changed(self):
        us_roi=self.view.get_us_roi()
        us_roi[:2] = self.data.calculate_ind(us_roi[:2])  
        self.data.roi_data.set_us_roi(us_roi)

    def ds_roi_txt_changed(self):
        ds_roi=self.view.get_ds_roi()      
        ds_roi[:2] = self.data.calculate_ind(ds_roi[:2])
        self.data.roi_data.set_ds_roi(ds_roi)

    def key_pressed(self,event):
        if type(event) == QtGui.QKeyEvent and \
            event.key() == QtCore.Qt.Key_Up:
            ds_roi = self.data.get_ds_roi()
            us_roi = self.data.get_us_roi()
            ds_roi[2:]=[ds_roi[2]-1, ds_roi[3]-1]
            us_roi[2:]=[us_roi[2]-1, us_roi[3]-1]
            self.data.roi_data.set_ds_roi(ds_roi)
            self.data.roi_data.set_us_roi(us_roi)
        elif type(event) == QtGui.QKeyEvent and \
            event.key() == QtCore.Qt.Key_Down:
            ds_roi = self.data.get_ds_roi()
            us_roi = self.data.get_us_roi()
            ds_roi[2:]=[ds_roi[2]+1, ds_roi[3]+1]
            us_roi[2:]=[us_roi[2]+1, us_roi[3]+1]
            self.data.roi_data.set_ds_roi(ds_roi)
            self.data.roi_data.set_us_roi(us_roi)

    def fit_txt_changed(self):
        converted_limits = self.data.calculate_ind(self.view.get_fit_x_limits())
        self.data.roi_data.set_x_limits(converted_limits)

    def roi_changed(self):
        self.view.update_graph_roi()
        self.view.update_txt_roi()

    def ds_roi_graph_changed(self, data):
        self.data.roi_data.set_ds_roi(data)

    def us_roi_graph_changed(self, data):
        self.data.roi_data.set_us_roi(data)

    def min_roi_line_changed(self,data):
        new_x_min = self.data.calculate_ind(data)
        self.data.roi_data.set_x_min(new_x_min)
        self.view.graph_panel.update_line_limits()

    def max_roi_line_changed(self,data):
        new_x_max = self.data.calculate_ind(data)
        self.data.roi_data.set_x_max(new_x_max)
        self.view.graph_panel.update_line_limits()

    def exp_data_changed(self):
        self.view.update_img()
        self.view.update_txt_roi()

    def save_btn_click(self):
        self.shut_down_window()

    def cancel_btn_click(self):
        self.reset_roi_data()
        self.shut_down_window()

    def reset_roi_data(self):
        self.data.roi_data.set_ds_roi(self.initial_ds_row)
        self.data.roi_data.set_us_roi(self.initial_us_row)

    def save_roi_data(self):
        self.initial_ds_row = self.data.roi_data.ds_roi.get_roi_as_list()
        self.initial_us_row = self.data.roi_data.us_roi.get_roi_as_list()

    def shut_down_window(self):
        self.view.close()

    def img_loaded(self):
        self.mode = 'IMAGE'
        self.view.downstream_roi_box.show()
        self.view.upstream_roi_box.show()
        self.view.fitting_roi_box.hide()

    def graph_loaded(self):
        self.mode = 'GRAPH'
        self.view.downstream_roi_box.hide()
        self.view.upstream_roi_box.hide()
        self.view.fitting_roi_box.show()

    def show(self):
        self.save_roi_data()
        self.view.show()
        self.view.activateWindow()
        if self.mode =='IMAGE':
            self.img_loaded()
        elif self.mode =='GRAPH':
            self.graph_loaded()
        self.view.move(self.parent.x(), 
                       self.parent.y()+self.parent.height()+50)
        self.view.resize(self.parent.size().width(),self.view.size().height())
