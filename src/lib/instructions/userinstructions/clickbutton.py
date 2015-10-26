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


class ClickButtonInstruction(Instruction):
    """
        click  button  (  STRING-LIST | TEXT-LIST | NUM  )

        Clicks a button. The button can be identified by it's label, name
        or by it's position in the current window. Position index starts with 1.

        Example 1:   click button (OK)
        Example 2:   click btn ("Save as...")
        Example 3:   click button(2)
        Example 4:   click button (Cancel | Avbryt)
        Example 5:   click button ("Cancel | Avbryt")
    """

    @Overrides(Instruction)
    def _execute(self):
        super(ClickButtonInstruction, self).click_button("wxButton")
