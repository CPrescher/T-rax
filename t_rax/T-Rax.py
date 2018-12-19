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
#
# import sys
# from sys import platform
#
# from qtpy import QtWidgets
#
# from controller.MainController import MainController
#
#
# app = QtWidgets.QApplication(sys.argv)
# if platform != "darwin":
#     app.setStyle('plastique')
# controller = MainController()
# controller.show_window()
# app.exec_()

import t_rax.__init__
t_rax.__init__.run_t_rax()

