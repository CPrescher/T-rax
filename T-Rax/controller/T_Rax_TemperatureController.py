import sys
import os
import pickle
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL
import numpy as np
from epics import caput, PV

from controller.T_Rax_ModuleController import TRaxModuleController
from controller.T_Rax_OutputGraphController import TRaxOutputGraphController
from controller.T_Rax_ROISelectorTemperatureController import TRaxROITemperatureController
from data.T_Rax_TemperatureData import TraxTemperatureData


class TRaxTemperatureController(TRaxModuleController):
    def __init__(self, parent, main_view):
        self.data = TraxTemperatureData()
        self.parent = parent
        super(TRaxTemperatureController, self).__init__(parent, self.data,main_view.temperature_control_widget)
        self.main_view = main_view
        self.load_standard_parameter()
        self.create_signals()
        pub.sendMessage("EXP DATA CHANGED")
        pub.sendMessage("ROI CHANGED")

    def load_standard_parameter(self):
        try:
            self.data.load_calib_etalon()
        except IOError:
            self.data.set_ds_calib_modus(0)
            self.data.set_us_calib_modus(0) 

    def create_signals(self):
        self.create_frame_signals()

        self.create_temperature_pub_listeners()
        self.create_calibration_signals()
        self.create_fit_range_signals()
        self.create_settings_signals()

        self.main_view.temperature_control_widget.epics_connection_cb.clicked.connect(self.epics_connection_cb_clicked)
        self.epics_is_connected = False

    def load_settings(self):
        self._settings_files_list = []
        self._settings_file_names_list = []
        try:
            for file in os.listdir(self._settings_working_dir):
                if file.endswith('.trs'):
                    self._settings_files_list.append(file)
                    self._settings_file_names_list.append(file.split('.')[:-1][0])
        except:
            pass
        self.main_view.temperature_control_widget.settings_cb.blockSignals(True)
        self.main_view.temperature_control_widget.settings_cb.clear()
        self.main_view.temperature_control_widget.settings_cb.addItem('None')
        self.main_view.temperature_control_widget.settings_cb.addItems(self._settings_file_names_list)
        self.main_view.temperature_control_widget.settings_cb.blockSignals(False)

    def create_temperature_pub_listeners(self):
        pub.subscribe(self.data_changed, "EXP DATA CHANGED")
        pub.subscribe(self.frame_changed, "EXP DATA FRAME CHANGED")
        pub.subscribe(self.roi_changed, "ROI CHANGED")

    def create_frame_signals(self):
        self.main_view.temperature_control_widget.frame_number_txt.editingFinished.connect(self.frame_txt_value_changed)
        self.connect_click_function(self.main_view.temperature_control_widget.next_frame_btn, self.load_next_frame)
        self.connect_click_function(self.main_view.temperature_control_widget.previous_frame_btn, self.load_previous_frame)
        self.connect_click_function(self.main_view.temperature_control_widget.time_lapse_btn, self.start_time_lapse)
    
    def create_calibration_signals(self):
        self.connect_click_function(self.main_view.temperature_control_widget.load_ds_calib_data_btn,
                                    self.load_ds_calib_data)
        self.connect_click_function(self.main_view.temperature_control_widget.load_us_calib_data_btn,
                                    self.load_us_calib_data)
        self.main_view.temperature_control_widget.ds_temperature_rb.clicked.connect(self.ds_temperature_rb_clicked)
        self.main_view.temperature_control_widget.us_temperature_rb.clicked.connect(self.us_temperature_rb_clicked)
        self.main_view.temperature_control_widget.ds_etalon_rb.clicked.connect(self.ds_etalon_rb_clicked)
        self.main_view.temperature_control_widget.us_etalon_rb.clicked.connect(self.us_etalon_rb_clicked)
        self.connect_click_function(self.main_view.temperature_control_widget.ds_etalon_btn,self.load_ds_etalon_data)
        self.connect_click_function(self.main_view.temperature_control_widget.us_etalon_btn,self.load_us_etalon_data)
        self.main_view.temperature_control_widget.ds_temperature_txt.editingFinished.connect(self.ds_temperature_changed)
        self.main_view.temperature_control_widget.us_temperature_txt.editingFinished.connect(self.us_temperature_changed)

    def create_fit_range_signals(self):
        self.main_view.temperature_control_widget.fit_from_txt.editingFinished.connect(self.fit_txt_changed)
        self.main_view.temperature_control_widget.fit_to_txt.editingFinished.connect(self.fit_txt_changed)

    def create_settings_signals(self):
        self.connect_click_function(self.main_view.temperature_control_widget.save_settings_btn, self.save_settings_btn_click)
        self.connect_click_function(self.main_view.temperature_control_widget.load_settings_btn, self.load_settings_btn_click)
        self.main_view.temperature_control_widget.settings_cb.currentIndexChanged.connect(self.settings_cb_changed)

    def load_roi_view(self):
        try:
            self.roi_controller.show()
        except AttributeError:
            self.roi_controller = TRaxROITemperatureController(self.data, parent=self.main_view)
            self.roi_controller.show()

    def data_changed(self):
        self.frame_changed()
        self.update_time_lapse()

    def frame_changed(self):
        self.main_view.temperature_axes.update_graph(self.data.get_ds_spectrum(), self.data.get_us_spectrum(),
                                                self.data.get_ds_roi_max(), self.data.get_us_roi_max(),
                                                self.data.get_ds_calib_file_name(), self.data.get_us_calib_file_name())
        self.main_view.set_temperature_filename(self.data.get_exp_file_name().replace('\\','/').split('/')[-1])
        self.main_view.set_temperature_foldername('/'.join(self.data.get_exp_file_name().replace('\\','/').split('/')[-3:-1]))
        self.main_view.status_file_information_lbl.setText(self.data.exp_data.get_file_information())
        self.main_view.set_fit_limits(self.data.get_x_roi_limits())
        self.update_frames_widget()
        self.update_calibration_view()
        self.update_pv_names()

    def update_frames_widget(self):
        if self.data.exp_data.num_frames > 1:
            self.main_view.temperature_control_widget.frames_widget.show()
            self.main_view.temperature_control_widget.frame_line.show()
            self.main_view.temperature_control_widget.frame_number_txt.blockSignals(True)
            self.main_view.temperature_control_widget.frame_number_txt.setText(str(self.data.exp_data.current_frame + 1))
            if self.data.exp_data.current_frame + 1 == self.data.exp_data.num_frames:
                self.main_view.temperature_control_widget.next_frame_btn.setDisabled(True)
            else:
                self.main_view.temperature_control_widget.next_frame_btn.setDisabled(False)
            if self.data.exp_data.current_frame == 0:
                self.main_view.temperature_control_widget.previous_frame_btn.setDisabled(True)
            else:
                self.main_view.temperature_control_widget.previous_frame_btn.setDisabled(False)
            self.main_view.temperature_control_widget.frame_number_txt.blockSignals(False)
        else:
            self.main_view.temperature_control_widget.frames_widget.hide()
            self.main_view.temperature_control_widget.frame_line.hide()

    def update_time_lapse(self):
        if self.data.exp_data.num_frames > 1:
            try:
                if self._time_lapse_is_on:
                    self.plot_time_lapse()
            except:
                pass
        else:
             self.parent.output_graph_controller.hide()

    def update_calibration_view(self):
        self.main_view.set_calib_filenames(self.data.get_ds_calib_file_name().replace('\\','/').split('/')[-1],
                                           self.data.get_us_calib_file_name().replace('\\','/').split('/')[-1])
        self.main_view.temperature_control_widget.ds_etalon_lbl.setText(self.data.get_ds_calib_etalon_file_name().replace('\\','/').split('/')[-1])
        self.main_view.temperature_control_widget.us_etalon_lbl.setText(self.data.get_us_calib_etalon_file_name().replace('\\','/').split('/')[-1])
        ds_modus = self.data.get_ds_calib_modus()
        us_modus = self.data.get_us_calib_modus()
        if us_modus == 0:
            self.main_view.temperature_control_widget.us_temperature_rb.toggle()
        elif us_modus == 1:
            self.main_view.temperature_control_widget.us_etalon_rb.toggle()

        if ds_modus == 0:
            self.main_view.temperature_control_widget.ds_temperature_rb.toggle()
        elif ds_modus == 1:
            self.main_view.temperature_control_widget.ds_etalon_rb.toggle()

    def roi_changed(self):
        self.data.calc_spectra()
        self.main_view.temperature_axes.update_graph(self.data.get_ds_spectrum(), self.data.get_us_spectrum(),
                                                self.data.get_ds_roi_max(), self.data.get_us_roi_max(),
                                                self.data.get_ds_calib_file_name(), self.data.get_us_calib_file_name())
        self.main_view.set_fit_limits(self.data.get_x_roi_limits())
        self.update_pv_names()

    def frame_txt_value_changed(self):
        self.data.set_current_frame(int(self.main_view.temperature_control_widget.frame_number_txt.text()) - 1)

    def load_next_frame(self):
        self.data.load_next_frame()

    def load_previous_frame(self):
        self.data.load_previous_frame()

    def start_time_lapse(self):
        self._time_lapse_is_on = True
        self.plot_time_lapse()
            

    def plot_time_lapse(self):
        ds_temperature, ds_temperature_err, us_temperature, us_temperature_err = self.data.calculate_time_lapse()
        self.parent.output_graph_controller.show()
        self.parent.output_graph_controller.plot_temperature_series(self.data.exp_data.get_exposure_time(),\
            ds_temperature, ds_temperature_err, us_temperature, us_temperature_err)

    def update_pv_names(self):
        if self.epics_is_connected:
            #self.pv_us_temperature.put(self.data.get_us_temp())
            #self.pv_ds_temperature.put(self.data.get_ds_temp())
            #self.pv_us_int.put(self.data.get_us_roi_max())
            #self.pv_ds_int.put(self.data.get_ds_roi_max())
            caput('13IDD:us_las_temp.VAL', self.data.get_us_temp())
            caput('13IDD:ds_las_temp.VAL', self.data.get_ds_temp())

            caput('13IDD:up_t_int', str(self.data.get_us_roi_max()))
            caput('13IDD:dn_t_int', str(self.data.get_ds_roi_max()))
    
    def load_ds_calib_data(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.main_view, caption="Load Downstream calibration SPE", 
                                          directory = self._calib_working_dir))
        
        if filename is not '':
            self._calib_working_dir = '/'.join(str(filename).replace('\\','/').split('/')[0:-1]) + '/'
            self.data.load_ds_calib_data(filename)

    def load_us_calib_data(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.main_view, caption="Load Upstream calibration SPE", 
                                          directory = self._calib_working_dir))
        
        if filename is not '':
            self._calib_working_dir = '/'.join(str(filename).replace('\\','/').split('/')[0:-1]) + '/'
            self.data.load_us_calib_data(filename)

    def ds_temperature_rb_clicked(self):
        self.data.set_ds_calib_modus(0)

    def us_temperature_rb_clicked(self):
        self.data.set_us_calib_modus(0)

    def ds_etalon_rb_clicked(self):
        self.data.set_ds_calib_modus(1)
    
    def us_etalon_rb_clicked(self):
        self.data.set_us_calib_modus(1)

    def load_ds_etalon_data(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.main_view, caption="Load Downstream Etalaon Spectrum", 
                                          directory = self._calib_working_dir))
        
        if filename is not '':
            self.data.load_ds_calib_etalon(filename)

    def load_us_etalon_data(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.main_view, caption="Load Upstream Etalaon Spectrum", 
                                          directory = self._calib_working_dir))
        
        if filename is not '':
            self.data.load_us_calib_etalon(filename)

    def ds_temperature_changed(self):
        self.data.set_ds_calib_temp(np.double(self.main_view.temperature_control_widget.ds_temperature_txt.text()))
    
    def us_temperature_changed(self):
        self.data.set_us_calib_temp(np.double(self.main_view.temperature_control_widget.us_temperature_txt.text()))
    
    def fit_txt_changed(self):
        limits = self.main_view.temperature_control_widget.get_fit_limits()
        self.data.set_x_roi_limits_to(limits)  


    def save_settings_btn_click(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getSaveFileName(self.main_view, caption="Save current settings", 
                                          directory = self._settings_working_dir, filter='*.trs'))
        
        if filename is not '':
            pickle.dump(self.data.get_settings(),open(filename,'wb'))
            self._settings_working_dir = '/'.join(str(filename).replace('\\','/').split('/')[0:-1]) + '/'
            self.load_settings()            
            try:
                ind = self.main_view.temperature_control_widget.settings_cb.findText(filename.replace('\\','/').split('/')[-1].split('.')[:-1][0])
                self.main_view.temperature_control_widget.settings_cb.blockSignals(True)
                self.main_view.temperature_control_widget.settings_cb.setCurrentIndex(ind)
                self.main_view.temperature_control_widget.settings_cb.blockSignals(False)
            except:
                pass

    def load_settings_btn_click(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.main_view, caption="Load new setting", 
                                          directory = self._settings_working_dir, filter='*.trs'))
        
        if filename is not '':
            settings = pickle.load(open(filename,'rb'))
            self._settings_working_dir = '/'.join(str(filename).replace('\\','/').split('/')[0:-1]) + '/'
            self.load_settings()
            self.main_view.temperature_control_widget.ds_temperature_txt.setText(str(int(settings.ds_calibration_temperature)))
            self.main_view.temperature_control_widget.us_temperature_txt.setText(str(int(settings.us_calibration_temperature)))
            
            self.main_view.temperature_control_widget.ds_temperature_rb.blockSignals(True)
            self.main_view.temperature_control_widget.us_temperature_rb.blockSignals(True)
            self.main_view.temperature_control_widget.ds_etalon_rb.blockSignals(True)
            self.main_view.temperature_control_widget.us_etalon_rb.blockSignals(True)
            if settings.ds_calibration_modus == 0:
                self.main_view.temperature_control_widget.ds_temperature_rb.toggle()
            else:
                self.main_view.temperature_control_widget.ds_etalon_rb.toggle()

            if settings.us_calibration_modus == 0:
                self.main_view.temperature_control_widget.us_temperature_rb.toggle()
            else:
                self.main_view.temperature_control_widget.us_etalon_rb.toggle()

            self.main_view.temperature_control_widget.ds_temperature_rb.blockSignals(False)
            self.main_view.temperature_control_widget.us_temperature_rb.blockSignals(False)
            self.main_view.temperature_control_widget.ds_etalon_rb.blockSignals(False)
            self.main_view.temperature_control_widget.us_etalon_rb.blockSignals(False)

            self.data.load_settings(settings)
            try:
                ind = self.main_view.temperature_control_widget.settings_cb.findText(filename.replace('\\','/').split('/')[-1].split('.')[:-1][0])
                self.main_view.temperature_control_widget.settings_cb.blockSignals(True)
                self.main_view.temperature_control_widget.settings_cb.setCurrentIndex(ind)
                self.main_view.temperature_control_widget.settings_cb.blockSignals(False)
            except:
                pass
                    

    def settings_cb_changed(self):
        current_index = self.main_view.temperature_control_widget.settings_cb.currentIndex()
        if not current_index == 0: #is the None index
            new_file_name = self._settings_working_dir + self._settings_files_list[current_index - 1] # therefore also one has to be deleted
            self.load_settings_btn_click(new_file_name)


    def epics_connection_cb_clicked(self):
        if self.main_view.temperature_control_widget.epics_connection_cb.isChecked():
            self.pv_us_temperature = PV('13IDD:us_las_temp.VAL')
            self.pv_ds_temperature = PV('13IDD:ds_las_temp.VAL')
            self.pv_us_int = PV('13IDD:up_t_int')
            self.pv_ds_int = PV('13IDD:dn_t_int')
            self.epics_is_connected = True
            self.update_pv_names()
        else:
            self.epics_is_connected = False