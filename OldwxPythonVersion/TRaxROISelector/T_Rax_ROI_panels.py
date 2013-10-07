import wx
import matplotlib as mpl
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from wx.lib.pubsub import Publisher as pub


import colors
import copy

from TRaxROISelector.T_Rax_ROI_boxes import ROIEditBox, XLimitBox
from TRaxROISelector.T_Rax_ROI_graph_helper import MoveableLine, ResizeableRectangle


class TRaxROIControlPanel(wx.Panel):
    def __init__(self, parent, data):
        super(TRaxROIControlPanel, self).__init__(parent)
        self.data = data
        self.create_controls()
        self.SetBackgroundColour(colors.BACKGROUND_COLOR)

        self.set_sizer()

    def create_controls(self):
        us_roi = self.data.roi_data.us_roi.get_list()
        us_roi[2:] = self.data.calculate_wavelength(us_roi[2:])
        ds_roi = self.data.roi_data.ds_roi.get_list()
        ds_roi[2:] = self.data.calculate_wavelength(ds_roi[2:])

        
        self.us_roi_box = ROIEditBox(self, us_roi, 'Upstream ROI', colors.UPSTREAM_COLOR)
        self.ds_roi_box = ROIEditBox(self, ds_roi, 'Downstream ROI', colors.DOWNSTREAM_COLOR)
        self.limits_box = XLimitBox(self, self.data.calculate_wavelength(self.data.roi_data.ds_roi.get_list()[2:]), 'X - Limits')
        self.create_buttons()

    def create_buttons(self):
        self.ok_button = wx.Button(self, wx.ID_OK, 'OK', size=(63,26))
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, 'Cancel', size=(63,26))
        self.btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_sizer.AddMany([(self.ok_button,0,wx.ALL,3),(self.cancel_button,0,wx.ALL,3)])    

    def set_sizer(self):
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.us_roi_box.panel,0, wx.EXPAND)
        self.main_sizer.Add(self.ds_roi_box.panel,0, wx.EXPAND)
        self.main_sizer.Add(self.limits_box.panel, 0, wx.EXPAND)
        self.main_sizer.Add(self.btn_sizer,0, wx.ALIGN_RIGHT)
        self.SetSizer(self.main_sizer)

    def update_rois(self):
        ds_txt_roi = self.data.roi_data.ds_roi.get_list()
        us_txt_roi = self.data.roi_data.us_roi.get_list()
        ds_txt_roi[2:] = self.data.calculate_wavelength(ds_txt_roi[2:])
        us_txt_roi[2:] = self.data.calculate_wavelength(us_txt_roi[2:])
        self.ds_roi_box.update_roi(ds_txt_roi)
        self.us_roi_box.update_roi(us_txt_roi)
        self.limits_box.update_limits(ds_txt_roi[2:])



class TRaxROIGraphPanel(wx.Panel):
    def __init__(self, parent, data):
        super(TRaxROIGraphPanel, self).__init__(parent)
        
        self.data = data
        self.create_figure()
        self.create_sizer()

    def draw_image(self):
        try:
            self.plot_img()
            self.plot_rects()
            self.connect_rects()
            self.update_rects()
            self.mode = 'IMG'
            pub.sendMessage("IMG LOADED", None)
        except NotImplementedError, e:
            self.plot_graph()
            self.plot_lines()
            self.connect_lines()
            self.update_lines()
            self.mode = 'GRAPH'
            pub.sendMessage("GRAPH LOADED", None)

    def create_figure(self):
        self.figure = Figure(None, dpi=100)
        self.canvas = FigCanvas(self, wx.ID_ANY, self.figure)
        self.axes = self.figure.add_subplot(111)

    def create_sizer(self):
        box_sizer = wx.BoxSizer(wx.VERTICAL)
        box_sizer.Add(self.canvas,1, flag = wx.EXPAND)
        self.SetSizer(box_sizer)


    def resize_graph(self, event):
        border = 5
        w,h = event.GetSize()
        self.figure.set_size_inches([w / 100.0,h / 100.0])
        self.redraw_figure()

    def redraw_figure(self):
        self.figure.tight_layout(None, 0.4, None, None)
        self.canvas.draw()

    def plot_img(self):
        self.axes.cla()
        self.img_data = self.data.get_exp_img_data()
        y_max = len(self.data.get_exp_img_data()) - 1
        x_max = len(self.data.get_exp_img_data()[0]) - 1
        self.axes.set_ylim([0,y_max])
        self.axes.set_xlim([0,x_max])
        scaling = mpl.colors.Normalize()
        scaling.autoscale(self.img_data)
        self.img = self.axes.imshow(self.img_data, cmap = 'hot', aspect = 'auto',
                                    extent=[0,x_max + 1,y_max + 1,0],
                                    norm=scaling)
        self.axes.set_ylim([0,len(self.img_data) - 1])
        self.axes.set_xlim([0,len(self.img_data[0]) - 1])
        self.axes.invert_yaxis()
        self.img.autoscale()
        self.img_background = self.canvas.copy_from_bbox(self.axes.bbox)
        self.canvas.draw()
        self.create_wavelength_x_axis()
        self.redraw_figure()

    def plot_graph(self):
        self.axes.cla()
        self.graph_spec = self.data.get_exp_graph_data()
        self.axes.set_xlim(self.graph_spec.get_x_plot_limits())
        self.axes.set_ylim(self.graph_spec.get_y_plot_limits())
        self.graph = self.axes.plot(self.graph_spec.x, self.graph_spec.y, 'c-', lw=1)
        self.graph_background = self.canvas.copy_from_bbox(self.axes.bbox)
        self.canvas.draw()
        self.redraw_figure()

    def create_wavelength_x_axis(self):
        xlimits = self.data.get_x_limits()
        increment = self.get_x_axis_increment()
        xlimits = np.ceil(xlimits / increment) * increment
        xtick_num = np.arange(xlimits[0],xlimits[1],increment)
        xtick_pos = self.data.calculate_ind(xtick_num)
        self.axes.set_xticks(xtick_pos)
        self.axes.set_xticklabels((map(int,xtick_num)))

    def get_x_axis_increment(self):
        xlimits = self.data.get_x_limits()
        #try different binnings
        increments = [50,25,10,5,2,1]
        for increment in increments:
            x_tick_num=np.arange(xlimits[0],xlimits[1],increment)
            if len(x_tick_num)>5:
                return increment
        return 0.5

    def update_img(self):
        self.draw_image()

    def plot_rects(self):
        self.us_rect = self.create_rect(self.data.roi_data.us_roi, colors.UPSTREAM_COLOR_NORM, 'US')
        self.ds_rect = self.create_rect(self.data.roi_data.ds_roi, colors.DOWNSTREAM_COLOR_NORM, 'DS')    
        self.update_rects() 
        self.update_lines()

    def update_rects(self):
        self.axes.draw_artist(self.us_rect.rect)
        self.axes.draw_artist(self.ds_rect.rect)
        self.canvas.blit(self.axes.bbox)
    
    def create_rect(self, roi, color, flag):
        return ResizeableRectangle(self, self.axes, self.canvas,wx.Rect(roi.x_min,roi.y_min, roi.get_width(),roi.get_height()), color, flag)

    def connect_rects(self):
        self.us_rect.connect()
        self.ds_rect.connect()

    def set_rois(self):
        try:
            self.us_rect.set_roi(self.data.roi_data.us_roi)
            self.ds_rect.set_roi(self.data.roi_data.ds_roi)
        except:
            self.min_line.set_roi(self.data.calculate_wavelength(self.data.roi_data.us_roi.x_min))
            self.max_line.set_roi(self.data.calculate_wavelength(self.data.roi_data.us_roi.x_max))

    def plot_lines(self):
        x_limits = self.data.calculate_wavelength(self.data.roi_data.us_roi.get_x_limits())
        axes_xlim = self.axes.get_xlim()
                                             
        self.min_line = self.create_line(x_limits[0], [axes_xlim[0], x_limits[1] - 1],"MIN")
        self.max_line = self.create_line(x_limits[1], [x_limits[0] + 1, axes_xlim[1]],"MAX")

    def create_line(self, pos, limits, flag):
        return MoveableLine(self, self.axes, self.canvas,pos, limits, flag)

    def update_lines(self):
        self.redraw_figure()

    def update_line_limits(self):
        x_limits = self.data.calculate_wavelength(self.data.roi_data.us_roi.get_x_limits())
        axes_xlim = self.axes.get_xlim()
        self.min_line.set_limit([axes_xlim[0], x_limits[1] - 1])
        self.max_line.set_limit([x_limits[0] + 1, axes_xlim[1]])                       

    def connect_lines(self):
        self.min_line.connect()
        self.max_line.connect()