
__author__ = 'Clemens Prescher'

import pyqtgraph as pg
pg.setConfigOption('useOpenGL', True)
pg.setConfigOption('leftButtonPan', False)
pg.setConfigOption('background', 'k')
pg.setConfigOption('foreground', 'w')
pg.setConfigOption('antialias', True)
from  pyqtgraph.exporters.ImageExporter import ImageExporter
import numpy as np
from PyQt4 import QtCore, QtGui
from VerHistogramLUTItem import VerHistogramLUTItem


class ImgView(QtCore.QObject):
    mouse_moved = QtCore.pyqtSignal(float, float)
    mouse_left_clicked = QtCore.pyqtSignal(float, float)
    mouse_left_double_clicked = QtCore.pyqtSignal(float, float)

    def __init__(self, pg_layout, orientation='vertical'):
        super(ImgView, self).__init__()
        self.pg_layout = pg_layout
        self.orientation = orientation

        self.create_graphics()
        self.modify_mouse_behavior()

        self.img_data = None

    def create_graphics(self):
        self.img_view_box = self.pg_layout.addViewBox(0, 0)

        #create the item handling the Model img
        self.data_img_item = pg.ImageItem()
        self.img_view_box.addItem(self.data_img_item)
        self.img_histogram_LUT = VerHistogramLUTItem(self.data_img_item, orientation='vertical')
        self.img_histogram_LUT.gradient.loadPreset('thermal')

        #create axis:
        self.axis = pg.AxisItem(orientation='bottom', linkView=self.img_view_box)
        self.pg_layout.addItem(self.axis, 1,0)


        self.pg_layout.addItem(self.img_histogram_LUT, 0, 1)


    def plot_image(self, img_data, autoRange=False):
        self.img_data = img_data
        self.data_img_item.setImage(img_data.T, autoRange)
        if autoRange:
            self.auto_range()

    def save_img(self, filename):
        exporter = ImageExporter(self.img_view_box)
        exporter.parameters()['width'] = 2048
        exporter.export(filename)

    def auto_range(self):
        hist_x, hist_y = self.data_img_item.getHistogram()
        ind = np.where(np.cumsum(hist_y) < (0.995 * np.sum(hist_y)))
        if len(ind[0]):
            self.img_histogram_LUT.setLevels(np.min(np.min(self.img_data)), hist_x[ind[0][-1]])
        else:
            self.img_histogram_LUT.setLevels(np.min(np.min(self.img_data)), 0.5 * np.max(hist_x))


    def modify_mouse_behavior(self):
        #different mouse handlers
        self.img_view_box.setMouseMode(self.img_view_box.RectMode)

        self.pg_layout.scene().sigMouseMoved.connect(self.mouseMoved)
        self.img_view_box.mouseClickEvent = self.myMouseClickEvent
        self.img_view_box.mouseDragEvent = self.myMouseDragEvent
        self.img_view_box.mouseDoubleClickEvent = self.myMouseDoubleClickEvent
        self.img_view_box.wheelEvent = self.myWheelEvent

    def mouseMoved(self, pos):
        pos = self.data_img_item.mapFromScene(pos)
        self.mouse_moved.emit(pos.x(), pos.y())

    def myMouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton or \
                (ev.button() == QtCore.Qt.LeftButton and \
                             ev.modifiers() & QtCore.Qt.ControlModifier):
            view_range = np.array(self.img_view_box.viewRange()) * 2
            if self.img_data is not None:
                if (view_range[0][1] - view_range[0][0]) > self.img_data.shape[1] and \
                                (view_range[1][1] - view_range[1][0]) > self.img_data.shape[0]:
                    self.img_view_box.autoRange()
                else:
                    self.img_view_box.scaleBy(2)

        elif ev.button() == QtCore.Qt.LeftButton:
            pos = self.img_view_box.mapSceneToView(ev.pos())
            y = pos.x()
            x = pos.y()
            self.mouse_left_clicked.emit(x, y)

    def myMouseDoubleClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.img_view_box.autoRange()
        if ev.button() == QtCore.Qt.LeftButton:
            pos = self.img_view_box.mapSceneToView(ev.pos())
            self.mouse_left_double_clicked.emit(pos.x(), pos.y())

    def myMouseDragEvent(self, ev, axis=None):
        #most of this code is copied behavior of left click mouse drag from the original code
        ev.accept()
        pos = ev.pos()
        lastPos = ev.lastPos()
        dif = pos - lastPos
        dif *= -1
        ## Ignore axes if mouse is disabled
        mouseEnabled = np.array(self.img_view_box.state['mouseEnabled'], dtype=np.float)
        mask = mouseEnabled.copy()
        if axis is not None:
            mask[1 - axis] = 0.0

        if ev.button() == QtCore.Qt.RightButton or \
                (ev.button() == QtCore.Qt.LeftButton and \
                             ev.modifiers() & QtCore.Qt.ControlModifier):
            #determine the amount of translation
            tr = dif * mask
            tr = self.img_view_box.mapToView(tr) - self.img_view_box.mapToView(pg.Point(0, 0))
            x = tr.x()
            y = tr.y()

            self.img_view_box.translateBy(x=x, y=y)
            self.img_view_box.sigRangeChangedManually.emit(self.img_view_box.state['mouseEnabled'])
        else:
            pg.ViewBox.mouseDragEvent(self.img_view_box, ev)

    def myWheelEvent(self, ev):
        if ev.delta() > 0:
            pg.ViewBox.wheelEvent(self.img_view_box, ev)
        else:
            view_range = np.array(self.img_view_box.viewRange())
            if self.img_data is not None:
                if (view_range[0][1] - view_range[0][0]) > self.img_data.shape[1] and \
                                (view_range[1][1] - view_range[1][0]) > self.img_data.shape[0]:
                    self.img_view_box.autoRange()
                else:
                    pg.ViewBox.wheelEvent(self.img_view_box, ev)
            else:
                pg.ViewBox.wheelEvent(self.img_view_box, ev)