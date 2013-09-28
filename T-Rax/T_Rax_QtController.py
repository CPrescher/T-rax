import sys
import os
from wx.lib.pubsub import Publisher as pub
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL
from views.T_Rax_MainView import TRaxMainView
from T_Rax_QTROISelectorController import TRaxROIController
from convert_ui_files import convert_ui_files
from T_Rax_Data import TraxData


class TRaxMainController(object):
    def __init__(self):
        self.main_view = TRaxMainView()
        self.data = TraxData()

        self.create_signals()
        self.load_parameter()
        self.mode = "temperature"
        self.main_view.navigate_to(self.mode)
        self.temperature_btn_click()
        self.load_exp_data('D:/Programming/VS Projects/T-Rax/T-Rax/sample files/Test 2013-09-24/temper_011.spe')
        self.main_view.show()
        self.load_roi_view()
        self.load_next_exp_data()

    def create_sub_controller(self):
        #self.create_sub_controller(self, self.data, self.main_view)
        pass

    def set_parameter(self):
        ds_txt_roi = self.data.roi_data.ds_roi.get_roi_as_list()
        ds_txt_roi[2:] = self.data.calculate_wavelength(ds_txt_roi[2:])
        #self.exp_controls.set_fit_x_limits(ds_txt_roi[2:])
        
    def load_parameter(self):
       try:
            fid = open('parameters.txt', 'r')
            self._exp_working_dir = ':'.join(fid.readline().split(':')[1::])[1:-1]
            self._calib_working_dir = ':'.join(fid.readline().split(':')[1::])[1:-1]
            fid.close()
       except IOError:
            self._exp_working_dir = os.getcwd()
            self._calib_working_dir = os.getcwd()


    def create_signals(self):
        self.create_navigation_signals()
        self.create_exp_file_signals()
        self.create_roi_view_signals()
        self.create_pub_listeners()
        self.create_axes_listener()


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

    def create_pub_listeners(self):
        pub.subscribe(self.data_changed, "EXP DATA CHANGED")
        pub.subscribe(self.roi_changed, "ROI CHANGED")

    def create_axes_listener(self):
        self.main_view.graph_1axes.canvas.mpl_connect('motion_notify_event', self.on_mouse_move_in_graph)
        self.main_view.graph_2axes.canvas.mpl_connect('motion_notify_event', self.on_mouse_move_in_graph)

    def connect_click_function(self, emitter, function):
        self.main_view.connect(emitter, SIGNAL('clicked()'), function)

    def load_exp_data(self, filename=None):
        if filename is None:
            filename= str(QtGui.QFileDialog.getOpenFileName(self.main_view, caption="Load Experiment SPE", 
                                          directory = self._exp_working_dir))

        if filename is not '':
            self._exp_working_dir = '/'.join(str(filename).split('/')[0:-1])
            self._files_before = dict([(f, None) for f in os.listdir(self._exp_working_dir)]) #reset for the autoprocessing
            self.data.load_exp_data(filename)
            self.set_parameter()

    def load_next_exp_data(self):
        self.data.load_next_exp_file()

    def load_previous_exp_data(self):
        self.data.load_previous_exp_file()

    def load_roi_view(self):
        try:
            self.roi_controller.show()
        except AttributeError:
            self.roi_controller = TRaxROIController(self.data)
            self.roi_controller.show()

    def temperature_btn_click(self):
        self.main_view.navigate_to('temperature_btn')
        self.mode = "temperature"

    def ruby_btn_click(self):
        self.main_view.navigate_to('ruby_btn')
        self.mode = "ruby"

    def diamond_btn_click(self):
        self.main_view.navigate_to('diamond_btn')
        self.mode= "diamond"

    def raman_btn_click(self):
        self.main_view.update_navigation_bar('rgba(21, 134, 31, 255)', 'raman_btn')
        self.main_view.hide_control_widgets()

    def data_changed(self, event):
        self.main_view.graph_2axes.update_graph(self.data.get_ds_spectrum(), self.data.get_us_spectrum(),
                                                self.data.get_ds_roi_max(), self.data.get_us_roi_max(),
                                                self.data.get_ds_calib_file_name(), self.data.get_us_calib_file_name())
        self.main_view.set_exp_filename(self.data.get_exp_file_name().split('/')[-1])
        self.main_view.set_exp_foldername('/'.join(self.data.get_exp_file_name().split('/')[-3:-1]))
        self.main_view.set_calib_filenames(self.data.get_ds_calib_file_name().split('\\')[-1],
                                           self.data.get_us_calib_file_name().split('\\')[-1])
       #self.calib_controls.ds_calib_box.file_lbl.SetLabel(self.data.get_ds_calib_file_name().split('\\')[-1])
       #self.calib_controls.us_calib_box.file_lbl.SetLabel(self.data.get_us_calib_file_name().split('\\')[-1])
       #self.calib_controls.ds_calib_box.etalon_file_lbl.SetLabel(self.data.get_ds_calib_etalon_file_name().split('\\')[-1])
       #self.calib_controls.us_calib_box.etalon_file_lbl.SetLabel(self.data.get_us_calib_etalon_file_name().split('\\')[-1])
       #self.set_parameter()

    def roi_changed(self, event):
        self.data.calc_spectra()
        self.main_view.graph_2axes.update_graph(self.data.get_ds_spectrum(), self.data.get_us_spectrum(),
                                                self.data.get_ds_roi_max(), self.data.get_us_roi_max(),
                                                self.data.get_ds_calib_file_name(), self.data.get_us_calib_file_name())

    def on_mouse_move_in_graph(self, event):
        x_coord, y_coord = event.xdata, event.ydata
        if x_coord <> None:
           self.main_view.status_coord_lbl.setText('x: %(x).3F y: %(y).3F' \
                              % {'x':x_coord, 'y':y_coord})
        else:
           self.main_view.status_coord_lbl.setText('')

class TRaxTemperatureController():
    def __init__(self, parent, data, view):
        pass





if __name__=="__main__":
    #convert_ui_files()
    app=QtGui.QApplication(sys.argv)
    controller = TRaxMainController()
    controller.main_view.show()
    app.exec_()