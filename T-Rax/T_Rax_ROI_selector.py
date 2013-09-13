'''
This File includes the MVC pattern for the visual Selection of downstream and upstream ROIs.
To initiate the window instantiate the TRaxROIController Class.

Classes and use:

TRaxROIController(img_data, roi_data):
    Basic Controller for the Window, starting point, please give current image data and ROI data
    roi_data is given as ROIData class
    handles the bindings of the GUI except the draggable/resizeable rectangle, which is done by those themself

TRaxROIView(img_data, roi_data):
    sets up the basic GUI and is the container for the graph_panel and control_panel

TRaxROIGraphPanel(parent, img_data,roi_data):
    sets up the GUI for the Graph panel on the left

TRaxROIControlPanel(parent, roi_data):
    sets up the ROI txt controls in a static box
    the static boxes are further encapsulated in ROIEditBox

ROIEditBox(parent, roi, label)
    sets up a StaticBox with label as name and showing two rows: upper limit and lower limit
    textCtrl are set to the roi values roi should be of ROI class

ResizeableRectangle(axes, canvas, init_rect, flag)
    draws a resizable white unfilled rectangle in the axes which are enclosed in canvas. 
    Initial Rectangle size is defined by init_rect whereby init_rect should be of wx.Rect class.
    The flag is used for discriminating between downstreem and upstream Rectangle.

ROI(limits):
    Basic region of interest, should be initiated with a 2-element list containing lower ant upper limit

ROIData(ds_limits, us_limits):
    contains both downstream and upstram ROI classes
    ds_limits and us_limits are 2 element lists containing lower and upper limits.
'''


import wx
import matplotlib as mpl
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from SPE_module import SPE_File
from wx.lib.pubsub import Publisher as pub

from Helper import IntValidator
from T_Rax_Data import TraxData

class TRaxROIController():
    def __init__(self, parent, data):
        self.data = data
        self.initial_ds_row = data.roi_data.ds_roi.get_y_limits()
        self.initial_us_row = data.roi_data.us_roi.get_y_limits()
        self.view = TRaxROIView(parent, data)
        self.set_bindings()

    def set_bindings(self):
        self.view.control_panel.ds_roi_box.x_min_txt.Bind(wx.EVT_TEXT_ENTER, self.ds_roi_txt_changed)
        self.view.control_panel.ds_roi_box.x_max_txt.Bind(wx.EVT_TEXT_ENTER, self.ds_roi_txt_changed)
        self.view.control_panel.us_roi_box.x_min_txt.Bind(wx.EVT_TEXT_ENTER, self.us_roi_txt_changed)
        self.view.control_panel.us_roi_box.x_max_txt.Bind(wx.EVT_TEXT_ENTER, self.us_roi_txt_changed)

        self.view.control_panel.ds_roi_box.y_min_txt.Bind(wx.EVT_TEXT_ENTER, self.ds_roi_txt_changed)
        self.view.control_panel.ds_roi_box.y_max_txt.Bind(wx.EVT_TEXT_ENTER, self.ds_roi_txt_changed)
        self.view.control_panel.us_roi_box.y_min_txt.Bind(wx.EVT_TEXT_ENTER, self.us_roi_txt_changed)
        self.view.control_panel.us_roi_box.y_max_txt.Bind(wx.EVT_TEXT_ENTER, self.us_roi_txt_changed)

        pub.subscribe(self.ds_roi_graph_changed, "DS ROI GRAPH CHANGED")
        pub.subscribe(self.us_roi_graph_changed, "US ROI GRAPH CHANGED")
        pub.subscribe(self.roi_changed, "ROI CHANGED")
        pub.subscribe(self.exp_data_changed, "EXP DATA CHANGED")

        self.view.control_panel.ok_button.Bind(wx.EVT_BUTTON, self.ok_btn_click)
        self.view.control_panel.cancel_button.Bind(wx.EVT_BUTTON, self.cancel_btn_click)
        self.view.Bind(wx.EVT_CLOSE, self.close_window_click)

    def ds_roi_txt_changed(self, event):
        new_roi = self.view.control_panel.ds_roi_box.get_roi()
        self.data.roi_data.set_ds_roi(new_roi)

    def us_roi_txt_changed(self, event):
        new_roi = self.view.control_panel.us_roi_box.get_roi()
        self.data.roi_data.set_us_roi(new_roi)

    def ds_roi_graph_changed(self, event):
        self.data.roi_data.set_ds_roi(event.data)

    def us_roi_graph_changed(self, event):
        self.data.roi_data.set_us_roi(event.data)

    def roi_changed(self, event):
        self.view.control_panel.update_rois()
        self.view.graph_panel.set_rois()

    def exp_data_changed(self, event):
        img_data = event.data.exp_img_data
        self.view.graph_panel.update_img(img_data)

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
        pub.unsubscribe(self.exp_data_changed, "EXP DATA CHANGED")
        pub.sendMessage("ROI VIEW CLOSED")
        del self

class TRaxROIView(wx.MiniFrame):
    def __init__(self, parent, data):
        wx.MiniFrame.__init__(self, parent, -1, 'ROI Setup', pos=(1000,400), size=(700,500), style=wx.DEFAULT_FRAME_STYLE)
        self.data = data
        self.init_UI()
        self.SetMinSize((600,400))
        self.Show()

    def init_UI(self):
        self.create_panels()
        self.create_sizers()

    def create_panels(self):
        self.main_panel = wx.Panel(self)
        self.control_panel = TRaxROIControlPanel(self.main_panel,self.data)
        self.graph_panel = TRaxROIGraphPanel(self.main_panel,self.data)

    def create_sizers(self):
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer.AddMany([(self.graph_panel, 1 , wx.RIGHT | wx.EXPAND,10),(self.control_panel,0)])
        self.main_panel.SetSizer(self.main_sizer)

class TRaxROIControlPanel(wx.Panel):
    def __init__(self, parent, data):
        super(TRaxROIControlPanel, self).__init__(parent)
        self.data = data
        self.create_controls()
        self.set_sizer()

    def create_controls(self):
        self.ds_roi_box = ROIEditBox(self,self.data.roi_data.ds_roi, 'Downstream ROI')
        self.us_roi_box = ROIEditBox(self,self.data.roi_data.us_roi, 'Upstream ROI')
        self.create_buttons()

    def create_buttons(self):
        self.ok_button = wx.Button(self, wx.ID_OK, 'OK', size=(63,26))
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, 'Cancel', size=(63,26))
        self.btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_sizer.AddMany([(self.ok_button,0,wx.ALL,3),(self.cancel_button,0,wx.ALL,3)])    

    def set_sizer(self):
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.ds_roi_box.box_sizer,1, wx.EXPAND | wx.ALL,5)
        self.main_sizer.Add(self.us_roi_box.box_sizer,1, wx.EXPAND | wx.ALL,5)
        self.main_sizer.Add(self.btn_sizer,0, wx.ALIGN_RIGHT)
        self.SetSizer(self.main_sizer)

    def update_rois(self):
        ds_txt_roi=self.data.roi_data.ds_roi.get_list()
        us_txt_roi=self.data.roi_data.us_roi.get_list()
        ds_txt_roi[2:]=self.data.get_wavelength(ds_txt_roi[2:])
        us_txt_roi[2:]=self.data.get_wavelength(us_txt_roi[2:])
        self.ds_roi_box.update_roi(ds_txt_roi)
        self.us_roi_box.update_roi(us_txt_roi)

class ROIEditBox():
    def __init__(self, parent, roi, label):
        
        self.parent = parent
        self.roi = roi
        self.label = label

        self.create_controls()
        self.create_sizer()

    def create_controls(self):
        self.static_box = wx.StaticBox(self.parent, -1, self.label)
        self.static_box.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.min_lbl = wx.StaticText(self.parent, -1, 'min', style=wx.ALIGN_CENTER)
        self.max_lbl = wx.StaticText(self.parent, -1, 'max', style=wx.ALIGN_CENTER)
        self.x_lbl = wx.StaticText(self.parent, -1, 'x:')
        self.y_lbl = wx.StaticText(self.parent, -1, 'y:')
        self.x_min_txt = wx.TextCtrl(self.parent, -1, str(self.roi.x_min), size=(63,22),
                                           style =wx.ALIGN_RIGHT | wx.TE_PROCESS_ENTER, validator = IntValidator(2))
        self.x_max_txt = wx.TextCtrl(self.parent, -1, str(self.roi.x_max), size=(63,22),
                                           style =wx.ALIGN_RIGHT | wx.TE_PROCESS_ENTER, validator = IntValidator(2))
        self.y_min_txt = wx.TextCtrl(self.parent, -1, str(self.roi.y_min), size=(63,22),
                                           style =wx.ALIGN_RIGHT | wx.TE_PROCESS_ENTER, validator = IntValidator(2))
        self.y_max_txt = wx.TextCtrl(self.parent, -1, str(self.roi.y_max), size=(63,22),
                                           style =wx.ALIGN_RIGHT | wx.TE_PROCESS_ENTER, validator = IntValidator(2))

    def create_sizer(self):
        self.gb_sizer = wx.GridBagSizer(7,7)
        self.gb_sizer.Add(self.min_lbl, (0,1), flag=wx.EXPAND | wx.ALIGN_CENTER)
        self.gb_sizer.Add(self.max_lbl, (0,2), flag=wx.EXPAND | wx.ALIGN_CENTER)
        self.gb_sizer.Add(self.x_lbl, (1,0))
        self.gb_sizer.Add(self.x_min_txt, (1,1))
        self.gb_sizer.Add(self.x_max_txt, (1,2))
        self.gb_sizer.Add(self.y_lbl, (2,0))
        self.gb_sizer.Add(self.y_min_txt, (2,1))
        self.gb_sizer.Add(self.y_max_txt, (2,2))
        self.box_sizer = wx.StaticBoxSizer(self.static_box, wx.VERTICAL)
        self.box_sizer.Add(self.gb_sizer, 1, wx.EXPAND | wx.ALIGN_CENTRE)

    def get_roi(self):
        x_min = int(self.x_min_txt.GetLabel())
        x_max = int(self.x_max_txt.GetLabel())
        y_min = int(self.y_min_txt.GetLabel())
        y_max = int(self.y_max_txt.GetLabel())
        return [y_min, y_max, x_min, x_max]

    def update_roi(self, roi):
        self.x_min_txt.SetLabel(str(int(roi[2])))
        self.x_max_txt.SetLabel(str(int(roi[3])))
        self.y_min_txt.SetLabel(str(int(roi[0])))
        self.y_max_txt.SetLabel(str(int(roi[1])))

class TRaxROIGraphPanel(wx.Panel):
    def __init__(self, parent, data):
        super(TRaxROIGraphPanel, self).__init__(parent)
        
        self.data = data
        self.create_figure()
        self.create_sizer()
        self.plot_img()
        self.plot_rects()
        self.redraw_figure()
        self.connect_rects()
        self.create_bindings()

    def create_figure(self):
        self.figure = Figure(None, dpi=100)
        self.canvas = FigCanvas(self, wx.ID_ANY, self.figure)
        self.axes = self.figure.add_subplot(111)
        self.status_bar = wx.StatusBar(self, style=0)

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
        self.figure.tight_layout(None, 0.4, None, None)
        self.canvas.draw()

    def on_mouse_move(self, event):
        x_coord = event.xdata
        y_coord = event.ydata
        if x_coord <> None:
            self.status_bar.SetStatusText(u'x: %(x).0F y: %(y).0F' \
                               % {'x':self.data.get_wavelength(int(x_coord)), 'y':y_coord})
        else:
            self.status_bar.SetStatusText('')

    def plot_img(self):
        self.axes.cla()
        self.img_data=self.data.get_exp_img_data()
        self.img = self.axes.imshow(self.img_data, cmap = 'hot', aspect = 'auto')
        self.axes.set_ylim([0,len(self.img_data) - 1])
        self.axes.set_xlim([0,len(self.img_data[0]) - 1])
        self.img_background = self.canvas.copy_from_bbox(self.axes.bbox)
        self.canvas.draw()
        self.create_wavelength_x_axis()

    def create_wavelength_x_axis(self):
        xlimits = self.data.get_x_limits()
        xlimits = np.ceil(xlimits / 50.0) * 50
        xtick_num = np.arange(xlimits[0],xlimits[1],50)
        xtick_pos = self.data.calculate_ind(xtick_num)
        self.axes.set_xticks(xtick_pos)
        self.axes.set_xticklabels((map(int,xtick_num)))
        self.axes.set_xlabel("$\lambda$ $(nm)$")
        self.redraw_figure()

    def update_img(self, img_data):
        self.img.set_data(img_data)
        self.img.autoscale()
        self.canvas.draw()

    def plot_rects(self):
        self.us_rect = self.create_rect(self.data.roi_data.us_roi, 'US')
        self.ds_rect = self.create_rect(self.data.roi_data.ds_roi, 'DS')    
        self.update_rects() 

    def update_rects(self):                                    
        self.canvas.restore_region(self.img_background)
        self.axes.draw_artist(self.us_rect.rect)
        self.axes.draw_artist(self.ds_rect.rect)
        self.canvas.blit(self.axes.bbox)

    def create_rect(self, roi, flag):
        return ResizeableRectangle(self, self.axes, self.canvas,wx.Rect(roi.x_min,roi.y_min, roi.get_width(),roi.get_height()), flag)

    def connect_rects(self):
        self.us_rect.connect()
        self.ds_rect.connect()

    def set_rois(self):
        self.us_rect.set_roi(self.data.roi_data.us_roi)
        self.ds_rect.set_roi(self.data.roi_data.ds_roi)

class ResizeableRectangle:
    lock = None #only one rect can be animated at a time
    def __init__(self, parent, axes, canvas, init_rect, flag):       
        self.flag = flag
        self.parent = parent
        self.axes = axes
        self.canvas = canvas
        
        self.xlim = self.axes.get_xlim()
        self.ylim = self.axes.get_ylim()

        self.x_border = 25
        self.y_border = 3
        self.min_width = 100
        self.min_height = 1

        self.rect = mpl.patches.Rectangle((init_rect.x,init_rect.y),init_rect.width, init_rect.height, ec='w', fill=False, lw=2)
        self.axes.add_artist(self.rect)
               
        self.press = None 
        self.mode = None

    def set_roi(self, roi): 
        if self.press == None:
            self.rect.set_y(roi.y_min)
            self.rect.set_x(roi.x_min)
            self.rect.set_height(roi.get_height())
            self.rect.set_width(roi.get_width())
            self.rect.figure.canvas.draw()

    def connect(self):
        self.cidpress = self.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.rect.axes: return
        if ResizeableRectangle.lock is not None: return
        y_click = event.ydata
        x_click = event.xdata
        y0 = self.rect.get_y()
        x0 = self.rect.get_x()
        height = self.rect.get_height()
        width = self.rect.get_width()

        if y_click >= y0 - self.y_border and y_click <= y0 + height + self.y_border and \
            x_click >= x0 - self.x_border and x_click <= x0 + width + self.x_border:
            self.set_mode(x_click, y_click, x0, y0, width, height)
            self.press = x0, y0, x_click, y_click
            #self.rect.set_animated(True)
            ResizeableRectangle.lock = self

    def set_mode(self,x_click, y_click, x0, y0, width, height):
        if y_click >= y0 + self.y_border and y_click <= y0 + height - self.y_border and \
            x_click >= x0 + self.x_border and x_click <= x0 + width - self.x_border:
            self.mode = 'move'
        elif y_click > y0 + height - self.y_border and y_click <= y0 + height + self.y_border and \
            x_click >= x0 + self.x_border and x_click <= x0 + width - self.x_border:
            self.mode = 'resize_top'
        elif y_click > y0 - self.y_border and y_click < y0 + self.y_border and \
            x_click >= x0 + self.x_border and x_click <= x0 + width - self.x_border:
            self.mode = 'resize_bottom'
        elif x_click > x0 + width - self.x_border and x_click <= x0 + width + self.x_border and \
            y_click >= y0 - self.y_border and y_click <= y0 + height + self.y_border:
            self.mode = 'resize_right'
        elif x_click > x0 - self.x_border and x_click < x0 + self.x_border and \
            y_click >= y0 - self.y_border and y_click <= y0 + height + self.y_border:
            self.mode = 'resize_left'

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.rect.axes: return
        
        y_click = event.ydata
        x_click = event.xdata
        x0, y0, xpress, ypress = self.press
        dy = event.ydata - ypress
        dx = event.xdata - xpress
        height = self.rect.get_height()
        width = self.rect.get_width()

        if self.mode == 'move':
            y_new_pos = int(y0 + dy)
            x_new_pos = int(x0 + dx)
            top_pos = y_new_pos + height
            right_pos = x_new_pos + width
            if y_new_pos >= 0 and (top_pos) <= self.ylim[1]:
                self.rect.set_y(y_new_pos)
            elif y_new_pos <= 0:
                self.rect.set_y(0)
            elif top_pos > self.ylim[1]:
                self.rect.set_y(self.ylim[1] - height)

            if x_new_pos >= 0 and (right_pos) <= self.xlim[1]:
                self.rect.set_x(x_new_pos)
            elif x_new_pos <= 0:
                self.rect.set_x(0)
            elif right_pos > self.xlim[1]:
                self.rect.set_x(self.xlim[1] - width)

        elif self.mode == 'resize_top':
            new_height = int(event.ydata - y0)
            if new_height < self.min_height:
                new_height = self.min_height
            self.rect.set_height(new_height)
        elif self.mode == 'resize_bottom':
            new_height = int(self.rect.get_y() - y_click + height)
            if new_height < self.min_height:
                new_height = self.min_height
            self.rect.set_height(new_height)
            self.rect.set_y(int(self.rect.get_y() + height - new_height))
        elif self.mode == 'resize_right':
            new_width = int(event.xdata - x0)
            if new_width < self.min_width:
                new_width = self.min_width
            self.rect.set_width(new_width)
        elif self.mode == 'resize_left':
            new_width = int(self.rect.get_x() - x_click + width)
            if new_width < self.min_width:
                new_width = self.min_width
            self.rect.set_width(new_width)
            self.rect.set_x(int(self.rect.get_x() + width - new_width))

        self.send_message()
        self.parent.update_rects()

    def send_message(self):
        pub.sendMessage(self.flag + " ROI GRAPH CHANGED", 
                        [int(self.rect.get_y()),int(self.rect.get_y() + self.rect.get_height()),
                         int(self.rect.get_x()),int(self.rect.get_x() + self.rect.get_width())])

    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.mode = None
        ResizeableRectangle.lock = None
        self.rect.set_animated(False)


        


if __name__ == "__main__":
    spe_file = SPE_File('spe files\Pt_230.SPE')
    data = TraxData()
    data.load_exp_data('spe files\Pt_230.SPE')
    app = wx.App(None)
    TRaxROIController(None,data)
    
    app.MainLoop()







