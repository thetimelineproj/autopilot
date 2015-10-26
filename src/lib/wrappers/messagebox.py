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


wxMessageBox = wx.MessageBox


def MessageBox(*args, **kw):
    Logger.add_result("MessageBox '%s' opened" % args[1])
    wx.CallLater(TIME_TO_WAIT_FOR_DIALOG_TO_SHOW_IN_MILLISECONDS, _explore_and_register)
    rv = wxMessageBox(*args, **kw)
    Logger.add_result("MessageBox '%s' closed" % args[1])
    return rv


def _explore_and_register():
    wrapper = Wrapper()
    wrapper._explore(None)
    wrapper.messagebox = True
    MessageBox.register(wrapper)


def wrap(register):
    wx.MessageBox = MessageBox
    MessageBox.register = register
