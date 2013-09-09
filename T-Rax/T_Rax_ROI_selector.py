import wx
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from SPE_module import SPE_File
from wx.lib.pubsub import Publisher as pub
from Helper import IntValidator



class TRaxROIView(wx.MiniFrame):
    def __init__(self):
        wx.MiniFrame.__init__(self, None, -1, 'ROI selector', size=(950,600))
        self.init_UI()
        self.Show()

    def init_UI(self):
        self.create_panels()
        self.create_sizers()

    def create_panels(self):
        self.main_panel = wx.Panel(self)
        self.control_panel = TRaxROIControlPanel(self.main_panel)
        self.graph_panel = TraxROIGraphPanel(self.main_panel)

    def create_sizers(self):
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer.AddMany([(self.graph_panel, 1 , wx.RIGHT | wx.EXPAND,10),(self.control_panel,0)])
        self.main_panel.SetSizer(self.main_sizer)

class TRaxROIControlPanel(wx.Panel):
    def __init__(self, parent):
        super(TRaxROIControlPanel, self).__init__(parent)
    
        self.create_us_box()
        self.create_ds_box()
        self.create_buttons()
        self.create_listener()

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.us_box_sizer,1, wx.EXPAND | wx.ALL,5)
        self.main_sizer.Add(self.ds_box_sizer,1, wx.EXPAND | wx.ALL,5)
        self.main_sizer.Add(self.btn_sizer,0, wx.EXPAND |wx.ALL,5)
        self.SetSizer(self.main_sizer)

    def create_us_box(self):
        self.create_us_controls()
        self.create_us_sizer()

    def create_us_controls(self):
        self.us_static_box = wx.StaticBox(self, -1, 'Upstream ROI')
        self.us_box_sizer = wx.StaticBoxSizer(self.us_static_box, wx.VERTICAL)
        self.us_upper_limit_lbl = wx.StaticText(self, -1, 'Upper Limit:')
        self.us_lower_limit_lbl = wx.StaticText(self, -1, 'Lower Limit:')
        self.us_lower_limit_txt = wx.TextCtrl(self, -1, '25', style =wx.ALIGN_RIGHT, validator = IntValidator(2))
        self.us_upper_limit_txt = wx.TextCtrl(self, -1, '3', style =wx.ALIGN_RIGHT, validator = IntValidator(2))

    def create_us_sizer(self):
        lower_limit_box=wx.BoxSizer(wx.HORIZONTAL)
        lower_limit_box.AddMany([(self.us_lower_limit_lbl, 0, wx.ALL|wx.EXPAND,3), (self.us_lower_limit_txt, 1, wx.ALL|wx.EXPAND,3)])
        upper_limit_box=wx.BoxSizer(wx.HORIZONTAL)
        upper_limit_box.AddMany([(self.us_upper_limit_lbl, 0, wx.ALL|wx.EXPAND,3), (self.us_upper_limit_txt, 1, wx.ALL|wx.EXPAND,3)])
        self.us_box_sizer.AddMany([(lower_limit_box, 1, wx.EXPAND),(upper_limit_box, 1, wx.EXPAND)])

    def create_ds_box(self):
        self.create_ds_controls()
        self.create_ds_sizer()

    def create_ds_controls(self):
        self.ds_static_box = wx.StaticBox(self, -1, 'Upstream ROI')
        self.ds_box_sizer = wx.StaticBoxSizer(self.ds_static_box, wx.VERTICAL)
        self.ds_upper_limit_lbl = wx.StaticText(self, -1, 'Upper Limit:')
        self.ds_lower_limit_lbl = wx.StaticText(self, -1, 'Lower Limit:')
        self.ds_lower_limit_txt = wx.TextCtrl(self, -1, '25', style =wx.ALIGN_RIGHT, validator = IntValidator(2))
        self.ds_upper_limit_txt = wx.TextCtrl(self, -1, '3', style =wx.ALIGN_RIGHT, validator = IntValidator(2))

    def create_ds_sizer(self):
        lower_limit_box=wx.BoxSizer(wx.HORIZONTAL)
        lower_limit_box.AddMany([(self.ds_lower_limit_lbl, 0, wx.ALL|wx.EXPAND,3), (self.ds_lower_limit_txt, 1, wx.ALL|wx.EXPAND,3)])
        upper_limit_box=wx.BoxSizer(wx.HORIZONTAL)
        upper_limit_box.AddMany([(self.ds_upper_limit_lbl, 0, wx.ALL|wx.EXPAND,3), (self.ds_upper_limit_txt, 1, wx.ALL|wx.EXPAND,3)])
        self.ds_box_sizer.AddMany([(lower_limit_box, 1, wx.EXPAND),(upper_limit_box, 1, wx.EXPAND)])

    def create_buttons(self):
        self.ok_button=wx.Button(self, wx.ID_OK, 'OK')
        self.cancel_button=wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.btn_sizer=wx.BoxSizer(wx.HORIZONTAL)
        self.btn_sizer.AddMany([(self.ok_button,0,wx.ALL,3),(self.cancel_button,0,wx.ALL,3)])

    def create_listener(self):
        pub.subscribe(self.us_roi_changed, "US ROI CHANGED")
        pub.subscribe(self.ds_roi_changed, "DS ROI CHANGED")
        self.ds_lower_limit_txt.Bind(wx.EVT_TEXT, self.ds_txt_changed)
        self.ds_upper_limit_txt.Bind(wx.EVT_TEXT, self.ds_txt_changed)
        self.us_lower_limit_txt.Bind(wx.EVT_TEXT, self.us_txt_changed)
        self.us_upper_limit_txt.Bind(wx.EVT_TEXT, self.us_txt_changed)

    def us_roi_changed(self, e):
        self.us_lower_limit_txt.SetLabel(str(int(e.data[0])))
        self.us_upper_limit_txt.SetLabel(str(int(e.data[1])))

    def ds_roi_changed(self, e):
        self.ds_lower_limit_txt.SetLabel(str(int(e.data[0])))
        self.ds_upper_limit_txt.SetLabel(str(int(e.data[1])))

    def ds_txt_changed(self, e):
        lower_bound=int(self.ds_lower_limit_txt.GetLabel())
        upper_bound=int(self.ds_upper_limit_txt.GetLabel())
        height=upper_bound-lower_bound
        pub.sendMessage("DS TXT CHANGED", [lower_bound, height])

    def us_txt_changed(self, e):
        lower_bound=int(self.us_lower_limit_txt.GetLabel())
        upper_bound=int(self.us_upper_limit_txt.GetLabel())
        height=upper_bound-lower_bound
        pub.sendMessage("US TXT CHANGED", [lower_bound, height])




class TraxROIGraphPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(TraxROIGraphPanel, self).__init__(*args, **kwargs)

        self.create_figure()
        self.create_sizer()
        self.create_bindings()

    def create_figure(self):
        self.figure = Figure(None, dpi=100)
        self.canvas = FigCanvas(self, wx.ID_ANY, self.figure)
        self.axes = self.figure.add_subplot(111)
        self.status_bar = wx.StatusBar(self)

    def create_sizer(self):
        box_sizer = wx.BoxSizer(wx.VERTICAL)
        box_sizer.Add(self.canvas,1, flag = wx.EXPAND)
        box_sizer.Add(self.status_bar, 0, wx.EXPAND)
        self.SetSizer(box_sizer)

    def create_bindings(self):
        self.canvas.Bind(wx.EVT_SIZE, self.resize_graph)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

    def resize_graph(self, event):
        border = 5
        w,h = event.GetSize()
        self.figure.set_size_inches([w / 100.0,h / 100.0])
        self.redraw_figure()

    def redraw_figure(self):
        self.figure.tight_layout(None, 1.2, None, None)
        self.canvas.draw()

    def on_mouse_move(self, event):
        x_coord = event.xdata
        y_coord = event.ydata
        if x_coord <> None:
            self.status_bar.SetStatusText('x: %(x).3F y: %(y).3F' \
                               % {'x':x_coord, 'y':y_coord})
        else:
            self.status_bar.SetStatusText('')

    def plot_img(self, img_data):
        self.axes.cla()
        self.axes.imshow(img_data, cmap = 'hot', aspect = 'auto')
        self.axes.set_ylim([0,len(img_data)-1])
        self.axes.set_xlim([0,len(img_data[0])-1])
        self.us_rect = ResizableRectangle(self.axes, self.canvas, wx.Rect(0,80,len(img_data[0])-1,10), "US ROI CHANGED", "US TXT CHANGED")
        self.ds_rect = ResizableRectangle(self.axes, self.canvas, wx.Rect(0,30,len(img_data[0])-1,12), "DS ROI CHANGED", "DS TXT CHANGED")
        self.redraw_figure()
        self.us_rect.connect()
        self.ds_rect.connect()


class ResizableRectangle:
    def __init__(self, axes, canvas, init_rect, pub_send_str, pub_receive_str):
       
        self.axes=axes
        self.canvas = canvas
        self.ylim = self.axes.get_ylim()
        self.pub_send_str=pub_send_str
        self.pub_receive_str=pub_receive_str
        pub.subscribe(self.on_txt_change, pub_receive_str)

        self.rect = mpl.patches.Rectangle((init_rect.x,init_rect.y),init_rect.width, init_rect.height, ec='w', fill=False, lw=2)
        self.axes.add_artist(self.rect)
               
        self.press = None 
        self.mode = None


    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.rect.axes: return
        
        y_click=event.ydata
        y0 = self.rect.get_y()
        height = self.rect.get_height()

        self.set_mode(y_click,y0,height)
        self.press = y0, event.ydata

    def set_mode(self,y_click, y0,height):
        if y_click >= y0+height*0.1 and y_click<=y0+height*0.9:
            self.mode='move'
        elif y_click>y0+height-3 and y_click<=y0+height+3:
            self.mode='resize_top'
        elif y_click>y0-3 and y_click<y0+3:
            self.mode='resize_bottom'


    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.rect.axes: return
        
        y_click=event.ydata
        y0, ypress = self.press
        dy = event.ydata - ypress
        height=self.rect.get_height()

        if self.mode=='move':
            new_pos = y0+dy
            top_pos = new_pos+height
            if new_pos >=0 and (top_pos)<=self.ylim[1]:
                self.rect.set_y(new_pos)
            elif new_pos<=0:
                self.rect.set_y(0)
            elif top_pos>self.ylim[1]:
                self.rect.set_y(self.ylim[1]-height)
        elif self.mode=='resize_top':
            self.rect.set_height(event.ydata-y0)
        elif self.mode=='resize_bottom':
            self.rect.set_height(self.rect.get_y()-y_click + height)
            self.rect.set_y(y_click)

        pub.sendMessage(self.pub_send_str, [self.rect.get_y(), self.rect.get_y()+self.rect.get_height()])

        self.rect.figure.canvas.draw()


    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.mode = None

    def on_txt_change(self,event):
        if self.press==None:
            self.rect.set_y=(event.data[0])
            self.rect.set_height(event.data[1])
            self.rect.figure.canvas.draw()

        


if __name__ == "__main__":
    spe_file = SPE_File('spe files\Pt_230.SPE')
    #spe_file = SPE_File('binary files\lamp_15_up(v3.0).SPE')
    img = spe_file.img
    app = wx.App(None)
    view = TRaxROIView()
    view.graph_panel.plot_img(img)
    app.MainLoop()







