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
import time

from PyQt4 import QtCore


class NewFileInDirectoryWatcher(QtCore.QObject):
    """
    This class watches a given filepath for any new files with a given file extension added to it.

    Typical usage::
        def callback_fcn(path):
            print(path)

        watcher = NewFileInDirectoryWatcher(example_path, file_types = ['.tif', '.tiff'])
        watcher.file_added.connect(callback_fcn)

    """
    file_added = QtCore.pyqtSignal(str)

    def __init__(self, path=None, file_types=None, activate=False, interval=50):
        """
        :param path: path to folder which will be watched
        :param file_types: list of file types which will be watched for, e.g. ['.tif', '.jpeg]
        :param activate: whether or not the Watcher will already emit signals
        """
        super(NewFileInDirectoryWatcher, self).__init__()

        self._file_system_watcher = QtCore.QFileSystemWatcher()
        if path is None:
            path = os.getcwd()
        self.path = path

        if file_types is None:
            self.file_types = set([])
        else:
            self.file_types = set(file_types)

        self.interval = interval
        self.check_timer = QtCore.QTimer(self)
        self.check_timer.setInterval(interval)
        self.check_timer.timeout.connect(self.check_files)

        if activate:
            self.check_timer.start()

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path):
        self._path = new_path
        self._files_in_path = os.listdir(new_path)

    def activate(self):
        """
        activates the watcher to emit signals when a new file is added
        """
        if ~self.check_timer.isActive():
            self._files_in_path = os.listdir(self.path)
            self.check_timer.start()

    def deactivate(self):
        """
        deactivates the watcher so it will not emit a signal when a new file is added
        """
        if self.check_timer.isActive():
            self.check_timer.stop()

    def check_files(self):
        files_now = os.listdir(self.path)
        files_added = [f for f in files_now if not f in self._files_in_path]

        if len(files_added) > 0:
            print 'added'
            new_file_path = os.path.join(str(self.path), files_added[-1])

            # abort if the new_file added is actually a directory...
            if os.path.isdir(new_file_path):
                self._files_in_path = files_now
                return

            valid_file = False
            if len(self.file_types) == 0:
                valid_file = True
            else:
                for file_type in self.file_types:
                    if new_file_path.endswith(file_type):
                        valid_file = True
                        break

            if valid_file:
                print os.stat(new_file_path).st_size
                if os.stat(new_file_path).st_size > 100:
                    time.sleep(self.interval/1000.)
                    self.file_added.emit(new_file_path)
                else:
                    return
        self._files_in_path = files_now

