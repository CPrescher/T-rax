import wx
import numpy as np
from Helper import IntValidator


class ROIEditBox():
    def __init__(self, parent, roi, label, color):
        self.parent = parent
        self.roi = roi
        self.label = label
        self.color = color
        self.create_controls()
        self.create_sizer()

    def create_controls(self):
        self.panel = wx.Panel(self.parent, -1)
        self.panel.SetBackgroundColour(self.color)
        self.static_box = wx.StaticBox(self.panel, -1, self.label)
        self.static_box.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.min_lbl = wx.StaticText(self.panel, -1, 'min', style=wx.ALIGN_CENTER)
        self.max_lbl = wx.StaticText(self.panel, -1, 'max', style=wx.ALIGN_CENTER)
        self.x_lbl = wx.StaticText(self.panel, -1, 'x:')
        self.y_lbl = wx.StaticText(self.panel, -1, 'y:')
        self.x_min_txt = wx.TextCtrl(self.panel, -1, str(int(np.round(self.roi[2]))), size=(63,22),
                                           style =wx.ALIGN_RIGHT | wx.TE_PROCESS_ENTER, validator = IntValidator(2))
        self.x_max_txt = wx.TextCtrl(self.panel, -1, str(int(np.round(self.roi[3]))), size=(63,22),
                                           style =wx.ALIGN_RIGHT | wx.TE_PROCESS_ENTER, validator = IntValidator(2))
        self.y_min_txt = wx.TextCtrl(self.panel, -1, str(int(np.round(self.roi[0]))), size=(63,22),
                                           style =wx.ALIGN_RIGHT | wx.TE_PROCESS_ENTER, validator = IntValidator(2))
        self.y_max_txt = wx.TextCtrl(self.panel, -1, str(int(np.round(self.roi[1]))), size=(63,22),
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
        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_sizer.Add(self.box_sizer, 0, wx.EXPAND | wx.ALL, 7)
        self.panel.SetSizer(self.panel_sizer)

    def get_roi(self):
        x_min = int(self.x_min_txt.GetLabel())
        x_max = int(self.x_max_txt.GetLabel())
        y_min = int(self.y_min_txt.GetLabel())
        y_max = int(self.y_max_txt.GetLabel())
        return [y_min, y_max, x_min, x_max]

    def update_roi(self, roi):
        self.x_min_txt.SetLabel(str(int(np.round(roi[2]))))
        self.x_max_txt.SetLabel(str(int(np.round(roi[3]))))
        self.y_min_txt.SetLabel(str(int(np.round(roi[0]))))
        self.y_max_txt.SetLabel(str(int(np.round(roi[1]))))

    def Hide(self):
        self.panel.Hide()

    def Show(self):
        self.panel.Show()

class XLimitBox():
    def __init__(self, parent, limits, label):
        self.parent = parent
        self.limits = limits
        self.create_controls()
        self.create_sizer()

    def create_controls(self):
        self.panel = wx.Panel(self.parent, -1)
        self.panel.SetBackgroundColour
        self.box = wx.StaticBox(self.panel,-1, 'X - Limits')
        self.box.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.from_lbl = wx.StaticText(self.panel, -1, 'From')
        self.to_lbl = wx.StaticText(self.panel, -1, 'To')
        self.from_txt = wx.TextCtrl(self.panel, -1,  str(int(self.limits[0])), size=(55,24),
                                    style =wx.ALIGN_RIGHT | wx.TE_PROCESS_ENTER, validator = IntValidator(2))
        self.from_unit_lbl = wx.StaticText(self.panel, -1, 'nm')
        self.to_txt = wx.TextCtrl(self.panel, -1, str(int(self.limits[1])),size=(55,24),
                                    style =wx.ALIGN_RIGHT | wx.TE_PROCESS_ENTER, validator = IntValidator(2))
        self.to_unit_lbl = wx.StaticText(self.panel, -1, 'nm')

    def create_sizer(self):
        self.gb_sizer = wx.GridBagSizer(7,7)
        self.gb_sizer.Add(self.from_lbl, (0,0), flag = wx.ALL | wx.ALIGN_CENTER)
        self.gb_sizer.Add(self.to_lbl, (0,1),  flag =wx.ALL | wx.ALIGN_CENTER)

        self.from_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.from_sizer.AddMany([(self.from_txt, 1, wx.EXPAND | wx.ALIGN_CENTER),
                                 (self.from_unit_lbl, 0, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)])
        self.to_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.to_sizer.AddMany([(self.to_txt, 1, wx.EXPAND | wx.ALIGN_CENTER),
                                 (self.to_unit_lbl, 0, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)])
        self.gb_sizer.Add(self.from_sizer, (1,0), flag = wx.ALL | wx.ALIGN_CENTER | wx.EXPAND)
        self.gb_sizer.Add(self.to_sizer, (1,1), flag = wx.ALL | wx.ALIGN_CENTER | wx.EXPAND)

        self.gb_sizer.AddGrowableCol(1)
        self.box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        self.box_sizer.Add(self.gb_sizer, 0, wx.EXPAND)
        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_sizer.Add(self.box_sizer, 0, wx.EXPAND)
        self.panel.SetSizer(self.panel_sizer)

    def update_limits(self, limits):
        self.from_txt.SetLabel(str(int(np.round(limits[0]))))
        self.to_txt.SetLabel(str(int(np.round(limits[1]))))

    def get_limits(self):
        return [int(self.from_txt.GetLabel()), int(self.to_txt.GetLabel())]

    def Hide(self):
        self.panel.Hide()

    def Show(self):
        self.panel.Show()