import sys
import os
from wx.lib.pubsub import Publisher as pub
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL
import numpy as np

from views.T_Rax_MainView import TRaxMainView
from T_Rax_QTROISelectorController import TRaxROIController
from convert_ui_files import convert_ui_files
from T_Rax_Data import TraxData



class TRaxMainController(object):
    def __init__(self):
        self.main_view = TRaxMainView()
        self.data = TraxData()

        self.create_signals()
        self.create_sub_controller()
        self.mode = "temperature"
        
        self.main_view.navigate_to(self.mode)
        self.load_parameter()
        self.temperature_btn_click()

        self.load_exp_data('D:/Programming/VS Projects/T-Rax/T-Rax/sample files/Test 2013-09-24/temper_011.spe')
        self.main_view.show()
        self.load_roi_view()
        self.load_next_exp_data()

    def create_sub_controller(self):
        self.temperature_controller = TRaxTemperatureController(self,self.data,self.main_view)

    def set_parameter(self):
        ds_txt_roi = self.data.roi_data.ds_roi.get_roi_as_list()
        ds_txt_roi[2:] = self.data.calculate_wavelength(ds_txt_roi[2:])
        
    def load_parameter(self):
       try:
            fid = open('parameters.txt', 'r')
            self._exp_working_dir = ':'.join(fid.readline().split(':')[1::])[1:-1]
            self.temperature_controller._calib_working_dir = ':'.join(fid.readline().split(':')[1::])[1:-1]
            fid.close()
       except IOError:
            self._exp_working_dir = os.getcwd()
            self.temperature_controller._calib_working_dir = os.getcwd()

    def create_signals(self):
        self.create_navigation_signals()
        self.create_exp_file_signals()
        self.create_roi_view_signals()
        self.create_axes_listener()
        self.main_view.closeEvent=self.closeEvent  

    def create_navigation_signals(self):
        self.main_view.connect(self.main_view.ruby_btn, SIGNAL('clicked()'), self.ruby_btn_click)
        self.main_view.connect(self.main_view.raman_btn, SIGNAL('clicked()'), self.raman_btn_click)
        self.main_view.connect(self.main_view.diamond_btn, SIGNAL('clicked()'), self.diamond_btn_click)
        self.main_view.connect(self.main_view.temperature_btn, SIGNAL('clicked()'), self.temperature_btn_click)
        self.main_view.main_frame.resizeEvent = self.main_view.resize_graphs

    def create_exp_file_signals(self):
        self.connect_click_function(self.main_view.diamond_control_widget.load_exp_data_btn, self.load_exp_data)
        self.connect_click_function(self.main_view.ruby_control_widget.load_exp_data_btn, self.load_exp_data)
        self.connect_click_function(self.main_view.temperature_control_widget.load_exp_data_btn, self.load_exp_data)
        
        self.connect_click_function(self.main_view.diamond_control_widget.load_next_exp_data_btn, self.load_next_exp_data)
        self.connect_click_function(self.main_view.ruby_control_widget.load_next_exp_data_btn, self.load_next_exp_data)
        self.connect_click_function(self.main_view.temperature_control_widget.load_next_exp_data_btn, self.load_next_exp_data)
        
        self.connect_click_function(self.main_view.diamond_control_widget.load_previous_exp_data_btn, self.load_previous_exp_data)
        self.connect_click_function(self.main_view.ruby_control_widget.load_previous_exp_data_btn, self.load_previous_exp_data)
        self.connect_click_function(self.main_view.temperature_control_widget.load_previous_exp_data_btn, self.load_previous_exp_data)

    def create_roi_view_signals(self):
        self.connect_click_function(self.main_view.temperature_control_widget.roi_setup_btn, self.load_roi_view)
        self.connect_click_function(self.main_view.ruby_control_widget.roi_setup_btn, self.load_roi_view)
        self.connect_click_function(self.main_view.diamond_control_widget.roi_setup_btn, self.load_roi_view)

    def create_axes_listener(self):
        self.main_view.graph_1axes.canvas.mpl_connect('motion_notify_event', self.on_mouse_move_in_graph)
        self.main_view.graph_2axes.canvas.mpl_connect('motion_notify_event', self.on_mouse_move_in_graph)

    def connect_click_function(self, emitter, function):
        self.main_view.connect(emitter, SIGNAL('clicked()'), function)

    def load_exp_data(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.main_view, caption="Load Experiment SPE", 
                                          directory = self._exp_working_dir))

        if filename is not '':
            self._exp_working_dir = '/'.join(str(filename).replace('\\','/').split('/')[0:-1])
            self._files_before = dict([(f, None) for f in os.listdir(self._exp_working_dir)]) #reset for the autoprocessing
            self.data.load_exp_data(filename)

    def load_next_exp_data(self):
        self.data.load_next_exp_file()

    def load_previous_exp_data(self):
        self.data.load_previous_exp_file()

    def load_roi_view(self):
        try:
            self.roi_controller.show()
        except AttributeError:
            self.roi_controller = TRaxROIController(self.data, parent=self.main_view)
            self.roi_controller.show()

    def temperature_btn_click(self):
        self.main_view.navigate_to('temperature_btn')
        self.mode = "temperature"

    def ruby_btn_click(self):
        self.main_view.navigate_to('ruby_btn')
        self.mode = "ruby"

    def diamond_btn_click(self):
        self.main_view.navigate_to('diamond_btn')
        self.mode = "diamond"

    def raman_btn_click(self):
        self.main_view.update_navigation_bar('rgba(21, 134, 31, 255)', 'raman_btn')
        self.main_view.hide_control_widgets()

    def on_mouse_move_in_graph(self, event):
        x_coord, y_coord = event.xdata, event.ydata
        if x_coord <> None:
           self.main_view.status_coord_lbl.setText('x: %(x).3F y: %(y).3F' \
                              % {'x':x_coord, 'y':y_coord})
        else:
           self.main_view.status_coord_lbl.setText('')

    def save_directories(self):
        fid = open('parameters.txt', 'w')
        output_str = \
            'Working directory: ' + self._exp_working_dir + '\n' + \
            'Calibration directory: ' + self.temperature_controller._calib_working_dir
        fid.write(output_str)
        fid.close()

    def closeEvent(self, event):
        self.save_directories()
        self.roi_controller.view.close()
        self.main_view.close()
        event.accept()
        

class TRaxTemperatureController():
    def __init__(self, parent, data, main_view):
        self.parent=parent
        self.data=data
        self.main_view=main_view
        self.create_signals()

    def create_signals(self):
        self.create_temperature_pub_listeners()
        self.create_calibration_signals()
        self.create_temperature_control_signals()
        self.create_auto_process_signal()

    def create_temperature_pub_listeners(self):
        pub.subscribe(self.data_changed, "EXP DATA CHANGED")
        pub.subscribe(self.roi_changed, "ROI CHANGED")
    
    def create_calibration_signals(self):
        self.connect_click_function(self.main_view.temperature_control_widget.load_ds_calib_data_btn,
                                    self.load_ds_calib_data)
        self.connect_click_function(self.main_view.temperature_control_widget.load_us_calib_data_btn,
                                    self.load_us_calib_data)
        self.main_view.temperature_control_widget.ds_temperature_rb.toggled.connect(self.ds_temperature_rb_clicked)
        self.main_view.temperature_control_widget.us_temperature_rb.toggled.connect(self.us_temperature_rb_clicked)
        self.main_view.temperature_control_widget.ds_etalon_rb.toggled.connect(self.ds_etalon_rb_clicked)
        self.main_view.temperature_control_widget.us_etalon_rb.toggled.connect(self.us_etalon_rb_clicked)
        self.main_view.temperature_control_widget.ds_temperature_txt.editingFinished.connect(self.ds_temperature_changed)
        self.main_view.temperature_control_widget.us_temperature_txt.editingFinished.connect(self.us_temperature_changed)

    def create_temperature_control_signals(self):
        self.main_view.temperature_control_widget.fit_from_txt.editingFinished.connect(self.fit_txt_changed)
        self.main_view.temperature_control_widget.fit_to_txt.editingFinished.connect(self.fit_txt_changed)

    def create_auto_process_signal(self):
        self.main_view.temperature_control_widget.auto_process_cb.clicked.connect(self.auto_process_cb_click)
        self.autoprocess_timer = QtCore.QTimer(self.main_view)
        self.autoprocess_timer.setInterval(100)
        self.main_view.connect(self.autoprocess_timer,QtCore.SIGNAL('timeout()'), self.check_files)

    def connect_click_function(self, emitter, function):
        self.main_view.connect(emitter, SIGNAL('clicked()'), function)

    def data_changed(self, event):
        self.main_view.graph_2axes.update_graph(self.data.get_ds_spectrum(), self.data.get_us_spectrum(),
                                                self.data.get_ds_roi_max(), self.data.get_us_roi_max(),
                                                self.data.get_ds_calib_file_name(), self.data.get_us_calib_file_name())
        self.main_view.set_exp_filename(self.data.get_exp_file_name().replace('\\','/').split('/')[-1])
        self.main_view.set_exp_foldername('/'.join(self.data.get_exp_file_name().replace('\\','/').split('/')[-3:-1]))
        self.main_view.set_calib_filenames(self.data.get_ds_calib_file_name().replace('\\','/').split('/')[-1],
                                           self.data.get_us_calib_file_name().replace('\\','/').split('/')[-1])
        self.main_view.temperature_control_widget.ds_etalon_lbl.setText(self.data.get_ds_calib_etalon_file_name().replace('\\','/').split('/')[-1])
        self.main_view.temperature_control_widget.us_etalon_lbl.setText(self.data.get_us_calib_etalon_file_name().replace('\\','/').split('/')[-1])
        self.parent.set_parameter()

    def roi_changed(self, event):
        self.data.calc_spectra()
        self.main_view.graph_2axes.update_graph(self.data.get_ds_spectrum(), self.data.get_us_spectrum(),
                                                self.data.get_ds_roi_max(), self.data.get_us_roi_max(),
                                                self.data.get_ds_calib_file_name(), self.data.get_us_calib_file_name())
        self.main_view.set_fit_limits(self.data.get_x_roi_limits())
    
    def load_ds_calib_data(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.main_view, caption="Load Downstream calibration SPE", 
                                          directory = self._calib_working_dir))
        
        if filename is not '':
            self._calib_working_dir = '/'.join(str(filename).replace('\\','/').split('/')[0:-1])+'/'
            self.data.load_ds_calib_data(filename)

    def load_us_calib_data(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.main_view, caption="Load Upstream calibration SPE", 
                                          directory = self._calib_working_dir))
        
        if filename is not '':
            self._calib_working_dir = '/'.join(str(filename).replace('\\','/').split('/')[0:-1])+'/'
            self.data.load_us_calib_data(filename)

    def ds_temperature_rb_clicked(self):
        self.data.set_ds_calib_modus(0)

    def us_temperature_rb_clicked(self):
        self.data.set_us_calib_modus(0)

    def ds_etalon_rb_clicked(self):
        self.data.set_ds_calib_modus(1)
    
    def us_etalon_rb_clicked(self):
        self.data.set_us_calib_modus(1)

    def ds_temperature_changed(self):
        self.data.set_ds_calib_temp(np.double(self.main_view.temperature_control_widget.ds_temperature_txt.text()))
    
    def us_temperature_changed(self):
        self.data.set_us_calib_temp(np.double(self.main_view.temperature_control_widget.us_temperature_txt.text()))
    
    def fit_txt_changed(self):
        limits = self.main_view.temperature_control_widget.get_fit_limits()
        self.data.set_x_roi_limits_to(limits)

    
    def auto_process_cb_click(self):
        if self.main_view.temperature_control_widget.auto_process_cb.isChecked():
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
                path = self._exp_working_dir + '\\' + new_file_str
                self.data.load_exp_data(path)
            self._files_before = self._files_now
            
    def file_is_spe(self, filename):
        return filename.endswith('.SPE') or filename.endswith('.spe')
    
    def file_is_raw(self, filename):
        try:
            #checks if file contains "-raw" string at the end
            return filename.split('-')[-1].split('.')[0] == 'raw'
        except:
            return false         


    


if __name__ == "__main__":
    #convert_ui_files()
    app = QtGui.QApplication(sys.argv)
    controller = TRaxMainController()
    controller.main_view.show()
    app.exec_()