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


import os
from lib.reporting.logger import Logger


def find_path(manuscript, paths):
    Logger.add_debug("Searching data as given: %s" % manuscript)
    if os.path.exists(manuscript):
        Logger.add_debug("   Found")
        return manuscript
    Logger.add_debug("   Not found")
    Logger.add_debug("Searching data with given paths")
    if len(paths) == 0:
        Logger.add_debug("   No paths given")
    for path in paths:
        Logger.add_debug("   Path: %s" % os.path.join(path, manuscript))
        if os.path.exists(os.path.join(path, manuscript)):
            Logger.add_debug("   Found")
            return os.path.join(path, manuscript)
        Logger.add_debug("   Not found")
    Logger.add_debug("Searching data with environment var paths")
    for envar in ["USER_HOME", "AUTOPILOT_HOME"]:
        path = get_environment_path(envar, manuscript)
        if path is not None:
            return path


def get_environment_path(environment_variable, filename):
    try:
        home = os.environ[environment_variable]
        path = os.path.join(home, filename)
        Logger.add_debug("   Path: %s" % path)
        if os.path.exists(path):
            Logger.add_debug("   Found")
            return path
    except:
        pass
    Logger.add_debug("   Not found")
