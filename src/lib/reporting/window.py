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


from lib.reporting.logger import Logger
from lib.reporting.menubar import MenuBarDescriber
import lib.guinatives.facade as facade


described_windows = []


class WindowDescriber():

    @classmethod
    def describe(self, win):
        if Logger.log_dialog_descriptions:
            hwnd = facade.get_active_window()
            if hwnd not in described_windows:
                described_windows.append(hwnd) 
                self.describe_wxdialog(win)
                self.describe_window(hwnd)
                MenuBarDescriber.describe(win)

    @classmethod
    def describe_window(self, hwnd=None):
        if facade.has_win_implementation():
            nbr_of_children = len(facade.get_children(hwnd))
            if hwnd is None:
                hwnd = facade.get_active_window()
            rect = facade.get_window_rect(hwnd)
            Logger.bold_header("Window Description \n   hwnd:            %d \n   Classname:       '%s' \n   Label:           '%s'\n   Nbr of children: %d\n   Position:        (%d, %d)\n   Size:            (%d, %d)" % (
                hwnd, facade.get_classname(hwnd), facade.get_window_text(hwnd), nbr_of_children, rect[0], rect[1], rect[2], rect[3]))
            Logger.header2("Native Description")
            self.describe_children(hwnd)

    @classmethod
    def describe_children(self, hwnd):
        Logger.add("    hwnd     Classname                 ScreenPos    Label")
        Logger.add("    -------  ------------------------  ------------ ------------------")
        children = facade.get_children(hwnd)
        for hwnd, class_name, text in children:
            rect = facade.get_window_rect(hwnd)
            Logger.add("   %8d  %-24.24s  (%4d, %4d) '%s'" % (hwnd, class_name, rect[0], rect[1], text))

    @classmethod
    def describe_wxdialog(self, win, level=0):
        if win is None:
            return
        Logger.newline()
        Logger.bold_header("wx Description\n  Name:             '%s'\n  ClassName:        '%s'\n  Label:            '%s'\n  Nbr of children:  %d" % (win.get_name(), win.get_classname(), win.get_label(), win.get_nbr_of_children()))
        if win.get_nbr_of_children() > 0:
            self.describe_wxdialog_windows(win)

    @classmethod
    def describe_wxdialog_windows(self, win, level=0):
        msg = ""
        if len(win.Children) == 0:
            return
        margin = "%*.*s" % (level * 3, level * 3, "")
        if level > 0:
            Logger.add(" ")
            Logger.add("   %sClassName: %s" % (margin, win.ClassName))
        Logger.add("   %sId    Classname                Label                     Name" % margin)
        Logger.add("   %s----  ------------------------ ------------------------  ----------------" % margin)
        try:
            for child in win.Children:
                child_id = child.GetId()
                msg = "   %s%4d  %-24.24s %-24.24s  '%s'" % (margin, child_id, child.GetClassName(), child.GetLabel(), child.GetName())
                Logger.add(msg)
                self.describe_wxdialog_windows(child, level + 1)
        except AttributeError:
            Logger.add("   No children exists")
        except Exception, ex:
            pass
