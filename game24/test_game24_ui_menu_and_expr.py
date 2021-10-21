"""test_game24_ui_menu_and_expr"""
import pytest


from game24 import calc
from game24.hhelp import TestUiMenuAndExpr as hl
from game24 import hhelp


MENU = '''1. Definitely no solutions (n)\n2. Give me a hint (h)
3. I gave up, show me the answer (s)
4. Back to the main menu (b)
5. Quit the game (q)'''
CHOICES = '1n2h3s4b5q'


@pytest.mark.parametrize('test', [('12 + 12 + 12 - 12'),
                                  ('(12 + 12) / 12 * 12'),
                                  ('12 * 12 / 12 + 12')])
def test_ui_menu_and_expr_1(test):
    """checking the function 'ui_emnu_and_expr' when we give an
       equation that consists of the allowed numbers"""
    assert hl.test_help_ui_menu_and_expr_1(test,
                                           MENU, CHOICES) == calc.parse(test)


@pytest.mark.parametrize('test', [('1'), ('n'), ('2'), ('h'), ('3'), ('s'),
                                  ('4'), ('b'), ('5'), ('q')])
def test_ui_menu_and_expr_2(test):
    """checking the ui_emnu_and_expr function when
       we give characters from 'choices'"""
    assert hl.test_help_ui_menu_and_expr_2(test,
                                           MENU, CHOICES) == test


@pytest.mark.parametrize('test', [('12 - 12 + 12 + 12 - 12 + 12'),
                                  ('12 + 12 * 12 / 12 + 12 - 12'),
                                  ('12 + 12 + 12 + 12 - 12 - 12')])
def test_ui_menu_and_expr_negative_1(test):
    """checking the function 'ui_emnu_and_expr' when the program gets
       the correct equation, but more numbers are used than allowed"""
    check = hl.test_help_ui_menu_and_expr_negative_1(test, MENU, CHOICES)
    assert check == calc.parse(test)


@pytest.mark.parametrize('test', [('a'), ('A'), ('aA'),
                                  ('ggs'), ('AFAW'), ('ASffdS'),
                                  ('8s'), ('8S'), ('4dsf'),
                                  ('3FSE'), ('4GdsAd')])
def test_ui_menu_and_expr_negative_2(capsys, test):
    """checking the ui_emnu_and_expr function
       when we give unresolved characters"""
    check_symbol = 'Invalid character: ' + hhelp.help_letters_and_numbers(test)
    assert check_symbol in hl.test_help_ui_menu_and_expr_negative_2(capsys,
                                                                    test,
                                                                    MENU,
                                                                    CHOICES)


@pytest.mark.parametrize('test', [('6'), ('7'), ('67'), ('12'), ('12345')])
def test_ui_menu_and_expr_negative_3(capsys, test):
    """checking the ui_emnu_and_expr function when
       we give numbers not from 'choices'"""
    check = hl.test_help_ui_menu_and_expr_negative_3(capsys,
                                                     test,
                                                     MENU,
                                                     CHOICES)
    assert 'Invalid expression: operator missed' in check


@pytest.mark.xfail
def test_ui_menu_and_expr_negative_4(capsys):
    """if you give 'ui_menu_and_expr' an empty string"""
    check = hl.test_help_ui_menu_and_expr_negative_4(capsys, MENU, CHOICES)
    assert """Invalid expression: operator missed
""" in check or 'Invalid character:' in check


@pytest.mark.xfail
@pytest.mark.parametrize('test', [('1n'), ('n2'), ('2h'), ('h3'),
                                  ('3s'), ('s4'), ('4b'), ('b5'),
                                  ('5q'), ('1n2h3s4b5q')])
def test_ui_menu_and_expr_negative_5(capsys, test):
    """if you give ui_menu_and_expr invalid input but found in 'choices'"""
    check_symbol = 'Invalid character: ' + hhelp.help_letters_and_numbers(test)
    assert check_symbol in hl.test_help_ui_menu_and_expr_negative_5(capsys,
                                                                    test,
                                                                    MENU,
                                                                    CHOICES)


@pytest.mark.xfail
@pytest.mark.parametrize('test', [('N'), ('H'), ('S'), ('B'), ('Q')])
def test_ui_menu_and_expr_negative_6(capsys, test):
    """checking the 'ui_menu_and_expr' function when the
       program receives large letters of allowed characters"""
    check = 'Invalid character: ' + test
    assert check in hl.test_help_ui_menu_and_expr_negative_6(capsys,
                                                             test,
                                                             MENU,
                                                             CHOICES)
