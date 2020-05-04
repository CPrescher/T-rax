# -*- coding: utf-8 -*-
# T-Rax - GUI program for analysis of spectroscopy data during
# diamond anvil cell experiments
# Copyright (C) 2016 Clemens Prescher (clemens.prescher@gmail.com)
# Institute for Geology and Mineralogy, University of Cologne
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from functools import partial

import numpy as np

from qtpy import QtCore, QtWidgets, QtGui
import pyqtgraph as pg
from pyqtgraph.graphicsItems.ROI import Handle

from .HistogramLUTItem import HistogramLUTItem

from .Widgets import StatusBar

pg.setConfigOption('useOpenGL', False)
pg.setConfigOption('leftButtonPan', False)
pg.setConfigOption('background', (30, 30, 30))
pg.setConfigOption('foreground', 'w')
pg.setConfigOption('antialias', True)


class RoiWidget(QtWidgets.QWidget):
    rois_changed = QtCore.Signal(list)

    def __init__(self, roi_num=1, roi_titles=('',), roi_colors=((255, 255, 0)), *args, **kwargs):
        super(RoiWidget, self).__init__(*args, **kwargs)
        self.roi_num = roi_num
        self.roi_titles = roi_titles
        self.roi_colors = roi_colors

        self._main_vertical_layout = QtWidgets.QVBoxLayout()
        self._horizontal_layout = QtWidgets.QHBoxLayout()

        self.img_widget = RoiImageWidget(roi_num=roi_num, roi_colors=roi_colors)

        self._roi_gbs_layout = QtWidgets.QVBoxLayout()
        self.roi_gbs = []
        self.create_roi_gbs()
        self._roi_gbs_layout.addSpacerItem(QtWidgets.QSpacerItem(20, 20,
                                                             QtWidgets.QSizePolicy.Expanding,
                                                             QtWidgets.QSizePolicy.Expanding))

        self._horizontal_layout.addWidget(self.img_widget)
        self._horizontal_layout.addLayout(self._roi_gbs_layout)

        self._horizontal_layout.setStretch(0, 1)
        self._horizontal_layout.setStretch(1, 0)

        self.status_bar = StatusBar()
        self.pos_lbl = self.status_bar.left_lbl
        self._main_vertical_layout.addLayout(self._horizontal_layout)
        self._main_vertical_layout.addWidget(self.status_bar)
        self._main_vertical_layout.setContentsMargins(0, 0, 0, 8)

        self.setLayout(self._main_vertical_layout)

        self.create_signals()

    def create_roi_gbs(self):
        for ind in range(self.roi_num):
            self.roi_gbs.append(RoiGroupBox(self.roi_titles[ind], self.roi_colors[ind]))
            self.roi_gbs[-1].roi_txt_changed.connect(partial(self._update_img_roi, ind))
            self._roi_gbs_layout.addWidget(self.roi_gbs[-1])

    def create_signals(self):
        self.img_widget.rois_changed.connect(self._update_roi_gbs)

    def _update_roi_gbs(self, rois_list):
        for ind, roi_gb in enumerate(self.roi_gbs):
            roi_gb.blockSignals(True)
            roi_gb.update_roi_txt(rois_list[ind])
            roi_gb.blockSignals(False)
        self.rois_changed.emit(self.img_widget.get_roi_limits())

    def _update_img_roi(self, ind, roi_list):
        self.img_widget.blockSignals(True)
        self.img_widget.update_roi(ind, roi_list)
        self.img_widget.blockSignals(False)
        self.rois_changed.emit(self.img_widget.get_roi_limits())

    def set_rois(self, rois_list):
        self.blockSignals(True)
        self._update_roi_gbs(rois_list)
        for ind in range(self.roi_num):
            self._update_img_roi(ind, rois_list[ind])
        self.blockSignals(False)

    def get_rois(self):
        return self.img_widget.get_roi_limits()

    def plot_img(self, img_data):
        if img_data is not None:
            self.img_widget.plot_image(img_data.T)

    def add_item(self, pg_item):
        self.img_widget.pg_viewbox.addItem(pg_item)

class RoiGroupBox(QtWidgets.QGroupBox):
    roi_txt_changed = QtCore.Signal(list)

    def __init__(self, title, color):
        super(RoiGroupBox, self).__init__(title)
        self.color = color
        self._grid_layout = QtWidgets.QGridLayout()

        self.x_min_txt = IntegerTextField('0')
        self.x_max_txt = IntegerTextField('0')
        self.y_min_txt = IntegerTextField('0')
        self.y_max_txt = IntegerTextField('0')

        self._grid_layout.addWidget(CenteredQLabel('X:'), 1, 0)
        self._grid_layout.addWidget(self.x_min_txt, 1, 1)
        self._grid_layout.addWidget(self.x_max_txt, 1, 2)

        self._grid_layout.addWidget(CenteredQLabel('Y:'), 2, 0)
        self._grid_layout.addWidget(self.y_min_txt, 2, 1)
        self._grid_layout.addWidget(self.y_max_txt, 2, 2)

        self.setLayout(self._grid_layout)
        style_str = "color: rgb{0}; border: 1px solid rgb{0};".format(self.color)
        self.setStyleSheet('QGroupBox {' + style_str + '}')
        self.setMaximumWidth(230)
        self.create_signals()

    def create_signals(self):
        self.x_min_txt.editingFinished.connect(self._roi_txt_changed)
        self.x_max_txt.editingFinished.connect(self._roi_txt_changed)
        self.y_min_txt.editingFinished.connect(self._roi_txt_changed)
        self.y_max_txt.editingFinished.connect(self._roi_txt_changed)

    def get_roi_limits(self):
        x_min = int(str(self.x_min_txt.text()))
        x_max = int(str(self.x_max_txt.text()))
        y_min = int(str(self.y_min_txt.text()))
        y_max = int(str(self.y_max_txt.text()))

        return [x_min, x_max, y_min, y_max]

    def update_roi_txt(self, roi_list):
        self.x_min_txt.setText(str(int(np.round(roi_list[0]))))
        self.x_max_txt.setText(str(int(np.round(roi_list[1]))))
        self.y_min_txt.setText(str(int(np.round(roi_list[2]))))
        self.y_max_txt.setText(str(int(np.round(roi_list[3]))))

    def _roi_txt_changed(self):
        self.roi_txt_changed.emit(self.get_roi_limits())


class CenteredQLabel(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super(CenteredQLabel, self).__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)


class IntegerTextField(QtWidgets.QLineEdit):
    def __init__(self, *args, **kwargs):
        super(IntegerTextField, self).__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.setValidator(QtGui.QIntValidator())


class RoiImageWidget(QtWidgets.QWidget):
    mouse_moved = QtCore.Signal(float, float)
    mouse_left_clicked = QtCore.Signal(float, float)
    mouse_left_double_clicked = QtCore.Signal(float, float)

    rois_changed = QtCore.Signal(list)

    def __init__(self, roi_num=1, roi_colors=((255, 255, 0)), *args, **kwargs):
        super(RoiImageWidget, self).__init__(*args, **kwargs)
        self.roi_num = roi_num
        self.roi_colors = roi_colors

        self.pg_widget = pg.GraphicsLayoutWidget()
        self.pg_layout = self.pg_widget.ci
        self.pg_layout.setContentsMargins(0, 10, 15, 0)
        self.pg_viewbox = self.pg_layout.addViewBox(1, 1, lockAspect=False)
        self.pg_viewbox.invertY(True)

        self.bottom_axis = pg.AxisItem('bottom', linkView=self.pg_viewbox)
        self.left_axis = pg.AxisItem('left', linkView=self.pg_viewbox)

        self.pg_layout.addItem(self.bottom_axis, 2, 1)
        self.pg_layout.addItem(self.left_axis, 1, 0)

        self.pg_img_item = pg.ImageItem()
        self.pg_viewbox.addItem(self.pg_img_item)

        self.pg_hist_item = HistogramLUTItem(self.pg_img_item, orientation='vertical',
                                             autoLevel=[0, 0.996])
        self.pg_layout.addItem(self.pg_hist_item, 1, 2, 1, 3)

        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self.pg_widget)
        self.setLayout(self._layout)

        self.add_rois()

        self.modify_mouse_behavior()

    def add_rois(self):
        self.rois = []
        for ind in range(self.roi_num):
            self.rois.append(ImgROI((25, 25), (150, 150),
                                    pen=pg.mkPen(self.roi_colors[ind], width=2),
                                    active_pen=pg.mkPen('r', width=3)))
            self.pg_viewbox.addItem(self.rois[-1])
            self.rois[-1].sigRegionChanged.connect(self.roi_changed)

    def get_roi_limits(self):
        roi_limits = []
        for roi in self.rois:
            roi_limits.append([roi.pos()[0], roi.pos()[0] + roi.size()[0],
                               roi.pos()[1], roi.pos()[1] + roi.size()[1]])
        return roi_limits

    def roi_changed(self):
        self.rois_changed.emit(self.get_roi_limits())

    def update_roi(self, ind, roi_limits):
        self.rois[ind].setPos((roi_limits[0], roi_limits[2]))
        self.rois[ind].setSize((roi_limits[1] - roi_limits[0],
                                roi_limits[3] - roi_limits[2]))

    def plot_image(self, data):
        self.pg_img_item.setImage(data)
        x_max, y_max = data.shape
        self.pg_viewbox.setLimits(xMin=0, xMax=x_max,
                                  yMin=0, yMax=y_max)

    @property
    def img_data(self):
        return self.pg_img_item.image

    def mouseMoved(self, pos):
        pos = self.pg_img_item.mapFromScene(pos)
        self.mouse_moved.emit(pos.x(), pos.y())

    def modify_mouse_behavior(self):
        # different mouse handlers
        self.pg_viewbox.setMouseMode(self.pg_viewbox.RectMode)

        self.pg_layout.scene().sigMouseMoved.connect(self.mouseMoved)
        self.pg_viewbox.mouseClickEvent = self.myMouseClickEvent
        self.pg_viewbox.mouseDragEvent = self.myMouseDragEvent
        self.pg_viewbox.mouseDoubleClickEvent = self.myMouseDoubleClickEvent

    def myMouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton or \
                (ev.button() == QtCore.Qt.LeftButton and
                         ev.modifiers() & QtCore.Qt.ControlModifier):
            self.pg_viewbox.scaleBy((2, 2))

        elif ev.button() == QtCore.Qt.LeftButton:
            pos = self.pg_viewbox.mapFromScene(ev.pos())
            y = pos.x()
            x = pos.y()
            self.mouse_left_clicked.emit(x, y)

    def myMouseDoubleClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.pg_viewbox.autoRange()
        if ev.button() == QtCore.Qt.LeftButton:
            pos = self.pg_viewbox.mapFromScene(ev.pos())
            self.mouse_left_double_clicked.emit(pos.x(), pos.y())

    def myMouseDragEvent(self, ev, axis=None):
        # most of this code is copied behavior of left click mouse drag from the original code
        ev.accept()
        pos = ev.pos()
        lastPos = ev.lastPos()
        dif = pos - lastPos
        dif *= -1
        ## Ignore axes if mouse is disabled
        mouseEnabled = np.array(self.pg_viewbox.state['mouseEnabled'], dtype=np.float)
        mask = mouseEnabled.copy()
        if axis is not None:
            mask[1 - axis] = 0.0

        if ev.button() == QtCore.Qt.RightButton or \
                (ev.button() == QtCore.Qt.LeftButton and \
                             ev.modifiers() & QtCore.Qt.ControlModifier):
            # determine the amount of translation
            tr = dif * mask
            tr = self.pg_viewbox.mapToView(tr) - self.pg_viewbox.mapToView(pg.Point(0, 0))
            x = tr.x()
            y = tr.y()

            self.pg_viewbox.translateBy(x=x, y=y)
            self.pg_viewbox.sigRangeChangedManually.emit(self.pg_viewbox.state['mouseEnabled'])
        else:
            if ev.isFinish():  ## This is the final move in the drag; change the view scale now
                # print "finish"
                self.pg_viewbox.rbScaleBox.hide()
                # ax = QtCore.QRectF(Point(self.pressPos), Point(self.mousePos))
                ax = QtCore.QRectF(pg.Point(ev.buttonDownPos(ev.button())), pg.Point(pos))
                ax = self.pg_viewbox.childGroup.mapRectFromParent(ax)
                self.pg_viewbox.showAxRect(ax)
                self.pg_viewbox.axHistoryPointer += 1
                self.pg_viewbox.axHistory = self.pg_viewbox.axHistory[:self.pg_viewbox.axHistoryPointer] + [ax]
            else:
                ## update shape of scale box
                self.pg_viewbox.updateScaleBox(ev.buttonDownPos(), ev.pos())


class ImgROI(pg.ROI):
    def __init__(self, pos, size, pen, active_pen):
        super(ImgROI, self).__init__(pos, size, False, True)

        self.setPen(pen)
        self.active_pen = active_pen

        self.addScaleHandle([1, 0.5], [0, 0.5],
                            item=CustomHandle(7.5, typ='f', pen=pen, activePen=active_pen, parent=self))
        self.addScaleHandle([0.5, 1], [0.5, 0],
                            item=CustomHandle(7.5, typ='f', pen=pen, activePen=active_pen, parent=self))
        self.addScaleHandle([0, 0.5], [1, 0.5],
                            item=CustomHandle(7.5, typ='f', pen=pen, activePen=active_pen, parent=self))
        self.addScaleHandle([0.5, 0], [0.5, 1],
                            item=CustomHandle(7.5, typ='f', pen=pen, activePen=active_pen, parent=self))

    def hoverEvent(self, ev):
        hover = False
        if not ev.isExit():
            if ev.acceptDrags(QtCore.Qt.LeftButton):
                hover = True
            for btn in [QtCore.Qt.LeftButton, QtCore.Qt.RightButton, QtCore.Qt.MidButton]:
                if int(self.acceptedMouseButtons() & btn) > 0 and ev.acceptClicks(btn):
                    hover = True

        if hover:
            self.currentPen = self.active_pen
        else:
            self.currentPen = self.pen
        self.update()

    def addHandle(self, info, index=None):
        h = super(ImgROI, self).addHandle(info, index)
        h.setPos(info['pos'] * self.state['size'])
        return h


class CustomHandle(pg.graphicsItems.ROI.Handle):
    def __init__(self, radius, typ=None, pen=pg.mkPen(200, 200, 220), parent=None, deletable=False,
                 activePen=pg.mkPen(255, 255, 0)):
        super(CustomHandle, self).__init__(radius, typ=typ, pen=pen, parent=parent, deletable=deletable)

        self.pen = pen
        self.activePen = activePen

    def hoverEvent(self, ev):
        hover = False
        if not ev.isExit():
            if ev.acceptDrags(QtCore.Qt.LeftButton):
                hover = True
            for btn in [QtCore.Qt.LeftButton, QtCore.Qt.RightButton, QtCore.Qt.MidButton]:
                if int(self.acceptedMouseButtons() & btn) > 0 and ev.acceptClicks(btn):
                    hover = True

        if hover:
            self.currentPen = self.activePen
        else:
            self.currentPen = self.pen
        self.update()

    def mouseDragEvent(self, ev):
        super(CustomHandle, self).mouseDragEvent(ev)
        if ev.isFinish():
            self.currentPen = self.pen
        elif ev.isStart():
            self.currentPen = self.activePen

        if self.isMoving:  ## note: isMoving may become False in mid-drag due to right-click.
            self.currentPen = self.activePen
        self.update()
