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


from lib.manuscript.manuscript import Manuscript
import unittest
import os


class describe_manuscript(unittest.TestCase):

    def test_no_input_returns_empty_instruction_list(self):
        manuscripts = []
        paths = []
        manuscript = Manuscript(manuscripts, paths)
        instructions = manuscript.get_instructions()
        self.assertEquals([], instructions)

    def test_no_manuscript_found_returns_commented_instruction_list(self):
        manuscripts = ["test_dialog1.txt"]
        paths = []
        manuscript = Manuscript(manuscripts, paths)
        instructions = manuscript.get_instructions()
        self.assertEquals(["# Loading data 'test_dialog1.txt'", "# Path not found for data file 'test_dialog1.txt'"], instructions)

    def test_manuscript_found_in_current_directory_returns_instruction_list(self):
        FILE = "test_dialog1.txt"
        PATH = FILE
        self.given_file_with_instructions(PATH, ["click OK"])
        manuscripts = [FILE]
        paths = []
        manuscript = Manuscript(manuscripts, paths)
        instructions = manuscript.get_instructions()
        self.assertEquals(["# Loading data 'test_dialog1.txt'", "click OK"], instructions)
        os.remove(PATH)

    def test_manuscript_found_in_given_directory_returns_instruction_list(self):
        PATH = r"c:\temp\test_dialog1.txt"
        self.given_file_with_instructions(PATH, ["click OK"])
        manuscripts = ["test_dialog1.txt"]
        paths = [r"c:\temp"]
        manuscript = Manuscript(manuscripts, paths)
        instructions = manuscript.get_instructions()
        self.assertEquals(["# Loading data 'test_dialog1.txt'", "click OK"], instructions)
        os.remove(PATH)

    def test_manuscript_found_in_user_home_directory_returns_instruction_list(self):
        PATH = r"c:\temp\test_dialog1.txt"
        self.given_file_with_instructions(PATH, ["click OK"])
        manuscripts = ["test_dialog1.txt"]
        paths = []
        os.environ["USER_HOME"] = r"c:\temp"
        manuscript = Manuscript(manuscripts, paths)
        instructions = manuscript.get_instructions()
        self.assertEquals(["# Loading data 'test_dialog1.txt'", "click OK"], instructions)
        os.remove(PATH)

    def test_manuscript_found_in_autopilot_home_directory_returns_instruction_list(self):
        FILE = "test_dialog1.txt"
        DIR = r"c:\temp"
        PATH = r"%s\%s" % (DIR, FILE)
        self.given_file_with_instructions(PATH, ["click OK"])
        manuscripts = [FILE]
        paths = []
        os.environ["AUTOPILOT_HOME"] = DIR
        manuscript = Manuscript(manuscripts, paths)
        self.assertEquals(["# Loading data 'test_dialog1.txt'", "click OK"], manuscript.get_instructions())
        os.remove(PATH)

    def test_manuscripts_are_concatenated(self):
        FILE1 = "test_dialog1.txt"
        FILE2 = "test_dialog2.txt"
        DIR = r"c:\temp"
        PATH1 = r"%s\%s" % (DIR, FILE1)
        PATH2 = r"%s\%s" % (DIR, FILE2)
        self.given_file_with_instructions(PATH1, ["click OK"])
        self.given_file_with_instructions(PATH2, ["click Cancel"])
        manuscripts = [FILE1, FILE2]
        os.environ["AUTOPILOT_HOME"] = DIR
        manuscript = Manuscript(manuscripts, [])
        self.assertEquals([
            "# Loading data 'test_dialog1.txt'",
            "click OK",
            "# Loading data 'test_dialog2.txt'",
            "click Cancel",
        ], manuscript.get_instructions())
        os.remove(PATH1)
        os.remove(PATH2)

    def test_manuscripts_are_included(self):
        FILE1 = "test_dialog1.txt"
        FILE2 = "test_dialog2.txt"
        DIR = r"c:\temp"
        PATH1 = r"%s\%s" % (DIR, FILE1)
        PATH2 = r"%s\%s" % (DIR, FILE2)
        self.given_file_with_instructions(PATH1, ["include test_dialog2.txt"])
        self.given_file_with_instructions(PATH2, ["click Cancel"])
        manuscripts = [FILE1, FILE2]
        os.environ["AUTOPILOT_HOME"] = DIR
        manuscript = Manuscript(manuscripts, [])
        self.assertEquals([
            "# Loading data 'test_dialog1.txt'", 
            "# including 'test_dialog2.txt'", 
            'click Cancel', 
            "# Loading data 'test_dialog2.txt'", 
            'click Cancel'
        ], manuscript.get_instructions())
        os.remove(PATH1)
        os.remove(PATH2)

    def given_file_with_instructions(self, path, instructions):
        f = open(path, "w")
        f.write(instructions[0])
        for instruction in instructions[1:]:
            f.write("\n")
            f.write(instruction)
        f.close()

    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()