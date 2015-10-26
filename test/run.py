# Copyright (C) 2009-2015 Contributors as noted in the AUTHORS file
#
# This file is part of autopilot.
#
# autopilot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# autopilot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with autopilot.  If not, see <http://www.gnu.org/licenses/>.


import unittest
from mock import Mock
from lib.app.testengine import TestEngine


class describe_run(unittest.TestCase):

    def test_exits_with_0_on_success(self):
        self.save_file_data()
        self.assertTrue(isinstance(to_unicode(self.read_file_data()), unicode))
        self.remove_file()

    def setUp(self):
        self.test_engine = Mock(TestEngine)
