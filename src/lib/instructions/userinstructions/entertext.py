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


class EnterTextInstruction(Instruction):
    """
        exnter text ( STRING-LIST | TEXT-LIST | NUM  ,  STRING | TEXT )

        Enter the given text into a Text Control field.
        NUM     Indicates the n:th text field in the dialog. n starts with 1.

        Example 1:   Enter text(1, "2013-10-12")
        Example 2:   Enter text(2, myname)
    """

    @Overrides(Instruction)
    def _execute(self):
        super(EnterTextInstruction, self).enter_text("wxTextCtrl")
