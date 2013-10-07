import wx
import matplotlib as mpl
mpl.rcParams['font.size'] = 9
mpl.rcParams['lines.linewidth'] = 0.5
mpl.rcParams['lines.color'] = 'g'
mpl.rcParams['text.color'] = 'white'
mpl.rc('axes', facecolor='black', edgecolor='white', labelcolor='white')
mpl.rc('xtick', color='white')
mpl.rc('ytick', color='white')
mpl.rc('figure', facecolor='black', edgecolor='black')

import numpy as np
import random
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from Helper import IntValidator   
from T_Rax_Data import black_body_function, Spectrum, FitSpectrum


#text font parameter:
class TraxMainWindow(wx.Frame):
    def __init__(self, controller):
        wx.Frame.__init__(self, None, -1, 'T-Rax ver 0.1', size=(900,450), style = wx.DEFAULT_FRAME_STYLE | wx.CLIP_CHILDREN)
        self.controller = controller
        self.init_UI()
        self.Show()

    def init_UI(self):
        self.create_panels()
        self.create_notebook()
        self.create_sizers()

    def create_panels(self):
        self.main_panel = wx.Panel(self)
        self.control_panel = wx.Panel(self.main_panel)
        self.graph_panel = TraxMainGraphPanel(self.main_panel)

    def create_notebook(self):
        self.note_book = wx.Notebook(self.control_panel, -1, style = wx.BK_TOP)
        self.exp_panel = TraxExpControlPanel(self.note_book)
        self.calib_panel = TraxCalibControlPanel(self.note_book)
        self.note_book.AddPage(self.exp_panel,'Experiment')
        self.note_book.AddPage(self.calib_panel, 'Calibration')
        self.control_sizer = wx.BoxSizer(wx.VERTICAL)
        self.control_sizer.Add(self.note_book,1,wx.ALL)
        self.control_panel.SetSizer(self.control_sizer)

    def create_sizers(self):
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer.AddMany([(self.graph_panel, 1 ,wx.EXPAND),(self.control_panel,0, wx.EXPAND)])
        self.main_panel.SetSizer(self.main_sizer)
        self.Layout()
        self.SetMinSize((900,450))

class TraxExpControlPanel(wx.Panel):
    def __init__(self, parent):
        super(TraxExpControlPanel, self).__init__(parent)        
        self.static_box_font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.file_lbl_font = wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.file_lbl_color_None = (20,118,10)
        self.file_lbl_color_loaded = (30,30,255)
        
        self.SetBackgroundColour((255,255,255))

        self.create_controls()
        self.set_sizer()

    def create_controls(self):
        self.create_experiment_box()
        self.create_fit_box()
        self.roi_setup_btn = wx.Button(self, -1, 'ROI Setup')

    def create_experiment_box(self):
        self.exp_box = wx.StaticBox(self,-1, 'Experiment')
        self.exp_box.SetFont(self.static_box_font)
        self.exp_load_data_btn = wx.Button(self, wx.ID_ANY, 'Load Data')

        self.exp_file_lbl = wx.StaticText(self, -1, 'Select file...')
        self.exp_file_lbl.SetForegroundColour(self.file_lbl_color_None)
        self.exp_file_lbl.SetFont(self.file_lbl_font)

        self.exp_previous_btn = wx.Button(self, wx.ID_ANY,'<-', size=(30,20))
        self.exp_next_btn = wx.Button(self, wx.ID_ANY, '->', size=(30,20))
        self.exp_auto_process_cb = wx.CheckBox(self, -1, 'autoprocess')
        self.exp_folder_lbl = wx.StaticText(self, -1, 'Folder')
        self.exp_folder_lbl.SetForegroundColour(self.file_lbl_color_None)
        self.exp_folder_lbl.SetFont(self.file_lbl_font)

        self.exp_subtract_background_cb = wx.CheckBox(self, -1, 'Subtract Background')
        self.exp_load_bkg_btn = wx.Button(self, -1, 'Background Setup')

    def create_fit_box(self):
        self.fit_box = wx.StaticBox(self,-1, 'Fitting parameters')
        self.fit_box.SetFont(self.static_box_font)
        self.fit_from_lbl = wx.StaticText(self, -1, 'From')
        self.fit_to_lbl = wx.StaticText(self, -1, 'To')
        self.fit_from_txt = wx.TextCtrl(self, -1, '500', size=(75,24),
                                    style =wx.ALIGN_RIGHT | wx.TE_PROCESS_ENTER, validator = IntValidator(2))
        self.fit_from_unit_lbl = wx.StaticText(self, -1, 'nm')
        self.fit_to_txt = wx.TextCtrl(self, -1, '900',size=(75,24), 
                                    style =wx.ALIGN_RIGHT | wx.TE_PROCESS_ENTER, validator = IntValidator(2))
        self.fit_to_unit_lbl = wx.StaticText(self, -1, 'nm')

    def set_experiment_sizer(self):
        self.experiment_walk_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.experiment_walk_sizer.AddMany([(self.exp_previous_btn, 1, wx.ALL | wx.EXPAND),
                                            (self.exp_next_btn, 1, wx.ALL | wx.EXPAND)])
        self.experiment_gb_sizer = wx.GridBagSizer(7,7)
        self.experiment_gb_sizer.Add(self.exp_load_data_btn, (0,0))
        self.experiment_gb_sizer.Add(self.exp_file_lbl, (0,1), flag=wx.ALL | wx.ALIGN_CENTRE_VERTICAL, border=3)
        self.experiment_gb_sizer.Add(self.experiment_walk_sizer, (1,0), flag=wx.EXPAND)
        self.experiment_gb_sizer.Add(self.exp_auto_process_cb, (1,1), flag=wx.ALL | wx.ALIGN_CENTRE_VERTICAL, border=3)
        self.experiment_gb_sizer.Add(self.exp_folder_lbl, (2,0),(1,2),flag=wx.ALL | wx.ALIGN_CENTRE_VERTICAL, border=3)
        self.experiment_gb_sizer.Add(wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL),
                                     (3,0),(1,2), flag=wx.EXPAND)

        self.experiment_gb_sizer.Add(self.exp_load_bkg_btn, (4,0), (1,2), flag =wx.EXPAND)
        self.experiment_gb_sizer.Add(self.exp_subtract_background_cb, (5,0),(1,2), flag=wx.ALL | wx.ALIGN_CENTRE_VERTICAL, border=3)

        self.experiment_gb_sizer.AddGrowableCol(1)
        self.experiment_box_sizer = wx.StaticBoxSizer(self.exp_box, wx.VERTICAL)
        self.experiment_box_sizer.Add(self.experiment_gb_sizer, 1, wx.EXPAND | wx.ALIGN_CENTRE)
 
    def set_fit_sizer(self):
        self.fit_gb_sizer = wx.GridBagSizer(7,7)
        self.fit_gb_sizer.Add(self.fit_from_lbl, (0,0), flag = wx.ALL | wx.ALIGN_CENTER)
        self.fit_gb_sizer.Add(self.fit_to_lbl, (0,1),  flag =wx.ALL | wx.ALIGN_CENTER)

        self.fit_from_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.fit_from_sizer.AddMany([(self.fit_from_txt, 1, wx.EXPAND | wx.ALIGN_CENTER),
                                     (self.fit_from_unit_lbl, 0, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)])
        self.fit_to_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.fit_to_sizer.AddMany([(self.fit_to_txt, 1, wx.EXPAND | wx.ALIGN_CENTER),
                                     (self.fit_to_unit_lbl, 0, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)])
        self.fit_gb_sizer.Add(self.fit_from_sizer, (1,0), flag = wx.ALL | wx.ALIGN_CENTER | wx.EXPAND)
        self.fit_gb_sizer.Add(self.fit_to_sizer, (1,1), flag = wx.ALL | wx.ALIGN_CENTER | wx.EXPAND)

        self.fit_gb_sizer.AddGrowableCol(1)
        self.fit_box_sizer = wx.StaticBoxSizer(self.fit_box, wx.VERTICAL)
        self.fit_box_sizer.Add(self.fit_gb_sizer, 1, wx.EXPAND)
                                    
    def set_sizer(self):
        self.set_experiment_sizer()
        self.set_fit_sizer()
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.experiment_box_sizer, 0, wx.ALL | wx.EXPAND, 7)
        self.main_sizer.Add(self.roi_setup_btn, 0, wx.ALL | wx.EXPAND, 7)
        self.main_sizer.Add(self.fit_box_sizer,0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL,7)
        self.Layout()
        self.SetSizerAndFit(self.main_sizer)

    def set_fit_x_limits(self, limits):
        self.fit_from_txt.SetLabel(str(int(np.round(limits[0]))))
        self.fit_to_txt.SetLabel(str(int(np.round(limits[1]))))

    def get_fit_x_limits(self):
        x_min = int(self.fit_from_txt.GetLabel())
        x_max = int(self.fit_to_txt.GetLabel())
        return [x_min, x_max]

    def hide_folder_lbl(self):
        self.experiment_gb_sizer.Hide(self.exp_folder_lbl)
        
        self.Layout()
        self.experiment_gb_sizer.Layout()

    def show_folder_lbl(self):
        self.experiment_gb_sizer.Show(self.exp_folder_lbl)
        self.Layout()
        self.experiment_gb_sizer.Layout()

class TraxMainGraphPanel(wx.Panel):
    def __init__(self, parent):
        super(TraxMainGraphPanel, self).__init__(parent)
        self.figure = Figure(None, dpi=100)
        self.canvas = FigCanvas(self, wx.ID_ANY, self.figure)
        self.status_bar = wx.StatusBar(self, style=0)

        box_sizer = wx.BoxSizer(wx.VERTICAL)
        box_sizer.Add(self.canvas,1, flag = wx.EXPAND)
        box_sizer.Add(self.status_bar, 0, wx.EXPAND)
        self.SetSizer(box_sizer)

        self.ds_axes = self.figure.add_subplot(121)
        self.us_axes = self.figure.add_subplot(122)
    
        self.create_ds_graph()
        self.create_us_graph()
        self.redraw_figure()
        #make the thing resizable:
        self.canvas.Bind(wx.EVT_SIZE, self.resize_graph)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

    def resize_graph(self, event):
        w,h = event.GetSize()
        self.figure.set_size_inches([w / 100.0,h / 100.0])
        self.redraw_figure()

    def on_mouse_move(self, event):
        x_coord = event.xdata
        y_coord = event.ydata
        if x_coord <> None:
            self.status_bar.SetStatusText('x: %(x).3F y: %(y).3F' \
                               % {'x':x_coord, 'y':y_coord})
        else:
            self.status_bar.SetStatusText('')

    def create_us_graph(self):
        self.us_data_line , self.us_fit_line, self.us_temp_txt, \
            self.us_int_txt, self.us_warning_txt, self.us_calib_file_txt = \
            self.create_axes_lines(self.us_axes)    
        self.us_axes.set_title('UPSTREAM', color=(1,0.55,0), weight = 'bold', va='bottom')
        
    def create_ds_graph(self):
        self.ds_data_line , self.ds_fit_line, self.ds_temp_txt, \
            self.ds_int_txt, self.ds_warning_txt, self.ds_calib_file_txt = \
            self.create_axes_lines(self.ds_axes)  
        self.ds_axes.set_title('DOWNSTREAM', color=(1, 1, 0), weight = 'bold', va='bottom') 

    def create_axes_lines(self, axes):
        fit_line, = axes.plot([], [], 'r-',  lw=3)
        data_line, = axes.plot([], [], '-', color = (0.7,0.9,0.9), lw=1)
        temp_txt = axes.text(0,0, '', size=20, ha='left', va='top')
        int_txt = axes.text(0,0,'',size=13, color = (0.04,0.76,0.17), ha='right')
        warning_txt=axes.text(0,0,'', size=25, color = 'r', va='center', ha='center', weight = 'bold') 
        calib_file_txt = axes.text(0,0, '', size=9, color =  (0.04,0.76,0.17), ha='left', va='top', weight = 'bold')

        axes.yaxis.set_visible(False)
        axes.set_xlabel('$\lambda$ $(nm)$', size=11)
        return data_line, fit_line, temp_txt, int_txt, warning_txt, calib_file_txt

    def update_graph(self, ds_spectrum, us_spectrum, ds_max_int, us_max_int, ds_calib_fname, us_calib_fname):
        if isinstance(ds_spectrum,list):
            ds_exp_spectrum = ds_spectrum[0]
            ds_fit_spectrum = ds_spectrum[1]
        else:
            ds_exp_spectrum = ds_spectrum
            ds_fit_spectrum = None

        if isinstance(us_spectrum,list):
            us_exp_spectrum = us_spectrum[0]
            us_fit_spectrum = us_spectrum[1]
        else:
            us_exp_spectrum = us_spectrum
            us_fit_spectrum = None

        self.ds_data_line.set_data(ds_exp_spectrum.get_data())
        self.ds_axes.set_xlim(ds_exp_spectrum.get_x_plot_limits())
        self.ds_axes.set_ylim(ds_exp_spectrum.get_y_plot_limits())
        self.us_data_line.set_data(us_exp_spectrum.get_data())
        self.us_axes.set_xlim(us_exp_spectrum.get_x_plot_limits())
        self.us_axes.set_ylim(us_exp_spectrum.get_y_plot_limits())

        #Temperature labels:
        if ds_fit_spectrum==None:
            self.ds_temp_txt.set_text('')
            self.ds_fit_line.set_data([[],[]])
        else:
            self.ds_temp_txt.set_text('{0:.0f} K $\pm$ {1:.0f}'.format(ds_fit_spectrum.T, ds_fit_spectrum.T_err))
            self.ds_fit_line.set_data(ds_fit_spectrum.get_data())
            self.ds_temp_txt.set_x(min(ds_exp_spectrum.x)+0.05*ds_exp_spectrum.get_x_range())
            self.ds_temp_txt.set_y(min(ds_exp_spectrum.y)+0.9*ds_exp_spectrum.get_y_range()*1.05)

        if us_fit_spectrum==None:
            self.us_temp_txt.set_text('')
            self.us_fit_line.set_data([[],[]])
        else:
            self.us_temp_txt.set_text('{0:.0f} K $\pm$ {1:.0f}'.format(us_fit_spectrum.T, us_fit_spectrum.T_err))
            self.us_fit_line.set_data(us_fit_spectrum.get_data())
            self.us_temp_txt.set_x(min(us_exp_spectrum.x)+0.05*us_exp_spectrum.get_x_range())
            self.us_temp_txt.set_y(min(us_exp_spectrum.y)+0.9*us_exp_spectrum.get_y_range()*1.05)

        #Maximum intensity:
        self.ds_int_txt.set_text('Max Int: {0:,.0f}'.format(ds_max_int))
        self.ds_int_txt.set_x(min(ds_exp_spectrum.x)+0.97*ds_exp_spectrum.get_x_range())
        self.ds_int_txt.set_y(min(ds_exp_spectrum.y)+0.03*ds_exp_spectrum.get_y_range())

        self.us_int_txt.set_text('Max Int: {0:,.0f}'.format(us_max_int))
        self.us_int_txt.set_x(min(us_exp_spectrum.x)+0.97*us_exp_spectrum.get_x_range())
        self.us_int_txt.set_y(min(us_exp_spectrum.y)+0.03*us_exp_spectrum.get_y_range())

        #do a warning if it is over a specific value:
        if ds_max_int>=64400:
            self.ds_warning_txt.set_text('SATURATION')
            self.ds_warning_txt.set_x(min(ds_exp_spectrum.x)+0.5*ds_exp_spectrum.get_x_range())
            self.ds_warning_txt.set_y(min(ds_exp_spectrum.y)+0.5*ds_exp_spectrum.get_y_range())
        else:
            self.ds_warning_txt.set_text('')

        if us_max_int>=64400:
            self.us_warning_txt.set_text('SATURATION')
            self.us_warning_txt.set_x(min(us_exp_spectrum.x)+0.5*us_exp_spectrum.get_x_range())
            self.us_warning_txt.set_y(min(us_exp_spectrum.y)+0.5*us_exp_spectrum.get_y_range())
        else:
            self.us_warning_txt.set_text('')

        #Calibration files:
        str='\\'.join(ds_calib_fname.split('\\')[-3:])
        self.ds_calib_file_txt.set_text(str)
        self.ds_calib_file_txt.set_x(min(ds_exp_spectrum.x)+0.03*ds_exp_spectrum.get_x_range())
        self.ds_calib_file_txt.set_y(min(ds_exp_spectrum.y)+0.96*ds_exp_spectrum.get_y_range()*1.05)

        str='\\'.join(us_calib_fname.split('\\')[-3:])
        self.us_calib_file_txt.set_text(str)
        self.us_calib_file_txt.set_x(min(us_exp_spectrum.x)+0.03*us_exp_spectrum.get_x_range())
        self.us_calib_file_txt.set_y(min(us_exp_spectrum.y)+0.96*us_exp_spectrum.get_y_range()*1.05)

        self.canvas.draw()

    def redraw_figure(self):
        self.figure.tight_layout(None, 1.2, None, None)
        self.canvas.draw()


        
class TraxCalibControlPanel(wx.Panel):
    def __init__(self, parent):
        super(TraxCalibControlPanel, self).__init__(parent)        
        self.static_box_font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.file_lbl_font = wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.file_lbl_color_None = (20,118,10)
        self.file_lbl_color_loaded = (30,30,255)
        self.SetBackgroundColour((255,255,150))
        self.create_controls()
        self.set_sizer()

    def create_controls(self):
        self.us_calib_box = CalibBox(self, 'Upstream', (255,140,0))
        self.ds_calib_box = CalibBox(self, 'Downstream', (255,255,0))

    def set_sizer(self):
        self.main_sizer=wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.AddMany([(self.us_calib_box.panel, 0, wx.EXPAND),
                                 (self.ds_calib_box.panel, 0, wx.EXPAND)])
        self.SetSizer(self.main_sizer)
    

class CalibBox():
    def __init__(self, parent, label, color):
        self.label = label
        self.parent = parent
        self.color = color
        self.create_controls()
        self.set_sizer()

    def create_controls(self):
        self.panel = wx.Panel(self.parent,-1)
        self.panel.SetBackgroundColour(self.color)
        self.static_box = wx.StaticBox(self.panel, -1, self.label)
        self.static_box.SetFont(self.parent.static_box_font)

        self.load_data_btn = wx.Button(self.panel, wx.ID_ANY, 'Load Data')
        self.file_lbl = wx.StaticText(self.panel, -1, 'Select file...')
        self.file_lbl.SetForegroundColour(self.parent.file_lbl_color_None)
        self.file_lbl.SetFont(self.parent.file_lbl_font)
        self.temperature_txt = wx.TextCtrl(self.panel, -1, '2000', size=(30,24),
                                           style=wx.ALIGN_RIGHT|wx.PROCESS_ENTER,  
                                           validator = IntValidator(2))
        self.temperature_unit_lbl = wx.StaticText(self.panel, -1, 'K')
        
        self.known_temperature_rb = wx.RadioButton(self.panel, -1, 'Temp', style =wx.RIGHT|wx.RB_GROUP)
        self.etalon_spectrum_rb = wx.RadioButton(self.panel, -1, 'Etalon')
        self.etalon_spectrum_rb.SetValue(1)
        self.etalon_file_lbl = wx.StaticText(self.panel, -1, 'Select File...')
        self.etalon_file_lbl.SetForegroundColour(self.parent.file_lbl_color_None)
        self.etalon_file_lbl.SetFont(self.parent.file_lbl_font)
        self.load_etalon_data_btn = wx.Button(self.panel, wx.ID_ANY,'...', size =(35,22))

    def set_sizer(self):
        self.gb_sizer = wx.GridBagSizer(7,7)
        self.gb_sizer.Add(self.load_data_btn, (0,0))
        self.gb_sizer.Add(self.file_lbl, (0,1), flag = wx.ALL | wx.ALIGN_CENTRE_VERTICAL)
        self.gb_sizer.Add(wx.StaticLine(self.panel, -1, style=wx.LI_HORIZONTAL),
                                     (1,0),(1,2), flag=wx.EXPAND)

        
        self.temp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.temp_sizer.AddMany([(self.temperature_txt, 1, wx.EXPAND | wx.ALIGN_CENTER),
                               (self.temperature_unit_lbl, 0, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 3)])

        self.gb_sizer.Add(self.temp_sizer, (2,0),  flag = wx.ALIGN_CENTRE_VERTICAL | wx.EXPAND)

        self.gb_sizer.Add(self.known_temperature_rb, (2,1), flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTRE_VERTICAL)
        self.gb_sizer.Add(self.etalon_spectrum_rb, (3,1), flag = wx.EXPAND | wx.ALIGN_CENTRE_VERTICAL)
        self.gb_sizer.Add(self.load_etalon_data_btn, (3,0), flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL)
        self.gb_sizer.Add(self.etalon_file_lbl, (4,1), flag=wx.ALIGN_LEFT | wx.ALIGN_CENTRE_VERTICAL)
        self.gb_sizer.AddGrowableCol(1)
        self.box_sizer = wx.StaticBoxSizer(self.static_box, wx.HORIZONTAL)
        self.box_sizer.Add(self.gb_sizer, 50, wx.ALL | wx.EXPAND)

        self.panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.panel_sizer.Add(self.box_sizer, 1, wx.EXPAND|wx.ALL, 10)
        self.panel.SetSizer(self.panel_sizer)
