import sys
import os
import pickle
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL
import numpy as np

from controller.T_Rax_ROISelectorDiamondController import TRaxROIControllerDiamond
from data.T_Rax_DiamondData import TraxDiamondData

class TRaxDiamondController():
    def __init__(self, parent, main_view):
        self.parent = parent
        self.data = TraxDiamondData()
        
        self.main_view = main_view
        self.main_view.diamond_control_widget.derivative_smoothing_sb.setValue(5)
        self.main_view.diamond_control_widget.derivative_show_cb.toggle()
        self.create_signals()
        
        pub.sendMessage("EXP DIAMOND DATA CHANGED")

    def create_signals(self):
        self.create_exp_file_signals()
        self.create_roi_view_signals()
        self.create_diamond_pub_listeners()
        self.create_auto_process_signal()
        self.create_pressure_signals()
        self.create_derivative_signals()
        self.create_axes_click_signal()

    def create_diamond_pub_listeners(self):
        pub.subscribe(self.data_changed, "EXP DIAMOND DATA CHANGED")
        pub.subscribe(self.roi_changed, "DIAMOND ROI CHANGED")
        pub.subscribe(self.diamond_pos_changed, "DIAMOND POS CHANGED")

    def create_auto_process_signal(self):
        self.main_view.diamond_control_widget.auto_process_cb.clicked.connect(self.auto_process_cb_click)
        self.autoprocess_timer = QtCore.QTimer(self.main_view)
        self.autoprocess_timer.setInterval(100)
        self.main_view.connect(self.autoprocess_timer,QtCore.SIGNAL('timeout()'), self.check_files)
    
    def create_exp_file_signals(self):
        self.connect_click_function(self.main_view.diamond_control_widget.load_exp_data_btn, self.load_exp_data)        
        self.connect_click_function(self.main_view.diamond_control_widget.load_next_exp_data_btn, self.load_next_exp_data)        
        self.connect_click_function(self.main_view.diamond_control_widget.load_previous_exp_data_btn, self.load_previous_exp_data)

    def create_roi_view_signals(self):
        self.connect_click_function(self.main_view.diamond_control_widget.roi_setup_btn, self.load_roi_view)

    def create_axes_click_signal(self):
        self.pos_update_timer = QtCore.QTimer(self.main_view)
        self.pos_update_timer.setInterval(5)
        self.main_view.connect(self.pos_update_timer, QtCore.SIGNAL('timeout()'),self.update_diamond_mouse_move_pos)
        self.main_view.diamond_axes.canvas.mpl_connect('button_press_event', self.axes_click)
        self.main_view.diamond_axes.canvas.mpl_connect('button_release_event', self.axes_release)
        self.main_view.diamond_axes.canvas.mpl_connect('motion_notify_event', self.axes_move)
        self.main_view.diamond_axes.canvas.mpl_connect('scroll_event', self.axes_mouse_scroll)

    def create_pressure_signals(self):
        self.main_view.diamond_control_widget.reference_pos_txt.editingFinished.connect(self.reference_txt_changed)

    def create_derivative_signals(self):
        self.connect_click_function(self.main_view.diamond_control_widget.derivative_show_cb, self.derivative_show_cb_click)
        self.main_view.diamond_control_widget.derivative_smoothing_sb.valueChanged.connect(self.change_derivative_smoothing)
    
    def connect_click_function(self, emitter, function):
        self.main_view.connect(emitter, SIGNAL('clicked()'), function)

    def load_exp_data(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.main_view, caption="Load Experiment SPE", 
                                          directory = self._exp_working_dir))

        if filename is not '':
            self._exp_working_dir = '/'.join(str(filename).replace('\\','/').split('/')[0:-1]) + '/'
            self._files_before = dict([(f, None) for f in os.listdir(self._exp_working_dir)]) #reset for the autoprocessing
            self.data.load_diamond_data(filename)

    def load_next_exp_data(self):
        self.data.load_next_diamond_file()

    def load_previous_exp_data(self):
        self.data.load_previous_diamond_file()

    def load_roi_view(self):
        try:
            self.roi_controller.show()
        except AttributeError:
            self.roi_controller = TRaxROIControllerDiamond(self.data, parent=self.main_view)
            self.roi_controller.show()

    def data_changed(self):
        self.main_view.diamond_axes.update_graph(self.data.get_spectrum(), self.data.click_pos, self.data.get_derivative_spectrum())
        self.main_view.diamond_control_widget.exp_filename_lbl.setText(self.data.get_exp_file_name().replace('\\','/').split('/')[-1])
        self.main_view.diamond_control_widget.exp_folder_name_lbl.setText('/'.join(self.data.get_exp_file_name().replace('\\','/').split('/')[-3:-1]))
        self.main_view.status_file_information_lbl.setText(self.data.exp_data.get_file_information())

    def roi_changed(self):
        self.main_view.diamond_axes.update_graph(self.data.get_spectrum(), self.data.click_pos, self.data.get_derivative_spectrum())

    def diamond_pos_changed(self):
        self.main_view.diamond_axes.update_graph(self.data.get_spectrum(), self.data.click_pos, self.data.get_derivative_spectrum())

    def axes_click(self,event):
        if event.button == 1:
            self._axes_mouse_x = event.xdata
            self.pos_update_timer.start()
        else: #means right click, which is causing a complete unzoom
            self.data.set_x_roi_limits_to(self.data.get_x_limits())
            pub.sendMessage("DIAMOND ROI CHANGED")

    def axes_move(self,event):
        self._axes_mouse_x = event.xdata

    def axes_release(self,event):
        self.pos_update_timer.stop()
    
    def update_diamond_mouse_move_pos(self):
        x_coord = self._axes_mouse_x
        if x_coord is not None:
            self.update_diamond_pos(x_coord)

    def update_diamond_pos(self,x_coord):
        self.data.set_click_pos(x_coord)
        self.main_view.diamond_control_widget.measured_pos_lbl.setText('%.2f' % x_coord)
        self.main_view.diamond_control_widget.pressure_lbl.setText('%.1f' % self.data.get_pressure())

    def axes_mouse_scroll(self,event):
        curr_xlim = self.main_view.diamond_axes.axes.get_xlim()
        base_scale = 1.5
        if event.button == 'up':
            #zoom in
            scale_factor = 1 / base_scale
        elif event.button == 'down':
            #zoom out
            scale_factor = base_scale
        else:
            scale_factor = 1
            print event.button

        new_width = (curr_xlim[1] - curr_xlim[0]) * scale_factor

        relx = (curr_xlim[1] - event.xdata) / (curr_xlim[1] - curr_xlim[0])
        new_xlim = ([event.xdata - new_width * (1 - relx), event.xdata + new_width * (relx)])
        self.main_view.diamond_axes.axes.set_xlim(new_xlim)
        self.data.set_x_roi_limits_to(new_xlim)
        pub.sendMessage("DIAMOND ROI CHANGED")
        self.main_view.diamond_axes.redraw_figure()


    def reference_txt_changed(self):
        self.data.set_diamond_reference_pos(np.double(self.main_view.diamond_control_widget.reference_pos_txt.text()))
        self.main_view.diamond_control_widget.pressure_lbl.setText('%.1f' % self.data.get_pressure())
            
    def auto_process_cb_click(self):
        if self.main_view.diamond_control_widget.auto_process_cb.isChecked():
            self._files_before = dict([(f, None) for f in os.listdir(self._exp_working_dir)])
            self.autoprocess_timer.start()
        else:
            self.autoprocess_timer.stop()

    def check_files(self):
        self._files_now = dict([(f,None) for f in os.listdir(self._exp_working_dir)])
        self._files_added = [f for f in self._files_now if not f in self._files_before]
        self._files_removed = [f for f in self._files_before if not f in self._files_now]
        if len(self._files_added) > 0:
            new_file_str = self._files_added[-1]
            if self.file_is_spe(new_file_str) and not self.file_is_raw(new_file_str):
                file_info = os.stat(self._exp_working_dir + new_file_str)
                if file_info.st_size > 1000: #needed because there are some timing issues with WinSpec
                    path = self._exp_working_dir + new_file_str
                    self.data.load_diamond_data(path)
                    self._files_before = self._files_now
            
    def file_is_spe(self, filename):
        return filename.endswith('.SPE') or filename.endswith('.spe')
    
    def file_is_raw(self, filename):
        try:
            #checks if file contains "-raw" string at the end
            return filename.split('-')[-1].split('.')[0] == 'raw'
        except:
            return false

    def derivative_show_cb_click(self):
        if self.main_view.diamond_control_widget.derivative_show_cb.isChecked():
            self.data.return_derivative = True
            pub.sendMessage("DIAMOND ROI CHANGED")
        else:
            self.data.return_derivative = False
            pub.sendMessage("DIAMOND ROI CHANGED")

    def change_derivative_smoothing(self):
        self.data.derivative_smoothing = self.main_view.diamond_control_widget.derivative_smoothing_sb.value()
        pub.sendMessage("DIAMOND ROI CHANGED")
    