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
from humblewx import Dialog
from lib.gui.dialogs.testeditor.controller import TestEditorDialogController


class TestEditorDialog(Dialog):

    """
    <BoxSizerVertical>
        <FlexGridSizer columns="3" growableColumns="1" proportion="1" border="ALL">
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(name_text)" />
            <TextCtrl
                name="txt_name"
                width="150"
            />
            <StretchSpacer />
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(aut_text)" />
            <TextCtrl
                name="txt_aut"
                width="350" />
            <Button
                label="..."
                size="$(open_button_size)"
                event_EVT_BUTTON="on_find_app"
            />
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(manuscript_text)" />
            <TextCtrl
                name="txt_manuscript"
                width="350"
            />
            <Button
                label="..."
                size="$(open_button_size)"
                event_EVT_BUTTON="on_find_dir"
            />
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(placeholders_text)" />
            <TextCtrl
                name="txt_placeholders"
                width="350"
            />
            <Button
                label="..."
                size="$(open_button_size)"
                event_EVT_BUTTON="on_find_placeholders"
            />
        </FlexGridSizer>
        <StaticBoxSizerVertical label="$(flags)" border="LEFT|RIGHT">
            <CheckBox
                name="cbx_debug"
                label="Debug"
                border="LEFT|TOP"
            />
            <CheckBox
                name="cbx_log_dialogs"
                label="Log dialog descriptions"
                border="LEFT|TOP"
            />
            <CheckBox
                name="cbx_inspect"
                label="Inspect manuscript"
                border="LEFT|TOP"
            />
            <CheckBox
                name="cbx_exit"
                label="Exit Application when done"
                border="LEFT|TOP"
            />
            <BoxSizerHorizontal border="LEFT|TOP">
                <StaticText align="ALIGN_CENTER_VERTICAL" label="$(delay_text)" />
                <TextCtrl name="txt_delay" width="30" />
                <StretchSpacer/>
            </BoxSizerHorizontal>
        </StaticBoxSizerVertical>
        <BoxSizerHorizontal>
            <StretchSpacer />
            <Button
                label='OK'
                border="BOTTOM|RIGHT"
                event_EVT_BUTTON="on_ok_clicked"
            />
            <Button
                label='Cancel'
                border="BOTTOM|RIGHT"
                event_EVT_BUTTON="on_cancel_clicked"
            />
        </BoxSizerHorizontal>
    </BoxSizerVertical>
    """

    def __init__(self, parent, title, autopilot_test):
        Dialog.__init__(self, TestEditorDialogController, parent, {
            "name_text": "Test Name:",
            "aut_text": "Program to Test:",
            "manuscript_text": "Start Manuscript:",
            "flags": "Properties",
            "delay_text": "Delay in seconds: ",
            "open_button_size": (25, -1),
            "placeholders_text": "Placeholders file"
        }, title=title)
        self.controller.on_init(autopilot_test)

    def Close(self):
        self.EndModal(wx.ID_CANCEL)

    def CloseOk(self):
        self.EndModal(wx.ID_OK)

    def GetName(self):
        return self.txt_name.GetValue()

    def SetName(self, name):
        self.txt_name.SetValue(name)

    def GetAppllicationUnderTest(self):
        return self.txt_aut.GetValue()

    def SetAppllicationUnderTest(self, aut):
        self.txt_aut.SetValue(aut)

    def GetManuscript(self):
        return self.txt_manuscript.GetValue()

    def SetManuscript(self, manuscript_dir):
        return self.txt_manuscript.SetValue(manuscript_dir)

    def GetPlaceholders(self):
        return self.txt_placeholders.GetValue()

    def SetPlaceholders(self, dir):
        return self.txt_placeholders.SetValue(dir)

    def GetLogDialogs(self):
        return self.cbx_log_dialogs.GetValue()

    def SetLogDialogs(self, log_dialogs):
        self.cbx_log_dialogs.SetValue(log_dialogs)

    def GetDebug(self):
        return self.cbx_debug.GetValue()

    def SetDebug(self, debug):
        self.cbx_debug.SetValue(debug)

    def GetInspect(self):
        return self.cbx_inspect.GetValue()

    def SetInspect(self, inspect):
        self.cbx_inspect.SetValue(inspect)

    def GetDelay(self):
        return self.txt_delay.GetValue()

    def SetDelay(self, delay):
        self.txt_delay.SetValue(delay)

    def GetExit(self):
        return self.cbx_exit.GetValue()

    def SetExit(self, do_exit):
        self.cbx_exit.SetValue(do_exit)
