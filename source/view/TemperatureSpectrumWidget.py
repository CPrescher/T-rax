# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtGui
import pyqtgraph as pg

from view.ModifiedPlotItem import ModifiedPlotItem


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
    'combined': 'FFCC00'
}


class TemperatureSpectrumWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(TemperatureSpectrumWidget, self).__init__(*args, **kwargs)
        self._layout = QtGui.QVBoxLayout()
        self._layout.setContentsMargins(0,0,0,0)

        self.create_plot_items()
        self.create_data_items()

        self.setLayout(self._layout)

    def create_plot_items(self):
        self._pg_layout_widget = pg.GraphicsLayoutWidget()
        self._pg_layout = pg.GraphicsLayout()
        self._pg_layout.setContentsMargins(0,0,0,0)
        self._pg_layout.layout.setVerticalSpacing(0)

        self._us_plot = ModifiedPlotItem()
        self._us_plot.showAxis('top', show=True)
        self._us_plot.showAxis('right', show=True)
        self._us_plot.getAxis('top').setStyle(showValues=False)
        self._us_plot.getAxis('right').setStyle(showValues=False)
        self._us_plot.getAxis('left').setStyle(showValues=False)
        self._us_plot.setTitle("Upstream", color=colors['upstream'], size='20pt')
        self._us_plot.setLabel('bottom', '&lambda; (nm)')
        self._us_plot.setMinimumWidth(120)

        self._ds_plot = ModifiedPlotItem()
        self._ds_plot.showAxis('top', show=True)
        self._ds_plot.showAxis('right', show=True)
        self._ds_plot.getAxis('top').setStyle(showValues=False)
        self._ds_plot.getAxis('right').setStyle(showValues=False)
        self._ds_plot.getAxis('left').setStyle(showValues=False)
        self._ds_plot.setTitle("Downstream", color=colors['downstream'], size='20pt')
        self._ds_plot.setLabel('bottom', '&lambda; (nm)')
        self._ds_plot.setMinimumWidth(120)

        self._time_lapse_plot = ModifiedPlotItem()
        self._time_lapse_plot.showAxis('top', show=True)
        self._time_lapse_plot.showAxis('right', show=True)
        self._time_lapse_plot.getAxis('top').setStyle(showValues=False)
        self._time_lapse_plot.getAxis('right').setStyle(showValues=False)
        self._time_lapse_plot.getAxis('bottom').setStyle(showValues=False)
        self._time_lapse_plot.setLabel('left', "T (K)")


        self._pg_layout.addItem(self._ds_plot,0,0)
        self._pg_layout.addItem(self._us_plot,0,1)

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
        self._us_data_item = pg.ScatterPlotItem(pen=pg.mkPen(colors['data_pen'], width=1),
                                                brush=pg.mkBrush(colors['data_brush']),
                                                size=3,
                                                symbol ='o')
        self._us_fit_item = pg.PlotDataItem(pen=pg.mkPen(colors['fit_pen'], width=3))

        self._us_plot.addItem(self._us_data_item)
        self._us_plot.addItem(self._us_fit_item)

        self._us_temperature_txt_item = pg.LabelItem()
        self._us_temperature_txt_item.setParentItem(self._us_plot.vb)
        self._us_temperature_txt_item.anchor(itemPos=(0, 0), parentPos=(0, 0), offset=(15, 10))

        self._us_roi_max_txt_item = pg.LabelItem()
        self._us_roi_max_txt_item.setParentItem(self._us_plot.vb)
        self._us_roi_max_txt_item.anchor(itemPos=(1,1), parentPos=(1,1), offset=(-10,-10))


        self._us_intensity_indicator = IntensityIndicator()
        self._us_intensity_indicator.setParentItem(self._us_plot)

        self._ds_data_item = pg.ScatterPlotItem(pen=pg.mkPen(colors['data_pen'], width=1),
                                                brush=pg.mkBrush(colors['data_brush']),
                                                size=3,
                                                symbol ='o')
        self._ds_fit_item = pg.PlotDataItem(pen=pg.mkPen(colors['fit_pen'], width=3))

        self._ds_plot.addItem(self._ds_data_item)
        self._ds_plot.addItem(self._ds_fit_item)

        self._ds_temperature_txt_item = pg.LabelItem()
        self._ds_temperature_txt_item.setParentItem(self._ds_plot.vb)
        self._ds_temperature_txt_item.anchor(itemPos=(0, 0), parentPos=(0, 0), offset=(15, 10))

        self._ds_roi_max_txt_item = pg.LabelItem()
        self._ds_roi_max_txt_item.setParentItem(self._ds_plot.vb)
        self._ds_roi_max_txt_item.anchor(itemPos=(1,1), parentPos=(1,1), offset=(-10,-10))

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
                                              size='24pt')

    def update_ds_temperature_txt(self, temperature, temperature_error):
        self._ds_temperature_txt_item.setText('{0:.0f} K &plusmn; {1:.0f}'.format(temperature,
                                                                                  temperature_error),
                                              size='24pt')

    def update_us_roi_max_txt(self, roi_max, format_max=65536):
        self._us_roi_max_txt_item.setText('Max Int {0:.0f}'.format(roi_max),
                                          size='18pt',
                                          color='33CC00')
        self._us_intensity_indicator.set_intensity(float(roi_max)/format_max)

    def update_ds_roi_max_txt(self, roi_max, format_max=65536):
        self._ds_roi_max_txt_item.setText('Max Int {0:.0f}'.format(roi_max),
                                          size='18pt',
                                          color='33CC00')
        self._ds_intensity_indicator.set_intensity(float(roi_max)/format_max)

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
                                                    color=colors['downstream'])

    def update_time_lapse_us_temperature_txt(self, temperature, temperature_error):
        self._time_lapse_us_temperature_txt.setText('{0:.0f} K &plusmn; {1:.0f}'.format(temperature,
                                                                                        temperature_error),
                                                    size='16pt',
                                                    color=colors['upstream'])

    def update_time_lapse_combined_temperature_txt(self, temperature, temperature_error):
        self._time_lapse_combined_temperature_txt.setText('{0:.0f} K &plusmn; {1:.0f}'.format(temperature,
                                                                                              temperature_error),
                                                          size='30pt',
                                                          color=colors['combined'])


class IntensityIndicator(pg.GraphicsWidget):
    def __init__(self):
        pg.GraphicsWidget.__init__(self)
        self.outside_rect = QtGui.QGraphicsRectItem(0,0,100,100)
        self.inside_rect = QtGui.QGraphicsRectItem(0,0,50,50)

        self._layout=QtGui.QGraphicsGridLayout()

        self.outside_rect.setPen(pg.mkPen(color=(255, 255, 255), width=1))
        self.inside_rect.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0, 150)))

        self.__parent = None
        self.__parentAnchor = None
        self.__itemAnchor = None
        self.__offset = (0,0)

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

        self.inside_rect.setRect(1,
                                 title_label_height + bounding_rect.height() * (1 - self._intensity_level) + 1,
                                 bar_width,
                                 bounding_rect.height()*self._intensity_level)


    def set_intensity(self, int):
        self._intensity_level = int
        self.__geometryChanged()




if __name__ == '__main__':
    import numpy as np
    app = QtGui.QApplication([])
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