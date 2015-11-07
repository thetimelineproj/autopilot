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
import os.path
from optparse import OptionParser


USAGE = """%prog [options] filename

filename:  The name of the python program to test.

The program starts the program to test (PUT) and executes instructions
read from one or more data files. The instructions executed
and their result are written to an output log file.

The program searches for the program to test in the following ways:
 1. As given on the command line
 2. In the current working directory
 3. In the directory %USER_HOME%/autopilot
 4. In the directories given by AUTOPILOT_HOME environment variable

 The log file is written to the same directory where the first start
 script is found and will have the name autopilot.log.

 If no script file is given as an option the default start script is
 %USER_HOME%/autopilot/autopilot.data.txt. Scriptfiles are
 searched for in the same order as for the program to test as described
 above.

 options:
    -p     extra path for search of files
    -m     start data file(s)
    -l     log dialog descriptions or not
    -d     set debug on or off
    -e     add a last 'exit application' instruction
    -t     time delay between instructions in seconds
    -i     don't run test just display effective paths to program, script and log files",
"""


VERSION = "1.0"
HELP = {
    "p": "extra path for search of files",
    "m": "start data file(s)",
    "l": "log dialog descriptions or not",
    "d": "set debug on or off",
    "e": "add a last 'exit application' instruction",
    "t": "time delay between instructions in seconds",
    "i": "don't run test just display effective paths to program, script and log files",
}


class ApplicationArguments(object):

    def __init__(self):
        arguments = sys.argv
        self.parser = self.create_parser()
        self.options, self.arguments = self.parser.parse_args(arguments[1:])
        self.validate()

    def create_parser(self):
        version_string = "Ver. %s" % VERSION
        parser = OptionParser(usage=USAGE, version=version_string)
        parser.add_option(
            "-p", "--path", dest="path", default=None, help=HELP["p"])
        parser.add_option(
            "-m", "--manuscripts", dest="manuscripts", default="autopilot.txt", help=HELP["m"])
        parser.add_option(
            "-l", "--descriptions", dest="descriptions", action="store_true", default=False, help=HELP["l"])
        parser.add_option(
            "-d", "--debug", dest="debug", action="store_true", default=False, help=HELP["d"])
        parser.add_option(
            "-e", "--autoexit", dest="autoexit", action="store_true", default=False, help=HELP["e"])
        parser.add_option(
            "-i", "--investigate", dest="investigate", action="store_true", default=False, help=HELP["i"])
        parser.add_option(
            "-t", "--time-delay", dest="timedelay", type="int", default=4, help=HELP["t"])
        return parser

    def validate(self):
        self.validate_nbr_of_args()
        self.validate_program()

    def validate_nbr_of_args(self):
        if len(self.arguments) != 1:
            self.parser.error("One and only one python-program must be given")

    def validate_program(self):
        filename = self.arguments[0]
        self.validate_file_existance(filename)
        self.validate_py_extension(filename)

    def validate_file_existance(self, filename):
        if self.get_path(filename) is None:
            self.parser.error("Can't find the program %s" % filename)

    def get_path(self, filename):
        if os.path.exists(filename):
            return filename
        else:
            if self.paths() is not None:
                for path in self.paths():
                    pgmpath = os.path.join(path, filename)
                    if os.path.exists(pgmpath):
                        return pgmpath
        for envar in ["USER_HOME", "AUTOPILOT_HOME"]:
            path = self.get_environment_path(envar, filename)
            if path is not None:
                return path
        return None

    def get_environment_path(self, environment_variable, filename):
        try:
            home = os.environ[environment_variable]
            path = os.path.join(home, filename)
            if os.path.exists(path):
                return path
        except:
            return None

    def paths(self):
        if self.options.path is not None:
            path_string = self.options.path.strip()
            if path_string.endswith(";"):
                path_string = path_string[:-1]
            paths = path_string.split(";")
            return paths
        return []

    def validate_py_extension(self, filename):
        if not filename.endswith(".py"):
            self.parser.error("The program must have a .py extension [%s]" % filename)

    def myname(self):
        return self.parser.get_prog_name()

    def myversion(self):
        return self.parser.get_version()

    def program(self):
        return self.get_path(self.arguments[0])

    def log_dialog_descriptions(self):
        return self.options.descriptions

    def investigate(self):
        return self.options.investigate

    def timedelay(self):
        # TODO: The system can't handle 0 time!
        return max(0, self.options.timedelay)

    def manuscripts(self):
        filenames = self.options.manuscripts.split(";")
        if filenames[-1] == '':
            del(filenames[-1])
        return filenames

    def degbug(self):
        return self.options.debug

    def autoexit(self):
        return self.options.autoexit
