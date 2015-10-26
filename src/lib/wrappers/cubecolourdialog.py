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
import wx.lib.agw.cubecolourdialog

from lib.reporting.logger import Logger
from lib.wrappers.wrapper import Wrapper
from lib.app.constants import TIME_TO_WAIT_FOR_DIALOG_TO_SHOW_IN_MILLISECONDS
from lib.app.decorators import Overrides


wxCubeColourDialog = wx.lib.agw.cubecolourdialog.CubeColourDialog


class CubeColourDialog(wx.lib.agw.cubecolourdialog.CubeColourDialog, Wrapper):

    def __init__(self, *args, **kw):
        wxCubeColourDialog.__init__(self, *args, **kw)

    def ShowModal(self, *args, **kw):
        self.shown = True
        Logger.add_result("Dialog opened")
        wx.CallLater(TIME_TO_WAIT_FOR_DIALOG_TO_SHOW_IN_MILLISECONDS, self._register_and_explore)
        super(CubeColourDialog, self).ShowModal(*args, **kw)

    @Overrides(wxCubeColourDialog)
    def IsShown(self):
        return self.shown

    @Overrides(wxCubeColourDialog)
    def Destroy(self, *args, **kw):
        self.shown = False
        Logger.add_result("Dialog '%s' closed" % self.GetLabel())
        wxCubeColourDialog.Destroy(self, *args, **kw)

    def _register_and_explore(self):
        CubeColourDialog.register_win(self)
        self._explore()

    @classmethod
    def wrap(self, register_win):
        wx.lib.agw.cubecolourdialog.CubeColourDialog = CubeColourDialog
        CubeColourDialog.register_win = register_win
