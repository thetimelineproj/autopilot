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


class InstructionPopup(wx.PopupWindow):

    def __init__(self, parent):
        try:
            wx.PopupWindow.__init__(self, parent, wx.SIMPLE_BORDER)
            self._create_gui()
            self.Show(True)
            wx.CallAfter(self.Refresh)
        except TypeError:
            pass

    def SetText(self, text):
        try:
            self.st.SetLabel(text)
        except AttributeError:
            pass

    def _create_gui(self):
        self.SetBackgroundColour("GOLDENROD")
        self.st = wx.StaticText(self, -1, "", pos=(10,10))
        sz = self.st.GetBestSize()
        self.SetSize((sz.width + 20 + 350, sz.height + 20))
        w, h = wx.DisplaySize()
        w1, h1 = self.GetSize()
        x = w - w1 - 20
        y = h - 2.5 * h1
        self.SetPosition((x,y))
        # TODO:
        # Adjustments for two screens
        #   displays = (wx.Display(i) for i in range(wx.Display.GetCount()))
        #   sizes = [display.GetGeometry().GetSize() for display in displays]

    def Destroy(self):
        self.EndModal(wx.ID_CANCEL)
