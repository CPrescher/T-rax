# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

pg.setConfigOption('useOpenGL', False)
pg.setConfigOption('leftButtonPan', False)
pg.setConfigOption('background', 'k')
pg.setConfigOption('foreground', 'w')
pg.setConfigOption('antialias', True)


plot_colors = {
    'data_pen': '#ffffff',
    'data_brush': '#FFF',
    'fit_pen': 'r',
}


class SpectrumWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(SpectrumWidget, self).__init__(*args, **kwargs)
        self._layout = QtGui.QVBoxLayout()
        self._layout.setContentsMargins(0,0,0,0)

        self.create_plot_items()
        self.create_data_items()

        self.setLayout(self._layout)

    def create_plot_items(self):
        self._pg_layout_widget = pg.GraphicsLayoutWidget()
        self._pg_layout = pg.GraphicsLayout()
        self._pg_layout.setContentsMargins(0,0,0,0)

        self._us_plot = ModifiedPlotItem()
        self._ds_plot = ModifiedPlotItem()

        self._pg_layout.addItem(self._ds_plot,0,0)
        self._pg_layout.addItem(self._us_plot,0,1)

        self._pg_layout_widget.addItem(self._pg_layout)
        self._layout.addWidget(self._pg_layout_widget)

    def create_data_items(self):
        self._us_data_item = pg.ScatterPlotItem(pen=pg.mkPen(plot_colors['data_pen'], width=1),
                                                brush=pg.mkBrush(plot_colors['data_brush']),
                                                size=3,
                                                symbol ='o')
        self._us_fit_item = pg.PlotDataItem(pen = pg.mkPen(plot_colors['fit_pen'], width = 3))

        self._us_plot.addItem(self._us_data_item)
        self._us_plot.addItem(self._us_fit_item)

        self._ds_data_item = pg.ScatterPlotItem(pen=pg.mkPen(plot_colors['data_pen'], width=1),
                                                brush=pg.mkBrush(plot_colors['data_brush']),
                                                size=3,
                                                symbol ='o')
        self._ds_fit_item = pg.PlotDataItem(pen = pg.mkPen(plot_colors['fit_pen'], width = 3))
        self._ds_plot.addItem(self._ds_data_item)
        self._ds_plot.addItem(self._ds_fit_item)

    def plot_ds_data(self, x, y):
        self._ds_data_item.setData(x, y)

    def plot_us_data(self, x, y):
        self._us_data_item.setData(x, y)

    def plot_ds_fit(self, x, y):
        self._ds_fit_item.setData(x, y)

    def plot_us_fit(self, x, y):
        self._us_fit_item.setData(x, y)

    def plot_ds_data_spectrum(self, spectrum):
        self.plot_ds_data(*spectrum.data)

    def plot_us_data_spectrum(self, spectrum):
        self.plot_us_data(*spectrum.data)

    def plot_ds_fit_spectrum(self, spectrum):
        self.plot_ds_fit(*spectrum.data)

    def plot_us_fit_spectrum(self, spectrum):
        self.plot_us_fit(*spectrum.data)


class ModifiedPlotItem(pg.PlotItem):
    mouse_moved = QtCore.pyqtSignal(float, float)
    mouse_left_clicked = QtCore.pyqtSignal(float, float)
    range_changed = QtCore.pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super(ModifiedPlotItem, self).__init__(*args, **kwargs)

        self.modify_mouse_behavior()

    def modify_mouse_behavior(self):
        self.vb.mouseClickEvent = self.mouse_click_event
        self.vb.mouseDragEvent = self.mouse_drag_event
        self.vb.mouseDoubleClickEvent = self.mouse_double_click_event
        self.vb.wheelEvent = self.wheel_event
        self.range_changed_timer = QtCore.QTimer()
        self.range_changed_timer.timeout.connect(self.emit_sig_range_changed)
        self.range_changed_timer.setInterval(30)

        self.cur_mouse_position_x = 0
        self.cur_mouse_position_y = 0

        self.mouse_moved.connect(self.update_cur_mouse_position)
        self.last_view_range = np.array(self.vb.viewRange())

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
            self.vb.scaleBy(2)
            self.vb.sigRangeChangedManually.emit(self.vb.state['mouseEnabled'])
        elif ev.button() == QtCore.Qt.LeftButton:
            if self.sceneBoundingRect().contains(ev.pos()):
                pos = self.vb.mapToView(ev.pos())
                x = pos.x()
                y = pos.y()
                self.mouse_left_clicked.emit(x, y)

    def update_cur_mouse_position(self, x, y):
        self.cur_mouse_position_x = x
        self.cur_mouse_position_y = y

    def get_mouse_position(self):
        return self.cur_mouse_position_x, self.cur_mouse_position_y

    def mouse_double_click_event(self, ev):
        if (ev.button() == QtCore.Qt.RightButton) or (ev.button() == QtCore.Qt.LeftButton and
                                                              ev.modifiers() & QtCore.Qt.ControlModifier):
            self.vb.autoRange()
            self.vb.enableAutoRange()
            self._auto_range = True
            self.vb.sigRangeChangedManually.emit(self.vb.state['mouseEnabled'])

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


if __name__ == '__main__':
    app = QtGui.QApplication([])
    widget = SpectrumWidget()
    widget.show()
    widget.raise_()
    app.exec_()