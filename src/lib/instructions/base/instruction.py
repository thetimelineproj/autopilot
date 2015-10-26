# -*- coding: cp1252 -*-
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

import lib.instructions.base.scanner as scanner
from lib.app.exceptions import InstructionSyntaxException
from lib.app.exceptions import NotFoundException
from lib.reporting.logger import Logger
from lib.reporting.logger import placeholders
from lib.guinatives.ctrlfinder import GuiExplorer
import lib.guinatives.facade as facade


class Instruction(object):
    """
    The base class for all types of instructions.

    An instruction always belongs to a Manuscript.

    Textual syntax:  <instruction-name> <instruction-target>  <optional-arglist>

    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.tokens = self._compress_tokens()
        self.include = False
        self.comment = False
        self.gui_explorer = GuiExplorer()
        self.placeholders = {}

    def add_placeholder(self):
        Logger.add_placeholder(self.arg(1), self.arg(2))

    def _replace_placeholders(self):
        for token in self.tokens:
            if token.id == scanner.PLACEHOLDER:
                if token.lexeme not in placeholders:
                    raise InstructionSyntaxException("Unknown placeholder %s" % token.lexeme)
                replacement = '"%s"' % placeholders[token.lexeme]
                token.lexeme = replacement
                token.id = scanner.STRING

    def _compress_tokens(self):
        t = []
        tk = None
        state = 0
        for token in self.tokens:
            if state == 0:
                if token.id == scanner.LP:
                    state = 1
                t.append(token)
            elif state == 1:
                tk = token
                state = 2
            elif state == 2:
                if token.id == scanner.RP:
                    t.append(tk)
                    t.append(token)
                elif token.id == scanner.COMMA:
                    t.append(tk)
                    t.append(token)
                    state = 1
                else:
                    tk.lexeme += token.lexeme
        return t

    def __str__(self):
        text = []

        def prefix_keyword(token):
            if token.id == scanner.KEYWORD:
                text.append(u" ")

        def append_lexeme(token):
            prefix_keyword(token)
            text.append(token.lexeme)

        def join_token_lexemes():
            for token in self.tokens:
                append_lexeme(token)
            return text

        a = u"".join(join_token_lexemes())
        b = a.strip()
        return b

    def to_unicode(self):
        text = []

        def prefix_keyword(token):
            if token.id == scanner.KEYWORD:
                text.append(u" ")

        def append_lexeme(token):
            prefix_keyword(token)
            text.append(token.lexeme)

        def join_token_lexemes():
            for token in self.tokens:
                append_lexeme(token)
            return text

        a = u"".join(join_token_lexemes())
        b = a.strip()
        return b

    def execute(self, manuscript, win):
        self.wrapper_win = win
        manuscript.execute_next_instruction()
        Logger.add_debug("Executing instruction '%s'" % (self))
        self._execute()

    def _execute(self):
        raise NotImplementedError("_execute")

    def arg(self, n):
        """
        Return the n:th argument, where n = 1,2,....
        """
        try:
            tokens = self._find_tokens_between_parenthesis()
            if n < 1 or n > len(tokens):
                raise NotFoundException
            token = tokens[n - 1]
            return self._token_lexem_without_string_markers(token)
        except:
            return None

    def _token_lexem_without_string_markers(self, token):
        """
           case 1:   "arg"
           case 2:arg1|"arg2"
        """
        return token.lexeme.replace('"', "")

    def _find_tokens_between_parenthesis(self):
        tokens = []
        lp_found = False
        for token in self.tokens:
            if lp_found:
                if token.id == scanner.RP:
                    return tokens
                else:
                    if token.id != scanner.COMMA:
                        tokens.append(token)
            else:
                if token.id == scanner.LP:
                    lp_found = True
        raise NotFoundException()

    def _symbol(self, index):
        try:
            token = self.tokens[index]
            if token.id == scanner.STRING:
                return token.lexeme[1:-1]
            else:
                return token.lexeme
        except:
            return None

    def get_all_args(self):
        args = []
        for token in self.tokens:
            if token.id in (scanner.ID, scanner.NUM):
                args.append(token.lexeme)
            elif token.id == scanner.STRING:
                args.append(token.lexeme[1:-1])
        return args

    def result_message(self, result):
        return "%s. %s" % (self, result)

    #
    # Serach for the control specified in the first argument of the instruction.
    # Returns True if a wx-control is found
    # Returns False if a native control is found.
    # Returns None if the control isn't found
    # Loggs the success or failure of this search
    #
    def find_wxctrl(self, classname):
        alternative_names = [name.strip() for name in self.arg(1).split("|")]
        for name in alternative_names:
            try:
                self.gui_explorer.find_ctrl(self.wrapper_win, name, classname)
                Logger.success(self.result_message("Found"))
                return self.gui_explorer.is_wx_control()
            except NotFoundException:
                pass
        Logger.failure(self.result_message("NOT Found"))

    #
    # Send message to control
    #
    def _find_control_and_send_message(self, wx_classname, wx_func, native_func):
        self.find_wxctrl(wx_classname)
        if self.gui_explorer.is_wx_control():
            wx_func()
        elif self.gui_explorer.is_native_control():
            native_func()

    #
    # Click button
    #
    def click_button(self, wx_classname):
        self._find_control_and_send_message(wx_classname,
                                            self._click_wx_button,
                                            self._click_native_button)

    def _click_wx_button(self):
        wxid = self.gui_explorer.get_wxid()
        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, wxid)
        wx.PostEvent(self.wrapper_win, evt)

    def _click_native_button(self):
        hwnd = self.gui_explorer.get_ctrl()
        facade.send_click_message_to_button(hwnd)

    #
    # select combobox item
    #
    def select_combobox_item(self, wx_classname):
        """
        The control can be found as a wx-control or in second hand
        a win native control.
        If no control is found a NotFoundException has been raised.
        """
        self._find_control_and_send_message(wx_classname,
                                            self._select_wx_itemcontainer_item,
                                            self._select_native_combobox_item())

    def _select_wx_itemcontainer_item(self):
        wxctrl = self.gui_explorer.get_ctrl()
        wxctrl.SetSelection(self.get_wx_itemcontainer_item_index(wxctrl, self.arg(2)))

    def get_wx_itemcontainer_item_index(self, ctrl, item):
        """
        The item specification can be a text string or a 1-based index.
        """
        try:
            inx = int(item) - 1
        except:
            inx = ctrl.FindString(item)
            if inx is wx.NOT_FOUND:
                raise NotFoundException()
        return inx

    def _select_native_combobox_item(self):
        # TODO:
        # facade.send_text_to_text_control(self.gui_explorer.get_ctrl(), text)
        pass

    #
    # select customtreecontrol item
    #
    def select_customtreecontrol_item(self, wx_classname):
        """
        The control can be found as a wx-control or in second hand
        a win native control.
        If no control is found a NotFoundException has been raised.
        """
        self._find_control_and_send_message(wx_classname,
                                            self._select_wx_itemcontainer_item,
                                            self._select_native_customtreecontrol_item())

    def _select_native_customtreecontrol_item(self):
        # TODO:
        pass

    #
    # click a checkbox
    #
    def click_checkbox(self, wx_classname):
        self._find_control_and_send_message(wx_classname,
                                            self._check_wx_checkbox,
                                            self._check_native_checkbox)

    def _check_wx_checkbox(self):
        """
        What a mess! Isn't it an easier way?
        The PostEvent acts as if the checkbox was clicked but the checkbox gui isn't updated.
        That's why the SetValue() function is called
        """
        CHECKED = 1
        UNCHECKED = 0
        evt = wx.PyCommandEvent(wx.EVT_CHECKBOX.typeId, self.gui_explorer.get_wxid())
        evt.SetEventObject(self.wrapper_win)
        cbx = self.gui_explorer.get_ctrl()
        if cbx.IsChecked():
            evt.SetInt(UNCHECKED)
            cbx.SetValue(False)
        else:
            evt.SetInt(CHECKED)
            cbx.SetValue(True)
        wx.PostEvent(self.wrapper_win, evt)

    def _check_native_checkbox(self):
        facade.send_click_message_to_button(self.gui_explorer.get_ctrl())

    #
    # click mouse
    #
    def click_mouse(self):
        """
        This method never fails but we keep the catching of NotFoundException
        in case we should change the code.s
        """
        pos = (int(self.arg(1)), int(self.arg(2)))
        try:
            Logger.success(self.result_message("Clicked"))
            facade.send_lbutton_click_to_window(pos, self.hold_down_ctrl_key_when_clicking())
        except NotFoundException:
            Logger.failure(self.result_message("Failed"))

    def hold_down_ctrl_key_when_clicking(self):
        return self.arg(3) is not None and self.arg(3) == "ctrl"

    #
    # Enter text
    #
    def enter_text(self, classname):
        self._find_control_and_send_message(classname, self._set_wx_control_text, self._set_native_control_text)

    def _set_wx_control_text(self):
        self.gui_explorer.get_ctrl().SetValue(self.arg(2))

    def _set_native_control_text(self):
        facade.send_text_to_text_control(self.gui_explorer.get_ctrl(), self.arg(2))

    #
    # Select listbox item
    #
    def select_listbox_item(self, classname):
        try:
            self._select_listbox_item(classname)
        except NotFoundException:
            Logger.failure(self.result_message("NOT Found"))

    def _select_listbox_item(self, classname):
        name_label_or_position = self.arg(1)
        text = self.arg(2)
        self.gui_explorer.find_ctrl(self.wrapper_win, name_label_or_position, classname)
        if self.gui_explorer.is_wx_control():
            ctrl = self.gui_explorer.get_ctrl()
            try:
                inx = int(text) - 1
            except:
                inx = ctrl.FindString(text)
            if inx is not wx.NOT_FOUND:
                Logger.success(self.result_message("Found"))
                ctrl.SetSelection(inx)
            else:
                raise NotFoundException("ListBox row(%s) in '%s'" % (text, name_label_or_position))
        else:
            # TODO:
            # facade.send_text_to_text_control(self.gui_explorer.get_ctrl(), text)
            pass

    #
    # Select menu
    #
    def select_menu(self):
        try:
            self.gui_explorer.find_menu(self.get_all_args())
            Logger.success(self.result_message("Found"))
            wx.GetApp().GetTopWindow().click_menu_item(self.gui_explorer.item_id)
        except NotFoundException:
            Logger.failure(self.result_message("NOT Found"))

    #
    # Close dialog
    #
    def close_dialog(self):
        name_or_label = self.arg(1)
        if name_or_label is None:
            name_or_label = self.wrapper_win.GetLabel()
        self.gui_explorer.find_win_by_name_or_label(name_or_label)
        if self.gui_explorer.is_wx_control():
            self.gui_explorer.get_ctrl().Destroy()
        else:
            facade.send_close_message_to_window(self.gui_explorer.get_ctrl())
        Logger.success(self.result_message("Closed"))

    #
    # Assert open
    # Assert closed
    #
    def assert_open(self):
        alternative_names = self.arg(1).split("|")
        for name in alternative_names:
            if self._open(name):
                Logger.success(self.result_message("Open"))
                return
        Logger.failure(self.result_message("Closed"))

    def assert_closed(self):
        alternative_names = self.arg(1).split("|")
        for name in alternative_names:
            if self._open(name):
                Logger.failure(self.result_message("Open"))
                return
        Logger.success(self.result_message("Closed"))

    def _open(self, name):
        wins = [window for window in wx.GetTopLevelWindows()
                if name == window.get_name() or
                name == window.get_dialog_label()]
        return len(wins) > 0

    #
    # Exit application
    #
    def exit_application(self):
        win = wx.GetApp().GetTopWindow()
        if win:
            win.Destroy()
        else:
            facade.send_close_message_to_window(facade.get_active_window())
        Logger.success(self.result_message("Application destroyed"))
