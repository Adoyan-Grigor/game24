#!usr/bin/python3
'''test_game24_main'''
import pytest


from game24 import gameconsole as gc
from game24 import hhelp as hl


MSG_SELECT = gc.MSG_SELECT
INPUT_EOF = gc.INPUT_EOF
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
12 + 12 × 12 ÷ 12""", """Seems no solutions""", """
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


@pytest.mark.xfail
def test_main_5(capsys):
    """checking the 'main' function, when the user starts the
       game, gives an empty string and exits"""
    assert 'Invalid input!' in hl.test_help_main_5(capsys)


@pytest.mark.xfail
@pytest.mark.parametrize('test', [('P'), ('C'), ('Q')])
def test_main_6(capsys, test):
    """checking the 'main' function when the user types
       capital letters from allowed characters"""
    assert 'Invalid input!' in hl.test_help_main_6(capsys, test)
