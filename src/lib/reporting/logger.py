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
import codecs
from __builtin__ import Exception


INSTRUCTION = 0
RESULT = 1
ERROR = 2
DEBUG = 3
LABELS = {INSTRUCTION: "INSTRUCTION:",
          RESULT: "RESULT     :",
          ERROR: "ERROR      :",
          DEBUG: "DEBUG      :",
          }
DEFAULT_PATH = r"c:\temp"
DEBUG_ON = False

reports = []
placeholders = {}


def set_debug(value):
    global DEBUG_ON
    DEBUG_ON = value


class Logger():

    path = None
    log_dialog_descriptions = False

    @classmethod
    def add_placeholder(self, key, value):
        placeholders[key] = value

    @classmethod
    def set_path(self, path_to_logfile):
        Logger.path = os.path.join(path_to_logfile, "Autopilot.log")
        try:
            fp = open(Logger.path, "w")
            fp.close()
        except IOError, ex:
            print ex
            Logger.path = DEFAULT_PATH
            fp = open(Logger.path, "w")
            fp.close()
            print "WARNING: Logger path changed to %s" % DEFAULT_PATH

    @classmethod
    def add(self, message):
        if Logger.path is None:
            print message
            return
        fp = open(Logger.path, "a")
        try:
            message = self._tostr(message)
            fp.write(message)
        except Exception, ex:
            print ex
            print type(message), message
            fp.close()
        fp.close()

    @classmethod
    def _tostr(self, msg):
        if isinstance(msg, unicode):
            msg = msg.encode('cp1252') 
        return msg + "\n"

    @classmethod
    def add_instruction(self, message):
        self.add("\nINSTRUCTION: %s" % message)

    @classmethod
    def add_debug(self, message):
        if DEBUG_ON:
            self._add_log(DEBUG, message)

    @classmethod
    def bold_line(self):
        self.add("=============================================================================")

    @classmethod
    def line(self):
        self.add("-------------------------------------------------")

    @classmethod
    def line2(self):
        self.add("   ----------------------------------------------")

    @classmethod
    def newline(self):
        self.add("")

    @classmethod
    def bold_header(self, label):
        self.add("\n")
        self.bold_line()
        self.add(" %s" % label)
        self.bold_line()

    @classmethod
    def header(self, label):
        self.line()
        self.add(" %s" % label)
        self.line()

    @classmethod
    def header2(self, label):
        self.line2()
        self.add("    %s" % label)
        self.line2()

    @classmethod
    def add_section(self, header, text):
        self.bold_header(header)
        lines = text.split("\n")
        for line in lines:
            self.add("   %s" % line)
        self.newline()

    @classmethod
    def add_result(self, result):
        self._add_log(RESULT, result)

    @classmethod
    def success(self, result):
        self.add_result(result)
        reports.append((result, True))

    @classmethod
    def failure(self, result):
        self.add_result(result)
        reports.append((result, False))

    @classmethod
    def add_open(self, win):
        self._add_log(RESULT, "%s '%s' opened" % (win.GetClassName(), win.GetLabel()))

    @classmethod
    def add_close(self, win):
        self._add_log(RESULT, "%s '%s' closed" % (win.GetClassName(), win.GetLabel()))

    @classmethod
    def add_error(self, result):
        self._add_log(ERROR, result)

    @classmethod
    def _add_log(self, logtype, result):
        self.add("%s %s" % (LABELS[logtype], result))

    @classmethod
    def set_log_dialog_descriptions(self, log_descriptions):
        Logger.log_dialog_descriptions = log_descriptions

    @classmethod
    def log(cls):
        collector = []
        collector.append("Result Expected")
        collector.append("------ --------------------------------")
        for expected, result in reports:
            collector.append("%-6.6s %s" % (result, expected))
        cls.add_section("Autopilot resultReport", "\n".join(collector))

