# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtCore, QtGui
import pyqtgraph as pg

from .ModifiedPlotItem import ModifiedPlotItem

from pyqtgraph.exporters.ImageExporter import ImageExporter
from pyqtgraph.exporters.SVGExporter import SVGExporter

class SpectrumWidget(QtGui.QWidget):
    mouse_left_clicked = QtCore.pyqtSignal(float, float)
    mouse_moved = QtCore.pyqtSignal(float, float)

    def __init__(self, *args, **kwargs):
        super(SpectrumWidget, self).__init__(*args, **kwargs)
        self._layout = QtGui.QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self.create_plot_items()
        self.create_data_items()

        self.setLayout(self._layout)
        self._plot_item.connect_mouse_move_event()

    def create_plot_items(self):
        self._pg_layout_widget = pg.GraphicsLayoutWidget()
        self._pg_layout = pg.GraphicsLayout()
        self._pg_layout.setContentsMargins(0, 0, 0, 0)
        self._pg_layout.layout.setVerticalSpacing(0)

        self._plot_item = ModifiedPlotItem(enableMouseInteraction=True)
        self._plot_item.showAxis('top', show=True)
        self._plot_item.showAxis('right', show=True)
        self._plot_item.getAxis('top').setStyle(showValues=False)
        self._plot_item.getAxis('right').setStyle(showValues=False)
        self._plot_item.getAxis('left').setStyle(showValues=True)
        self._plot_item.setLabel('bottom', 'v (cm<sup>-1</sup>)')
        self._plot_item.mouse_left_clicked.connect(self.mouse_left_clicked)
        self._plot_item.mouse_moved.connect(self.mouse_moved)
        self._pg_layout.addItem(self._plot_item, 0, 0)

        self._pg_layout_widget.addItem(self._pg_layout)
        self._layout.addWidget(self._pg_layout_widget)

    def create_data_items(self):
        self._data_item = pg.PlotDataItem(pen=pg.mkPen("#fff", width=1.5))
        self._plot_item.addItem(self._data_item)

    def add_item(self, pg_item):
        self._plot_item.addItem(pg_item)

    def plot_data(self, x, y):
        self._data_item.setData(x, y)

    def get_data(self):
        return self._data_item.getData()

    def set_xlabel(self, label_string):
        self._plot_item.setLabel('bottom', label_string)

    def save_graph(self, filename):
        self._pg_layout.setContentsMargins(20, 20, 20, 20)
        QtGui.QApplication.processEvents()
        if filename.endswith('.png'):
            exporter = ImageExporter(self._pg_layout)
            exporter.export(filename)
        elif filename.endswith('.svg'):
            self._invert_color()
            exporter = SVGExporter(self._pg_layout)
            exporter.export(filename)
            self._norm_color()
        self._pg_layout.setContentsMargins(0, 0, 0, 0)
        QtGui.QApplication.processEvents()

    def _invert_color(self):
        self._plot_item.getAxis('bottom').setPen('k')
        self._plot_item.getAxis('top').setPen('k')
        self._plot_item.getAxis('left').setPen('k')
        self._plot_item.getAxis('right').setPen('k')
        self._data_item.setPen(pg.mkPen("#000", width=1.5))

    def _norm_color(self):
        self._plot_item.getAxis('bottom').setPen('w')
        self._plot_item.getAxis('top').setPen('w')
        self._plot_item.getAxis('left').setPen('w')
        self._plot_item.getAxis('right').setPen('w')
        self._data_item.setPen(pg.mkPen("#FFF", width=1.5))
