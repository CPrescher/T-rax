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

import os
from PyQt4 import QtCore, QtGui
from functools import partial

from .TemperatureWidget import TemperatureWidget
from .RubyWidget import RubyWidget
from .DiamondWidget import DiamondWidget
from .RamanWidget import RamanWidget

module_path = os.path.dirname(__file__)


class MainWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWidget, self).__init__(*args, **kwargs)
        self._main_layout = QtGui.QVBoxLayout()
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        self.navigation_widget = NavigationWidget(self)
        self.temperature_widget = TemperatureWidget(self)
        self.ruby_widget = RubyWidget(self)
        self.diamond_widget = DiamondWidget(self)
        self.raman_widget = RamanWidget(self)

        self._main_layout.addWidget(self.navigation_widget)
        self._main_layout.addWidget(self.temperature_widget)
        self._main_layout.addWidget(self.ruby_widget)
        self._main_layout.addWidget(self.diamond_widget)
        self._main_layout.addWidget(self.raman_widget)

        self.ruby_widget.hide()
        self.diamond_widget.hide()
        self.raman_widget.hide()

        self.load_stylesheet()
        self.setLayout(self._main_layout)

    def load_stylesheet(self):
        main_stylesheet_file = open(os.path.join(module_path, "TRaxStyle.qss"), 'r')
        main_stylesheet_str = main_stylesheet_file.read()
        main_stylesheet_file.close()
        navigation_stylesheet_file = open(os.path.join(module_path, "NavigationStyle.qss"), 'r')
        navigation_stylesheet_str = navigation_stylesheet_file.read()
        navigation_stylesheet_file.close()
        self.setStyleSheet(main_stylesheet_str + '\n' + navigation_stylesheet_str)


class NavigationWidget(QtGui.QFrame):
    colors = {
        'temperature': 'rgba(221, 124, 40, 180)',
        'ruby': 'rgba(197, 0, 3, 255)',
        'diamond': 'rgba(27, 0, 134, 255)',
        'raman': 'rgba(21, 134, 31, 255)'
    }

    def __init__(self, *args, **kwargs):
        super(NavigationWidget, self).__init__()
        self.setObjectName("navigation_frame")

        self._layout = QtGui.QHBoxLayout()

        self.temperature_btn = QtGui.QPushButton('Temperature')
        self.ruby_btn = QtGui.QPushButton('Ruby')
        self.diamond_btn = QtGui.QPushButton('Diamond')
        self.raman_btn = QtGui.QPushButton('Raman')

        # setting object names for stylesheet access
        self.temperature_btn.setObjectName('temperature_btn')
        self.ruby_btn.setObjectName('ruby_btn')
        self.diamond_btn.setObjectName('diamond_btn')
        self.raman_btn.setObjectName('raman_btn')

        self.copyright_lbl = QtGui.QLabel('written by Clemens Prescher, GSECARS, UofC')
        self.copyright_lbl.setObjectName('copyright_label')
        self._layout.addWidget(self.temperature_btn)
        self._layout.addWidget(self.ruby_btn)
        self._layout.addWidget(self.diamond_btn)
        self._layout.addWidget(self.raman_btn)
        self._layout.addSpacerItem(QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Expanding,
                                                     QtGui.QSizePolicy.Fixed))
        self._layout.addWidget(self.copyright_lbl)
        self.setLayout(self._layout)

        self.setup_color_change()

    def setup_color_change(self):
        self.temperature_btn.clicked.connect(partial(self.update_colors,
                                                     self.colors['temperature'],
                                                     self.temperature_btn))
        self.ruby_btn.clicked.connect(partial(self.update_colors,
                                              self.colors['ruby'],
                                              self.ruby_btn))
        self.diamond_btn.clicked.connect(partial(self.update_colors,
                                                 self.colors['diamond'],
                                                 self.diamond_btn))
        self.raman_btn.clicked.connect(partial(self.update_colors,
                                               self.colors['raman'],
                                               self.raman_btn))

    def connect_click_function(self, emitter, function):
        self.control_widget.connect(emitter, QtCore.SIGNAL('clicked()'), function)

    def update_colors(self, new_color, sender, ):
        str1 = '#navigation_frame {background: qlineargradient(spread:reflect, x1:0, y1:0.5, x2:0, y2:0, stop:0.12 %s, stop:0.6 rgb(30, 30, 30));}' % new_color
        str2 = 'QPushButton { border: 1px solid #999}'
        str3 = '#%s { border: 2px solid #fff}' % sender.objectName()
        self.setStyleSheet('\n'.join([str1, str2, str3]))


if __name__ == '__main__':
    app = QtGui.QApplication([])
    widget = MainWidget()
    widget.show()
    widget.raise_()
    app.exec_()
