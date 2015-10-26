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

from lib.app.constants import MILLISECONDS_TO_WAIT_FOR_DIALOG_TO_SHOW
from lib.app.exceptions import NotFoundException
from lib.reporting.window import WindowDescriber
import lib.guinatives.facade as facade
from lib.guinatives.ctrlfinder import get_dialog_label
from lib.guinatives.ctrlfinder import GuiExplorer


BUTTON = "Button"
EDIT = "Edit"
COMBOBOX = "ComboBox"


class Wrapper(object):
    """
    This is the base class for all wrappers.

    A wrapper wraps a wx-defined window/dialog class, to be able to detect a
    call to the constructor, from the AUT, to such a class.

    This base class contains generic functions for manipulate the children of
    the window/dialog. These functions are used by Instruction objects.
    The childrens of a window/dialog are buttons edit fields etc.

    Internally this base class is used by all wrappers to explore and register
    all the childrens of the window/dialog. The explorer assumes that the
    window to be explored is the 'active' window of the AUT.
    The explorer also uses a Describer class to log the description of the
    window/dialog.

    """

    def __init__(self):
        self.gui_explorer = GuiExplorer()

    #
    # Public methods
    #
    def get_name(self):
        try:
            return self.Name
        except AttributeError:
            return ""

    def get_classname(self):
        try:
            return self.ClassName
        except AttributeError:
            return ""

    def get_label(self):
        try:
            return self.Label
        except AttributeError:
            return ""

    def get_dialog_label(self):
        label = self.get_label()
        if label == "":
            label = get_dialog_label()
        return label

    def get_nbr_of_children(self):
        try:
            return len(self.Children)
        except AttributeError:
            return 0

    def select_custom_tree_control_item(self, nbr, label):
        position = 1
        for child in self.Children:
            if child.GetLabel() == "CustomTreeCtrl" and position == nbr:
                tree = child
                item = self.get_item_by_label(tree, label, tree.GetRootItem())
                tree.SelectItem(item)
                return
        raise NotFoundException()

    def get_item_by_label(self, tree, search_text, root_item):
        item, cookie = tree.GetFirstChild(root_item)
        while item.IsOk():
            text = tree.GetItemText(item)
            if text.lower() == search_text.lower():
                return item
            if tree.ItemHasChildren(item):
                match = self.get_item_by_label(tree, search_text, item)
                if match.IsOk():
                    return match
            item, cookie = tree.GetNextChild(root_item, cookie)

    def click_menu_item(self, item_id):
        self.ProcessCommand(item_id)

    #
    # Internals
    #
    def _explore(self, register_win=None):
        self.messagebox = False
        WindowDescriber.describe(self)
        if register_win is not None:
            register_win(self)

    def set_active_window(self):
        self._active_window = facade.get_active_window()

    def call_when_win_shows(self, method):
        self._prev_win = None
        try:
            self._prev_win = self._active_window
        except:
            pass
        if self._prev_win is None:
            self._prev_win = facade.get_active_window()
        wx.CallLater(MILLISECONDS_TO_WAIT_FOR_DIALOG_TO_SHOW, self._wait_for_win_to_show, method)

    def _wait_for_win_to_show(self, method):
        if self._prev_win == facade.get_active_window():
            wx.CallLater(MILLISECONDS_TO_WAIT_FOR_DIALOG_TO_SHOW, self._wait_for_win_to_show, method)
        else:
            method()
