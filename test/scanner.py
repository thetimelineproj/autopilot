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
from lib.instructions.base.scanner import scan


class describe_manuscript(unittest.TestCase):

    def test_empty_text_returns_no_tokens(self):
        self.assertEquals([], scan(""))

    def test_comment_starts_with_hash(self):
        tokens = scan("# Comment")
        self.assertEquals("id= Keyword          subid= #            lexeme='# Comment' ", tokens[0].tostr())

    def test_comment_can_start_with_spaces(self):
        tokens = scan("    # Comment")
        self.assertEquals("id= Keyword          subid= #            lexeme='# Comment' ", tokens[0].tostr())

    def test_click_command_with_identifier_arg(self):
        tokens = scan("Click Button (OK)")
        self.assertEquals("id= Keyword          subid= click        lexeme='click' ", tokens[0].tostr())
        self.assertEquals("id= Keyword          subid= button       lexeme='button' ", tokens[1].tostr())
        self.assertEquals("id= (                subid=              lexeme='(' ", tokens[2].tostr())
        self.assertEquals("id= Identifier       subid=              lexeme='OK' ", tokens[3].tostr())
        self.assertEquals("id= )                subid=              lexeme=')' ", tokens[4].tostr())

    def test_click_command_with_string_arg(self):
        tokens = scan('Click Button ("Save as...")')
        self.assertEquals("id= Keyword          subid= click        lexeme='click' ", tokens[0].tostr())
        self.assertEquals("id= Keyword          subid= button       lexeme='button' ", tokens[1].tostr())
        self.assertEquals("id= (                subid=              lexeme='(' ", tokens[2].tostr())
        self.assertEquals("id= String           subid=              lexeme='\"Save as...\"' ", tokens[3].tostr())
        self.assertEquals("id= )                subid=              lexeme=')' ", tokens[4].tostr())

    def test_click_command_with_number_arg(self):
        tokens = scan("Click Button (5)")
        self.assertEquals("id= Keyword          subid= click        lexeme='click' ", tokens[0].tostr())
        self.assertEquals("id= Keyword          subid= button       lexeme='button' ", tokens[1].tostr())
        self.assertEquals("id= (                subid=              lexeme='(' ", tokens[2].tostr())
        self.assertEquals("id= Number           subid=              lexeme='5' ", tokens[3].tostr())
        self.assertEquals("id= )                subid=              lexeme=')' ", tokens[4].tostr())

    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()