# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import pyqtgraph as pg
from pyqtgraph.exporters.SVGExporter import SVGExporter
from PyQt4 import QtGui

if __name__ == '__main__':
    app = QtGui.QApplication([])
    win = pg.GraphicsWindow("title SVG Exporter bug")
    win.resize(1000, 600)
    p1 = win.addPlot()
    p1.plot(x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], y=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], pen=(200, 200, 200),
            symbolBrush=(255, 0, 0), symbolPen='w')
    QtGui.QApplication.processEvents()
    QtGui.QApplication.processEvents()
    exporter = SVGExporter(p1)
    exporter.export("test.svg")
