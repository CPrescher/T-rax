# -*- coding: utf8 -*- # T-Rax - GUI program for analysis of spectroscopy data during # diamond anvil cell experiments # Copyright (C) 2016 Clemens Prescher (clemens.prescher@gmail.com) # Institute for Geology and Mineralogy, University of Cologne # # This program is free software: you can redistribute it and/or modify # it under the terms of the GNU General Public License as published by # the Free Software Foundation, either version 3 of the License, or # (at your option) any later version. # # This program is distributed in the hope that it will be useful, # but WITHOUT ANY WARRANTY; without even the implied warranty of # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the # GNU General Public License for more details. # # You should have received a copy of the GNU General Public License # along with this program.  If not, see <http://www.gnu.org/licenses/>.
__author__ = 'Clemens Prescher'

import pyqtgraph as pg
from pyqtgraph.exporters.SVGExporter import SVGExporter
from qtpy import QtWidgets

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = pg.GraphicsWindow("title SVG Exporter bug")
    win.resize(1000, 600)
    p1 = win.addPlot()
    p1.plot(x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], y=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], pen=(200, 200, 200),
            symbolBrush=(255, 0, 0), symbolPen='w')
    QtWidgets.QApplication.processEvents()
    QtWidgets.QApplication.processEvents()
    exporter = SVGExporter(p1)
    exporter.export("test.svg")
