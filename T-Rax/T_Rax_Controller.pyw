import T_Rax_Data as TRData
import T_Rax_Main_View as TRMView
from T_Rax_ROI_selector import TRaxROIController
import wx
from wx.lib.pubsub import Publisher as pub
import os

class TraxMainViewController(object):
    def __init__(self):
        self.data=TRData.TraxData()
        self.roi_view = None
        self.main_view = TRMView.TraxMainWindow(self)
        self.controls = self.main_view.exp_panel
        self._working_dir=os.getcwd()
        self.set_bindings()

    def set_bindings(self):
        self.controls.exp_load_data_btn.Bind(wx.EVT_BUTTON, self.load_data)
        self.controls.exp_next_btn.Bind(wx.EVT_BUTTON, self.load_next_data)
        self.controls.exp_previous_btn.Bind(wx.EVT_BUTTON, self.load_previous_data)
        self.controls.roi_setup_btn.Bind(wx.EVT_BUTTON, self.roi_setup_btn_click)
        pub.subscribe(self.data_changed, "EXP DATA CHANGED")
        pub.subscribe(self.ds_roi_changed, "DS ROI CHANGED")
        pub.subscribe(self.us_roi_changed, "US ROI CHANGED")
        pub.subscribe(self.unload_roi_view, "ROI VIEW CLOSED")
        self.main_view.Bind(wx.EVT_CLOSE, self.close_window_click)

    def load_data(self, e):
        dlg = wx.FileDialog(self.main_view, message="Load Experiment SPE", 
                            defaultDir = self._working_dir,
                            defaultFile ="", style=wx.OPEN)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()  
            self._working_dir=os.path.split(path)[0]     
            self.data.load_data(path)

    def load_next_data(self, e):
        self.data.load_next_file()

    def load_previous_data(self, e):
        self.data.load_previous_file()

    def roi_setup_btn_click(self, event):
        if self.roi_view==None:
            self.roi_view = TRaxROIController(self.main_view, self.data)

    def unload_roi_view(self, message):
        self.roi_view=None

    def data_changed(self, message):
        data=message.data
        ds_x,ds_y = data.get_ds_spectrum()
        us_x,us_y = data.get_us_spectrum()
        self.main_view.graph_panel.plot_ds_graph(ds_x,ds_y)
        self.main_view.graph_panel.plot_us_graph(us_x,us_y)
        self.main_view.graph_panel.redraw_figure()
        self.controls.exp_file_lbl.SetLabel(data.file_name.split('\\')[-1])

    def ds_roi_changed(self, message):
        x,y=message.data.get_ds_spectrum()
        self.main_view.graph_panel.update_ds_graph(x,y)
    
    def us_roi_changed(self, message):
        x,y=message.data.get_us_spectrum()
        self.main_view.graph_panel.update_us_graph(x,y)

    def close_window_click(self, event):
        self.main_view.Destroy()
        self.data.save_roi_data()

if __name__=="__main__":
    app=wx.App(None)
    main_view=TraxMainViewController()
    main_view.data.load_data('binary files\\lamp_15_up(v3.0).SPE')
    app.MainLoop()

