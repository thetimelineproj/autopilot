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


from lib.instructions.base.instruction import Instruction
from lib.app.decorators import Overrides


class SelectListBoxInstruction(Instruction):
    """
        select listbox  (  n  ,  text|num )

        n       ::=  position of control starting with 1
        text    ::=  STRING | TEXT
        num     ::=  1-based index

        Select an item in th n:th listbox control. The item to selected is
        identified by text.

        Example 1:   select listbox (1, "Private")
        Example 2:   select listbox (1, 1)
    """

    @Overrides(Instruction)
    def _execute(self):
        super(SelectListBoxInstruction, self).select_listbox_item("wxListBox")
