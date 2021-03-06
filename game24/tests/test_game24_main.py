'''test_game24_main'''
import pytest


from game24 import gameconsole as gc
from game24.tests import hhelp as hl


testargs = ['']


def test_main_1(capsys):
    """checking the 'main' function when the user launches the game"""
    assert '''Total 5 hands solved
Total 1 hands solved with hint
Total 7 hands failed to solve''' in hl.test_help_main_1(capsys)


def test_main_2(capsys):
    """checking the 'main' function, when the user wants
       to use the 'ui_check_answer' function"""
    check_list = ['Invalid input!', """12 + 12 + 12 - 12
12 × (12 + 12) ÷ 12
12 + 12 × 12 ÷ 12""", "Seems no solutions", """
5 × 5 - 5 ÷ 5"""]
    for check in check_list:
        assert check in hl.test_help_main_2(capsys)


def test_main_3(capsys):
    """checking the 'main' function, when the user skips an
       equation that has no solution and exits the program"""
    assert 'Seems no solutions' in hl.test_help_main_3(capsys)


def test_main_4(capsys):
    """checking the 'main' function, when the user gives the correct answer,
       skips the task, gives the wrong answer and exits"""
    assert """12 + 12 + 12 - 12
12 × (12 + 12) ÷ 12
12 + 12 × 12 ÷ 12""" in hl.test_help_main_4(capsys)


def test_main_5(capsys):
    """checking the 'main' function when the user starts the game and correctly
       solves the equation but using more numbers than allowed"""
    assert gc.MSG_MENU_PLAY_RIGHT not in hl.test_help_main_5(capsys)


def test_main_6(capsys):
    """checking the 'main' function, when the user starts the
       game, gives an empty stchecking the 'main' function when the user types
       capital letters from allowed charactersring and exits"""
    assert gc.MSG_INVALID_INPUT in hl.test_help_main_6(capsys)


@pytest.mark.parametrize('test', [('P'), ('C'), ('Q')])
def test_main_7(capsys, test):
    """checking the 'main' function when the user types
       capital letters from allowed characters"""
    assert gc.MSG_INVALID_INPUT in hl.test_help_main_7(capsys, test)


def test_main_8(capsys):
    """checking the 'main' function when the user starts
       the game, enters a blank line and exits"""
    assert gc.MSG_INVALID_INPUT in hl.test_help_main_8(capsys)


@pytest.mark.parametrize('test', [('12 + 12 + 12 + 12'),
                                  ('12 - 12 - 12 + 12'),
                                  ('12 * 12 - 12 * 12')])
def test_main_9(capsys, test):
    """checking the 'main' function when the user starts the
       game first gives an incorrect answer, then he gives a
       correct answer and exits"""
    assert gc.MSG_PLAY_WRONG in hl.test_help_main_9(capsys, test)


def test_main_10(capsys):
    """checking the 'main' function, when the user starts
       the game, gives the wrong answer several times and exits"""
    assert gc.MSG_MENU_PLAY_RIGHT not in hl.test_help_main_10(capsys)


@pytest.mark.parametrize('test', [('a'), ('A'), ('Aa'), ('aA'), (','),
                                  ('./,'), ('agsg'), ('SGRH'), ('sAfsW'),
                                  ('AfsfAsf'), ('1s2sf24'),
                                  ('124fs'), ('asd1')])
def test_main_11(capsys, test):
    """checking the 'main' function when the user gives unauthorized input"""
    check = 'Invalid character: ' + hl.help_letters_and_numbers(test)
    assert check in hl.test_help_main_11_12(capsys, test)


@pytest.mark.parametrize('test', [('6'), ('7'), ('12'),
                                  ('21'), ('12345'), ('3536')])
def test_main_12(capsys, test):
    """checking the 'main' function when the user gives unauthorized input"""
    check = 'Invalid expression: operator missed'
    assert check in hl.test_help_main_11_12(capsys, test)


@pytest.mark.parametrize('test', [('4'), ('5'), ('dasf'),
                                  ('ASD'), ('1p'), ('2c'),
                                  ('3q'), ('65x')])
def test_main_13(capsys, test):
    """checking the "main" function when the user
       gives an unauthorized input in the main menu"""
    check = 'Invalid input!'
    assert check in hl.test_help_main_13(capsys, test)


def test_main_14(capsys):
    """checking the 'main' function, when the user starts the game,
    skips the task, solves the equation correctly, fails to solve
    the same equation again, asks for help, solves the equation
    correctly, skips the remaining tasks and exits the game"""
    check = """Total 0 hands solved
Total 1 hands solved with hint
Total 12 hands failed to solve"""
    assert check in hl.test_help_main_14(capsys)
