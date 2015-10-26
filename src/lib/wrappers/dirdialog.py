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

from lib.app.decorators import Overrides
from lib.reporting.logger import Logger
from lib.wrappers.wrapper import Wrapper


wxDirDialog = wx.DirDialog


class DirDialog(wx.DirDialog, Wrapper):

    def __init__(self, *args, **kw):
        self.set_active_window()
        wxDirDialog.__init__(self, *args, **kw)
        Wrapper.__init__(self)
        self._shown = False

    def name(self):
        return self.GetMessage()

    def classname(self):
        return self.GetClassName()

    @Overrides(wxDirDialog)
    def IsShown(self):
        return self.shown

    @Overrides(wxDirDialog)
    def ShowModal(self):
        self._shown = True
        Logger.add_open(self)
        self.call_when_win_shows(self._explore_and_register)
        super(DirDialog, self).ShowModal()

    def _explore_and_register(self):
        self._explore()
        DirDialog.register(self)

    @Overrides(wxDirDialog)
    def Destroy(self, *args, **kw):
        self._shown = False
        Logger.add_close(self)
        wxDirDialog.Destroy(self, *args, **kw)

    @classmethod
    def wrap(self, register):
        wx.DirDialog = DirDialog
        DirDialog.register = register
