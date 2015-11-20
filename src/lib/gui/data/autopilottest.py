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
import xml.etree.ElementTree as ET


class AutopilotTest(object):

    def __init__(self):
        self.name = ""
        self.app_under_test = ""
        self.start_manuscript = ""
        self.manuscript_paths = "."
        self.debug = False
        self.log_dialogs = False
        self.inspect = False
        self.exit_when_done = True
        self.delay = "4"

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_app(self):
        return self.app_under_test

    def set_app_under_test(self, app_under_test):
        self.app_under_test = app_under_test

    def get_log_path(self):
        return self.manuscript_paths.split(";")[0]

    def get_manuscript(self):
        return os.path.join(self.manuscript_paths, self.start_manuscript)

    def set_start_manuscript(self, start_manuscript):
        try:
            path, name = os.path.split(start_manuscript)
        except:
            path = "."
            name = start_manuscript
        self.start_manuscript = name
        self.manuscript_paths = path

    def get_debug(self):
        return self.debug

    def set_debug(self, debug):
        self.debug = debug

    def get_log_dialogs(self):
        return self.log_dialogs

    def set_log_dialogs(self, log_dialogs):
        self.log_dialogs = log_dialogs

    def get_inspect(self):
        return self.inspect

    def set_inspect(self, inspect):
        self.inspect = inspect

    def get_exit(self):
        return self.exit_when_done

    def set_exit_when_done(self, exit_when_done):
        self.exit_when_done = exit_when_done

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        try:
            d = int(delay)
            self.delay = delay
        except:
            pass

    def get_argv(self):
        argv = [self.app_under_test,
                "-p", self.manuscript_paths,
                "-m", self.start_manuscript,
                "-t", self.delay]
        if self.exit_when_done:
            argv.append("-e")
        if self.log_dialogs:
            argv.append("-l")
        if self.debug:
            argv.append("-d")
        if self.inspect:
            argv.append("-i")
        return argv

    def to_display_format(self):
        collector = []
        collector.append("Name: %s" % self.name)
        collector.append("Application under test: %s" % self.app_under_test)
        collector.append("Start manuscript: %s" % self.start_manuscript)
        collector.append("Manuscript paths: %s" % self.manuscript_paths)
        collector.append("Exit when done: %s" % self.exit_when_done)
        collector.append("Inspect dialogs: %s" % self.inspect)
        collector.append("Log dialogs: %s" % self.log_dialogs)
        collector.append("Delay in ms: %s" % self.delay)
        collector.append("Debug on: %s" % self.debug)
        return "\n".join(collector)

    def to_xml(self):
        root = ET.Element("autopilottest")
        ET.SubElement(root, "name").text = self.name
        ET.SubElement(root, "app").text = self.app_under_test
        ET.SubElement(root, "manuscript").text = os.path.join(self.manuscript_paths, self.start_manuscript)
        ET.SubElement(root, "exit").text = "%s" % self.exit_when_done
        ET.SubElement(root, "delay").text = self.delay
        ET.SubElement(root, "debug").text = "%s" % self.debug
        ET.SubElement(root, "log").text = "%s" % self.log_dialogs
        ET.SubElement(root, "inspect").text = "%s" % self.inspect
        tree = ET.ElementTree(root)
        tree.write("autopilottest.xml")
