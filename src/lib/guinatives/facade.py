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


from lib.guinatives.strategy import WinStrategy


WIN_STRATEGY = WinStrategy()


def has_win_implementation():
    return WIN_STRATEGY.has_implementation()


def get_foreground_window():
    return WIN_STRATEGY.get_foreground_window()


def get_active_window():
    return WIN_STRATEGY.get_active_window()


def get_classname(hwnd):
    return WIN_STRATEGY.get_classname(hwnd)


def get_window_text(hwnd):
    return WIN_STRATEGY.get_window_text(hwnd)


def get_children(hwnd):
    return WIN_STRATEGY.get_children(hwnd)


def send_ctrl_key_down():
    return WIN_STRATEGY.send_ctrl_key_down()


def send_ctrl_key_up(self):
    return WIN_STRATEGY.send_ctrl_key_up()


def send_lbutton_click_to_window(position, ctrl=False):
    return WIN_STRATEGY.send_lbutton_click_to_window(position, ctrl)


def send_text_to_text_control(hwnd, text):
    return WIN_STRATEGY.send_text_to_text_control(hwnd, text)


def send_click_message_to_button(hwnd):
    return WIN_STRATEGY.send_click_message_to_button(hwnd)


def send_select_combobox_item(hwnd, text):
    return WIN_STRATEGY.send_select_combobox_item(hwnd, text)


def wx_to_win_classname(wx_classname):
    return WIN_STRATEGY.wx_to_win_classname(wx_classname)


def send_close_message_to_window(hwnd):
    return WIN_STRATEGY.send_close_message_to_window(hwnd)


def get_window_rect(hwnd):
    return WIN_STRATEGY.get_window_rect(hwnd)
