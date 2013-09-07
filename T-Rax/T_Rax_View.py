import wx
import matplotlib as mpl
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['lines.color'] = 'g'
mpl.rcParams['text.color'] = 'white'
mpl.rc('axes', facecolor='black', edgecolor='white')
mpl.rc('xtick', color='white')
mpl.rc('ytick', color='white')
mpl.rc('figure', facecolor='black', edgecolor='black')

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas

class TraxMainWindow(wx.Frame):
    def __init__(self, controller):
        wx.Frame.__init__(self, None, -1, 'T-Rax ver 0.1', size=(950,500))
        self.controller = controller
        self.init_UI()
        self.Show()

    def init_UI(self):
        self.main_panel = wx.Panel(self)
        self.control_panel = TraxControlPanel(self.main_panel)
        self.graph_panel = TraxGraphPanel(self.main_panel)
        
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer.AddMany([(self.graph_panel, 1 , wx.RIGHT | wx.EXPAND,10),(self.control_panel,0)])
        self.main_panel.SetSizer(self.main_sizer)

class TraxControlPanel(wx.Panel):
    def __init__(self, parent):
        super(TraxControlPanel, self).__init__(parent)
        self.load_btn = wx.Button(self, wx.ID_ANY, 'Load Data')
        self.previous_btn = wx.Button(self, wx.ID_ANY,'<-', size=(30,20))
        self.next_btn = wx.Button(self, wx.ID_ANY, '->', size=(30,20))

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dir_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.dir_sizer.Add(self.previous_btn, 1, wx.EXPAND | wx.ALL, 5)
        self.dir_sizer.Add(self.next_btn,1, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(self.load_btn,0)
        self.main_sizer.Add(self.dir_sizer,0, wx.EXPAND)
        self.SetSizer(self.main_sizer)

class TraxGraphPanel(wx.Panel):
    def __init__(self, parent):
        super(TraxGraphPanel, self).__init__(parent)
        self.figure = Figure(None, dpi=100)
        self.canvas = FigCanvas(self, wx.ID_ANY, self.figure)
        self.status_bar = wx.StatusBar(self)

        box_sizer = wx.BoxSizer(wx.VERTICAL)
        box_sizer.Add(self.canvas,1, flag = wx.EXPAND)
        box_sizer.Add(self.status_bar, 0, wx.EXPAND)
        self.SetSizer(box_sizer)

        self.graph_axes = self.figure.add_subplot(121)
        self.image_axes = self.figure.add_subplot(122)

        #make the thing resizable:
        self.canvas.Bind(wx.EVT_SIZE, self.resize_graph)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

    def resize_graph(self, event):
        border = 5
        w,h = event.GetSize()
        self.figure.set_size_inches([w / 100.0,h / 100.0])
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