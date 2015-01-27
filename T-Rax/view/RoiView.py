import sys

from PyQt4 import QtGui, QtCore
from wx.lib.pubsub import pub
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import animation
import matplotlib as mpl

from view.UIFiles.T_Rax_ROI_Selector import Ui_roi_selector_main_widget


mpl.rcParams['font.size'] = 10
mpl.rcParams['lines.linewidth'] = 0.5
mpl.rcParams['lines.color'] = 'g'
mpl.rcParams['text.color'] = 'white'
mpl.rc('axes', facecolor='#1E1E1E', edgecolor='white', lw=1, labelcolor='white')
mpl.rc('xtick', color='white')
mpl.rc('ytick', color='white')
mpl.rc('figure', facecolor='#1E1E1E', edgecolor='black')
import numpy as np


class TRaxROIView(QtGui.QWidget, Ui_roi_selector_main_widget):
    def __init__(self, data, parent=None):
        super(TRaxROIView, self).__init__(parent)
        self.data = data
        self.parent = parent

        self.setup_data()
        self.setup_ui()
        self.setup_window()

    def setup_data(self):
        self.img_vmin_rel = 0.05
        self.img_vmax_rel = 0.95

    def setup_ui(self):
        self.setupUi(self)
        self.setWindowTitle('Temperature ROI Selector')
        self.set_validator()
        self.create_graph()
        self.dummy_group.hide()
        self.fitting_roi_box.hide()
        self.downstream_roi_box.hide()
        self.upstream_roi_box.hide()

    def setup_window(self):
        self.resizeEvent = self.resize_graph
        self.axes_frame.leaveEvent = self.axes_leave_event
        self.setWindowFlags(QtCore.Qt.Tool)
        if self.parent is not None:
            self.move(self.parent.x(), self.parent.y() + self.parent.height() + 50)
            self.resize(self.parent.size().width(), 150)

    def set_validator(self):
        self.set_ds_validator()
        self.set_us_validator()
        self.set_fit_validator()

    def set_ds_validator(self):
        self.ds_x_min_txt.setValidator(QtGui.QIntValidator())
        self.ds_x_max_txt.setValidator(QtGui.QIntValidator())
        self.ds_y_min_txt.setValidator(QtGui.QIntValidator())
        self.ds_y_max_txt.setValidator(QtGui.QIntValidator())

    def set_us_validator(self):
        self.us_x_min_txt.setValidator(QtGui.QIntValidator())
        self.us_x_max_txt.setValidator(QtGui.QIntValidator())
        self.us_y_min_txt.setValidator(QtGui.QIntValidator())
        self.us_y_max_txt.setValidator(QtGui.QIntValidator())

    def set_fit_validator(self):
        self.fit_from_txt.setValidator(QtGui.QIntValidator())
        self.fit_to_txt.setValidator(QtGui.QIntValidator())

    def create_graph(self):
        self.figure = Figure(None, dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.axes_frame)

        graph_layout = QtGui.QVBoxLayout(self.axes_frame)
        graph_layout.setContentsMargins(0, 0, 0, 0)
        graph_layout.setSpacing(0)
        graph_layout.setMargin(0)
        graph_layout.addWidget(self.canvas)
        self.canvas.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                  QtGui.QSizePolicy.Expanding)
        self.canvas.updateGeometry()

        self.gs = mpl.gridspec.GridSpec(1, 2, width_ratios=[6, 1])
        self.img_axes = self.figure.add_subplot(self.gs[0, 0])
        self.histogram_axes = self.figure.add_subplot(self.gs[0, 1])

        self.canvas.mpl_connect('button_press_event', self.reset_limits)

    def draw_image(self):
        self.plot_img()
        self.plot_rects()
        self.redraw_figure()
        self.connect_rectangles()
        self.plot_histogram()
        self.plot_histogram_lines()
        self.connect_histogram_lines()

    def plot_img(self):
        self.img_axes.cla()
        self.img_data = self.data.exp_data.get_img_data()
        self.img_max_intensity = np.max(np.max(self.img_data))
        self.img_min_intensity = np.min(np.min(self.img_data))
        self.img_range_intensity = self.img_max_intensity - self.img_min_intensity
        y_max = len(self.img_data) - 1
        x_max = len(self.img_data[0]) - 1
        self.img_axes.set_ylim([0, y_max])
        self.img_axes.set_xlim([0, x_max])

        self.img = self.img_axes.imshow(self.img_data, cmap='copper', aspect='auto',
                                        extent=[0, x_max + 1, y_max + 1, 0],
                                        vmin=self.img_vmin_rel * self.img_range_intensity + self.img_min_intensity,
                                        vmax=self.img_vmax_rel * self.img_range_intensity + self.img_min_intensity)
        self.img_axes.set_ylim([0, len(self.img_data) - 1])
        self.img_axes.set_xlim([0, len(self.img_data[0]) - 1])
        self.img_axes.invert_yaxis()
        self.create_wavelength_x_axis()

    def plot_histogram(self):
        self.histogram_axes.cla()
        self.histogram_data = np.concatenate((np.ravel(self.data.exp_data.get_ds_roi_img()),
                                              np.ravel(self.data.exp_data.get_us_roi_img())))
        self.histogram_axes.hist(self.histogram_data, bins=100,
                                 orientation='horizontal', normed=False, histtype='stepfilled',
                                 log=True, color=(0.40, 0.40, 0.4))
        self.histogram_axes.set_ylim(np.min(np.min(self.data.exp_data.get_img_data())),
                                     np.max(np.max(self.data.exp_data.get_img_data())))
        self.histogram_axes.yaxis.set_visible(False)
        self.histogram_axes.xaxis.set_visible(False)

    def plot_histogram_lines(self):
        histogram_limits = self.histogram_axes.get_ylim()
        img_vmin = self.img_vmin_rel * self.img_range_intensity + self.img_min_intensity
        img_vmax = self.img_vmax_rel * self.img_range_intensity + self.img_min_intensity
        self.histogram_min_line = self.create_histogram_line(img_vmin, [histogram_limits[0], img_vmax - 1],
                                                             "HISTOGRAM MIN")
        self.histogram_max_line = self.create_histogram_line(img_vmax, [img_vmin + 1, histogram_limits[1]],
                                                             "HISTOGRAM MAX")

    def update_histogram(self):
        MoveableLine.reset()
        self.histogram_min_line.active = False
        self.histogram_max_line.active = False
        self.plot_histogram()
        self.plot_histogram_lines()
        self.connect_histogram_lines()
        self.repaint()

    def connect_histogram_lines(self):
        self.histogram_min_line.connect()
        self.histogram_max_line.connect()

    def reset_limits(self, event):
        if event.inaxes == self.histogram_axes:
            if event.button != 1:
                self.setup_data()
                vmin = self.img_vmin_rel * self.img_range_intensity + self.img_min_intensity
                vmax = self.img_vmax_rel * self.img_range_intensity + self.img_min_intensity
                self.histogram_max_line.set_limit( \
                    [vmin + 1, self.histogram_axes.get_ylim()[1]])
                self.histogram_min_line.set_limit(
                    [self.histogram_axes.get_ylim()[0], vmax - 1])
                self.histogram_min_line.set_pos(vmin)
                self.histogram_max_line.set_pos(vmax)
                self.redraw_img()


    def plot_rects(self):
        self.us_rect = self.create_rectangle(self.data.roi_data.us_roi, (1, 0.55, 0), 'US')
        self.ds_rect = self.create_rectangle(self.data.roi_data.ds_roi, (1, 1, 0), 'DS')

    def update_with_new_img(self):
        self.update_img()
        self.update_histogram()
        self.redraw_figure()

    def update_img(self):
        self.ds_rect.active = False
        self.us_rect.active = False
        ResizeableRectangle.reset()
        self.plot_img()
        self.plot_rects()
        self.connect_rectangles()

    def set_img_vmin(self, vmin):
        self.img_vmin_rel = float(vmin - self.img_min_intensity) / self.img_range_intensity
        self.redraw_img()
        self.histogram_max_line.set_limit([vmin + 1, self.histogram_axes.get_ylim()[1]])

    def set_img_vmax(self, vmax):
        self.img_vmax_rel = float(vmax - self.img_min_intensity) / self.img_range_intensity
        self.redraw_img()
        self.histogram_min_line.set_limit([self.histogram_axes.get_ylim()[0], vmax - 1])

    def redraw_img(self):
        ResizeableRectangle.reset()
        self.plot_img()
        self.plot_rects()
        self.redraw_figure()
        self.connect_rectangles()
        self.repaint()

    def create_rectangle(self, roi, color, flag):
        return ResizeableRectangle(self, self.img_axes, self.canvas,
                                   QtCore.QRect(roi.x_min, roi.y_min, roi.get_width(), roi.get_height()), color, flag)

    def connect_rectangles(self):
        self.us_rect.connect()
        self.ds_rect.connect()

    def plot_graph(self):
        self.graph_spec = self.data.get_exp_graph_data()
        self.img_axes.set_xlim(self.graph_spec.get_x_plot_limits())
        self.img_axes.set_ylim(self.graph_spec.get_y_plot_limits())
        self.graph = self.img_axes.plot(self.graph_spec.x, self.graph_spec.y, 'c-', lw=1)

    def plot_lines(self):
        x_limits = self.data.calculate_wavelength(self.data.roi_data.us_roi.get_x_limits())
        axes_xlim = self.img_axes.get_xlim()
        self.min_line = self.create_line(x_limits[0], [axes_xlim[0], x_limits[1] - 1],"MIN")
        self.max_line = self.create_line(x_limits[1], [x_limits[0] + 1, axes_xlim[1]],"MAX")

    def create_line(self, pos, limits, flag):
        return MoveableLine(self, self.img_axes, self.canvas,pos, limits, flag)

    def create_histogram_line(self, pos, limits, flag):
        return MoveableLine(self, self.histogram_axes, self.canvas, pos, limits, flag)

    def connect_lines(self):
        self.min_line.connect()
        self.max_line.connect()

    def create_wavelength_x_axis(self):
        xlimits = self.data.get_x_limits()
        increment = self.get_x_axis_increment()
        xlimits = np.ceil(xlimits / increment) * increment
        xtick_num = np.arange(xlimits[0], xlimits[1], increment)
        xtick_pos = self.data.calculate_ind(xtick_num)
        self.img_axes.set_xticks(xtick_pos)
        self.img_axes.set_xticklabels((map(int, xtick_num)))

    def get_x_axis_increment(self):
        data_x_limits = self.data.get_x_limits()
        possible_increments = [50, 25, 10, 5, 2, 1]
        for increment in possible_increments:
            x_tick_num = np.arange(data_x_limits[0], data_x_limits[1], increment)
            if len(x_tick_num) > 5:
                return increment
        return 0.5

    def redraw_figure(self):
        self.figure.tight_layout(None, 0.4, None, None)
        self.canvas.draw()

    def resize_graph(self, event):
        new_size = self.axes_frame.size()
        self.figure.set_size_inches([new_size.width() / 100.0, new_size.height() / 100.0])
        self.redraw_figure()
        self.update_rect_pick_limits(new_size.width(), new_size.height())

    def axes_leave_event(self, event):
        #QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        QtGui.QApplication.restoreOverrideCursor()

    def update_rect_pick_limits(self, graph_width, graph_height):
        xlimits = self.img_axes.get_xlim()
        ylimits = self.img_axes.get_ylim()
        axes_width = graph_width - 50
        axes_height = graph_height - 50

        fixed_pixel_pick_limit = 3
        x_pick_limit_percentage = fixed_pixel_pick_limit / axes_width
        y_pick_limit_percentage = fixed_pixel_pick_limit / axes_width

        x_range = xlimits[1] - xlimits[0]
        y_range = ylimits[1] - ylimits[0]

    def update_graph_roi(self):
        try:
            self.us_rect.set_roi(self.data.roi_data.us_roi)
            self.ds_rect.set_roi(self.data.roi_data.ds_roi)
        except:
            self.min_line.set_pos(self.data.calculate_wavelength(self.data.roi_data.us_roi.x_min))
            self.max_line.set_pos(self.data.calculate_wavelength(self.data.roi_data.us_roi.x_max))
            self.redraw_figure()

    def update_txt_roi(self):
        ds_txt_roi = self.data.roi_data.ds_roi.get_roi_as_list()
        us_txt_roi = self.data.roi_data.us_roi.get_roi_as_list()
        ds_txt_roi[:2] = self.data.calculate_wavelength(ds_txt_roi[:2])
        us_txt_roi[:2] = self.data.calculate_wavelength(us_txt_roi[:2])
        self.set_ds_txt_roi(ds_txt_roi)
        self.set_us_txt_roi(us_txt_roi)
        self.set_fit_limits(ds_txt_roi[:2])

    def set_ds_txt_roi(self, roi):
        self.ds_x_min_txt.setText(str(int(np.round(roi[0]))))
        self.ds_x_max_txt.setText(str(int(np.round(roi[1]))))
        self.ds_y_min_txt.setText(str(int(np.round(roi[2]))))
        self.ds_y_max_txt.setText(str(int(np.round(roi[3]))))

    def set_us_txt_roi(self, roi):
        self.us_x_min_txt.setText(str(int(np.round(roi[0]))))
        self.us_x_max_txt.setText(str(int(np.round(roi[1]))))
        self.us_y_min_txt.setText(str(int(np.round(roi[2]))))
        self.us_y_max_txt.setText(str(int(np.round(roi[3]))))

    def set_fit_limits(self, limits):
        self.fit_from_txt.setText(str(int(np.round(limits[0]))))
        self.fit_to_txt.setText(str(int(np.round(limits[1]))))

    def get_ds_roi(self):
        return [int(str(self.ds_x_min_txt.text())),
                int(str(self.ds_x_max_txt.text())),
                int(str(self.ds_y_min_txt.text())),
                int(str(self.ds_y_max_txt.text()))]

    def get_us_roi(self):
        return [int(str(self.us_x_min_txt.text())),
                int(str(self.us_x_max_txt.text())),
                int(str(self.us_y_min_txt.text())),
                int(str(self.us_y_max_txt.text()))]

    def get_fit_x_limits(self):
        return [int(str(self.fit_from_txt.text())),
                int(str(self.fit_to_txt.text()))]


class MoveableLine:
    lock = None  # only one can be animated at a time
    lines = []

    def __init__(self, parent, axes, canvas, pos, limit, flag):
        self.flag = flag
        self.parent = parent
        self.axes = axes
        self.canvas = canvas

        self.xlim = self.axes.get_xlim()
        self.ylim = self.axes.get_ylim()

        self.y_border = 0.05 * (self.ylim[1] - self.ylim[0])

        self.line, = axes.plot(self.xlim, [pos, pos], color=(1, 1, 1), lw=2)
        self.limit = limit

        self.active = True  #needed because of garbage collection issues
        self.press = None
        self.mode = None
        self.is_animated = False

        MoveableLine.lines.append(self.line)

        self.animation_timer = QtCore.QTimer(self.parent)
        self.update_timer = QtCore.QTimer(self.parent)
        self.update_timer.setInterval(75)
        self.parent.connect(self.update_timer, QtCore.SIGNAL('timeout()'), self.send_message)

    def set_pos(self, pos):
        if self.press == None:
            self.line.set_ydata([pos, pos])

    def connect(self):
        self.cidpress = self.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.line.axes: return
        if MoveableLine.lock is not None: return
        if self.active is not True: return
        y_click = event.ydata
        y0 = self.line.get_ydata()[0]

        if y0 - self.y_border <= y_click <= y0 + self.y_border:
            self.press = y0, y_click
            MoveableLine.lock = self
            self.line.set_animated(True)
            if not self.is_animated:
                ResizeableRectangle.lock = self
                self.animate()
                self.update_timer.start()
                self.is_animated = True

    def animate(self):
        try:
            self.ani._stop()
        except:
            pass
        self.ani = animation.FuncAnimation(self.axes.figure, self.get_lines, interval=5, frames=1, blit=True)

    def get_lines(self, i):
        return MoveableLine.lines

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        x_mouse = event.xdata
        y_mouse = event.ydata
        y0 = self.line.get_ydata()[0]

        if event.inaxes != self.line.axes:
            if self.press is not None:
                for line in MoveableLine.lines:
                    line.set_animated(False)
                try:
                    self.ani._stop()
                    self.ani._draw_next_frame(self.get_lines, True)
                    self.update_timer.stop()
                    self.send_message()
                except:
                    pass
                self.press = None
                self.mode = None
                MoveableLine.lock = None
                self.is_animated = False
                QtGui.QApplication.restoreOverrideCursor()
                QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
                QtGui.QApplication.restoreOverrideCursor()
            else:
                QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
                QtGui.QApplication.restoreOverrideCursor()
            return

        if MoveableLine.lock is None:
            if y_mouse >= y0 - self.y_border and y_mouse <= y0 + self.y_border and \
                            x_mouse >= self.line.axes.get_xlim()[0] and \
                            x_mouse <= self.line.axes.get_xlim()[1]:

                QtGui.QApplication.restoreOverrideCursor()
                QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
            else:
                for line in MoveableLine.lines:
                    if y_mouse >= line.get_ydata()[0] - self.y_border \
                            and y_mouse <= line.get_ydata()[0] + self.y_border and \
                                    x_mouse >= line.axes.get_xlim()[0] and \
                                    x_mouse <= line.axes.get_xlim()[1]:
                        return
                QtGui.QApplication.restoreOverrideCursor()
                QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
                QtGui.QApplication.restoreOverrideCursor()
                return

        if self.press is None:
            return

        y0, ypress = self.press
        dx = event.xdata - ypress
        y_new_pos = y_mouse

        if y_new_pos >= self.limit[0] and y_new_pos <= self.limit[1]:
            self.line.set_ydata([y_new_pos, y_new_pos])
        elif y_new_pos < self.limit[0]:
            self.line.set_ydata([self.limit[0], self.limit[0]])
        elif y_new_pos > self.limit[1]:
            self.line.set_ydata([self.limit[1], self.limit[1]])

    def send_message(self):
        try:
            pub.sendMessage(self.flag + " ROI LINE CHANGED", data=self.line.get_ydata()[0])
        except AttributeError:
            pass

    def on_release(self, event):
        for line in MoveableLine.lines:
            line.set_animated(False)
        try:
            self.ani._stop()
            self.ani._draw_next_frame(self.get_lines, True)
            self.update_timer.stop()
        except:
            pass

        self.press = None
        self.mode = None
        MoveableLine.lock = None
        self.is_animated = False

    def set_limit(self, limit):
        self.limit = limit

    @classmethod
    def reset(cls):
        cls.lines = []


class ResizeableRectangle:
    lock = None  #only one rect can be animated at a time
    rects = []

    def __init__(self, parent, axes, canvas, init_rect, color, flag):
        self.flag = flag
        self.parent = parent
        self.axes = axes
        self.canvas = canvas
        self.color = color

        self.xlim = self.axes.get_xlim()
        self.ylim = self.axes.get_ylim()

        self.x_border = 25
        self.y_border = 3
        self.min_width = 5
        self.min_height = 1

        self.rect = mpl.patches.Rectangle((init_rect.x(), init_rect.y()), init_rect.width(), init_rect.height(),
                                          ec=self.color, fill=False, lw=2)
        self.axes.add_artist(self.rect)

        ResizeableRectangle.rects.append(self.rect)

        self.active = True  #needed because of garbage collection issues
        self.press = None
        self.mode = None
        self.is_animated = False

        self.animation_timer = QtCore.QTimer(self.parent)

        self.update_timer = QtCore.QTimer(self.parent)
        self.update_timer.setInterval(40)
        self.parent.connect(self.update_timer, QtCore.SIGNAL('timeout()'), self.send_message)

    def set_border(self, x_border, y_border):
        self.x_border = x_border
        self.y_border = y_border

    def set_roi(self, roi):
        if self.press == None:
            self.rect.set_y(roi.y_min)
            self.rect.set_x(roi.x_min)
            self.rect.set_height(roi.get_height())
            self.rect.set_width(roi.get_width())
            self.rect.figure.canvas.draw()

    def update_limits(self):
        self.xlim = self.axes.get_xlim()
        self.ylim = self.axes.get_ylim()

    def connect(self):
        self.cidpress = self.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.rect.axes: return
        if ResizeableRectangle.lock is not None: return
        if self.active is not True: return
        y_click = event.ydata
        x_click = event.xdata
        y0 = self.rect.get_y()
        x0 = self.rect.get_x()
        height = self.rect.get_height()
        width = self.rect.get_width()

        if y_click >= y0 - self.y_border and y_click <= y0 + height + self.y_border and \
                        x_click >= x0 - self.x_border and x_click <= x0 + width + self.x_border:
            self.set_mode(x_click, y_click, self.rect)
            self.press = x0, y0, x_click, y_click
            for rect in ResizeableRectangle.rects:
                rect.set_animated(True)
            if not self.is_animated:
                ResizeableRectangle.lock = self
                self.animate()
                self.update_timer.start()
                self.is_animated = True

    def animate(self):
        try:
            self.ani._stop()
        except:
            pass
        self.ani = animation.FuncAnimation(self.axes.figure, self.get_rect, interval=5, frames=1, blit=True)

    def get_rect(self, i):
        return ResizeableRectangle.rects

    def set_mode(self, x_click, y_click, rect):
        self.mode = self.get_mode(x_click, y_click, rect)

    def get_mode(self, x_mouse_pos, y_mouse_pos, rect):
        y0 = rect.get_y()
        x0 = rect.get_x()
        height = rect.get_height()
        width = rect.get_width()
        if y_mouse_pos >= y0 + self.y_border / 2.0 and y_mouse_pos <= y0 + height - self.y_border / 2.0 and \
                        x_mouse_pos >= x0 + self.x_border / 2.0 and x_mouse_pos <= x0 + width - self.x_border / 2.0:
            return 'move'
        elif y_mouse_pos > y0 + height - self.y_border and y_mouse_pos <= y0 + height + self.y_border and \
                        x_mouse_pos >= x0 + self.x_border and x_mouse_pos <= x0 + width - self.x_border:
            return 'resize_top'
        elif y_mouse_pos > y0 - self.y_border and y_mouse_pos < y0 + self.y_border and \
                        x_mouse_pos >= x0 + self.x_border and x_mouse_pos <= x0 + width - self.x_border:
            return 'resize_bottom'
        elif x_mouse_pos > x0 + width - self.x_border and x_mouse_pos <= x0 + width + self.x_border and \
                        y_mouse_pos >= y0 - self.y_border and y_mouse_pos <= y0 + height + self.y_border:
            return 'resize_right'
        elif x_mouse_pos > x0 - self.x_border and x_mouse_pos < x0 + self.x_border and \
                        y_mouse_pos >= y0 - self.y_border and y_mouse_pos <= y0 + height + self.y_border:
            return 'resize_left'
        else:
            return 'None'

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if event.inaxes != self.rect.axes:
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            QtGui.QApplication.restoreOverrideCursor()
            return

        y0 = self.rect.get_y()
        x0 = self.rect.get_x()
        height = self.rect.get_height()
        width = self.rect.get_width()
        y_click = event.ydata
        x_click = event.xdata
        if self.press is None:
            if ResizeableRectangle.lock is None:
                mode = self.get_mode(x_click, y_click, self.rect)
                if mode == 'move':
                    QtGui.QApplication.restoreOverrideCursor()
                    QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
                elif mode == 'resize_bottom' or mode == 'resize_top':
                    QtGui.QApplication.restoreOverrideCursor()
                    QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
                elif mode == 'resize_right' or mode == 'resize_left':
                    QtGui.QApplication.restoreOverrideCursor()
                    QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
                else:
                    for rect in ResizeableRectangle.rects:
                        rect_mode = self.get_mode(x_click, y_click, rect)
                        if rect_mode is not 'None':
                            return

                    QtGui.QApplication.restoreOverrideCursor()
                    QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
                    QtGui.QApplication.restoreOverrideCursor()
            return

        x0, y0, xpress, ypress = self.press
        dy = event.ydata - ypress
        dx = event.xdata - xpress

        if self.mode == 'move':
            y_new_pos = int(y0 + dy)
            x_new_pos = int(x0 + dx)
            top_pos = y_new_pos + height
            right_pos = x_new_pos + width
            if y_new_pos >= 0 and (top_pos) <= self.ylim[0]:
                self.rect.set_y(y_new_pos)
            elif y_new_pos <= 0:
                self.rect.set_y(0)
            elif top_pos > self.ylim[0]:
                self.rect.set_y(self.ylim[0] - height)

            if x_new_pos >= 0 and (right_pos) <= self.xlim[1]:
                self.rect.set_x(x_new_pos)
            elif x_new_pos <= 0:
                self.rect.set_x(0)
            elif right_pos > self.xlim[1]:
                self.rect.set_x(self.xlim[1] - width)

        elif self.mode == 'resize_top':
            new_height = int(event.ydata - y0)
            if new_height < self.min_height:
                new_height = self.min_height
            self.rect.set_height(new_height)
        elif self.mode == 'resize_bottom':
            new_height = int(self.rect.get_y() - y_click + height)
            if new_height < self.min_height:
                new_height = self.min_height
            self.rect.set_height(new_height)
            self.rect.set_y(int(self.rect.get_y() + height - new_height))
        elif self.mode == 'resize_right':
            new_width = int(event.xdata - x0)
            if new_width < self.min_width:
                new_width = self.min_width
            self.rect.set_width(new_width)
        elif self.mode == 'resize_left':
            new_width = int(self.rect.get_x() - x_click + width)
            if new_width < self.min_width:
                new_width = self.min_width
            self.rect.set_width(new_width)
            self.rect.set_x(int(self.rect.get_x() + width - new_width))

    def send_message(self):
        try:
            pub.sendMessage(self.flag + " ROI GRAPH CHANGED", data=
            [int(self.rect.get_x()), int(self.rect.get_x() + self.rect.get_width()),
             int(self.rect.get_y()), int(self.rect.get_y() + self.rect.get_height())])
        except AttributeError:
            pass

    def on_release(self, event):
        'on release we reset the press Model'
        for rect in ResizeableRectangle.rects:
            rect.set_animated(False)
        try:
            self.ani._stop()
            self.ani._draw_next_frame(self.get_rect, True)
            self.update_timer.stop()
            self.send_message()
        except:
            pass
        self.press = None
        self.mode = None
        ResizeableRectangle.lock = None
        self.is_animated = False

    @classmethod
    def reset(cls):
        cls.rects = []


if __name__ == "__main__":
    from Model.TemperatureData import TemperatureData
    app = QtGui.QApplication(sys.argv)
    data = TemperatureData()
    view = TRaxROIView(data)
    view.show()
    app.exec_()