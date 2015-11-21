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


LOADED = False
SETTINGS_NAME = "autopilot.settings"
RECENTLY_OPENED = "Recently opened: "


class Settings(object):

    def __init__(self):
        if not LOADED:
            self._load()
            global LOADED
            LOADED = True

    def _load(self):
        self.recently_opened = []
        path = os.path.join(os.getcwd(), SETTINGS_NAME)
        if os.path.exists(path):
            self._load_recently_opened(path)

    def _load_recently_opened(self, path):
        with open(path) as f:
            self.recently_opened = [line[len(RECENTLY_OPENED):] for line in f.read().decode("utf-8").split("\n")
                                    if line.startswith(RECENTLY_OPENED) and os.path.exists(line[len(RECENTLY_OPENED):].strip())]

    def save_recently_opened(self, path):
        if os.path.exists(path) and path not in self.recently_opened:
            self.recently_opened.append(path)
            if len(self.recently_opened) > 10:
                del(self.recently_opened[0])
            with open(os.path.join(os.getcwd(), "autopilot.settings"), "w") as f:
                for path in self.recently_opened:
                    f.write("%s%s" % (RECENTLY_OPENED, path.encode("utf-8")))
                    f.write("\n")
            return True
        else:
            return False

    def get_recently_opened(self):
        return self.recently_opened

    def _save(self):
        with open(os.path.join(os.getcwd(), "autopilot.settings"), "w") as f:
            for path in self.recently_opened:
                f.write("%s%s" % (RECENTLY_OPENED, path.encode("utf-8")))
                f.write("\n")
