from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib as mpl

from view.UIFiles.T_Rax_ROI_Ruby_Selector import Ui_roi_selector_ruby_widget
from view.old.RoiView import ResizeableRectangle


mpl.rcParams['font.size'] = 10
mpl.rcParams['lines.linewidth'] = 0.5
mpl.rcParams['lines.color'] = 'g'
mpl.rcParams['text.color'] = 'white'
mpl.rc('axes', facecolor='#1E1E1E', edgecolor='white', lw=1, labelcolor='white')
mpl.rc('xtick', color='white')
mpl.rc('ytick', color='white')
mpl.rc('figure', facecolor='#1E1E1E', edgecolor='black')
import numpy as np


class TRaxROIViewRuby(QtGui.QWidget, Ui_roi_selector_ruby_widget):
    def __init__(self, data, parent=None):
        super(TRaxROIViewRuby, self).__init__(None)
        self.data = data
        self.setupUi(self)
        self.setWindowTitle('Ruby ROI Selector')
        self.set_validator()
        self.create_graph()
        self.draw_image()
        self.resizeEvent = self.resize_graph
        self.setWindowFlags(QtCore.Qt.Tool)
        self.resize(900, 150)
        self.move(parent.x(), parent.y() + parent.height() + 50)

    def set_validator(self):
        self.x_min_txt.setValidator(QtGui.QIntValidator())
        self.x_max_txt.setValidator(QtGui.QIntValidator())
        self.y_min_txt.setValidator(QtGui.QIntValidator())
        self.y_max_txt.setValidator(QtGui.QIntValidator())

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
        self.axes = self.figure.add_subplot(111)
        self.old_size = 0, 0

    def draw_image(self):
        self.plot_img()
        self.plot_rects()
        self.redraw_figure()
        self.connect_rectangles()
        self.mode = 'IMG'

    def plot_img(self):
        self.axes.cla()
        self.img_data = self.data.exp_data.get_img_data()
        y_max = len(self.img_data) - 1
        x_max = len(self.img_data[0]) - 1
        self.axes.set_ylim([0, y_max])
        self.axes.set_xlim([0, x_max])
        img_data_1d = np.reshape(self.img_data, np.size(self.img_data))
        img_data_1d_sorted = np.sort(img_data_1d)
        self.img = self.axes.imshow(self.img_data, cmap='copper', aspect='auto',
                                    extent=[0, x_max + 1, y_max + 1, 0],
                                    vmin=img_data_1d_sorted[int(0.3 * len(img_data_1d))], vmax=max(img_data_1d))
        self.axes.set_ylim([0, len(self.img_data) - 1])
        self.axes.set_xlim([0, len(self.img_data[0]) - 1])
        self.axes.invert_yaxis()
        self.create_wavelength_x_axis()

    def plot_rects(self):
        self.rect = self.create_rectangle(self.data.roi, (0.77, 0, 0.01), 'SINGLE')

    def update_img(self):
        self.plot_img()
        # need to reset the ResizeableRectangles like that, because the Garbage Collector is not fast enough to
        #delete all the rectangles.
        self.rect.active = False
        ResizeableRectangle.reset()
        #----------------------------------------------------
        self.plot_rects()
        self.redraw_figure()
        self.connect_rectangles()

    def create_rectangle(self, roi, color, flag):
        return ResizeableRectangle(self, self.axes, self.canvas,
                                   QtCore.QRect(roi.x_min, roi.y_min, roi.get_width(), roi.get_height()), color, flag)

    def connect_rectangles(self):
        self.rect.connect()

    def create_wavelength_x_axis(self):
        xlimits = self.data.get_x_limits()
        increment = self.get_x_axis_increment()
        xlimits = np.ceil(xlimits / increment) * increment
        xtick_num = np.arange(xlimits[0], xlimits[1], increment)
        xtick_pos = self.data.get_index_from(xtick_num)
        self.axes.set_xticks(xtick_pos)
        self.axes.set_xticklabels((map(int, xtick_num)))

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

    def update_graph_roi(self):
        self.rect.set_roi(self.data.roi)

    def update_txt_roi(self):
        txt_roi = self.data.roi.as_list()
        txt_roi[:2] = self.data.get_wavelength_from(txt_roi[:2])
        self.set_txt_roi(txt_roi)

    def set_txt_roi(self, roi):
        self.x_min_txt.setText(str(int(np.round(roi[0]))))
        self.x_max_txt.setText(str(int(np.round(roi[1]))))
        self.y_min_txt.setText(str(int(np.round(roi[2]))))
        self.y_max_txt.setText(str(int(np.round(roi[3]))))

    def get_roi(self):
        return [int(str(self.x_min_txt.text())),
                int(str(self.x_max_txt.text())),
                int(str(self.y_min_txt.text())),
                int(str(self.y_max_txt.text()))]