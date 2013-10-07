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

from TRaxROISelector.T_Rax_ROI_panels import TRaxROIControlPanel, TRaxROIGraphPanel

class TRaxROIView(wx.MiniFrame):
    def __init__(self, parent, data):
        wx.MiniFrame.__init__(self, parent, -1, 'ROI Setup', pos=(0,550), size=(900,350), style=wx.DEFAULT_FRAME_STYLE)
        self.data = data
        self.init_UI()
        self.SetMinSize((600,310))
        self.Show()

    def init_UI(self):
        self.create_panels()
        self.create_sizers()

    def create_panels(self):
        self.main_panel = wx.Panel(self)
        self.main_panel.SetBackgroundColour((255,255,150))
        self.control_panel = TRaxROIControlPanel(self.main_panel,self.data)
        self.graph_panel = TRaxROIGraphPanel(self.main_panel,self.data)

    def create_sizers(self):
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer.AddMany([(self.graph_panel, 1 , wx.RIGHT | wx.EXPAND),(self.control_panel,0)])
        self.main_panel.SetSizer(self.main_sizer)
