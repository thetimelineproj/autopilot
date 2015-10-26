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
from lib.instructions.base.parser import parse
from lib.app.exceptions import NotFoundException


call_count = 0
ok_count = 0


class describe(unittest.TestCase):

    def test_instruction_specific_execute_command(self):
        self.instruction._execute(self.win)
        self.assertEquals(1, self.win.get_ok_count())
        self.assertEquals(2, self.win.get_call_count())

    def test_baseclass_instruction_execute_command(self):
        self.instruction.execute(self.manuscript, self.win)
        self.assertEquals(1, self.win.get_ok_count())
        self.assertEquals(2, self.win.get_call_count())

    def setUp(self):
        self.instruction = parse("click button (OK|Cancel)")
        self.win = Win()
        self.manuscript = Mock()
        self.manuscript.execute_next_instruction.return_value = None


class Win(object):

    def __init__(self):
        global call_count
        global ok_count
        call_count = 0
        ok_count = 0

    def click_button(self, name):
        global call_count
        global ok_count
        call_count += 1
        if name == "OK":
            raise NotFoundException()
        else:
            ok_count += 1

    def get_ok_count(self):
        return ok_count

    def get_call_count(self):
        return call_count


if __name__ == '__main__':
    unittest.main()
