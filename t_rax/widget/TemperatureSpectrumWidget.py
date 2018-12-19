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

from qtpy import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
from pyqtgraph.exporters.ImageExporter import ImageExporter
from pyqtgraph.exporters.SVGExporter import SVGExporter

from .ModifiedPlotItem import ModifiedPlotItem

pg.setConfigOption('useOpenGL', False)
pg.setConfigOption('leftButtonPan', False)
pg.setConfigOption('background', 'k')
pg.setConfigOption('foreground', 'w')
pg.setConfigOption('antialias', True)

colors = {
    'data_pen': '#ffffff',
    'data_brush': '#FFF',
    'fit_pen': 'r',
    'downstream': 'FFFF00',
    'upstream': 'FF9900',
    'combined': '66FFFF'
}

export_colors = {
    'downstream': '#235CDB',
    'combined': '#DE5757',
}


class TemperatureSpectrumWidget(QtWidgets.QWidget):
    mouse_moved = QtCore.Signal(float, float)

    def __init__(self, *args, **kwargs):
        super(TemperatureSpectrumWidget, self).__init__(*args, **kwargs)
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self.create_plot_items()
        self.create_data_items()

        self.setLayout(self._layout)

        self.connect_mouse_signals()

    def create_plot_items(self):
        self._pg_layout_widget = pg.GraphicsLayoutWidget()
        self._pg_layout = pg.GraphicsLayout()
        self._pg_layout.setContentsMargins(0, 0, 0, 0)
        self._pg_layout.layout.setVerticalSpacing(0)

        self._us_plot = ModifiedPlotItem(enableMouseInteraction=False)
        self._us_plot.showAxis('top', show=True)
        self._us_plot.showAxis('right', show=True)
        self._us_plot.getAxis('top').setStyle(showValues=False)
        self._us_plot.getAxis('right').setStyle(showValues=False)
        self._us_plot.getAxis('left').setStyle(showValues=False)
        self._us_plot.setTitle("Upstream", color=colors['upstream'], size='20pt')
        self._us_plot.setLabel('bottom', '&lambda; (nm)')
        self._us_plot.setMinimumWidth(120)

        self._ds_plot = ModifiedPlotItem(False)
        self._ds_plot.showAxis('top', show=True)
        self._ds_plot.showAxis('right', show=True)
        self._ds_plot.getAxis('top').setStyle(showValues=False)
        self._ds_plot.getAxis('right').setStyle(showValues=False)
        self._ds_plot.getAxis('left').setStyle(showValues=False)
        self._ds_plot.setTitle("Downstream", color=colors['downstream'], size='20pt')
        self._ds_plot.setLabel('bottom', '&lambda; (nm)')
        self._ds_plot.setMinimumWidth(120)

        self._time_lapse_plot = ModifiedPlotItem(False)
        self._time_lapse_plot.showAxis('top', show=True)
        self._time_lapse_plot.showAxis('right', show=True)
        self._time_lapse_plot.getAxis('top').setStyle(showValues=False)
        self._time_lapse_plot.getAxis('right').setStyle(showValues=False)
        self._time_lapse_plot.getAxis('bottom').setStyle(showValues=False)
        self._time_lapse_plot.setLabel('left', "T (K)")

        self._pg_layout.addItem(self._ds_plot, 0, 0)
        self._pg_layout.addItem(self._us_plot, 0, 1)

        self._pg_time_lapse_layout = pg.GraphicsLayout()
        self._pg_time_lapse_layout.setContentsMargins(0, 0, 0, 0)
        self._pg_time_lapse_layout.setSpacing(0)

        self._time_lapse_ds_temperature_txt = pg.LabelItem()
        self._time_lapse_us_temperature_txt = pg.LabelItem()
        self._time_lapse_combined_temperature_txt = pg.LabelItem()

        self._pg_time_lapse_layout.addItem(self._time_lapse_ds_temperature_txt, 0, 0)
        self._pg_time_lapse_layout.addItem(self._time_lapse_combined_temperature_txt, 0, 1)
        self._pg_time_lapse_layout.addItem(self._time_lapse_us_temperature_txt, 0, 2)

        self._pg_time_lapse_layout.addItem(self._time_lapse_plot, 1, 0, 1, 3)

        self._pg_layout.layout.setColumnStretchFactor(0, 1)
        self._pg_layout.layout.setColumnStretchFactor(1, 1)

        self._pg_layout_widget.addItem(self._pg_layout)
        self._layout.addWidget(self._pg_layout_widget)

    def create_data_items(self):
        # self._us_data_item = pg.ScatterPlotItem(pen=pg.mkPen(colors['data_pen'], width=1),
        #                                         brush=pg.mkBrush(colors['data_brush']),
        #                                         size=3,
        #                                         symbol ='o')
        self._us_data_item = pg.PlotDataItem(pen=pg.mkPen("#fff", width=1.5))
        self._us_fit_item = pg.PlotDataItem(pen=pg.mkPen(colors['fit_pen'], width=3))

        self._us_plot.addItem(self._us_data_item)
        self._us_plot.addItem(self._us_fit_item)

        self._us_temperature_txt_item = pg.LabelItem()
        self._us_temperature_txt_item.setParentItem(self._us_plot.vb)
        self._us_temperature_txt_item.anchor(itemPos=(0, 0), parentPos=(0, 0), offset=(15, 10))

        self._us_roi_max_txt_item = pg.LabelItem()
        self._us_roi_max_txt_item.setParentItem(self._us_plot.vb)
        self._us_roi_max_txt_item.anchor(itemPos=(1, 1), parentPos=(1, 1), offset=(-10, -10))

        self._us_intensity_indicator = IntensityIndicator()
        self._us_intensity_indicator.setParentItem(self._us_plot)

        # self._ds_data_item = pg.ScatterPlotItem(pen=pg.mkPen(colors['data_pen'], width=1),
        #                                         brush=pg.mkBrush(colors['data_brush']),
        #                                         size=3,
        #                                         symbol ='o')
        self._ds_data_item = pg.PlotDataItem(pen=pg.mkPen("#fff", width=1.5))
        self._ds_fit_item = pg.PlotDataItem(pen=pg.mkPen(colors['fit_pen'], width=3))

        self._ds_plot.addItem(self._ds_data_item)
        self._ds_plot.addItem(self._ds_fit_item)

        self._ds_temperature_txt_item = pg.LabelItem()
        self._ds_temperature_txt_item.setParentItem(self._ds_plot.vb)
        self._ds_temperature_txt_item.anchor(itemPos=(0, 0), parentPos=(0, 0), offset=(15, 10))

        self._ds_roi_max_txt_item = pg.LabelItem()
        self._ds_roi_max_txt_item.setParentItem(self._ds_plot.vb)
        self._ds_roi_max_txt_item.anchor(itemPos=(1, 1), parentPos=(1, 1), offset=(-10, -10))

        self._ds_intensity_indicator = IntensityIndicator()
        self._ds_intensity_indicator.setParentItem(self._ds_plot)

        self._time_lapse_ds_data_item = pg.PlotDataItem(
            pen=pg.mkPen(colors['downstream'], width=3),
            brush=pg.mkBrush(colors['downstream']),
            symbolPen=pg.mkPen(colors['downstream'], width=1),
            symbolBrush=pg.mkBrush(colors['downstream']),
            size=3,
            symbol='s'
        )
        self._time_lapse_us_data_item = pg.PlotDataItem(
            pen=pg.mkPen(colors['upstream'], width=3),
            brush=pg.mkBrush(colors['upstream']),
            symbolPen=pg.mkPen(colors['upstream'], width=1),
            symbolBrush=pg.mkBrush(colors['upstream']),
            size=3,
            symbol='s'
        )

        self._time_lapse_plot.addItem(self._time_lapse_ds_data_item)
        self._time_lapse_plot.addItem(self._time_lapse_us_data_item)

    def connect_mouse_signals(self):
        self._ds_plot.connect_mouse_move_event()
        self._us_plot.connect_mouse_move_event()
        self._pg_layout.addItem(self._pg_time_lapse_layout, 2, 0, 1, 2)
        self._time_lapse_plot.connect_mouse_move_event()
        self._pg_layout.removeItem(self._pg_time_lapse_layout)
        self._ds_plot.mouse_moved.connect(self.mouse_moved)
        self._us_plot.mouse_moved.connect(self.mouse_moved)
        self._time_lapse_plot.mouse_moved.connect(self.mouse_moved)

    def plot_ds_data(self, x, y):
        self._ds_data_item.setData(x, y)

    def plot_us_data(self, x, y):
        self._us_data_item.setData(x, y)

    def plot_ds_fit(self, x, y):
        self._ds_fit_item.setData(x, y)

    def plot_us_fit(self, x, y):
        self._us_fit_item.setData(x, y)

    def plot_ds_time_lapse(self, x, y):
        self._time_lapse_ds_data_item.setData(x, y)

    def plot_us_time_lapse(self, x, y):
        self._time_lapse_us_data_item.setData(x, y)

    def update_us_temperature_txt(self, temperature, temperature_error):
        self._us_temperature_txt_item.setText('{0:.0f} K &plusmn; {1:.0f}'.format(temperature,
                                                                                  temperature_error),
                                              size='24pt',
                                              color=colors['upstream'],
                                              justify='left')

    def update_ds_temperature_txt(self, temperature, temperature_error):
        self._ds_temperature_txt_item.setText('{0:.0f} K &plusmn; {1:.0f}'.format(temperature,
                                                                                  temperature_error),
                                              size='24pt',
                                              color=colors['downstream'],
                                              justify='left')

    def update_us_roi_max_txt(self, roi_max, format_max=65536):
        self._us_roi_max_txt_item.setText('Max Int {0:.0f}'.format(roi_max),
                                          size='18pt',
                                          color='33CC00',
                                          justify='right')
        self._us_intensity_indicator.set_intensity(float(roi_max) / format_max)

    def update_ds_roi_max_txt(self, roi_max, format_max=65536):
        self._ds_roi_max_txt_item.setText('Max Int {0:.0f}'.format(roi_max),
                                          size='18pt',
                                          color='33CC00',
                                          justify='left')
        self._ds_intensity_indicator.set_intensity(float(roi_max) / format_max)

    def show_time_lapse_plot(self, bool):
        if bool:
            if self._pg_time_lapse_layout not in self._pg_layout.items:
                self._pg_layout.addItem(self._pg_time_lapse_layout, 1, 0, 1, 2)
                self._pg_layout.layout.setRowStretchFactor(0, 4)
                self._pg_layout.layout.setRowStretchFactor(1, 3)
        else:
            if self._pg_time_lapse_layout in self._pg_layout.items:
                self._pg_layout.removeItem(self._pg_time_lapse_layout)

    def update_time_lapse_ds_temperature_txt(self, temperature, temperature_error):
        self._time_lapse_ds_temperature_txt.setText('{0:.0f} K &plusmn; {1:.0f}'.format(temperature,
                                                                                        temperature_error),
                                                    size='16pt',
                                                    color=colors['downstream'],
                                                    justify='left')

    def update_time_lapse_us_temperature_txt(self, temperature, temperature_error):
        self._time_lapse_us_temperature_txt.setText('{0:.0f} K &plusmn; {1:.0f}'.format(temperature,
                                                                                        temperature_error),
                                                    size='16pt',
                                                    color=colors['upstream'],
                                                    justify='right')

    def update_time_lapse_combined_temperature_txt(self, temperature, temperature_error):
        self._time_lapse_combined_temperature_txt.setText('{0:.0f} K &plusmn; {1:.0f}'.format(temperature,
                                                                                              temperature_error),
                                                          size='30pt',
                                                          color=colors['combined'])

    def save_graph(self, filename):
        self._pg_layout.setContentsMargins(20, 20, 20, 20)
        QtWidgets.QApplication.processEvents()
        if filename.endswith('.png'):
            exporter = ImageExporter(self._pg_layout)
            exporter.export(filename)
        elif filename.endswith('.svg'):
            self._prepare_svg_export()

            exporter = SVGExporter(self._pg_layout)
            exporter.export(filename)

            self._finalize_svg_export()

        self._pg_layout.setContentsMargins(0, 0, 0, 0)
        QtWidgets.QApplication.processEvents()

    def _prepare_svg_export(self):
        # since the svg will always have a transparent background we need to invert the colors of the original plot
        self._invert_color()
        # the pyqtgraph SVG Exporter cannot handle non ascii characters
        self._convert_symbols_to_ascii()

        # due to a strange bug in SVG export we are not going to use the symbols of the time lapse plot
        self._time_lapse_ds_data_item.setSymbol(None)
        self._time_lapse_us_data_item.setSymbol(None)

    def _finalize_svg_export(self):
        self._norm_color()
        self._convert_symbols_to_unicode()
        self._time_lapse_ds_data_item.setSymbol("s")
        self._time_lapse_us_data_item.setSymbol("s")
        QtWidgets.QApplication.processEvents()
        QtWidgets.QApplication.processEvents()

    def _convert_symbols_to_ascii(self):
        self._us_plot.setLabel('bottom', 'wavelength (nm)')
        self._ds_plot.setLabel('bottom', 'wavelength (nm)')

        self._ds_temperature_txt_item.setText(self._ds_temperature_txt_item.text.replace("&plusmn;", '+-'))
        self._us_temperature_txt_item.setText(self._us_temperature_txt_item.text.replace("&plusmn;", '+-'))
        self._time_lapse_ds_temperature_txt.setText(self._time_lapse_ds_temperature_txt.text.replace("&plusmn;", '+-'))
        self._time_lapse_us_temperature_txt.setText(self._time_lapse_us_temperature_txt.text.replace("&plusmn;", '+-'))
        self._time_lapse_combined_temperature_txt.setText(self._time_lapse_combined_temperature_txt. \
                                                          text.replace("&plusmn;", '+-'))

    def _convert_symbols_to_unicode(self):
        self._us_plot.setLabel('bottom', '&lambda; (nm)')
        self._ds_plot.setLabel('bottom', '&lambda; (nm)')

        self._ds_temperature_txt_item.setText(self._ds_temperature_txt_item.text.replace("+-", "&plusmn;"))
        self._us_temperature_txt_item.setText(self._us_temperature_txt_item.text.replace("+-", "&plusmn;"))
        self._time_lapse_ds_temperature_txt.setText(self._time_lapse_ds_temperature_txt.text.replace("+-", "&plusmn;"))
        self._time_lapse_us_temperature_txt.setText(self._time_lapse_us_temperature_txt.text.replace("+-", "&plusmn;"))
        self._time_lapse_combined_temperature_txt.setText(self._time_lapse_combined_temperature_txt. \
                                                          text.replace('+-', "&plusmn;"))

    def _set_plot_item_axis_color(self, plot_item, color):
        plot_item.getAxis('bottom').setPen(color)
        plot_item.getAxis('top').setPen(color)
        plot_item.getAxis('left').setPen(color)
        plot_item.getAxis('right').setPen(color)

    def _invert_color(self):
        self._set_plot_item_axis_color(self._ds_plot, 'k')
        self._set_plot_item_axis_color(self._us_plot, 'k')
        self._set_plot_item_axis_color(self._time_lapse_plot, 'k')

        self._ds_data_item.setPen(pg.mkPen("#000", width=1))
        self._ds_data_item.setBrush(pg.mkBrush("#000"))
        self._us_data_item.setPen(pg.mkPen("#000", width=1))
        self._us_data_item.setBrush(pg.mkBrush("#000"))

        self._ds_intensity_indicator.outside_rect.setPen(pg.mkPen("k", width=1))
        self._us_intensity_indicator.outside_rect.setPen(pg.mkPen("k", width=1))

        self._ds_temperature_txt_item.opts['color'] = export_colors['downstream']
        self._time_lapse_ds_temperature_txt.opts['color'] = export_colors['downstream']
        self._ds_plot.setTitle("Downstream", color=export_colors['downstream'], size='20pt')
        self._time_lapse_ds_data_item.setPen(pg.mkPen(export_colors['downstream'], width=3))

        self._time_lapse_combined_temperature_txt.opts['color'] = export_colors['combined']

    def _norm_color(self):
        self._set_plot_item_axis_color(self._ds_plot, 'w')
        self._set_plot_item_axis_color(self._us_plot, 'w')
        self._set_plot_item_axis_color(self._time_lapse_plot, 'w')

        self._ds_data_item.setPen(pg.mkPen('w', width=1))
        self._ds_data_item.setBrush(pg.mkBrush('w'))
        self._us_data_item.setPen(pg.mkPen('w', width=1))
        self._us_data_item.setBrush(pg.mkBrush('w'))

        self._ds_intensity_indicator.outside_rect.setPen(pg.mkPen("w", width=1))
        self._us_intensity_indicator.outside_rect.setPen(pg.mkPen("w", width=1))

        self._ds_temperature_txt_item.opts['color'] = colors['downstream']
        self._time_lapse_ds_temperature_txt.opts['color'] = colors['downstream']
        self._ds_plot.setTitle("Downstream", color=colors['downstream'], size='20pt')
        self._time_lapse_ds_data_item.setPen(pg.mkPen(colors['downstream'], width=3))

        self._time_lapse_combined_temperature_txt.opts['color'] = colors['combined']


class IntensityIndicator(pg.GraphicsWidget):
    def __init__(self):
        pg.GraphicsWidget.__init__(self)
        self.outside_rect = QtWidgets.QGraphicsRectItem(0, 0, 100, 100)
        self.inside_rect = QtWidgets.QGraphicsRectItem(0, 0, 50, 50)

        self._layout = QtWidgets.QGraphicsGridLayout()

        self.outside_rect.setPen(pg.mkPen(color=(255, 255, 255), width=1))
        self.inside_rect.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0, 150)))

        self.__parent = None
        self.__parentAnchor = None
        self.__itemAnchor = None
        self.__offset = (0, 0)

        self.inside_rect.setParentItem(self)
        self.outside_rect.setParentItem(self)
        self.inside_rect.setZValue(-100000)
        self.outside_rect.setZValue(200)

        self._intensity_level = 0

    def setParentItem(self, parent):
        pg.GraphicsWidget.setParentItem(self, parent)
        parent = self.parentItem()
        self.__parent = parent
        parent.geometryChanged.connect(self.__geometryChanged)
        self.__geometryChanged()

    def __geometryChanged(self):
        if self.__parent is None:
            return

        bounding_rect = self.__parent.vb.boundingRect()
        title_label_height = self.__parent.titleLabel.boundingRect().height()
        bar_width = 12
        self.outside_rect.setRect(1,
                                  title_label_height + 1,
                                  bar_width,
                                  bounding_rect.height())

        if self._intensity_level < 0.8:
            set_color = QtGui.QColor(0, 255, 0, 150)
        else:
            set_color = QtGui.QColor(255, 0, 0, 150)
        self.inside_rect.setRect(1,
                                 title_label_height + bounding_rect.height() * (1 - self._intensity_level) + 1,
                                 bar_width,
                                 bounding_rect.height() * self._intensity_level)
        self.inside_rect.setBrush(QtGui.QBrush(set_color))

    def set_intensity(self, intensity):
        self._intensity_level = intensity
        self.__geometryChanged()


if __name__ == '__main__':
    import numpy as np

    app = QtWidgets.QApplication([])
    widget = TemperatureSpectrumWidget()
    widget.show()
    widget.raise_()
    widget.update_us_temperature_txt(20, 3)
    widget.update_ds_roi_max_txt(2000)
    widget.update_time_lapse_ds_temperature_txt(2001, 23)
    widget.update_time_lapse_us_temperature_txt(1998, 23)
    widget.update_time_lapse_combined_temperature_txt(1999, 35)

    x = np.arange(10, step=1)
    widget.plot_ds_time_lapse(x, np.sin(x))
    widget.plot_us_time_lapse(x, np.cos(x))

    # widget._us_temperature_txt_item.setText('12415123')
    app.exec_()
