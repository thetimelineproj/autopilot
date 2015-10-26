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


wxPageSetupDialog = wx.PageSetupDialog


class PageSetupDialog(wx.PageSetupDialog, Wrapper):

    def __init__(self, *args, **kw):
        wxPageSetupDialog.__init__(self, *args, **kw)
        Wrapper.__init__(self)
        self.shown = False

    def name(self):
        return "Page Setup"

    def classname(self):
        return self.GetClassName()

    def IsShown(self):
        return self.shown

    def ShowModal(self):
        self.shown = True
        Logger.add_open(self)
        self.call_when_win_shows(self._explore_and_register)
        super(PageSetupDialog, self).ShowModal()

    def _explore_and_register(self):
        self._explore()
        PageSetupDialog.register(self)

    @Overrides(wxPageSetupDialog)
    def Destroy(self, *args, **kw):
        self.shown = False
        Logger.add_close(self)
        wxPageSetupDialog.Destroy(self, *args, **kw)

    @classmethod
    def wrap(self, register):
        wx.PageSetupDialog = PageSetupDialog
        PageSetupDialog.register = register
