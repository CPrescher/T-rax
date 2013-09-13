import scipy
import T_Rax_Data as TRData
import T_Rax_Main_View as TRMView
from T_Rax_ROI_selector import TRaxROIController
import wx
from wx.lib.pubsub import Publisher as pub
import os

wx.lib.pubsub.Publisher

class TraxMainViewController(object):
    def __init__(self):
        self.data=TRData.TraxData()
        self.roi_view = None
        self.main_view = TRMView.TraxMainWindow(self)
        self.exp_controls = self.main_view.exp_panel
        self.calib_controls = self.main_view.calib_panel
        self._working_dir=os.getcwd()
        self.set_bindings()

    def set_bindings(self):
        self.exp_controls.exp_load_data_btn.Bind(wx.EVT_BUTTON, self.load_exp_data)
        self.exp_controls.exp_next_btn.Bind(wx.EVT_BUTTON, self.load_exp_next_data)
        self.exp_controls.exp_previous_btn.Bind(wx.EVT_BUTTON, self.load_exp_previous_data)
        self.exp_controls.roi_setup_btn.Bind(wx.EVT_BUTTON, self.roi_setup_btn_click)
        pub.subscribe(self.data_changed, "EXP DATA CHANGED")
        pub.subscribe(self.spectra_changed, "ROI CHANGED")
        pub.subscribe(self.unload_roi_view, "ROI VIEW CLOSED")
        self.main_view.Bind(wx.EVT_CLOSE, self.close_window_click)

        self.calib_controls.ds_calib_box.load_data_btn.Bind(wx.EVT_BUTTON, self.load_ds_calib_data)
        self.calib_controls.us_calib_box.load_data_btn.Bind(wx.EVT_BUTTON, self.load_us_calib_data)

        self.calib_controls.ds_calib_box.temperature_txt.Bind(wx.EVT_TEXT_ENTER, self.update_ds_temp)
        self.calib_controls.us_calib_box.temperature_txt.Bind(wx.EVT_TEXT_ENTER, self.update_us_temp)


    def load_exp_data(self, e):
        dlg = wx.FileDialog(self.main_view, message="Load Experiment SPE", 
                            defaultDir = self._working_dir,
                            defaultFile ="", style=wx.OPEN)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()  
            self._working_dir=os.path.split(path)[0]     
            self.data.load_exp_data(path)

    def load_exp_next_data(self, e):
        self.data.load_next_file()

    def load_exp_previous_data(self, e):
        self.data.load_previous_file()

    def roi_setup_btn_click(self, event):
        if self.roi_view==None:
            self.roi_view = TRaxROIController(self.main_view, self.data)

    def unload_roi_view(self, message):
        self.roi_view=None

    def load_ds_calib_data(self, event):
        dlg = wx.FileDialog(self.main_view, message="Load Downstream calibration SPE", 
                            defaultDir = self._working_dir,
                            defaultFile ="", style=wx.OPEN)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()  
            self._working_dir=os.path.split(path)[0]     
            self.data.load_ds_calib_data(path)
            self.calib_controls.ds_calib_box.file_lbl.SetLabel(self.data.get_ds_calib_file_name())

    def load_us_calib_data(self, event):
        dlg = wx.FileDialog(self.main_view, message="Load Upstream calibration SPE", 
                            defaultDir = self._working_dir,
                            defaultFile ="", style=wx.OPEN)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()  
            self._working_dir=os.path.split(path)[0]     
            self.data.load_us_calib_data(path)
            self.calib_controls.us_calib_box.file_lbl.SetLabel(self.data.get_us_calib_file_name())

    def update_us_temp(self, event):
        self.data.us_temp = int(self.calib_controls.us_calib_box.temperature_txt.GetLabel())

    def update_ds_temp(self, event):
        self.data.ds_temp = int(self.calib_controls.ds_calib_box.temperature_txt.GetLabel())

    def data_changed(self, message):
        data=message.data
        self.main_view.graph_panel.plot_ds_graph(data.get_ds_spectrum())
        self.main_view.graph_panel.plot_us_graph(data.get_us_spectrum())
        self.main_view.graph_panel.redraw_figure()
        self.exp_controls.exp_file_lbl.SetLabel(data.get_exp_file_name())

    def spectra_changed(self, message):
        data=message.data
        self.main_view.graph_panel.update_graph(data.get_ds_spectrum(), data.get_us_spectrum())

    def close_window_click(self, event):
        self.main_view.Destroy()
        self.data.save_roi_data()

if __name__=="__main__":
    app=wx.App(None)
    main_view=TraxMainViewController()
    main_view.data.load_exp_data('spe files\\t_47.SPE')
    #main_view.data.load_ds_calib_data('binary files\\lamp_15_dn.SPE')
    #main_view.data.load_us_calib_data('binary files\\lamp_15_up.SPE')
    app.MainLoop()

