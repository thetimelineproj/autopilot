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


import lib.instructions.base.scanner as scanner
from lib.instructions.base.scanner import scan
from lib.instructions.userinstructions.clickbutton import ClickButtonInstruction
from lib.instructions.userinstructions.clickcheckbox import ClickCheckboxInstruction
from lib.instructions.userinstructions.closedialog import CloseDialogInstruction
from lib.instructions.userinstructions.entertext import EnterTextInstruction
from lib.instructions.userinstructions.assertopen import AssertOpenInstruction
from lib.instructions.userinstructions.assertclosed import AssertClosedInstruction
from lib.instructions.userinstructions.asserttext import AssertTextInstruction
from lib.instructions.userinstructions.exit import ExitInstruction
from lib.instructions.userinstructions.selectmenu import SelectMenuInstruction
from lib.instructions.userinstructions.clickmouse import ClickMouseInstruction
from lib.instructions.userinstructions.selectlistbox import SelectListBoxInstruction
from lib.instructions.userinstructions.selectcombobox import SelectComboBoxInstruction
from lib.instructions.userinstructions.selectcustomtreecontrol import SelectCustomTreeControlInstruction
from lib.instructions.userinstructions.addplaceholder import AddPlaceholderInstruction
from lib.reporting.logger import Logger
from lib.app.exceptions import InstructionSyntaxException


def parse(instruction_line):
    tokens = scan(instruction_line)

    CMD_PARSERS = {scanner.ID_ASSERT: parse_assert,
                   scanner.ID_CLICK: parse_click,
                   scanner.ID_CLOSE: parse_close,
                   scanner.ID_ENTER: parse_enter,
                   scanner.ID_EXIT: parse_exit,
                   scanner.ID_SELECT: parse_select,
                   scanner.ID_ADD: parse_add,
                   }

    if len(tokens) == 0:
        raise InstructionSyntaxException("Empty instruction")

    if tokens[0].id != scanner.KEYWORD:
        raise InstructionSyntaxException(tokens[0].lexeme)

    if (tokens[0].subid in CMD_PARSERS):
        return CMD_PARSERS[tokens[0].subid](instruction_line, tokens)
    else:
        raise InstructionSyntaxException(tokens[0].lexeme)


def AssertThatInstructionSyntaxExceptionIsRaised(f):
    def wrap(instruction_line, tokens):
        try:
            rv = f(instruction_line, tokens)
            if rv is None:
                raise InstructionSyntaxException("")
            else:
                return rv
        except InstructionSyntaxException:
            Logger.add_error("Invalid instruction: '%s'. Instruction ignored" % instruction_line)
            raise
    return wrap


def create_instruction(CMDS, tokens):
    SYNTAX_CHECKERS = {AssertOpenInstruction: syntaxcheck_assert_open_instruction,
                       AssertClosedInstruction: syntaxcheck_assert_closed_instruction,
                       AssertTextInstruction: syntaxcheck_assert_text_instruction,
                       ClickButtonInstruction: syntaxcheck_click_button_instruction,
                       ClickCheckboxInstruction: syntaxcheck_click_checkbox_instruction,
                       ClickMouseInstruction: syntaxcheck_click_mouse_instruction,
                       CloseDialogInstruction: syntaxcheck_close_dialog_instruction,
                       EnterTextInstruction: syntaxcheck_enter_text_instruction,
                       ExitInstruction: syntaxcheck_exit_instruction,
                       SelectMenuInstruction: syntaxcheck_select_menu_instruction,
                       SelectListBoxInstruction: syntaxcheck_select_listbox_instruction,
                       SelectComboBoxInstruction: syntaxcheck_select_combobox_instruction,
                       SelectCustomTreeControlInstruction: syntaxcheck_select_customtreecontrol_instruction,
                       AddPlaceholderInstruction: syntaxcheck_add_placeholder_instruction,
                       }
    if tokens[1].lexeme in CMDS:
        instruction = CMDS[tokens[1].lexeme]
        SYNTAX_CHECKERS[instruction](tokens)
        return instruction(tokens)


@AssertThatInstructionSyntaxExceptionIsRaised
def parse_assert(instruction_line, tokens):
    CMDS = {"open": AssertOpenInstruction,
            "closed": AssertClosedInstruction,
            "text": AssertTextInstruction}
    return create_instruction(CMDS, tokens)


@AssertThatInstructionSyntaxExceptionIsRaised
def parse_click(instruction_line, tokens):
    CMDS = {"button": ClickButtonInstruction, "checkbox": ClickCheckboxInstruction, "mouse":  ClickMouseInstruction}
    return create_instruction(CMDS, tokens)


@AssertThatInstructionSyntaxExceptionIsRaised
def parse_close(instruction_line, tokens):
    CMDS = {"dialog": CloseDialogInstruction, }
    return create_instruction(CMDS, tokens)


@AssertThatInstructionSyntaxExceptionIsRaised
def parse_enter(instruction_line, tokens):
    CMDS = {"text": EnterTextInstruction, }
    return create_instruction(CMDS, tokens)


@AssertThatInstructionSyntaxExceptionIsRaised
def parse_exit(instruction_line, tokens):
    CMDS = {"application": ExitInstruction, }
    return create_instruction(CMDS, tokens)


@AssertThatInstructionSyntaxExceptionIsRaised
def parse_select(instruction_line, tokens):
    CMDS = {"menu": SelectMenuInstruction, "listbox": SelectListBoxInstruction, "combobox": SelectComboBoxInstruction,
            "customtreecontrol": SelectCustomTreeControlInstruction}
    return create_instruction(CMDS, tokens)


@AssertThatInstructionSyntaxExceptionIsRaised
def parse_add(instruction_line, tokens):
    CMDS = {"placeholder": AddPlaceholderInstruction, }
    return create_instruction(CMDS, tokens)


def syntaxcheck_add_placeholder_instruction(tokens):
    """
    State   token-id           token-subid        Next State
    -----   ------------------ ------------------ ----------
    """
    STATES = (
      (0,   scanner.KEYWORD,     scanner.ID_ADD,  1),
      (1,   scanner.KEYWORD,     scanner.ID_PLACEHOLDER, 2),
      (2,   scanner.LP,          None,               3),
      (3,   scanner.STRING,      None,               4),
      (3,   scanner.ID,          None,               4),
      (4,   scanner.COMMA,       None,               5),
      (5,   scanner.STRING,      None,               6),
      (6,   scanner.RP,          None,              -1),
    )
    validate(tokens, STATES)


def syntaxcheck_assert_closed_instruction(tokens):
    """
    State   token-id           token-subid        Next State
    -----   ------------------ ------------------ ----------
    """
    STATES = (
      (0,   scanner.KEYWORD,     scanner.ID_ASSERT,  1),
      (1,   scanner.KEYWORD,     scanner.ID_CLOSED,  2),
      (2,   scanner.LP,          None,               3),
      (3,   scanner.ID,          None,               4),
      (3,   scanner.STRING,      None,               4),
      (3,   scanner.KEYWORD,     None,               4),
      (3,   scanner.PLACEHOLDER, None,               5),
      (4,   scanner.OR,          None,               3),
      (4,   scanner.RP,          None,              -1),
      (5,   scanner.RP,          None,              -1),
    )
    validate(tokens, STATES)


def syntaxcheck_assert_text_instruction(tokens):
    """
    State   token-id           token-subid        Next State
    -----   ------------------ ------------------ ----------
    """
    STATES = (
      (0,   scanner.KEYWORD,     scanner.ID_ASSERT,  1),
      (1,   scanner.KEYWORD,     scanner.ID_TEXT,    2),
      (2,   scanner.LP,          None,               3),
      (3,   scanner.NUM,         None,               4),
      (3,   scanner.STRING,      None,               4),
      (3,   scanner.ID,          None,               4),
      (3,   scanner.PLACEHOLDER, None,               4),
      (4,   scanner.COMMA,       None,               5),
      (4,   scanner.OR,          None,               7),
      (5,   scanner.ID,          None,               6),
      (5,   scanner.STRING,      None,               6),
      (6,   scanner.RP,          None,              -1),
      (7,   scanner.NUM,         None,               4),
      (7,   scanner.STRING,      None,               4),
      (7,   scanner.ID,          None,               4),
      (8,   scanner.COMMA,       None,               5),
    )
    if len(tokens) < 7:
        raise InstructionSyntaxException("Wrong number of tokens")
    validate(tokens, STATES)


def syntaxcheck_assert_open_instruction(tokens):
    """
    State   token-id           token-subid        Next State
    -----   ------------------ ------------------ ----------
    """
    STATES = (
      (0,   scanner.KEYWORD,     scanner.ID_ASSERT,  1),
      (1,   scanner.KEYWORD,     scanner.ID_OPEN,    2),
      (2,   scanner.LP,          None,               3),
      (3,   scanner.ID,          None,               4),
      (3,   scanner.STRING,      None,               4),
      (3,   scanner.KEYWORD,     None,               4),
      (3,   scanner.PLACEHOLDER, None,               5),
      (4,   scanner.OR,          None,               3),
      (4,   scanner.RP,          None,              -1),
      (5,   scanner.RP,          None,              -1),
    )
    validate(tokens, STATES)


def syntaxcheck_click_button_instruction(tokens):
    """
    State   token-id           token-subid        Next State
    -----   ------------------ ------------------ ----------
    """
    STATES = (
      (0,   scanner.KEYWORD,     scanner.ID_CLICK,   1),
      (1,   scanner.KEYWORD,     scanner.ID_BUTTON,  2),
      (2,   scanner.LP,          None,               3),
      (3,   scanner.NUM,         None,               4),
      (3,   scanner.PLACEHOLDER, None,               5),
      (3,   scanner.ID,          None,               4),
      (3,   scanner.STRING,      None,               4),
      (3,   scanner.KEYWORD,     None,               4),
      (4,   scanner.OR,          None,               3),
      (4,   scanner.RP,          None,              -1),
      (5,   scanner.RP,          None,              -1),
      (5,   scanner.RP,          None,              -1),
    )
    validate(tokens, STATES)


def syntaxcheck_click_checkbox_instruction(tokens):
    """
    State   token-id           token-subid        Next State
    -----   ------------------ ------------------ ----------
    """
    STATES = (
      (0,   scanner.KEYWORD,     scanner.ID_CLICK,    1),
      (1,   scanner.KEYWORD,     scanner.ID_CHECKBOX, 2),
      (2,   scanner.LP,          None,                3),
      (3,   scanner.NUM,         None,                4),
      (3,   scanner.ID,          None,                4),
      (3,   scanner.STRING,      None,                4),
      (3,   scanner.KEYWORD,     None,                4),
      (3,   scanner.PLACEHOLDER, None,                5),
      (4,   scanner.RP,          None,               -1),
      (4,   scanner.OR,          None,                3),
      (5,   scanner.RP,          None,               -1),
    )
    if len(tokens) < 5:
        raise InstructionSyntaxException("Wrong number of tokens")
    validate(tokens, STATES)


def syntaxcheck_click_mouse_instruction(tokens):
    """
    State   token-id           token-subid        Next State
    -----   ------------------ ------------------ ----------
    """
    STATES = (
      (0,   scanner.KEYWORD,   scanner.ID_CLICK,          1),
      (1,   scanner.KEYWORD,   scanner.ID_MOUSE,          2),
      (2,   scanner.LP,        None,                      3),
      (3,   scanner.NUM,       None,                      4),
      (4,   scanner.COMMA,     None,                      5),
      (5,   scanner.NUM,       None,                      6),
      (6,   scanner.COMMA,     None,                      7),
      (6,   scanner.RP,        None,                     -1),
      (7,   scanner.ID,        None,                      8),
      (8,   scanner.RP,        None,                     -1),
    )
    validate(tokens, STATES)


def syntaxcheck_close_application_instruction(tokens):
    """
    State   token-id           token-subid        Next State
    -----   ------------------ ------------------ ----------
    """
    STATES = (
      (0,   scanner.KEYWORD,   scanner.ID_CLOSE,   1),
      (1,   scanner.KEYWORD,   scanner.ID_APP,    -1),
    )
    validate(tokens, STATES)


def syntaxcheck_close_dialog_instruction(tokens):
    """
    State   token-id           token-subid        Next State
    -----   ------------------ ------------------ ----------
    """
    STATES_ALT = (
      (0,   scanner.KEYWORD,     scanner.ID_CLOSE,   1),
      (1,   scanner.KEYWORD,     scanner.ID_DIALOG, -1),
    )
    STATES = (
      (0,   scanner.KEYWORD,     scanner.ID_CLOSE,   1),
      (1,   scanner.KEYWORD,     scanner.ID_DIALOG,  2),
      (2,   scanner.LP,          None,               3),
      (3,   scanner.ID,          None,               4),
      (3,   scanner.STRING,      None,               4),
      (3,   scanner.PLACEHOLDER, None,               5),
      (3,   scanner.RP,          None,              -1),
      (4,   scanner.RP,          None,              -1),
      (4,   scanner.OR,          None,               3),
      (5,   scanner.RP,          None,              -1),
    )

    if len(tokens) != 2 and len(tokens) < 5:
        raise InstructionSyntaxException("Wrong number of tokens")
    if len(tokens) == 2:
        validate(tokens, STATES_ALT)
    else:
        validate(tokens, STATES)


def syntaxcheck_enter_text_instruction(tokens):
    """
    State   token-id           token-subid        Next State
    -----   ------------------ ------------------ ----------
    """
    STATES = (
      (0,   scanner.KEYWORD,     scanner.ID_ENTER,   1),
      (1,   scanner.KEYWORD,     scanner.ID_TEXT,    2),
      (2,   scanner.LP,          None,               3),
      (3,   scanner.NUM,         None,               4),
      (3,   scanner.STRING,      None,               4),
      (3,   scanner.ID,          None,               4),
      (3,   scanner.PLACEHOLDER, None,               4),
      (4,   scanner.COMMA,       None,               5),
      (4,   scanner.OR,          None,               7),
      (5,   scanner.ID,          None,               6),
      (5,   scanner.STRING,      None,               6),
      (6,   scanner.RP,          None,              -1),
      (7,   scanner.NUM,         None,               4),
      (7,   scanner.STRING,      None,               4),
      (7,   scanner.ID,          None,               4),
      (8,   scanner.COMMA,       None,               5),
    )
    if len(tokens) < 7:
        raise InstructionSyntaxException("Wrong number of tokens")
    validate(tokens, STATES)


def syntaxcheck_exit_instruction(tokens):
    """
    State   token-id           token-subid        Next State
    -----   ------------------ ------------------ ----------
    """
    STATES = (
        (0, scanner.KEYWORD, scanner.ID_EXIT, 1),
        (1, scanner.KEYWORD, scanner.ID_APP, -1),
    )
    if len(tokens) != 2:
        raise InstructionSyntaxException("Wrong number of tokens")
    validate(tokens, STATES)


def syntaxcheck_select_combobox_instruction(tokens):
    """
    State   token-id           token-subid        Next State
    -----   ------------------ ------------------ ----------
    """
    STATES = (
      (0,   scanner.KEYWORD,     scanner.ID_SELECT,    1),
      (1,   scanner.KEYWORD,     scanner.ID_COMBOBOX,  2),
      (2,   scanner.LP,          None,                 3),
      (3,   scanner.NUM,         None,                 4),
      (3,   scanner.STRING,      None,                 4),
      (3,   scanner.ID,          None,                 4),
      (3,   scanner.PLACEHOLDER, None,                 8),
      (4,   scanner.COMMA,       None,                 5),
      (4,   scanner.OR,          None,                 7),
      (5,   scanner.ID,          None,                 6),
      (5,   scanner.STRING,      None,                 6),
      (5,   scanner.NUM,         None,                 6),
      (6,   scanner.RP,          None,                -1),
      (7,   scanner.NUM,         None,                 4),
      (7,   scanner.STRING,      None,                 4),
      (7,   scanner.ID,          None,                 4),
      (8,   scanner.COMMA,       None,                 5),
    )
    validate(tokens, STATES)


def syntaxcheck_select_customtreecontrol_instruction(tokens):
    """
    State   token-id           token-subid        Next State
    -----   ------------------ ------------------ ----------
    """
    STATES = (
      (0,   scanner.KEYWORD,     scanner.ID_SELECT,    1),
      (1,   scanner.KEYWORD,     scanner.ID_CUSTOMTREECTRL,  2),
      (2,   scanner.LP,          None,                 3),
      (3,   scanner.NUM,         None,                 4),
      (3,   scanner.STRING,      None,                 4),
      (3,   scanner.ID,          None,                 4),
      (3,   scanner.PLACEHOLDER, None,                 8),
      (4,   scanner.COMMA,       None,                 5),
      (4,   scanner.OR,          None,                 7),
      (5,   scanner.ID,          None,                 6),
      (5,   scanner.STRING,      None,                 6),
      (5,   scanner.NUM,         None,                 6),
      (6,   scanner.RP,          None,                -1),
      (7,   scanner.NUM,         None,                 4),
      (7,   scanner.STRING,      None,                 4),
      (7,   scanner.ID,          None,                 4),
      (8,   scanner.COMMA,       None,                 5),
    )
    validate(tokens, STATES)


def syntaxcheck_select_listbox_instruction(tokens):
    """
    State   token-id           token-subid        Next State
    -----   ------------------ ------------------ ----------
    """
    STATES = (
      (0,   scanner.KEYWORD,     scanner.ID_SELECT,  1),
      (1,   scanner.KEYWORD,     scanner.ID_LISTBOX, 2),
      (2,   scanner.LP,          None,               3),
      (3,   scanner.NUM,         None,               4),
      (3,   scanner.STRING,      None,               4),
      (3,   scanner.ID,          None,               4),
      (3,   scanner.PLACEHOLDER, None,               8),
      (4,   scanner.COMMA,       None,               5),
      (4,   scanner.OR,          None,               7),
      (5,   scanner.ID,          None,               6),
      (5,   scanner.STRING,      None,               6),
      (5,   scanner.NUM,         None,               6),
      (6,   scanner.RP,          None,              -1),
      (7,   scanner.NUM,         None,               4),
      (7,   scanner.STRING,      None,               4),
      (7,   scanner.ID,          None,               4),
      (8,   scanner.COMMA,       None,               5),
    )
    validate(tokens, STATES)


def syntaxcheck_select_menu_instruction(tokens):
    """
    State   token-id           token-subid        Next State
    -----   ------------------ ------------------ ----------
    """
    STATES = (
      (0,   scanner.KEYWORD,     scanner.ID_SELECT, 1),
      (1,   scanner.KEYWORD,     scanner.ID_MENU,   2),
      (2,   scanner.LP,          None,              3),
      (3,   scanner.ID,          None,              4),
      (3,   scanner.STRING,      None,              4),
      (3,   scanner.PLACEHOLDER, None,              6),
      (4,   scanner.COMMA,       None,              3),
      (4,   scanner.OR,          None,              5),
      (4,   scanner.RP,          None,             -1),
      (5,   scanner.ID,          None,              4),
      (5,   scanner.STRING,      None,              4),
      (6,   scanner.COMMA,       None,              3),
      (6,   scanner.RP,          None,             -1),
    )
    validate(tokens, STATES)

###############################################################################S

def validate(tokens, states):
    try:
        state = 0
        i = 0
        while state != -1:
            state = next_state(state, states, tokens[i])
            i += 1
    except IndexError:
        raise InstructionSyntaxException("state=%d" % state)


def next_state(current_state, states, token):
    transitions = [state for state in states if state[0] == current_state]
    for state, token_id, subid, next_state in transitions:
        if token.id == token_id:
            if subid is None or subid == token.subid:
                return next_state
    raise InstructionSyntaxException("")
