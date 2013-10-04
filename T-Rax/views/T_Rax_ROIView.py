from UIFiles.T_Rax_ROI_Selector import Ui_roi_selector_main_widget
from T_Rax_Data import TraxData, ROI
from PyQt4 import QtGui, QtCore
import sys
import colors
from wx.lib.pubsub import Publisher as pub


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import animation
import matplotlib as mpl

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
        super(TRaxROIView, self).__init__(None)
        self.data = data
        self.setupUi(self)   
        self.setWindowTitle('T-rax ver 0.2 ROI Selector')
        self.set_validator()     
        self.create_graph()
        self.draw_image()
        self.resizeEvent = self.resize_graph
        self.setWindowFlags(QtCore.Qt.Tool)
        self.move(parent.x(), parent.y()+parent.height()+50)
        self.resize(parent.size().width(),150)
    
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
        graph_layout.setContentsMargins(0,0,0,0)
        graph_layout.setSpacing(0)
        graph_layout.setMargin(0)
        graph_layout.addWidget(self.canvas)
        self.canvas.setSizePolicy( QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        self.canvas.updateGeometry()
        self.axes = self.figure.add_subplot(111)
        self.old_size = 0,0

    def draw_image(self):
        try:
            self.plot_img()
            self.plot_rects()
            self.redraw_figure()
            self.connect_rectangles()
            self.mode = 'IMG'
            pub.sendMessage("IMG LOADED", None)
            print 'image_loaded'
        except NotImplementedError, e:
            self.plot_graph()
            self.plot_lines()
            self.redraw_figure()
            self.connect_lines()
            self.mode='GRAPH'
            print 'graph_loaded'
            pub.sendMessage('GRAPH LOADED', None)

    def plot_img(self):
        self.axes.cla()
        self.img_data = self.data.get_exp_img_data()
        y_max = len(self.data.get_exp_img_data()) - 1
        x_max = len(self.data.get_exp_img_data()[0]) - 1
        self.axes.set_ylim([0,y_max])
        self.axes.set_xlim([0,x_max])
        scaling = mpl.colors.Normalize()
        scaling.autoscale(self.img_data)
        self.img = self.axes.imshow(self.img_data, cmap = 'copper', aspect = 'auto',
                                    extent=[0,x_max + 1,y_max + 1,0],
                                    norm=scaling)
        self.axes.set_ylim([0,len(self.img_data) - 1])
        self.axes.set_xlim([0,len(self.img_data[0]) - 1])
        self.axes.invert_yaxis()
        self.img.autoscale()
        self.create_wavelength_x_axis()

    def plot_rects(self):
        self.us_rect = self.create_rectangle(self.data.roi_data.us_roi, colors.UPSTREAM_COLOR_NORM, 'US')
        self.ds_rect = self.create_rectangle(self.data.roi_data.ds_roi, colors.DOWNSTREAM_COLOR_NORM, 'DS')    

    def update_img(self):
        #need to reset the ResizeableRectangles like that, because the Garbage Collector is not fast enough to
        #delete all the rectangles.
        try:
            self.ds_rect.active=False
            self.us_rect.active=False
            ResizeableRectangle.reset()
        except:
            pass
        try:
            self.min_line.active=False
            self.max_line.active=False
            MoveableLine.reset()
        except:
            pass
        try:
            self.plot_img()
            self.plot_rects()
            self.redraw_figure()
            self.connect_rectangles()
            self.mode = 'IMG'
            pub.sendMessage("IMG LOADED", None)
        except NotImplementedError, e:
            self.plot_graph()
            self.plot_lines()
            self.redraw_figure()
            self.connect_lines()
            self.mode='GRAPH'
            pub.sendMessage('GRAPH LOADED', None)
        
    def create_rectangle(self, roi, color, flag):
        return ResizeableRectangle(self, self.axes, self.canvas,QtCore.QRect(roi.x_min,roi.y_min, roi.get_width(),roi.get_height()), color, flag)

    def connect_rectangles(self):
        self.us_rect.connect()
        self.ds_rect.connect()

    def plot_graph(self):
        self.graph_spec = self.data.get_exp_graph_data()
        self.axes.set_xlim(self.graph_spec.get_x_plot_limits())
        self.axes.set_ylim(self.graph_spec.get_y_plot_limits())
        self.graph = self.axes.plot(self.graph_spec.x, self.graph_spec.y, 'c-', lw=1)

    def plot_lines(self):
        x_limits = self.data.calculate_wavelength(self.data.roi_data.us_roi.get_x_limits())
        axes_xlim = self.axes.get_xlim()
        self.min_line = self.create_line(x_limits[0], [axes_xlim[0], x_limits[1] - 1],"MIN")
        self.max_line = self.create_line(x_limits[1], [x_limits[0] + 1, axes_xlim[1]],"MAX")

    def create_line(self, pos, limits, flag):
        return MoveableLine(self, self.axes, self.canvas,pos, limits, flag)

    def connect_lines(self):
        self.min_line.connect()
        self.max_line.connect()

    def update_line_limits(self):
        x_limits = self.data.calculate_wavelength(self.data.roi_data.us_roi.get_x_limits())
        axes_xlim = self.axes.get_xlim()
        self.min_line.limit = [axes_xlim[0], x_limits[1] - 1]
        self.max_line.limit = [x_limits[0] + 1, axes_xlim[1]]

    def create_wavelength_x_axis(self):
        xlimits = self.data.get_x_limits()
        increment = self.get_x_axis_increment()
        xlimits = np.ceil(xlimits / increment) * increment
        xtick_num = np.arange(xlimits[0],xlimits[1],increment)
        xtick_pos = self.data.calculate_ind(xtick_num)
        self.axes.set_xticks(xtick_pos)
        self.axes.set_xticklabels((map(int,xtick_num)))

    def get_x_axis_increment(self):
        data_x_limits = self.data.get_x_limits()
        possible_increments = [50,25,10,5,2,1]
        for increment in possible_increments:
            x_tick_num=np.arange(data_x_limits[0],data_x_limits[1],increment)
            if len(x_tick_num)>5:
                return increment
        return 0.5

    def redraw_figure(self):
        self.figure.tight_layout(None, 0.4, None, None)
        self.canvas.draw()

    def resize_graph(self, event):
        new_size=self.axes_frame.size()
        self.figure.set_size_inches([new_size.width() / 100.0, new_size.height() / 100.0])
        self.redraw_figure()

    def update_graph_roi(self):
        try:
            self.us_rect.set_roi(self.data.roi_data.us_roi)
            self.ds_rect.set_roi(self.data.roi_data.ds_roi)
        except:
            self.min_line.set_roi(self.data.calculate_wavelength(self.data.roi_data.us_roi.x_min))
            self.max_line.set_roi(self.data.calculate_wavelength(self.data.roi_data.us_roi.x_max))
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
    lock = None # only one can be animated at a time
    lines=[]
    def __init__(self, parent, axes, canvas, pos, limit, flag):
        self.flag = flag
        self.parent = parent
        self.axes = axes
        self.canvas = canvas
        
        self.xlim = self.axes.get_xlim()
        self.ylim = self.axes.get_ylim()

        self.x_border = 0.05 * (self.xlim[1] - self.xlim[0])

        self.line, = axes.plot([pos, pos], self.ylim, 'w-', lw=3)
        self.limit = limit
        self.press = None
        self.mode = None
        self.active = True

        MoveableLine.lines.append(self.line)
        
        self.is_animated = False
        self.animation_timer=QtCore.QTimer(self.parent)
        self.update_timer = QtCore.QTimer(self.parent)
        self.update_timer.setInterval(40)
        self.parent.connect(self.update_timer,QtCore.SIGNAL('timeout()'), self.send_message)

    def set_roi(self, pos):
        if self.press == None:
            self.line.set_xdata([pos,pos])

    def update_limits(self):
        self.xlim = self.axes.get_xlim()
        self.ylim = self.axes.get_ylim()
        self.x_border = 0.05 * (self.xlim[1] - self.xlim[0])
        self.line.set_y(self.axes.get_ylim)

    def connect(self):
        self.cidpress = self.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.line.axes: return
        if MoveableLine.lock is not None: return
        if self.active is not True: return
        x_click = event.xdata
        x0 = self.line.get_xdata()[0]

        if x_click >= x0 - self.x_border and x_click <= x0 + self.x_border:
            self.press = x0, x_click
            MoveableLine.lock = self
            self.line.set_animated(True)
            if not self.is_animated:
                ResizeableRectangle.lock = self
                self.animate()
                self.update_timer.start()
                self.is_animated=True
    
    def animate(self):
        try: 
            self.ani._stop()
        except:
            pass
        self.ani = animation.FuncAnimation(self.axes.figure, self.get_lines, interval=5, frames=1, blit=True)

    def get_lines(self,i):
        return MoveableLine.lines

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.line.axes: return
        
        x_click = event.xdata
        x0, xpress = self.press
        dx = event.xdata - xpress
        x_new_pos = x_click

        if x_new_pos >= self.limit[0] and x_new_pos <= self.limit[1]:
            self.line.set_xdata([x_new_pos,x_new_pos])
        elif x_new_pos < self.limit[0]:
            self.line.set_xdata([self.limit[0], self.limit[0]])
        elif x_new_pos > self.limit[1]:
            self.line.set_xdata([self.limit[1], self.limit[1]])

    def send_message(self):
        try:
            pub.sendMessage(self.flag + " ROI LINE CHANGED", self.line.get_xdata()[0])
        except AttributeError:
            pass

    def on_release(self, event):
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
        self.is_animated=False
        self.parent.update_line_limits()

    def set_limit(self,limit):
        self.limit = limit

    @classmethod
    def reset(cls):
        cls.lines = []

class ResizeableRectangle:
    lock = None #only one rect can be animated at a time
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

        self.rect = mpl.patches.Rectangle((init_rect.x(),init_rect.y()),init_rect.width(), init_rect.height(), ec=self.color, fill=False, lw=2)
        self.axes.add_artist(self.rect)

        ResizeableRectangle.rects.append(self.rect)
              
        self.active = True #needed because of garbage collection issues
        self.press = None 
        self.mode = None
        self.is_animated = False
        
        self.animation_timer=QtCore.QTimer(self.parent)

        self.update_timer = QtCore.QTimer(self.parent)
        self.update_timer.setInterval(40)
        self.parent.connect(self.update_timer,QtCore.SIGNAL('timeout()'), self.send_message)

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
            self.set_mode(x_click, y_click, x0, y0, width, height)
            self.press = x0, y0, x_click, y_click
            for rect in ResizeableRectangle.rects:
                rect.set_animated(True)
            if not self.is_animated:
                ResizeableRectangle.lock = self
                self.animate()
                self.update_timer.start()
                self.is_animated=True

    def animate(self):
        try: 
            self.ani._stop()
        except:
            pass
        self.ani = animation.FuncAnimation(self.axes.figure, self.get_rect, interval=5, frames=1, blit=True)

    def get_rect(self,i):
        return ResizeableRectangle.rects

    def set_mode(self,x_click, y_click, x0, y0, width, height):
        if y_click >= y0 + self.y_border / 2.0 and y_click <= y0 + height - self.y_border / 2.0 and \
            x_click >= x0 + self.x_border / 2.0 and x_click <= x0 + width - self.x_border / 2.0:
            self.mode = 'move'
        elif y_click > y0 + height - self.y_border and y_click <= y0 + height + self.y_border and \
            x_click >= x0 + self.x_border and x_click <= x0 + width - self.x_border:
            self.mode = 'resize_top'
        elif y_click > y0 - self.y_border and y_click < y0 + self.y_border and \
            x_click >= x0 + self.x_border and x_click <= x0 + width - self.x_border:
            self.mode = 'resize_bottom'
        elif x_click > x0 + width - self.x_border and x_click <= x0 + width + self.x_border and \
            y_click >= y0 - self.y_border and y_click <= y0 + height + self.y_border:
            self.mode = 'resize_right'
        elif x_click > x0 - self.x_border and x_click < x0 + self.x_border and \
            y_click >= y0 - self.y_border and y_click <= y0 + height + self.y_border:
            self.mode = 'resize_left'

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.rect.axes: return
        
        y_click = event.ydata
        x_click = event.xdata
        x0, y0, xpress, ypress = self.press
        dy = event.ydata - ypress
        dx = event.xdata - xpress
        height = self.rect.get_height()
        width = self.rect.get_width()

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
            pub.sendMessage(self.flag + " ROI GRAPH CHANGED", 
                        [int(self.rect.get_x()),int(self.rect.get_x() + self.rect.get_width()),
                         int(self.rect.get_y()),int(self.rect.get_y() + self.rect.get_height())])
        except AttributeError:
            pass

    def on_release(self, event):
        'on release we reset the press data'
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
        self.is_animated=False

    @classmethod
    def reset(cls):
        cls.rects = []


if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    data=TraxData()
    view=TRaxROIView(data)
    view.show()
    app.exec_()