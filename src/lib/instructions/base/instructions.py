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


import wx
from lib.instructions.base.parser import parse
from lib.reporting.logger import Logger
from lib.app.constants import TIME_TO_WAIT_BEFORE_CONTINUING_IN_MILLISECONDS
from lib.instructions.base.instructionpopup import InstructionPopup
from lib.guinatives.facade import get_window_text
from lib.instructions.userinstructions.assertclosed import AssertClosedInstruction
from lib.instructions.userinstructions.addplaceholder import AddPlaceholderInstruction


class NoMoreInstructionsException(Exception):
    pass


class Instructions(object):

    def __init__(self, manuscript, timedelay):
        self.timedelay = timedelay
        self.popup = None
        self.execution_started = False
        self.windows = []
        self.instructions = []
        for line in [line for line in manuscript.get_instructions() if not line.startswith("#") and len(line.strip()) > 0]:
            instruction = parse(line)
            if instruction is not None:
                self.instructions.append(instruction)
        collector = []
        for instruction in self.instructions:
            collector.append(instruction.to_unicode())
        Logger.header("Effective Instructions:\n   %s" % "\n   ".join(collector))

    def register_dialog(self, win=None):
        if win is None:
            return
        Logger.add_debug("Registering window: %s" % win)
        self.windows.append(win)
        if not self.execution_started:
            Logger.add_instruction("Execution of instructions start")
            self.execution_started = True
            wx.CallLater(TIME_TO_WAIT_BEFORE_CONTINUING_IN_MILLISECONDS,
                         self.execute_next_instruction)

    def execute_next_instruction(self):
        try:
            instruction = self._next_instruction()
            instruction._replace_placeholders()
            self._display_instruction_in_popup_window(instruction)
            if isinstance(instruction, AddPlaceholderInstruction):
                delay = 0
            else:
                # TODO: We have some timing problem so we can't set
                #       waiting time to 0. 40 seems to be ok,
                delay = max(40, self.timedelay * 1000)
            Logger.add_debug("Preparing instruction '%s' for execution with delay %d" % (instruction, delay))
            wx.CallLater(delay, self._execute_instruction, instruction)
        except NoMoreInstructionsException:
            Logger.add_instruction("The last instruction has been executed")

    def _display_instruction_in_popup_window(self, instruction):
        if self.popup is None:
            self.popup = InstructionPopup(self.windows[0])
        self.popup.SetText("%s" % instruction)

    def _next_instruction(self):
        try:
            instruction = self.instructions[0]
            self.instructions = self.instructions[1:]
            return instruction
        except:
            raise NoMoreInstructionsException()

    def _execute_instruction(self, instruction):
        Logger.add_instruction(instruction)
        current_window = self._get_current_window()
        instruction.execute(self, current_window)

    def _get_current_window(self):
        Logger.add_debug("self.windows: %s" % self.windows)
        self._validate_windows()
        Logger.add_debug("self.windows: %s" % self.windows)
        try:
            current_window = self.windows[-1]
        except:
            current_window = None
        # MessageBox windows seems to to return ok on get_window_text(win.hwnd)
        # even though the dialog is closed!
        # So we remove it here because the only thing you can do is clicking a
        # a button and thereafter the dialog is closed.
        if current_window.messagebox:
            del(self.windows[-1])
        Logger.add_debug("current_window: %s" % current_window)
        return current_window

    def _validate_windows(self):
        """Make sure the topmost window in the list self.windows is still
        valid. If not, remove it from the list and continue checking the
        list until the list is exhausted or a valid dialog is found.
        """
        self.windows.reverse()
        while len(self.windows) > 1:
            win = self.windows[0]
            try:
                win.get_label()
                try:
                    if not win.IsShown():
                        self.windows = self.windows[1:]
                    else:
                        break
                except:
                    Logger.add_debug("Window is not visible")
                    break
            except:
                Logger.add_debug("get_window_text fails")
                self.windows = self.windows[1:]
        self.windows.reverse()
