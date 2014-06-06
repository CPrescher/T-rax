import sys
import os
import pickle
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL
import numpy as np

from controller.T_Rax_ModuleController import TRaxModuleController
from controller.T_Rax_ROISelectorRubyController import TRaxROIControllerRuby
from data.T_Rax_RubyData import TraxRubyData


class TRaxRubyController(TRaxModuleController):
    def __init__(self, parent, main_view):
        self.parent = parent
        self.data = TraxRubyData()
        super(TRaxRubyController, self).__init__(parent, \
                                                 self.data, main_view.ruby_control_widget)
        self.main_view = main_view
        self.create_signals()

        pub.sendMessage("EXP RUBY DATA CHANGED")

    def create_signals(self):
        self.create_ruby_pub_listeners()
        self.create_pressure_signals()
        self.create_axes_click_signal()

    def create_ruby_pub_listeners(self):
        pub.subscribe(self.data_changed, "EXP RUBY DATA CHANGED")
        pub.subscribe(self.roi_changed, "RUBY ROI CHANGED")
        pub.subscribe(self.ruby_pos_changed, "RUBY POS CHANGED")

    def create_axes_click_signal(self):
        self.pos_update_timer = QtCore.QTimer(self.main_view)
        self.pos_update_timer.setInterval(5)
        self.main_view.connect(self.pos_update_timer, QtCore.SIGNAL('timeout()'), self.update_ruby_mouse_move_pos)
        self.main_view.ruby_axes.canvas.mpl_connect('button_press_event', self.axes_click)
        self.main_view.ruby_axes.canvas.mpl_connect('button_release_event', self.axes_release)
        self.main_view.ruby_axes.canvas.mpl_connect('motion_notify_event', self.axes_move)
        self.main_view.ruby_axes.canvas.mpl_connect('scroll_event', self.axes_mouse_scroll)

    def create_pressure_signals(self):
        self.main_view.ruby_control_widget.reference_pos_txt.editingFinished.connect(self.reference_txt_changed)
        self.main_view.ruby_control_widget.temperature_txt.editingFinished.connect(self.temperature_txt_changed)
        self.main_view.ruby_control_widget.conditions_cb.currentIndexChanged.connect(self.condition_cb_changed)
        self.connect_click_function(self.main_view.ruby_control_widget.fit_ruby_btn, self.fit_ruby_btn_click)

    def load_roi_view(self):
        try:
            self.roi_controller.show()
        except AttributeError:
            self.roi_controller = TRaxROIControllerRuby(self.data, parent=self.main_view)
            self.roi_controller.show()

    def data_changed(self):
        self.main_view.ruby_axes.update_graph(self.data.get_exp_data().get_spectrum(), self.data.click_pos,
                                              self.data.get_fitted_spectrum())
        self.main_view.set_ruby_filename(self.data.get_exp_data().get_filename().replace('\\', '/').split('/')[-1])
        self.main_view.set_ruby_foldername(
            '/'.join(self.data.get_exp_data().get_filename().replace('\\', '/').split('/')[-3:-1]))
        self.main_view.status_file_information_lbl.setText(self.data.exp_data.get_file_information_string())

    def roi_changed(self):
        self.main_view.ruby_axes.update_graph(self.data.get_exp_data().get_spectrum(), self.data.click_pos,
                                              self.data.get_fitted_spectrum())
        self.main_view.set_ruby_filename(self.data.get_exp_data().get_filename().replace('\\', '/').split('/')[-1])
        self.main_view.set_ruby_foldername(
            '/'.join(self.data.get_exp_data().get_filename().replace('\\', '/').split('/')[-3:-1]))

    def ruby_pos_changed(self):
        self.main_view.ruby_axes.update_graph(self.data.get_exp_data().get_spectrum(), self.data.click_pos,
                                              self.data.get_fitted_spectrum())

    def axes_click(self, event):
        if event.button == 1:
            self._axes_mouse_x = event.xdata
            self.pos_update_timer.start()
        else:
            self.data.set_x_roi_limits_to(self.data.get_x_limits())
            pub.sendMessage("RUBY ROI CHANGED")

    def axes_move(self, event):
        self._axes_mouse_x = event.xdata

    def axes_release(self, event):
        self.pos_update_timer.stop()

    def update_ruby_mouse_move_pos(self):
        x_coord = self._axes_mouse_x
        if x_coord is not None:
            self.update_ruby_pos(x_coord)

    def update_ruby_pos(self, x_coord):
        self.data.set_click_pos(x_coord)
        self.main_view.ruby_control_widget.measured_pos_lbl.setText('%.2f' % x_coord)
        self.main_view.ruby_control_widget.pressure_lbl.setText('%.1f' % self.data.get_pressure())

    def axes_mouse_scroll(self, event):
        curr_xlim = self.main_view.ruby_axes.axes.get_xlim()
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
        self.main_view.ruby_axes.axes.set_xlim(new_xlim)
        self.data.set_x_roi_limits_to(new_xlim)
        pub.sendMessage("RUBY ROI CHANGED")
        self.main_view.ruby_axes.redraw_figure()


    def reference_txt_changed(self):
        self.data.set_ruby_reference_pos(np.double(self.main_view.ruby_control_widget.reference_pos_txt.text()))
        self.main_view.ruby_control_widget.pressure_lbl.setText('%.1f' % self.data.get_pressure())

    def temperature_txt_changed(self):
        self.data.set_temperature(np.double(self.main_view.ruby_control_widget.temperature_txt.text()))
        self.main_view.ruby_control_widget.pressure_lbl.setText('%.1f' % self.data.get_pressure())

    def condition_cb_changed(self):
        ind = self.main_view.ruby_control_widget.conditions_cb.currentIndex()
        if ind == 0:
            self.data.set_ruby_condition('hydrostatic')
        elif ind == 1:
            self.data.set_ruby_condition('non-hydrostatic')
        self.main_view.ruby_control_widget.pressure_lbl.setText('%.1f' % self.data.get_pressure())

    def fit_ruby_btn_click(self):
        self.data.fit_spectrum()
        self.main_view.ruby_control_widget.measured_pos_lbl.setText('%.2f' % self.data.click_pos)
        self.main_view.ruby_control_widget.pressure_lbl.setText('%.1f' % self.data.get_pressure())
