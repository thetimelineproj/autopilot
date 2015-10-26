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


class CloseDialogInstruction(Instruction):
    """
        close  dialog  [  (  arg  )  ]?

        command ::=  Close
        object  ::=  Dialog
        arg     ::=  STRING | TEXT

        Closes a modal dialog. If no arg is given the dialog to close is
        assumed to be the current window.

        Example 1:   Close Dialog("Create Event")
        Example 2:   Close Dialog
    """

    @Overrides(Instruction)
    def _execute(self):
        super(CloseDialogInstruction, self).close_dialog()
