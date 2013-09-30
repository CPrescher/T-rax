import sys
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL
from UIFiles.T_Rax_MainWindow import Ui_T_Rax_MainWindow
from views.T_Rax_ControlWidgets import DiamondControlWidget, RubyControlWidget, TemperatureControlWidget

import numpy as np

import matplotlib as mpl
mpl.rcParams['font.size'] = 12
mpl.rcParams['lines.linewidth'] = 0.5
mpl.rcParams['lines.color'] = 'g'
mpl.rcParams['text.color'] = 'white'
mpl.rc('axes', facecolor='#1E1E1E', edgecolor='white', lw=1, labelcolor='white')
mpl.rc('xtick', color='white')
mpl.rc('ytick', color='white')
mpl.rc('figure', facecolor='#1E1E1E', edgecolor='black')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class TRaxMainView(QtGui.QMainWindow, Ui_T_Rax_MainWindow):
    def __init__(self, parent=None):
        super(TRaxMainView, self).__init__(parent)
        self.setupUi(self)
        self.main_layout = self.main_frame.layout()
        
        self.create_graphs()
        self.create_widgets()
        self.hide_control_widgets()
        self.resize(900,450)

    def create_graphs(self):
        self.graph_2axes = T_Rax_2axes_graph(self.figure1_frame)
        self.graph_1axes = T_Rax_1axes_graph(self.figure2_frame)
        self.graph_1axes.hide()

    
    def create_widgets(self):
        self.create_navigation_widgets()

    def create_navigation_widgets(self):
        self.temperature_control_widget = TemperatureControlWidget()
        self.ruby_control_widget = RubyControlWidget()
        self.diamond_control_widget = DiamondControlWidget()
        
        self.main_layout.addWidget(self.temperature_control_widget)
        self.main_layout.addWidget(self.ruby_control_widget)        
        self.main_layout.addWidget(self.diamond_control_widget)


    def navigate_to(self, btn_name):
        self.hide_control_widgets()
        if btn_name == 'temperature_btn':
            self.update_navigation_bar('rgba(221, 124, 40, 255)', 'temperature_btn')
            self.temperature_control_widget.show()
            self.graph_1axes.hide()
            self.graph_2axes.show()

        elif btn_name == 'ruby_btn':
            self.update_navigation_bar('rgba(197, 0, 3, 255)', 'ruby_btn')
            self.ruby_control_widget.show()
            self.graph_2axes.hide()            
            self.graph_1axes.show()

        elif btn_name == 'diamond_btn':
            self.update_navigation_bar('rgba(27, 0, 134, 255)', 'diamond_btn')
            self.diamond_control_widget.show()
            self.graph_2axes.hide()
            self.graph_1axes.show()

    def set_exp_filename(self, filename):      
        self.temperature_control_widget.exp_filename_lbl.setText(filename)
        self.ruby_control_widget.exp_filename_lbl.setText(filename)
        self.diamond_control_widget.exp_filename_lbl.setText(filename)

    def set_exp_foldername(self, folder_name):      
        self.temperature_control_widget.exp_folder_name_lbl.setText(folder_name)
        self.ruby_control_widget.exp_folder_name_lbl.setText(folder_name)
        self.diamond_control_widget.exp_folder_name_lbl.setText(folder_name)

    def set_calib_filenames(self, ds_filename, us_filename):
        self.temperature_control_widget.us_calib_filename_lbl.setText(us_filename)
        self.temperature_control_widget.ds_calib_filename_lbl.setText(ds_filename)
        self.status_ds_calib_filename_lbl.setText('DS calibration: '+ds_filename.replace('\\','/').split('/')[-1])
        self.status_us_calib_filename_lbl.setText('US calibration: '+us_filename.replace('\\','/').split('/')[-1])

    def hide_control_widgets(self):
        self.temperature_control_widget.hide()
        self.ruby_control_widget.hide()
        self.diamond_control_widget.hide()
    
    def resize_graphs(self, event):
        self.graph_1axes.resize_graph(self.figure2_frame.size())
        self.graph_2axes.resize_graph(self.figure1_frame.size())


    def update_navigation_bar(self, new_color, sender):
        str1 = '#navigation_frame {background: qlineargradient(spread:reflect, x1:0, y1:0.5, x2:0, y2:0, stop:0.12 %s, stop:0.6 rgb(30, 30, 30));}' % new_color
        str2 = '#QPushButton { border: 2px solid #999}'
        str3 = '#%s { border: 4px solid #fff}' % sender
        self.navigation_frame.setStyleSheet('\n'.join([str1, str2, str3]))

    def set_fit_limits(self, limits):
        self.temperature_control_widget.set_fit_limits(limits)

    
class T_Rax_2axes_graph():
    def __init__(self, parent):
        self._parent = parent
        self.figure = Figure(None, dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self._parent)

        graph_layout = QtGui.QVBoxLayout(self._parent)
        graph_layout.setContentsMargins(0,0,0,0)
        graph_layout.setSpacing(0)
        graph_layout.setMargin(0)
        graph_layout.addWidget(self.canvas)
        self.canvas.setSizePolicy( QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        self.canvas.updateGeometry()
        
        self.ds_axes = self.figure.add_subplot(121)
        self.us_axes = self.figure.add_subplot(122)
        self.create_ds_graph()
        self.create_us_graph()
        self._hidden = False
 
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
        data_line, = axes.plot([], [], '-', color = (0.7,0.9,0.9), lw=1)
        fit_line, = axes.plot([], [], 'r-',  lw=3)
        temp_txt = axes.text(0,0, '', size=20, ha='left', va='top')
        int_txt = axes.text(0,0,'',size=13, color = (0.04,0.76,0.17), ha='right')
        warning_txt = axes.text(0,0,'', size=25, color = 'r', va='center', ha='center', weight = 'bold') 
        calib_file_txt = axes.text(0,0, '', size=9, color =  'r', ha='left', va='top', weight = 'bold')

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
        if ds_fit_spectrum == None:
            self.ds_temp_txt.set_text('')
            self.ds_fit_line.set_data([[],[]])
        else:
            self.ds_temp_txt.set_text('{0:.0f} K $\pm$ {1:.0f}'.format(ds_fit_spectrum.T, ds_fit_spectrum.T_err))
            self.ds_fit_line.set_data(ds_fit_spectrum.get_data())
            self.ds_temp_txt.set_x(min(ds_exp_spectrum.x) + 0.05 * ds_exp_spectrum.get_x_range())
            self.ds_temp_txt.set_y(min(ds_exp_spectrum.y) + 0.9 * ds_exp_spectrum.get_y_range() * 1.05)

        if us_fit_spectrum == None:
            self.us_temp_txt.set_text('')
            self.us_fit_line.set_data([[],[]])
        else:
            self.us_temp_txt.set_text('{0:.0f} K $\pm$ {1:.0f}'.format(us_fit_spectrum.T, us_fit_spectrum.T_err))
            self.us_fit_line.set_data(us_fit_spectrum.get_data())
            self.us_temp_txt.set_x(min(us_exp_spectrum.x) + 0.05 * us_exp_spectrum.get_x_range())
            self.us_temp_txt.set_y(min(us_exp_spectrum.y) + 0.9 * us_exp_spectrum.get_y_range() * 1.05)

        #Maximum intensity:
        self.ds_int_txt.set_text('Max Int: {0:.0f}'.format(ds_max_int))
        self.ds_int_txt.set_x(min(ds_exp_spectrum.x) + 0.97 * ds_exp_spectrum.get_x_range())
        self.ds_int_txt.set_y(min(ds_exp_spectrum.y) + 0.03 * ds_exp_spectrum.get_y_range())

        self.us_int_txt.set_text('Max Int: {0:.0f}'.format(us_max_int))
        self.us_int_txt.set_x(min(us_exp_spectrum.x) + 0.97 * us_exp_spectrum.get_x_range())
        self.us_int_txt.set_y(min(us_exp_spectrum.y) + 0.03 * us_exp_spectrum.get_y_range())

        #do a warning if it is over a specific value:
        if ds_max_int >= 64400:
            self.ds_warning_txt.set_text('SATURATION')
            self.ds_warning_txt.set_x(min(ds_exp_spectrum.x) + 0.5 * ds_exp_spectrum.get_x_range())
            self.ds_warning_txt.set_y(min(ds_exp_spectrum.y) + 0.5 * ds_exp_spectrum.get_y_range())
        else:
            self.ds_warning_txt.set_text('')

        if us_max_int >= 64400:
            self.us_warning_txt.set_text('SATURATION')
            self.us_warning_txt.set_x(min(us_exp_spectrum.x) + 0.5 * us_exp_spectrum.get_x_range())
            self.us_warning_txt.set_y(min(us_exp_spectrum.y) + 0.5 * us_exp_spectrum.get_y_range())
        else:
            self.us_warning_txt.set_text('')

        #Calibration files:
        if ds_calib_fname == 'Select File...':
            self.ds_calib_file_txt.set_text('Load calibration file!')
            self.ds_calib_file_txt.set_x(min(ds_exp_spectrum.x) + 0.03 * ds_exp_spectrum.get_x_range())
            self.ds_calib_file_txt.set_y(min(ds_exp_spectrum.y) + 0.96 * ds_exp_spectrum.get_y_range() * 1.05)
        else:
            self.ds_calib_file_txt.set_text('')

        if us_calib_fname == 'Select File...':
            self.us_calib_file_txt.set_text('Load calibration file!')
            self.us_calib_file_txt.set_x(min(us_exp_spectrum.x) + 0.03 * us_exp_spectrum.get_x_range())
            self.us_calib_file_txt.set_y(min(us_exp_spectrum.y) + 0.96 * us_exp_spectrum.get_y_range() * 1.05)
        else:
            self.us_calib_file_txt.set_text('')

        self.canvas.draw()

    def hide(self):
        self._parent.hide()
        self._hidden = True

    def show(self):
        self._parent.show()
        self.redraw_figure()
        self._hidden = False

    def resize_graph(self, new_size):
        if not self._hidden:
            self.figure.set_size_inches([new_size.width() / 100.0, new_size.height() / 100.0])
            self.redraw_figure()

    def redraw_figure(self):
        self.figure.tight_layout(None, 1, None, None)
        self.canvas.draw()

class T_Rax_1axes_graph():
    def __init__(self, parent):
        self._parent = parent
        self.figure = Figure(None, dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self._parent)

        graph_layout = QtGui.QVBoxLayout(self._parent)        
        graph_layout.setContentsMargins(0,0,0,0)
        graph_layout.setMargin(0)
        graph_layout.addWidget(self.canvas)

        self.axes = self.figure.add_subplot(111)
        self.create_graph()
        self._hidden = False

    def create_graph(self):
        x=np.linspace(0,20,100)
        y=np.cos(x)
        self.line = self.axes.plot(x,y,'w-', lw=3)
    
    def hide(self):
        self._parent.hide()
        self._hidden = True

    def show(self):
        self._parent.show()
        self.redraw_figure()
        self._hidden = False

    def resize_graph(self, new_size):
        if not self._hidden:
            self.figure.set_size_inches([new_size.width() / 100.0, new_size.height() / 100.0])
            self.redraw_figure()

    def redraw_figure(self):
        self.figure.tight_layout(None, 0.3, None, None)
        self.canvas.draw()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = TRaxMainView()
    form.show()
    app.exec_()