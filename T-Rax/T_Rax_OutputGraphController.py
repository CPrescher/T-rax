from PyQt4.QtCore import SIGNAL
from PyQt4 import QtCore, QtGui
import colors

from views.T_Rax_OutputGraphView import TRaxOutputGraphView

class TRaxOutputGraphController(object):
    def __init__(self, parent_controller, parent_view =None):
        self.parent_view=parent_view
        self.parent_controller=parent_controller
        self.view=TRaxOutputGraphView()
        self.view.closeEvent = self.closeEvent 
            
    def plot_temperature_series(self, ds_temperature, ds_temperature_errors,
                                us_temperature, us_temperature_errors):
        self.view.axes.cla()
        self.view.plot_series(ds_temperature, ds_temperature_errors, colors.DOWNSTREAM_COLOR_NORM, 'Downstream')
        self.view.plot_series(us_temperature, us_temperature_errors, colors.UPSTREAM_COLOR_NORM, 'Upstream')
        self.view.set_axis_labels('Frames', 'Temperature (K)')
        self.view.adjust_axes_limits()
        self.view.create_legend()
        self.view.redraw_figure()

    def show(self):
        self.view.show()

    def closeEvent(self, event):
        self.parent_controller.temperature_controller._time_lapse_is_on=False