import numpy as np

from Views.OutputGraphView import TRaxOutputGraphView


class TRaxOutputGraphController(object):
    def __init__(self, parent_controller, parent_view=None):
        self.parent_view = parent_view
        self.parent_controller = parent_controller
        self.view = TRaxOutputGraphView()
        self.view.closeEvent = self.closeEvent

    def plot_temperature_series(self, time_step, ds_temperature, ds_temperature_errors,
                                us_temperature, us_temperature_errors):
        self.view.axes.cla()
        x = []
        for i in xrange(len(ds_temperature)):
            x.append(time_step * (i + 1))

        self.view.plot_series(x, ds_temperature, ds_temperature_errors, (1, 1, 0), 'Downstream')
        self.view.plot_series(x, us_temperature, us_temperature_errors, (1, 0.55, 0), 'Upstream')

        ds_temperature_avg = np.mean(ds_temperature)
        ds_temperature_std_err = np.std(ds_temperature)
        self.view.ds_temperature_lbl.setText('{T:1.0f} +- {T_err:1.0f} K'.format(T=ds_temperature_avg,
                                                                                 T_err=ds_temperature_std_err))

        us_temperature_avg = np.mean(us_temperature)
        us_temperature_std_err = np.std(us_temperature)
        self.view.us_temperature_lbl.setText('{T:1.0f} +- {T_err:1.0f} K'.format(T=us_temperature_avg,
                                                                                 T_err=us_temperature_std_err))

        combined_temperature_avg = np.mean(us_temperature + ds_temperature)
        combined_temperature_std_err = np.std(us_temperature + ds_temperature)
        self.view.combined_temperature_lbl.setText('{T:1.0f} +- {T_err:1.0f} K'
                                          .format(T=combined_temperature_avg,
                                                  T_err=combined_temperature_std_err))

        self.view.set_axis_labels('Time (s)', 'Temperature (K)')
        self.view.adjust_axes_limits()
        self.view.redraw_figure()


    def show(self):
        self.view.show()

    def hide(self):
        self.view.hide()

    def closeEvent(self, event):
        self.parent_controller.temperature_controller._time_lapse_is_on = False