import wx
from wx.lib.pubsub import Publisher as pub
from TRaxROISelector.T_Rax_ROI_view import TRaxROIView

from TRaxROISelector.T_Rax_ROI_panels import MoveableLine,ResizeableRectangle

class TRaxROIController():
    __single = None
    def __init__(self, parent, data):
        if TRaxROIController.__single:
            raise TRaxROIController.__single

        TRaxROIController.__single = self
        self.data = data
        self.initial_ds_row = data.roi_data.ds_roi.get_list()
        self.initial_us_row = data.roi_data.us_roi.get_list()
        self.view = TRaxROIView(parent, data)
        self.set_bindings()
        
        self.view.graph_panel.draw_image()

    def set_bindings(self):
        self.view.control_panel.ds_roi_box.x_min_txt.Bind(wx.EVT_TEXT_ENTER, self.ds_roi_txt_changed)
        self.view.control_panel.ds_roi_box.x_max_txt.Bind(wx.EVT_TEXT_ENTER, self.ds_roi_txt_changed)
        self.view.control_panel.us_roi_box.x_min_txt.Bind(wx.EVT_TEXT_ENTER, self.us_roi_txt_changed)
        self.view.control_panel.us_roi_box.x_max_txt.Bind(wx.EVT_TEXT_ENTER, self.us_roi_txt_changed)

        self.view.control_panel.ds_roi_box.y_min_txt.Bind(wx.EVT_TEXT_ENTER, self.ds_roi_txt_changed)
        self.view.control_panel.ds_roi_box.y_max_txt.Bind(wx.EVT_TEXT_ENTER, self.ds_roi_txt_changed)
        self.view.control_panel.us_roi_box.y_min_txt.Bind(wx.EVT_TEXT_ENTER, self.us_roi_txt_changed)
        self.view.control_panel.us_roi_box.y_max_txt.Bind(wx.EVT_TEXT_ENTER, self.us_roi_txt_changed)

        self.view.control_panel.limits_box.from_txt.Bind(wx.EVT_TEXT_ENTER, self.limits_txt_changed)
        self.view.control_panel.limits_box.to_txt.Bind(wx.EVT_TEXT_ENTER, self.limits_txt_changed)

        pub.subscribe(self.ds_roi_graph_changed, "DS ROI GRAPH CHANGED")
        pub.subscribe(self.us_roi_graph_changed, "US ROI GRAPH CHANGED")
        pub.subscribe(self.roi_changed, "ROI CHANGED")

        pub.subscribe(self.img_loaded, "IMG LOADED")
        pub.subscribe(self.graph_loaded, "GRAPH LOADED")

        pub.subscribe(self.min_roi_line_changed, "MIN ROI LINE CHANGED")
        pub.subscribe(self.max_roi_line_changed, "MAX ROI LINE CHANGED")

        pub.subscribe(self.exp_data_changed, "EXP DATA CHANGED")

        self.view.control_panel.ok_button.Bind(wx.EVT_BUTTON, self.ok_btn_click)
        self.view.control_panel.cancel_button.Bind(wx.EVT_BUTTON, self.cancel_btn_click)
        self.view.Bind(wx.EVT_CLOSE, self.close_window_click)


    def ds_roi_txt_changed(self, event):
        new_roi = self.view.control_panel.ds_roi_box.get_roi()
        new_roi[2:] = self.data.calculate_ind(new_roi[2:])
        self.data.roi_data.set_ds_roi(new_roi)

    def us_roi_txt_changed(self, event):
        new_roi = self.view.control_panel.us_roi_box.get_roi()
        new_roi[2:] = self.data.calculate_ind(new_roi[2:])
        self.data.roi_data.set_us_roi(new_roi)

    def ds_roi_graph_changed(self, event):
        self.data.roi_data.set_ds_roi(event.data)

    def us_roi_graph_changed(self, event):
        self.data.roi_data.set_us_roi(event.data)

    def min_roi_line_changed(self,event):
        new_x_min = self.data.calculate_ind(event.data)
        self.data.roi_data.set_x_min(new_x_min)
        self.view.graph_panel.update_line_limits()

    def max_roi_line_changed(self,event):
        new_x_max = self.data.calculate_ind(event.data)
        self.data.roi_data.set_x_max(new_x_max)
        self.view.graph_panel.update_line_limits()

    def limits_txt_changed(self, event):
        new_limits = self.view.control_panel.limits_box.get_limits()
        new_limits_ind = np.array(self.data.calculate_ind(new_limits))
        self.data.roi_data.set_x_limits(new_limits_ind)
        
        self.view.graph_panel.update_line_limits()
        self.view.graph_panel.update_lines()

    def roi_changed(self, event):
        self.view.control_panel.update_rois()
        self.view.graph_panel.set_rois()

    def exp_data_changed(self, event):
        self.view.graph_panel.update_img()

    def img_loaded(self, event):
        self.mode = 'IMAGE'
        self.view.control_panel.ds_roi_box.Show()
        self.view.control_panel.us_roi_box.Show()
        self.view.control_panel.limits_box.Hide()
        self.view.control_panel.Layout()
        self.view.Layout()

    def graph_loaded(self, event):
        self.mode = 'GRAPH'
        self.view.control_panel.ds_roi_box.Hide()
        self.view.control_panel.us_roi_box.Hide()
        self.view.control_panel.limits_box.Show()
        self.view.control_panel.Layout()
        self.view.Layout()

    def activate(self):
        self.view.Raise()

    def ok_btn_click(self, event):
        self.shut_down_window()
        del self

    def cancel_btn_click(self,event):
        self.reset_roi_data()
        self.shut_down_window()

    def close_window_click(self, event):
        #self.reset_roi_data() don't know what it should do...
        self.shut_down_window()

    def reset_roi_data(self):
        self.data.roi_data.set_ds_roi(self.initial_ds_row)
        self.data.roi_data.set_us_roi(self.initial_us_row)
        
    def shut_down_window(self):
        self.view.Destroy()
        pub.unsubscribe(self.ds_roi_graph_changed, "DS ROI GRAPH CHANGED")
        pub.unsubscribe(self.us_roi_graph_changed, "US ROI GRAPH CHANGED")
        pub.unsubscribe(self.roi_changed, "ROI CHANGED")
        pub.unsubscribe(self.min_roi_line_changed, "MIN ROI LINE CHANGED")
        pub.unsubscribe(self.max_roi_line_changed, "MAX ROI LINE CHANGED")
        pub.unsubscribe(self.exp_data_changed, "EXP DATA CHANGED")
        TRaxROIController.__single = None