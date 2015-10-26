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

from lib.reporting.logger import Logger
from lib.wrappers.wrapper import Wrapper
from lib.app.constants import TIME_TO_WAIT_FOR_DIALOG_TO_SHOW_IN_MILLISECONDS


wxMessageDialog = wx.MessageDialog


class MessageDialog(wxMessageDialog, Wrapper):

    def __init__(self, *args, **kw):
        wxMessageDialog.__init__(self, *args, **kw)
        Wrapper.__init__(self)

    def ShowModal(self):
        Logger.add_result("MessageDialog opened")
        wx.CallLater(TIME_TO_WAIT_FOR_DIALOG_TO_SHOW_IN_MILLISECONDS,
                     self._explore, MessageDialog.listener)
        return super(MessageDialog, self).ShowModal()

    def IsShown(self):
        """
        Some generic dialogs return False here, even when they
        are visible!!!!
        """
        return True

    @classmethod
    def wrap(self, listener):
        wx.MessageDialog = MessageDialog
        MessageDialog.listener = listener
