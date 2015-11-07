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
from lib.manuscript.pathfinder import find_path


class Manuscript():
    """
    This class holds all instructions for running a GUI application. The
    data can be merged from several data instruction files.
    All files given on the command line to Autopilot are concatenated into
    one Manuscript. A Manuscript can also have Include instructions that
    include other data instruction files.

    The program searches for the program to manuscripts in the following ways:
     1. As given on the command line
     2. In given paths (if any)
     3. In the directory %USER_HOME%/Autopilot
     4. In the directories given by AUTOPILOT_HOME environment variable

    If no script file is given as an option the default start script is
    Autopilot.data.txt.
    """

    def __init__(self, manuscripts, paths):
        self.windows = []
        self.execution_started = False
        self.first_manuscript_path_found = None
        self.paths = paths
        self.instructions = self._load_instructions(manuscripts)

    def __str__(self):
        collector = []
        for instruction in self.instructions:
            if isinstance(instruction, str):
                instruction = instruction.decode("cp1252")
            collector.append(instruction)
        return u"\n".join(collector)

    def get_instructions(self):
        return self.instructions

    def get_log_path(self):
        return self.first_manuscript_path_found

    def add_autoexit_instruction(self):
        self.instructions.append("exit application")

    def _load_instructions(self, manuscripts):
        self.instructions = []
        for manuscript in manuscripts:
            self.instructions.append("# Loading data '%s'" % manuscript)
            self._read_file_instructions(manuscript)
        return self.instructions

    def _read_file_instructions(self, manuscript):
        path = find_path(manuscript, self.paths)
        if path is None:
            self.instructions.append("# Path not found for data file '%s'" % manuscript)
        else:
            if self.first_manuscript_path_found is None:
                self.first_manuscript_path_found = path.rsplit("\\", 1)[0]
            for line in self._get_file_lines(path):
                self._load_instruction(line)

    def _load_instruction(self, line):
        if line.strip().startswith("include"):
            self._load_include_instruction(line)
        else:
            self.instructions.append(line.strip())

    def _load_include_instruction(self, line):
        parts = line.strip().split()
        if len(parts) == 2:
            self.instructions.append("# including '%s'" % parts[1])
            self._read_file_instructions(parts[1])
        else:
            self.instructions.append("# Invalid include statement '%s'" % line)

    def _get_file_lines(self, path):
        lines = []
        try:
            f = open(path)
            lines = f.read().split("\n")
        finally:
            f.close()
        return lines

