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

import os
import sys
from sys import platform
from optparse import OptionParser
from pyshortcuts import make_shortcut
from qtpy import QtWidgets

from .version import get_version
__version__ = get_version()

from .controller.MainController import MainController



def run_t_rax():
    usage = 'Usage: run_t_rax [options]'
    vers = 'run_t_rax %s' % __version__

    parser = OptionParser(usage=usage, prog='pyshortcut', version=vers)

    parser.add_option('-m', '--make_icon', dest='makeicon', action="store_true",
                      default=False, help='make desktop shortcut')
    (options, args) = parser.parse_args()
    
    if options.makeicon:
        bindir = 'bin'
        if os.name == 'nt':
            bindir = 'Scripts'
        script = os.path.join(sys.prefix, bindir, 'run_t_rax')
        _path, _fname = os.path.split(__file__)
        iconfile = os.path.join(_path, 'widget', 'icons', 't_rax.ico')
        make_shortcut(script, name='T-Rax',icon=iconfile, terminal=True)
        
    else:
        if len(sys.argv) == 1: # normal start
            app = QtWidgets.QApplication(sys.argv)
            if platform != "darwin":
                app.setStyle('plastique')
            controller = MainController()
            controller.show_window()
            app.exec_()
        else: # with command line arguments
            if sys.argv[1] == 'test':
                app = QtWidgets.QApplication(sys.argv)
                controller = MainController()
                controller.show_window()
