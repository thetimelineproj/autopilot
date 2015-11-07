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
from lib.gui.frames.mainframe.controller import MainFrameController


class MainFrane(wx.Frame):

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.controller = MainFrameController(self)
        self.create_gui()
        self.controller.on_init()

    def create_gui(self):
        self.set_icon()
        self.create_menu()
        self.create_status_bar()
        self.create_main_panel()
        self.SetSize((1000, 400))

    def set_icon(self):
        icon = wx.Icon(r'C:\Users\roger.RLDATA\workspace\Timeline\autopilot\icons\icon1.png', wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)

    def create_menu(self):
        try:
            menu_bar = wx.MenuBar()
            self.create_file_menu(menu_bar)
            self.create_test_menu(menu_bar)
            self.create_manuscript_menu(menu_bar)
            self.create_log_menu(menu_bar)
            self.SetMenuBar(menu_bar)
        except Exception, ex:
            pass

    def create_file_menu(self, menu_bar):
        menu = wx.Menu()
        mnu_open = menu.Append(wx.ID_ANY, 'Open...')
        menu.AppendSeparator()
        mnu_save = menu.Append(wx.ID_ANY, 'Save')
        mnu_save_as = menu.Append(wx.ID_ANY, 'Save As...')
        menu.AppendSeparator()
        mnu_exit = menu.Append(wx.ID_EXIT, 'Exit Program')
        menu_bar.Append(menu, 'File')
        self.Bind(wx.EVT_MENU, self.controller.on_open, mnu_open)
        self.Bind(wx.EVT_MENU, self.controller.on_save, mnu_save)
        self.Bind(wx.EVT_MENU, self.controller.on_save_as, mnu_save_as)
        self.Bind(wx.EVT_MENU, self.controller.on_app_exit, mnu_exit)

    def create_test_menu(self, menu_bar):
        menu = wx.Menu()
        mnu_new = menu.Append(wx.ID_ANY, 'New Test')
        mnu_run = menu.Append(wx.ID_ANY, 'Run Test')
        mnu_run_selection = menu.Append(wx.ID_ANY, 'Run Selection')
        menu.AppendSeparator()
        mnu_edit = menu.Append(wx.ID_ANY, 'Edit Test')
        menu_bar.Append(menu, 'Test')
        self.Bind(wx.EVT_MENU, self.controller.on_test_new, mnu_new)
        self.Bind(wx.EVT_MENU, self.controller.on_test_run, mnu_run)
        self.Bind(wx.EVT_MENU, self.controller.on_test_run_selection, mnu_run_selection)
        self.Bind(wx.EVT_MENU, self.controller.on_test_edit, mnu_edit)

    def create_manuscript_menu(self, menu_bar):
        menu = wx.Menu()
        mnu_effective = menu.Append(wx.ID_ANY, 'Display Effective')
        menu_bar.Append(menu, 'Manuscript')
        self.Bind(wx.EVT_MENU, self.controller.on_effective_manuscript, mnu_effective)

    def create_log_menu(self, menu_bar):
        menu = wx.Menu()
        mnu_open = menu.Append(wx.ID_ANY, "Open")
        mnu_open_temp = menu.Append(wx.ID_ANY, "Open temp")
        menu_bar.Append(menu, 'Log')
        self.Bind(wx.EVT_MENU, self.controller.on_open_log, mnu_open)
        self.Bind(wx.EVT_MENU, self.controller.on_open_temp_log, mnu_open_temp)

    def create_status_bar(self):
        self.CreateStatusBar()

    def create_main_panel(self):
        self.window_1 = wx.SplitterWindow(self, wx.ID_ANY, style=wx.SP_3D | wx.SP_BORDER)
        self.window_1_pane_1 = wx.Panel(self.window_1, wx.ID_ANY)
        self.window_1_pane_2 = wx.Panel(self.window_1, wx.ID_ANY)
        box = wx.BoxSizer(wx.HORIZONTAL)
        self.tests_list = wx.ListBox(self.window_1_pane_1)
        box.Add(self.tests_list, 1, wx.EXPAND)
        self.window_1_pane_1.SetSizer(box)
        box = wx.BoxSizer(wx.VERTICAL)
        self.text = wx.TextCtrl(self.window_1_pane_2, style=wx.TE_MULTILINE)
        font = self.GetFont()
        font.SetFaceName("Courier")
        font.SetPointSize(9)
        self.text.SetFont(font)
        self.progress = wx.Panel(self.window_1_pane_2)
        self.progress.SetBackgroundColour(wx.WHITE)
        box.Add(self.text, 10, wx.EXPAND)
        box.Add(self.progress, 0, wx.EXPAND)
        self.window_1_pane_2.SetSizer(box)
        self.__set_properties()
        self.__do_layout()
        self.Bind(wx.EVT_LISTBOX, self.controller.on_test_selection_changed, self.tests_list)

    def __set_properties(self):
        self.window_1_pane_1.SetBackgroundColour(wx.Colour(255, 255, 0))
        self.window_1_pane_2.SetBackgroundColour(wx.Colour(50, 153, 204))

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        self.window_1.SplitVertically(self.window_1_pane_1, self.window_1_pane_2, 200)
        sizer_1.Add(self.window_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

    def NewTest(self, test):
        self.tests_list.Append(test.get_name(), test)

    def DisplayTest(self, test):
        self.text.SetValue(test.to_display_format())

    def DisplayLog(self, log):
        self.text.SetValue(log)

    def GetTest(self):
        sel = self.tests_list.GetSelection()
        if sel >= 0:
            return self.tests_list.GetClientData(sel)

    def UpdateTest(self, test):
        sel = self.tests_list.GetSelection()
        if sel >= 0:
            self.tests_list.SetString(sel, test.get_name())
            self.DisplayTest(test)

    def GetAllTests(self):
        tests = []
        for i in range(self.tests_list.GetCount()):
            tests.append(self.tests_list.GetClientData(i))
        return tests

    def ClearTests(self):
        self.tests_list.Clear()

    def SelectFirstTest(self):
        try:
            self.tests_list.Select(0)
        except:
            pass

    def SetSuccess(self, success):
        if success:
            self.progress.SetBackgroundColour(wx.GREEN)
        else:
            self.progress.SetBackgroundColour(wx.RED)

    def ResetProgress(self):
        self.progress.SetBackgroundColour(wx.WHITE)
        self.Refresh()

    def GetSelection(self):
        return self.text.GetStringSelection()


def start_gui():
    app = wx.App()
    frame = MainFrane(None, -1, "Autopilot", style=wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
    frame.Centre()
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    start_gui()
