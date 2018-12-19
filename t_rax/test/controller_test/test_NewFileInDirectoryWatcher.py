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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.import unittest


import unittest
import os

from qtpy import QtWidgets
from mock import Mock

from controller.NewFileInDirectoryWatcher import NewFileInDirectoryWatcher

unittest_folder = os.path.join(os.path.dirname(__file__), '..', 'test_files')


class TestNewFileInDirectoryWatcher(unittest.TestCase):
    def setUp(self):
        self.app = QtWidgets.QApplication([])

    def tearDown(self):
        self.delete_if_exists('test.txt')

    def delete_if_exists(self, file_name):
        if os.path.exists(os.path.join(unittest_folder, file_name)):
            os.remove(os.path.join(unittest_folder, file_name))

    def test_new_file(self):
        self.watcher = NewFileInDirectoryWatcher(unittest_folder, file_types=['.txt'], activate=True)
        self.watcher.file_added = Mock()
        file_path = os.path.join(unittest_folder, 'test.txt')
        self.delete_if_exists('test.txt')

        f = open(file_path, 'w')
        f.write("abcdefg"*20)
        f.close()

        self.watcher.check_files()
        self.watcher.file_added.emit.assert_called_once_with(file_path)


