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
import threading
from lib.app.pythonlauncher import run_python_file
from lib.reporting.logger import Logger
import lib.wrappers.dialog as dialog
import lib.wrappers.filedialog as filedialog
import lib.wrappers.dirdialog as dirdialog
import lib.wrappers.aboutbox as aboutbox
import lib.wrappers.colourdialog as colourdialog
import lib.wrappers.messagebox as messagebox
import lib.wrappers.messagedialog as messagedialog
import lib.wrappers.pagesetup as pagesetup
import lib.wrappers.printer as printer
import lib.wrappers.printpreview as printpreview
import lib.wrappers.fontdialog as fontdialog
import lib.wrappers.textentrydialog as textentrydialog
import lib.wrappers.passwordentrydialog as passwordentrydialog
import lib.wrappers.singlechoicedialog as singlechoicedialog
import lib.wrappers.multichoicedialog as multichoicedialog
import lib.wrappers.cubecolourdialog as cubecolourdialog
import lib.wrappers.frame as frame


instructions = None


def start_app(myinstructions, path):
    global instructions
    instructions = myinstructions
    Logger.bold_header("Starting application %s" % os.path.basename(path))
    wrap_wx_classes()
    run_python_file([path, ])


def wrap_wx_classes():
    """
    All wx-classes that we wan't to detect the construction of in the
    application under test, must be wrapped in a class of it's own.
    """
    dialog.Dialog.wrap(instructions.register_dialog)
    filedialog.FileDialog.wrap(instructions.register_dialog)
    dirdialog.DirDialog.wrap(instructions.register_dialog)
    aboutbox.AboutBox.wrap(instructions.register_dialog)
    colourdialog.ColourDialog.wrap(instructions.register_dialog)
    messagebox.wrap(instructions.register_dialog)
    messagedialog.MessageDialog.wrap(instructions.register_dialog)
    pagesetup.PageSetupDialog.wrap(instructions.register_dialog)
    printer.Printer.wrap(instructions.register_dialog)
    printpreview.PreviewFrame.wrap(instructions.register_dialog)
    fontdialog.FontDialog.wrap(instructions.register_dialog)
    textentrydialog.TextEntryDialog.wrap(instructions.register_dialog)
    passwordentrydialog.PasswordEntryDialog.wrap(instructions.register_dialog)
    singlechoicedialog.SingleChoiceDialog.wrap(instructions.register_dialog)
    multichoicedialog.MultiChoiceDialog.wrap(instructions.register_dialog)
    cubecolourdialog.CubeColourDialog.wrap(instructions.register_dialog)
    frame.Frame.wrap(instructions.register_dialog)