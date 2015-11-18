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


import platform


if platform.system() == "Windows":
    import win32api
    import win32gui
    import win32con


class Win32Strategy(object):

    def get_foreground_window(self):
        return win32gui.GetForegroundWindow()

    def get_active_window(self):
        return win32gui.GetActiveWindow()

    def get_classname(self, hwnd):
        return win32gui.GetClassName(hwnd)

    def get_window_text(self, hwnd):
        return win32gui.GetWindowText(hwnd)

    def get_children(self, hwnd):
        children = []
        win32gui.EnumChildWindows(hwnd, self._get_child, children)
        collector = []
        for hwnd, x, label in children:
            collector.append((hwnd, x, label.decode("cp1252")))
        return collector

    def send_ctrl_key_down(self):
        win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)

    def send_ctrl_key_up(self):
        win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)

    def send_lbutton_click_to_window(self, position, ctrl=False):
        if ctrl:
            self.send_ctrl_key_down()
        try:
            win32api.SetCursorPos(position)
            flags = win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_ABSOLUTE
            win32api.mouse_event(flags, 0, 0)
            flags = win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_ABSOLUTE
            win32api.mouse_event(flags, 0, 0)
        finally:
            if ctrl:
                self.send_ctrl_key_up()

    def send_text_to_text_control(self, hwnd, text):
        win32gui.SetWindowText(hwnd, text)

    def send_click_message_to_button(self, hwnd):
        win32gui.SendMessage(hwnd, win32con.BM_CLICK)

    def send_select_combobox_item(self, hwnd, text):
        return win32gui.SendMessage(hwnd, win32con.CB_SELECTSTRING, -1, text)

    def _get_child(self, hwnd, children):
        class_name = win32gui.GetClassName(hwnd)
        text = win32gui.GetWindowText(hwnd)
        children.append((hwnd, class_name, text))
        return True

    def wx_to_win_classname(self, wx_classname):
        MAP = {"wxStaticText": "Static",
               "wxButton": "Button",
               "wxTextCtrl": "Edit",
               "wxComboBox": "ComboBox",
               "wxCheckBox": "Button",
               }
        return MAP[wx_classname]

    def send_close_message_to_window(self, hwnd):
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    def get_window_rect(self, hwnd):
        return win32gui.GetWindowRect(hwnd)