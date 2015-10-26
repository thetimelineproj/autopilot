# Copyright (C) 2009-2015 Contributors as noted in the AUTHORS file
#
# This file is part of Autopilot.
#
# Autopilot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Autopilot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Autopilot.  If not, see <http://www.gnu.org/licenses/>.


import sys
from lib.app.testengine import TestEngine
from lib.reporting.logger import Logger


def get_exit_code(result):
    if result is True:
        Logger.add("Exit with test success")
        return 0
    else:
        Logger.add("Exit with test failure")
        return 1


if __name__ == '__main__':
    sys.exit(get_exit_code(TestEngine().run()))
