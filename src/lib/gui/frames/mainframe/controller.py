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


import os
import wx
import xml.etree.ElementTree
from subprocess import Popen, PIPE
from lib.gui.dialogs.testeditor.view import TestEditorDialog
from lib.gui.data.autopilottest import AutopilotTest
from lib.app.settings import Settings
import xml.etree.ElementTree as ET


START_SCRIPT = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "run.py")
TEMPFILE = "autopilottest.tmp"
LOGFILE = "autopilot.log"


class NoTestFound(Exception):
    pass


class NoSelectionFound(Exception):
    pass


class NoFilePathSelected(Exception):
    pass


class MainFrameController(object):

    def __init__(self, view):
        self.view = view
        self.settings = Settings()

    def on_init(self):
        pass

    def get_recently_opened(self):
        return self.settings.get_recently_opened()

    #
    # File menu actions
    #

    def on_open(self, event):
        try:
            self._open(self._get_file_path("Open"))
        except NoFilePathSelected:
            pass

    def on_open_recent(self, event):
        self.open_path_if_exists(self.view.GetPath(event.GetId()))

    def on_save(self, event):
        try:
            self._save(self.path)
        except NoTestFound:
            pass

    def on_save_as(self, event):
        try:
            self._save(self._get_file_path("Save As"))
        except NoTestFound:
            pass
        except NoFilePathSelected:
            pass

    def on_app_exit(self, event):
        pass

    #
    # Test menu actions
    #

    def on_test_new(self, event):
        test = AutopilotTest()
        d = TestEditorDialog(self.view, "New Test", test)
        if d.ShowModal() == wx.ID_OK:
            self.view.NewTest(test)
            self._save(self.path)

    def on_remove_test(self, event):
        test = self._get_test()
        self.view.RemoveTest(test)
        self._save(self.path)

    def on_test_run(self, event):
        try:
            test = self._get_test()
            args = ["python", START_SCRIPT]
            args.extend(test.get_argv())
            self._execute_test(args)
        except NoTestFound:
            pass

    def on_test_run_selection(self, event):
        try:
            test = self._get_test()
            selection = self._get_selection()
            self._save_to_tempfile(selection)
            args = ["python", START_SCRIPT,
                    test.get_app(),
                    "-p", os.getcwd(),
                    "-m", TEMPFILE,
                    "-d",
                    "-l",
                    "-e"]
            self._execute_test(args)
        except NoTestFound:
            pass
        except NoSelectionFound:
            pass

    def on_test_edit(self, event):
        try:
            test = self._get_test()
            d = TestEditorDialog(self.view, "Edit Test", test)
            if d.ShowModal() == wx.ID_OK:
                self.view.UpdateTest(test)
        except NoTestFound:
            pass

    #
    # Manusctip menu actions
    #

    def on_effective_manuscript(self, event):
        try:
            test = self._get_test()
            args = ["python", START_SCRIPT,
                    test.get_app(),
                    "-p", test.manuscript_paths,
                    "-m", test.start_manuscript,
                    "-i"]
            self._execute_test(args)
            self.on_open_log(None)
        except NoTestFound:
            pass

    def on_edit(self, event):
        path = self.view.GetTest().get_manuscript()
        editor = os.getenv('EDITOR')
        if editor:
            os.system("%s %s" % (editor, path))
        else:
            os.system(path)

    #
    # Log menu actions
    #
    def on_open_log(self, event):
        try:
            test = self._get_test()
            self._display_logfile(test.get_log_path())
        except NoTestFound:
            pass

    def on_open_temp_log(self, event):
        self._display_logfile(os.getcwd())

    #
    # Other actions
    #

    def open_path_if_exists(self, path):
        if os.path.exists(path):
            self._open(path)

    def on_test_selection_changed(self, event):
        lbx = event.GetEventObject()
        test = lbx.GetClientData(lbx.GetSelection())
        self.view.DisplayTest(test)

    def _save_to_tempfile(self, text):
        f = open(TEMPFILE, "w")
        f.write(text.encode("utf-8"))
        f.close()

    def _get_test(self):
        test = self.view.GetTest()
        if test is None:
            wx.MessageBox("You have to select a test!")
            raise NoTestFound()
        return test

    def _get_selection(self):
        selection = self.view.GetSelection()
        if selection is None or selection.strip() == "":
            wx.MessageBox("You have to make a selection!")
            raise NoSelectionFound()
        return self._remove_empty_lines(selection)

    def _remove_empty_lines(self, text):
        lines = [line for line in text.split("\n") if line.strip() != ""]
        return "\n".join(lines)

    def _execute_test(self, args):
        self.view.ResetProgress()
        process = Popen(args, stdout=PIPE)
        process.communicate()
        self.view.SetSuccess(process.returncode == 0)

    def _save(self, path):
        tests = self.view.GetAllTests()
        root = ET.Element("autopilottests")
        for test in tests:
            atest = ET.SubElement(root, "autopilottest")
            ET.SubElement(atest, "name").text = test.name
            ET.SubElement(atest, "app").text = test.app_under_test
            ET.SubElement(atest, "manuscript").text = os.path.join(test.manuscript_paths, test.start_manuscript)
            ET.SubElement(atest, "exit").text = "%s" % test.exit_when_done
            ET.SubElement(atest, "delay").text = test.delay
            ET.SubElement(atest, "debug").text = "%s" % test.debug
            ET.SubElement(atest, "log").text = "%s" % test.log_dialogs
            ET.SubElement(atest, "inspect").text = "%s" % test.inspect
            tree = ET.ElementTree(root)
            tree.write(path)

    def _open(self, path):
        self.view.ClearTests()
        self.path = path
        e = xml.etree.ElementTree.parse(path).getroot()
        for xmltest in e.findall('autopilottest'):
            test = AutopilotTest()
            test.set_name(xmltest.find("name").text)
            test.set_app_under_test(xmltest.find("app").text)
            test.set_start_manuscript(xmltest.find("manuscript").text)
            test.set_delay(xmltest.find("delay").text)
            test.set_exit_when_done(xmltest.find("exit").text == "True")
            test.set_debug(xmltest.find("debug").text == "True")
            test.set_log_dialogs(xmltest.find("log").text == "True")
            test.set_inspect(xmltest.find("inspect").text == "True")
            self.view.NewTest(test)
        self.view.SelectFirstTest()
        self.view.DisplaySelectedTest()
        if self.settings.save_recently_opened(path):
            self.view.SetRecentlyOpened(path)

    def _display_logfile(self, path):
        with open(os.path.join(path, LOGFILE)) as f:
            log = f.read().decode("utf-8")
            self.view.DisplayLog(log)

    def _get_file_path(self, heading):
        d = wx.FileDialog(self.view, heading)
        if d.ShowModal() == wx.ID_OK:
            return d.GetPath()
        raise NoFilePathSelected()
