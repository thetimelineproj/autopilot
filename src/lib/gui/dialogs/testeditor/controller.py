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


class TestEditorDialogController(object):

    def __init__(self, view):
        self.view = view

    def on_init(self, autopilot_test):
        self.autopilot_test = autopilot_test
        self.populate_view()

    def populate_view(self):
        self.view.SetName(self.autopilot_test.get_name())
        self.view.SetAppllicationUnderTest(self.autopilot_test.get_app())
        self.view.SetManuscript(self.autopilot_test.get_manuscript())
        self.view.SetDebug(self.autopilot_test.get_debug())
        self.view.SetLogDialogs(self.autopilot_test.get_log_dialogs())
        self.view.SetInspect(self.autopilot_test.get_inspect())
        self.view.SetDelay(self.autopilot_test.get_delay())
        self.view.SetExit(self.autopilot_test.get_exit())

    def on_ok_clicked(self, event):
        if self._validate_input():
            self.autopilot_test.set_name(self.view.GetName())
            self.autopilot_test.set_app_under_test(self.view.GetAppllicationUnderTest())
            self.autopilot_test.set_start_manuscript(self.view.GetManuscript())
            self.autopilot_test.set_debug(self.view.GetDebug())
            self.autopilot_test.set_log_dialogs(self.view.GetLogDialogs())
            self.autopilot_test.set_inspect(self.view.GetInspect())
            self.autopilot_test.set_delay(self.view.GetDelay())
            self.autopilot_test.set_exit_when_done(self.view.GetExit())
            self.view.Close()
            self.autopilot_test.to_xml()

    def on_cancel_clicked(self, event):
        self.view.Close()

    def on_find_app(self, event):
        d = wx.FileDialog(self.view, "Find application under test")
        if d.ShowModal() == wx.ID_OK:
            self.view.SetAppllicationUnderTest(d.GetPath())

    def on_find_dir(self, event):
        d = wx.FileDialog(self.view, "Find manuscript directory")
        if d.ShowModal() == wx.ID_OK:
            path = self.view.GetManuscript()
            if path == "":
                self.view.SetManuscript(d.GetPath())
            else:
                self.view.SetManuscript(path + ";" + d.GetPath())

    def _validate_input(self):
        try:
            self._validate_test_name()
            self._validate_aut()
            self._validate_manuscript()
            return True
        except Exception, ex:
            wx.MessageBox(ex.message)
            return False

    def _validate_test_name(self):
        if self.view.GetName() == "":
            raise Exception(self._mandatory_message("Test Name"))

    def _validate_aut(self):
        if self.view.GetAppllicationUnderTest() == "":
            raise Exception(self._mandatory_message("Application under Test"))

    def _validate_manuscript(self):
        if self.view.GetManuscript() == "":
            raise Exception(self._mandatory_message("Start Manuscript"))

    def _mandatory_message(self, data):
        return "%s is a mandatory field" % data
