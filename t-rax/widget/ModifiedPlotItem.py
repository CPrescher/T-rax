# -*- coding: utf8 -*-
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

from qtpy import QtCore, QtWidgets
import pyqtgraph as pg
import numpy as np


class ModifiedPlotItem(pg.PlotItem):
    mouse_moved = QtCore.Signal(float, float)
    mouse_left_clicked = QtCore.Signal(float, float)
    range_changed = QtCore.Signal(list)

    def __init__(self, enableMouseInteraction=True, *args, **kwargs):
        super(ModifiedPlotItem, self).__init__(*args, **kwargs)
        self.enableMouseInterAction = enableMouseInteraction
        self.modify_mouse_behavior()

    def modify_mouse_behavior(self):
        self.vb.mouseClickEvent = self.mouse_click_event
        self.vb.mouseDoubleClickEvent = self.mouse_double_click_event

        if self.enableMouseInterAction:
            self.vb.mouseDragEvent = self.mouse_drag_event
            self.vb.wheelEvent = self.wheel_event
            self.range_changed_timer = QtCore.QTimer()
            self.range_changed_timer.timeout.connect(self.emit_sig_range_changed)
            self.range_changed_timer.setInterval(30)
            self.last_view_range = np.array(self.vb.viewRange())
        else:
            self.vb.mouseDragEvent = self.empty_event_function
            self.vb.wheelEvent = self.empty_event_function

        self.cur_mouse_position_x = 0
        self.cur_mouse_position_y = 0

        self.mouse_moved.connect(self.update_cur_mouse_position)

    def connect_mouse_move_event(self):
        self.scene().sigMouseMoved.connect(self.mouse_move_event)

    def mouse_move_event(self, pos):
        if self.sceneBoundingRect().contains(pos):
            pos = self.vb.mapSceneToView(pos)
            self.mouse_moved.emit(pos.x(), pos.y())

    def mouse_click_event(self, ev):
        if ev.button() == QtCore.Qt.RightButton or \
                (ev.button() == QtCore.Qt.LeftButton and
                         ev.modifiers() & QtCore.Qt.ControlModifier):
            if self.enableMouseInterAction:
                self.vb.scaleBy(2)
                self.vb.sigRangeChangedManually.emit(self.vb.state['mouseEnabled'])
        elif ev.button() == QtCore.Qt.LeftButton:
            if self.sceneBoundingRect().contains(ev.pos()):
                pos = self.vb.mapToView(ev.pos())
                x = pos.x()
                y = pos.y()
                self.mouse_left_clicked.emit(x, y)

    def mouse_double_click_event(self, ev):
        if self.enableMouseInterAction:
            if (ev.button() == QtCore.Qt.RightButton) or (ev.button() == QtCore.Qt.LeftButton and
                                                                  ev.modifiers() & QtCore.Qt.ControlModifier):
                self.vb.autoRange()
                self.vb.enableAutoRange()
                self._auto_range = True
                self.vb.sigRangeChangedManually.emit(self.vb.state['mouseEnabled'])

    def update_cur_mouse_position(self, x, y):
        self.cur_mouse_position_x = x
        self.cur_mouse_position_y = y

    def get_mouse_position(self):
        return self.cur_mouse_position_x, self.cur_mouse_position_y

    def empty_event_function(self, ev, *args, **kwargs):
        pass

    def mouse_drag_event(self, ev, axis=None):
        # most of this code is copied behavior mouse drag from the original code
        ev.accept()
        pos = ev.pos()
        last_pos = ev.lastPos()
        dif = pos - last_pos
        dif *= -1

        if ev.button() == QtCore.Qt.RightButton or \
                (ev.button() == QtCore.Qt.LeftButton and ev.modifiers() & QtCore.Qt.ControlModifier):
            # determine the amount of translation
            tr = dif
            tr = self.vb.mapToView(tr) - self.vb.mapToView(pg.Point(0, 0))
            x = tr.x()
            y = tr.y()
            self.vb.translateBy(x=x, y=y)
            if ev.start:
                self.range_changed_timer.start()
            if ev.isFinish():
                self.range_changed_timer.stop()
                self.emit_sig_range_changed()
        else:
            if ev.isFinish():  # This is the final move in the drag; change the view scale now
                self._auto_range = False
                self.vb.enableAutoRange(enable=False)
                self.vb.rbScaleBox.hide()
                ax = QtCore.QRectF(pg.Point(ev.buttonDownPos(ev.button())), pg.Point(pos))
                ax = self.vb.childGroup.mapRectFromParent(ax)
                self.vb.showAxRect(ax)
                self.vb.axHistoryPointer += 1
                self.vb.axHistory = self.vb.axHistory[:self.vb.axHistoryPointer] + [ax]
                self.vb.sigRangeChangedManually.emit(self.vb.state['mouseEnabled'])
            else:
                # update shape of scale box
                self.vb.updateScaleBox(ev.buttonDownPos(), ev.pos())

    def emit_sig_range_changed(self):
        new_view_range = np.array(self.vb.viewRange())
        if not np.array_equal(self.last_view_range, new_view_range):
            self.vb.sigRangeChangedManually.emit(self.vb.state['mouseEnabled'])
            self.last_view_range = new_view_range

    def wheel_event(self, ev, axis=None, *args):
        pg.ViewBox.wheelEvent(self.vb, ev, axis)
        self.vb.sigRangeChangedManually.emit(self.vb.state['mouseEnabled'])
