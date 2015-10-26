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
from lib.guinatives.strategywin32 import Win32Strategy


class WinStrategy(object):
    """
    This is the interface used to access native windows functions in
    different OS implementations.
    """

    def __init__(self):
        self.impl = None
        if platform.system() == "Windows":
            self.impl = Win32Strategy()

    def has_implementation(self):
        return self.impl is not None

    def get_foreground_window(self):
        return self.impl.get_foreground_window()

    def get_active_window(self):
        return self.impl.get_active_window()

    def get_classname(self, hwnd):
        return self.impl.get_classname(hwnd)

    def get_window_text(self, hwnd):
        return self.impl.get_window_text(hwnd)

    def get_children(self, hwnd):
        return self.impl.get_children(hwnd)

    def send_ctrl_key_down(self):
        return self.impl.send_ctrl_key_down()

    def send_ctrl_key_up(self):
        return self.impl.send_ctrl_key_up()

    def send_lbutton_click_to_window(self, position, ctrl=False):
        return self.impl.send_lbutton_click_to_window(position, ctrl)

    def send_text_to_text_control(self, hwnd, text):
        return self.impl.send_text_to_text_control(hwnd, text)

    def send_click_message_to_button(self, hwnd):
        return self.impl.send_click_message_to_button(hwnd)

    def send_select_combobox_item(self, hwnd, text):
        return self.impl.send_select_combobox_item(hwnd, text)

    def send_close_message_to_window(self, hwnd):
        return self.impl.send_close_message_to_window(hwnd)

    def wx_to_win_classname(self, classname):
        return self.impl.wx_to_win_classname(classname)

    def get_window_rect(self, hwnd):
        return self.impl.get_window_rect(hwnd)
