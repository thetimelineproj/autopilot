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
import lib.guinatives.facade as facade
from lib.app.exceptions import NotFoundException
from lib.reporting.logger import Logger
from lib.guinatives.facade import has_win_implementation


class Found(Exception):
    pass


def get_dialog_label():
    return facade.get_window_text(facade.get_active_window()).decode("utf-8")


class GuiExplorer(object):

    def find_win_by_name_or_label(self, name_or_label):
        self.wxctrl = None
        self.winctrl = None
        try:
            if name_or_label is None:
                self.wxctrl = wx.GetApp().GetTopWindow()
                raise Found("Top window")
            for name in name_or_label.split("|"):
                name = name.strip()
                self.find_wx_win(name, name)
                self.find_win_win(name)
        except Found, ex:
            Logger.add_debug(ex.message)
            return
        raise NotFoundException()

    def find_wx_win(self, name=None, label=None):
        self.find_wxwin_by_name(name)
        self.find_wxwin_by_label(label)

    def find_wxwin_by_name(self, name):
        for wxwin in wx.GetTopLevelWindows():
            if name is not None and hasattr(wxwin, "Name"):
                found_msg = "wx Name (%s) found" % name
                if wxwin.Name == name:
                    self.wxctrl = wxwin
                    raise Found(found_msg)

    def find_wxwin_by_label(self, label):
        for wxwin in wx.GetTopLevelWindows():
            if label is not None and hasattr(wxwin, "Label"):
                found_msg = "wx Label (%s) found" % label
                if wxwin.Label == label:
                    self.wxctrl = wxwin
                    raise Found(found_msg)

    def find_win_win(self, label):
        self.find_winwin_by_label(label)

    def find_winwin_by_label(self, label):
        if label is not None:
            found_msg = "win Label (%s) found" % label
            hwnd = facade.get_active_window()
            winlbl = facade.get_window_text(hwnd)
            winlbl = winlbl.decode("utf-8")
            if winlbl == label:
                self.winctrl = hwnd
                raise Found(found_msg)

    def find_ctrl(self, parent, key, wx_classname=None):
        self.wxctrl = None
        self.winctrl = None
        try:
            pos = int(key)
            wxid = pos
            name = None
            label = None
        except:
            pos = None
            wxid = None
            name = key
            label = key
        self._find_ctrl(parent, name, label, wxid=wxid, pos=pos, wx_classname=wx_classname)

    def is_wx_control(self):
        return self.wxctrl is not None

    def is_native_control(self):
        return self.winctrl is not None

    def get_ctrl(self):
        if self.is_wx_control():
            return self.wxctrl
        else:
            return self.winctrl

    def get_wxid(self):
        return self.wxctrl.GetId()

    def get_hwnd(self):
        return self.winctrl

    def _find_ctrl(self, parent, name=None, label=None, wxid=None, pos=None, wx_classname=None):
        try:
            self.find_wx_ctrl(parent, name, label, wxid, pos, wx_classname)
            self.find_win_ctrl(parent, name, label, wxid, pos, wx_classname)
        except Found, ex:
            Logger.add_debug(ex.message)
            return
        raise NotFoundException()

    def find_wx_ctrl(self, parent, name=None, label=None, wxid=None, pos=None, wx_classname=None):
        self.find_ctrl_by_name(parent, name)
        self.find_ctrl_by_label(parent, label)
        self.find_ctrl_by_wxid(parent, wxid)
        self.find_ctrl_by_pos(parent, wx_classname, pos)

    def find_win_ctrl(self, parent, name=None, label=None, wxid=None, pos=None, wx_classname=None):
        if has_win_implementation():
            self.find_win_ctrl_by_pos(parent, wx_classname, pos)
            self.find_win_ctrl_by_label(parent, label)

    def find_ctrl_by_name(self, parent, name):
        if name is not None and hasattr(parent, "GetChildren"):
            found_msg = "wx Name (%s) found" % name
            for ctrl in parent.GetChildren():
                if not hasattr(ctrl, "Name"):
                    continue
                if ctrl.Name == name:
                    self.wxctrl = ctrl
                    raise Found(found_msg)
                self.find_ctrl_by_name(ctrl, name)

    def find_ctrl_by_label(self, parent, label):
        if label is not None and hasattr(parent, "GetChildren"):
            found_msg = "wx Label (%s) found" % label
            for ctrl in parent.GetChildren():
                if not hasattr(ctrl, "Label"):
                    continue
                if ctrl.Label == label:
                    self.wxctrl = ctrl
                    raise Found(found_msg)
                # Try with elipses
                elif ctrl.Label == label + "...":
                    self.wxctrl = ctrl
                    raise Found(found_msg)
                # Try with accelerator
                else:
                    for i in range(len(label)):
                        lbl = label[0:i] + "&" + label[i:]
                        if ctrl.Label == lbl:
                            self.wxctrl = ctrl
                            raise Found(found_msg)

    def find_ctrl_by_wxid(self, parent, wxid):
        if wxid is not None:
            found_msg = "wx id found(%d)" % wxid
            for ctrl in parent.GetChildren():
                if not hasattr(ctrl, "GetId"):
                    continue
                if ctrl.GetId() == wxid:
                    self.wxctrl = ctrl
                    raise Found(found_msg)

    def find_ctrl_by_pos(self, parent, wx_classname, pos):
        if pos is not None:
            found_msg = "wx position found(%d)" % pos
            inx = 0
            for ctrl in parent.GetChildren():
                if not hasattr(ctrl, "ClassName"):
                    continue
                if ctrl.ClassName == wx_classname:
                    if inx == pos - 1:
                        self.wxctrl = ctrl
                        raise Found(found_msg)
                    else:
                        inx += 1

    def find_win_ctrl_by_pos(self, parent, wx_classname, pos):
        if wx_classname is not None and pos is not None:
            found_msg = "win order (%d) found for class(%s)" % (pos, facade.wx_to_win_classname(wx_classname))
            inx = 0
            try:
                hwnd = facade.get_active_window()
                children = facade.get_children(hwnd)
            except:
                return
            win_classname = facade.wx_to_win_classname(wx_classname)
            for hwnd, class_name, _ in children:
                if class_name == win_classname:
                    if inx == pos - 1:
                        self.winctrl = hwnd
                        raise Found(found_msg)
                    else:
                        inx += 1

    def find_win_ctrl_by_label(self, parent, label):
        if label is not None:
            found_msg = "win Label (%s) found" % label
            try:
                hwnd = facade.get_active_window()
                children = facade.get_children(hwnd)
            except:
                return
            for hwnd, _, winlbl in children:
                if winlbl == label:
                    self.winctrl = hwnd
                    raise Found(found_msg)
                # Try with elipses
                elif winlbl == label + "...":
                    self.winctrl = hwnd
                    raise Found(found_msg)
                # Try with accelerator
                else:
                    for i in range(len(label)):
                        lbl = label[0:i] + "&" + label[i:]
                        if winlbl == lbl:
                            self.winctrl = hwnd
                            raise Found(found_msg)

    def find_menu(self, args):
        try:
            win = wx.GetApp().GetTopWindow()
            item_id = self._find_menu_item_id(args)
            if item_id != wx.NOT_FOUND:
                self.item_id = item_id
                raise Found("Menu found")
        except Found, ex:
            Logger.add_debug(ex.message)
            return
        raise NotFoundException()

    def _find_menu_item_id(self, args):
        win = wx.GetApp().GetTopWindow()
        labels = args
        menu_bar = self._get_menu_bar(win)
        menu = self._find_menu(win, labels[0])
        if menu is None:
            raise NotFoundException()
        labels = labels[1:]
        while len(labels) > 0:
            item_id = self._get_menu_item_id(menu, labels[0])
            if len(labels) > 1:
                menu_item = menu_bar.FindItemById(item_id)
                menu = menu_item.GetSubMenu()
            labels = labels[1:]
        return item_id

    def _find_menu(self, win, label):
        menu_bar = self._get_menu_bar(win)
        labels = label.split("|")
        for label in labels:
            inx = menu_bar.FindMenu(label)
            if inx != -1:
                return menu_bar.GetMenu(inx)
        return None

    def _get_menu_bar(self, win):
        menu_bar = win.GetMenuBar()
        if menu_bar is None:
            raise NotFoundException()
        return menu_bar

    def _get_menu_item_id(self, menu, label):
        labels = label.split("|")
        for label in labels:
            valid_labels = self._get_valid_labels(label)
            for lbl in valid_labels:
                try:
                    itm = menu.FindItemByPosition(0)
                    l = itm.GetItemLabelText()
                    if l[-1] == u"\u2026":
                        pass
                    item_id = menu.FindItem(lbl)
                except Exception, ex:
                    pass
                if item_id != wx.NOT_FOUND:
                    return item_id
        raise NotFoundException()

    def _get_valid_labels(self, label):
        valid_labels = [label]
        self._get_elipsis_label(label, valid_labels)
        self._get_accelerator_labels(label, valid_labels)
        return valid_labels

    def _get_elipsis_label(self, label, alternative_labels):
        if label.endswith("..."):
            label = label[:-3]
        alternative_labels.append(label + "...")
        alternative_labels.append(label + u"\u2026")

    def _get_accelerator_labels(self, label, alternative_labels):
        for i in range(len(label)):
            alternative_label = label[0:i] + "&" + label[i:]
            alternative_labels.append(alternative_label)
        return alternative_labels
