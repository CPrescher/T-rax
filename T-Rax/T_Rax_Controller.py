import T_Rax_Data as TRData
import T_Rax_Main_View as TRMView
import wx
from wx.lib.pubsub import Publisher as pub

class TraxMainViewController(object):
    def __init__(self):
        self.data=TRData.TraxData()
        self.main_view=TRMView.TraxMainWindow(self)
        self.set_bindings()

    def set_bindings(self):
        self.main_view.control_panel.load_btn.Bind(wx.EVT_BUTTON, self.load_data)
        self.main_view.control_panel.next_btn.Bind(wx.EVT_BUTTON, self.load_next_data)
        self.main_view.control_panel.previous_btn.Bind(wx.EVT_BUTTON, self.load_previous_data)

        pub.subscribe(self.data_changed, "DATA CHANGED")

    def load_data(self, e):
        self.data.load_data('spe files\Pt_230.SPE')

    def load_next_data(self, e):
        self.data.load_next_file()

    def load_previous_data(self, e):
        self.data.load_previous_file()

    def data_changed(self, message):
        data_obj=message.data
        X,Y, img_data=data_obj.get_img_data()
        self.main_view.graph_panel.plot_img(X,Y,img_data)
        x,y = data_obj.get_whole_spectrum()
        self.main_view.graph_panel.plot_graph(x,y)
        self.main_view.graph_panel.redraw_figure()


if __name__=="__main__":
    app=wx.App(None)
    main_view=TraxMainViewController()
    main_view.data.load_data('spe files\Pt_230.SPE')
    app.MainLoop()

