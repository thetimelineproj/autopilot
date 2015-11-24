# Copyright (C) 2009-2015 Contributors as noted in the AUTHORS file
#
# This file is part of autopilot.
#
# autopilot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# autopilot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with autopilot.  If not, see <http://www.gnu.org/licenses/>.

import sys
sys.path.append(r"c:\Users\roger\workspace\PyDev\autopilot\src")

import unittest
from lib.instructions.base.parser import parse
from lib.instructions.base.parser import InstructionSyntaxException


class describe_assert_closed_instruction(unittest.TestCase):

    def test_assert_closed_with_name_argument_is_ok(self):
        self.do_parse("assert closed ( Mydialog )")
        self.assertIsNotNone(self.instruction)

    def test_assert_closed_with_string_argument_is_ok(self):
        self.do_parse("assert closed ( 'Mydialog' )")
        self.assertIsNotNone(self.instruction)

    def test_assert_closed_with_alternate_name_argument_is_ok(self):
        self.do_parse("assert closed ( Mydialog|AnyDialog )")
        self.assertIsNotNone(self.instruction)

    def test_assert_closed_with_alternate_string_argument_is_ok(self):
        self.do_parse("assert closed ( 'Mydialog|AnyDialog' )")
        self.assertIsNotNone(self.instruction)

    def test_assert_closed_with_placeholder_argument_is_ok(self):
        self.do_parse("assert closed ( $Close$ )")
        self.assertIsNotNone(self.instruction)

    def test_assert_closed_with_invalid_or_argument_is_not_ok(self):
        self.assertRaises(InstructionSyntaxException,  parse, "assert closed(Mydialog|)")

    def test_assert_closed_with_too_few_arguments_is_not_ok(self):
        self.assertRaises(InstructionSyntaxException,  parse, "assert closed")

    def test_assert_closed_with_too_many_arguments_is_not_ok(self):
        self.assertRaises(InstructionSyntaxException,  parse, "assert closed(Mydialog, YourDialog)")

    def do_parse(self, text):
        self.instruction = parse(text)


class describe_assert_open_instruction(unittest.TestCase):

    def test_assert_open_with_name_argument_is_ok(self):
        self.do_parse("assert open ( Mydialog )")
        self.assertIsNotNone(self.instruction)

    def test_assert_open_with_string_argument_is_ok(self):
        self.do_parse("assert open ( 'Mydialog' )")
        self.assertIsNotNone(self.instruction)

    def test_assert_open_with_mixed_argument_is_ok(self):
        self.do_parse("assert open ( MyDialog | 'My Dialog' )")
        self.assertIsNotNone(self.instruction)

    def test_assert_open_with_alternate_name_argument_is_ok(self):
        self.do_parse("assert open ( Mydialog | YourDialog )")
        self.assertIsNotNone(self.instruction)

    def test_assert_open_with_alternate_string_argument_is_ok(self):
        self.do_parse("assert open ( 'Mydialog | YourDialog' )")
        self.assertIsNotNone(self.instruction)

    def test_assert_open_with_placeholder_argument_is_ok(self):
        self.do_parse("assert open ( $Close$ )")
        self.assertIsNotNone(self.instruction)

    def test_assert_open_with_invalid_or_argument_is_not_ok(self):
        self.assertRaises(InstructionSyntaxException,  parse, "assert closed(Mydialog | )")

    def test_assert_open_with_placeholder_argument_and_alternate_name_is_not_ok(self):
        self.assertRaises(InstructionSyntaxException,  parse, "assert closed($Mydialog$ | Xxxx)")

    def test_assert_open_with_too_few_arguments_is_not_ok(self):
        self.assertRaises(InstructionSyntaxException,  parse, "assert open")

    def test_assert_open_with_too_many_arguments_is_not_ok(self):
        self.assertRaises(InstructionSyntaxException,  parse, "assert open(Mydialog, YourDialog)")

    def do_parse(self, text):
        self.instruction = parse(text)


class describe_click_button_instruction(unittest.TestCase):

    def test_click_button_with_name_argument_is_ok(self):
        self.do_parse("click button ( OK )")
        self.assertIsNotNone(self.instruction)

    def test_click_button_with_numeric_argument_is_ok(self):
        self.do_parse("click button ( 5 )")
        self.assertIsNotNone(self.instruction)

    def test_click_button_with_string_argument_is_ok(self):
        self.do_parse('click button ( "Save as..." )')
        self.assertIsNotNone(self.instruction)

    def test_click_button_with_alternate_names_argument_is_ok(self):
        self.do_parse('click button ( Cancel|Avbryt )')
        self.assertIsNotNone(self.instruction)

    def test_click_button_with_mixed_alternate_names_argument_is_ok(self):
        self.do_parse('click button ( 2 | Cancel | "Avbryt" )')
        self.assertIsNotNone(self.instruction)

    def test_click_button_with_alternate_string_argument_is_ok(self):
        self.do_parse('click button ( "Save as...|Foo bar..." )')
        self.assertIsNotNone(self.instruction)

    def test_click_button_with_placeholder_argument_is_ok(self):
        self.do_parse('click button ( $Close$ )')
        self.assertIsNotNone(self.instruction)

    def test_click_button_with_missing_name_is_not_ok(self):
        self.assertRaises(InstructionSyntaxException,  parse, "click button ( | Close )")

    def test_click_button_with_missing_alternate_name_is_not_ok(self):
        self.assertRaises(InstructionSyntaxException,  parse, "click button (Close | )")

    def test_click_button_with_placeholder_argument_and_alternative_name_is_not_ok(self):
        self.assertRaises(InstructionSyntaxException,  parse, "click button ($Close$ | Close)")

    def test_click_button_with_too_few_arguments_is_not_ok(self):
        self.assertRaises(InstructionSyntaxException,  parse, "click button ()")

    def test_click_button_with_too_many_arguments_is_not_ok(self):
        self.assertRaises(InstructionSyntaxException,  parse, "click button (a,b)")

    def do_parse(self, text):
        self.instruction = parse(text)


class describe_click_checkbox_instruction(unittest.TestCase):

    def test_click_checkbox_by_pos_is_ok(self):
        self.do_parse("click checkbox ( 1 )")
        self.assertIsNotNone(self.instruction)

    def test_click_checkbox_with_alternative_target_name_by_pos_is_ok(self):
        self.do_parse("click cbx ( 1 )")
        self.assertIsNotNone(self.instruction)

    def test_click_checkbox_by_name_is_ok(self):
        self.do_parse("click checkbox ( mycheckbox )")
        self.assertIsNotNone(self.instruction)

    def test_click_checkbox_by_placeholder_is_ok(self):
        self.do_parse('click checkbox ( $Close$ )')
        self.assertIsNotNone(self.instruction)

    def test_click_checkbox_by_namelist_is_ok(self):
        self.do_parse("click checkbox ( my_checkbox|mon_checkbox|anothercheckbox )")
        self.assertIsNotNone(self.instruction)

    def test_click_checkbox_by_mixed_namelist_is_ok(self):
        self.do_parse("click checkbox ( my_checkbox|'mon_checkbox'|2 )")
        self.assertIsNotNone(self.instruction)

    def test_click_checkbox_with_wrong_number_of_tokens_fails(self):
        self.assertRaises(InstructionSyntaxException,  parse, "click checkbox")

    def do_parse(self, text):
        self.instruction = parse(text)


class describe_click_mouse_instruction(unittest.TestCase):

    def test_click_mouse(self):
        self.do_parse('click mouse (1, 1)')
        self.assertIsNotNone(self.instruction)

    def test_click_mouse_with_ctrl_key_pressed(self):
        self.do_parse('click mouse (1, 1, ctrl)')
        self.assertIsNotNone(self.instruction)

    def test_click_mousex_with_too_few_arguments_is_not_ok(self):
        self.assertRaises(InstructionSyntaxException,  parse, "click mouse(1)")

    def test_click_mousex_with_too_many_arguments_is_not_ok(self):
        self.assertRaises(InstructionSyntaxException,  parse, "click mouse(1,2,3)")

    def do_parse(self, text):
        self.instruction = parse(text)


class describe_close_dialog_instruction(unittest.TestCase):

    def test_close_dialog_without_argument_is_ok(self):
        self.do_parse('close dialog')
        self.assertIsNotNone(self.instruction)

    def test_close_dialog_with_empty_argument_list_is_ok(self):
        self.do_parse('close dialog')
        self.assertIsNotNone(self.instruction)

    def test_close_dialog_with_name_argument_is_ok(self):
        self.do_parse('close dialog(FooBar)')
        self.assertIsNotNone(self.instruction)

    def test_close_dialog_withs_placeholder_is_ok(self):
        self.do_parse('close dialog ( $Close$ )')
        self.assertIsNotNone(self.instruction)

    def test_close_dialog_with_wrong_nbr_of_tokens_is_not_oks(self):
        self.assertRaises(InstructionSyntaxException,  self.do_parse, "close dialog(")

    def do_parse(self, text):
        self.instruction = parse(text)


class describe_enter_text_instruction(unittest.TestCase):

    def test_enter_text_by_pos_is_ok(self):
        self.do_parse("enter text ( 1, Haha )")
        self.assertIsNotNone(self.instruction)

    def test_enter_text_with_alternative_target_name_by_pos_is_ok(self):
        self.do_parse("enter txt ( 1, Haha )")
        self.assertIsNotNone(self.instruction)

    def test_enter_text_with_pos_and_target_by_string_is_ok(self):
        self.do_parse("enter text ( 1, 'Ha ha' )")
        self.assertIsNotNone(self.instruction)

    def test_enter_text_with_name_is_ok(self):
        self.do_parse("enter text ( mytextbox, Haha )")
        self.assertIsNotNone(self.instruction)

    def test_enter_text_with_placeholder_is_ok(self):
        self.do_parse('enter text ( $Close$, "ha ha" )')
        self.assertIsNotNone(self.instruction)

    def test_enter_text_with_namelist_is_ok(self):
        self.do_parse("enter text ( my_textbox|mon_textbox|anothertextbox, 'textbox text' )")
        self.assertIsNotNone(self.instruction)

    def test_enter_text_by_mixed_namelist_is_ok(self):
        self.do_parse("enter text ( my_textbox|'mon_textbox'|2, 'textbox text' )")
        self.assertIsNotNone(self.instruction)

    def test_enter_text_with_wrong_number_of_tokens_fails(self):
        self.assertRaises(InstructionSyntaxException,  self.do_parse, "enter text (1)")

    def test_single_quoted_string(self):
        instruction = parse("enter text(1, 'Roger')")
        self.assertEquals("enter text(1,'Roger')", "%s" % instruction)

    def test_enter_text_with_too_few_arguments_is_not_ok(self):
        self.assertRaises(InstructionSyntaxException,  parse, "exnter text")

    def test_enter_text_with_too_many_arguments_is_not_ok(self):
        self.assertRaises(InstructionSyntaxException,  parse, "asenter text(Mydialog, YourDialog)")

    def do_parse(self, text):
        self.instruction = parse(text)


class describe_exit_instruction(unittest.TestCase):

    def test_exit_instruction_is_ok(self):
        self.do_parse("exit application")
        self.assertIsNotNone(self.instruction)

    def test_exit_instruction_with_alternative_name_is_ok(self):
        self.do_parse("exit app")
        self.assertIsNotNone(self.instruction)

    def test_exit_instruction_with_invalid_target_name_fails(self):
        self.assertRaises(InstructionSyntaxException,  parse, "exit foo")

    def test_exit_instruction_with_wrong_number_of_tokens_fails(self):
        self.assertRaises(InstructionSyntaxException,  parse, "exit app ()")

    def do_parse(self, text):
        self.instruction = parse(text)


class describe_select_combobox_instruction(unittest.TestCase):

    def test_select_combobox_by_pos_and_item_by_pos_is_ok(self):
        self.do_parse("select combobox ( 1, 1 )")
        self.assertIsNotNone(self.instruction)

    def test_select_combobox_with_alternative_target_name_by_pos_and_item_by_pos_is_ok(self):
        self.do_parse("select cobx ( 1, 1 )")
        self.assertIsNotNone(self.instruction)

    def test_select_combobox_by_pos_and_item_by_text_is_ok(self):
        self.do_parse("select combobox ( 1, comboboxitem )")
        self.assertIsNotNone(self.instruction)

    def test_select_combobox_by_pos_and_item_by_string_text_is_ok(self):
        self.do_parse("select combobox ( 1, 'combo box item' )")
        self.assertIsNotNone(self.instruction)

    def test_select_combobox_by_name_and_item_by_string_text_is_ok(self):
        self.do_parse("select combobox ( my_combobox, 'combo box item' )")
        self.assertIsNotNone(self.instruction)

    def test_select_combobox_by_placeholder_and_item_by_string_text_is_ok(self):
        self.do_parse("select combobox ( $Close$, 'combo box item' )")
        self.assertIsNotNone(self.instruction)

    def test_select_combobox_by_namelist_and_item_by_string_text_is_ok(self):
        self.do_parse("select combobox ( my_combobox|mycombobox|anothercombobox, 'combo box item' )")
        self.assertIsNotNone(self.instruction)

    def test_select_combobox_by_mixed_namelist_and_item_by_string_text_is_ok(self):
        self.do_parse("select combobox ( my_combobox|'mycombobox'|1, 'combo box item' )")
        self.assertIsNotNone(self.instruction)

    def test_select_combobox_with_wrong_number_of_tokens_fails(self):
        self.assertRaises(InstructionSyntaxException,  parse, "select combobox (1)")

    def do_parse(self, text):
        self.instruction = parse(text)


class describe_select_customtreecontrol_instruction(unittest.TestCase):

    def test_select_customtreecontrol_by_pos_and_item_by_pos_is_ok(self):
        self.do_parse("select customtreecontrol ( 1, 1 )")
        self.assertIsNotNone(self.instruction)

    def test_select_customtreecontrol_by_pos_and_item_by_text_is_ok(self):
        self.do_parse("select customtreecontrol ( 1, customtreecontrolitem )")
        self.assertIsNotNone(self.instruction)
 
    def test_select_customtreecontrol_by_pos_and_item_by_string_text_is_ok(self):
        self.do_parse("select customtreecontrol ( 1, 'custom tree item' )")
        self.assertIsNotNone(self.instruction)
 
    def test_select_customtreecontrol_by_name_and_item_by_string_text_is_ok(self):
        self.do_parse("select customtreecontrol ( my_combobox, 'combo box item' )")
        self.assertIsNotNone(self.instruction)
 
    def test_select_customtreecontrol_by_placeholder_and_item_by_string_text_is_ok(self):
        self.do_parse("select customtreecontrol ( $Close$, 'combo box item' )")
        self.assertIsNotNone(self.instruction)
 
    def test_select_customtreecontrol_by_namelist_and_item_by_string_text_is_ok(self):
        self.do_parse("select customtreecontrol ( my_customtreecontrol|mycustomtreecontrol|anothercustomtreecontrol, 'customtreecontrol item' )")
        self.assertIsNotNone(self.instruction)
 
    def test_select_customtreecontrol_by_mixed_namelist_and_item_by_string_text_is_ok(self):
        self.do_parse("select customtreecontrol ( my_customtreecontrol|'mycustomtreecontrol'|1, 'customtreecontrol box item' )")
        self.assertIsNotNone(self.instruction)
 
    def test_select_customtreecontrol_with_wrong_number_of_tokens_fails(self):
        self.assertRaises(InstructionSyntaxException,  parse, "select customtreecontrol (1)")

    def do_parse(self, text):
        self.instruction = parse(text)


class describe_select_listbox_instruction(unittest.TestCase):

    def test_select_listbox_by_pos_and_item_by_pos_is_ok(self):
        self.do_parse("select listbox ( 1, 1 )")
        self.assertIsNotNone(self.instruction)

    def test_select_listbox_with_alternative_target_name_by_pos_and_item_by_pos_is_ok(self):
        self.do_parse("select lbx ( 1, 1 )")
        self.assertIsNotNone(self.instruction)

    def test_select_listbox_with_pos_and_item_by_text_is_ok(self):
        self.do_parse("select listbox ( 1, listboxitem )")
        self.assertIsNotNone(self.instruction)

    def test_select_listbox_with_pos_and_item_by_string_text_is_ok(self):
        self.do_parse("select listbox ( 1, 'list box item' )")
        self.assertIsNotNone(self.instruction)

    def test_select_listbox_with_name_and_item_by_string_text_is_ok(self):
        self.do_parse("select listbox ( my_listbox, 'list box item' )")
        self.assertIsNotNone(self.instruction)

    def test_select_listbox_with_placeholder_and_item_by_string_text_is_ok(self):
        self.do_parse("select listbox ( $Close$, 'list box item' )")
        self.assertIsNotNone(self.instruction)

    def test_select_listbox_with_namelist_and_item_by_string_text_is_ok(self):
        self.do_parse("select listbox ( my_listbox|mylistbox, 'list box item' )")
        self.assertIsNotNone(self.instruction)

    def test_select_listbox_with_wrong_number_of_tokens_fails(self):
        self.assertRaises(InstructionSyntaxException,  parse, "select listbox (1)")

    def do_parse(self, text):
        self.instruction = parse(text)


class describe_select_menu_instruction(unittest.TestCase):

    def test_select_menut_instruction_is_ok(self):
        self.do_parse("select menu ( File, Open )")
        self.assertIsNotNone(self.instruction)

    def test_select_menu_instruction_with_alternate_target_name_is_ok(self):
        self.do_parse("select mnu ( File, Open )")
        self.assertIsNotNone(self.instruction)

    def test_select_menu_instruction_with_placeholder_is_ok(self):
        self.do_parse("select mnu ( File, $Open$ )")
        self.assertIsNotNone(self.instruction)

    def test_select_menu_instruction_with_string_args_and_placeholder_is_ok(self):
        self.do_parse("select mnu ( 'File', $Open$ )")
        self.assertIsNotNone(self.instruction)

    def test_select_menu_instruction_with_placeholders_is_ok(self):
        self.do_parse("select mnu ( $Help$, $About$ )")
        self.assertIsNotNone(self.instruction)

    def do_parse(self, text):
        self.instruction = parse(text)


class describe_add_placeholder_instruction(unittest.TestCase):

    def test_add_placeholder_instruction_is_ok(self):
        self.do_parse("add placeholder ( About, 'About|Om' )")
        self.assertIsNotNone(self.instruction)

    def do_parse(self, text):
        self.instruction = parse(text)

class describe_change_tab_instruction(unittest.TestCase):

    def test_target_as_pos_is_ok(self):
        self.do_parse("change tab ( 1, 1 )")
        self.assertIsNotNone(self.instruction)

    def test_target_as_name_is_ok(self):
        self.do_parse("change tab ( notebook, 1 )")
        self.assertIsNotNone(self.instruction)

    def test_target_as_placeholder_is_ok(self):
        self.do_parse('change tab ( $notebook$, 1 )')
        self.assertIsNotNone(self.instruction)

    def test_target_as_string_is_ok(self):
        self.do_parse('change tab ( "notebook", 1 )')
        self.assertIsNotNone(self.instruction)

    def test_wrong_number_of_tokens_fails(self):
        self.assertRaises(InstructionSyntaxException,  self.do_parse, "change tab ( notebook, 1, 2 )")

    def do_parse(self, text):
        self.instruction = parse(text)


class describe_invalid_second_keyword_instructions(unittest.TestCase):

    def test_assert_with_invalid_second_keyword_fails(self):
        self.assertRaises(InstructionSyntaxException,  parse, "assert control open")

    def test_click_with_invalid_second_keyword_fails(self):
        self.assertRaises(InstructionSyntaxException,  parse, "click control (1)")

    def test_close_with_invalid_second_keyword_fails(self):
        self.assertRaises(InstructionSyntaxException,  parse, "close control (1)")

    def test_enter_with_invalid_second_keyword_fails(self):
        self.assertRaises(InstructionSyntaxException,  parse, "enter control (1)")

    def test_exit_with_invalid_second_keyword_fails(self):
        self.assertRaises(InstructionSyntaxException,  parse, "exit control")

    def test_select_with_invalid_second_keyword_fails(self):
        self.assertRaises(InstructionSyntaxException,  parse, "select control (1)")

    def do_parse(self, text):
        self.instruction = parse(text)


class describe_invalid_first_keyword_instructions(unittest.TestCase):

    def test_assert_with_invalid_second_keyword_fails(self):
        self.assertRaises(InstructionSyntaxException,  parse, "menu control open")

    def do_parse(self, text):
        self.instruction = parse(text)


if __name__ == '__main__':
    unittest.main()
