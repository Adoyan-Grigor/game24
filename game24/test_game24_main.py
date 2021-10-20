#!usr/bin/python3
'''test main "gameconsole"'''
import builtins
import sys

import mock

import pytest


from game24 import gameconsole as gc
from game24 import hhelp as hl


MSG_SELECT = gc.MSG_SELECT
INPUT_EOF = gc.INPUT_EOF
testargs = ['']


gc.GameConsole.new_hand = hl.MockGame1.new_hand
gc.GameConsole.raw_input_ex = hl.GGameConsole.raw_input_ex


def test_main_1(capsys):
    """checking the 'main' function when the user launches the game"""
    answers = (i for i in ('1', 's', '12 + 12 + 12 - 12',
                           't', '12 + 12 * 12 / 12', 'n',
                           'n', 'h', 'n', 's', 'n', 'h',
                           '6 + 6 + 6 + 6', 'n', 's', 's',
                           's', '2 + 2 + 2 + 2', 's',
                           '12 + 12 + 12 - 12', 'n', 'q'))
    with mock.patch.object(sys, 'argv', testargs):
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                gc.main()
        out, err = capsys.readouterr()
        print(err)
    assert '''Total 5 hands solved
Total 1 hands solved with hint
Total 7 hands failed to solve''' in out


def test_main_2(capsys):
    """checking the 'main' function, when the user wants
       to use the 'ui_check_answer' function"""
    answers = (i for i in ('2', '12 12 12',
                           '12 12 12 12', '2',
                           '2 2 2 2', '2',
                           '5 5 5 5', 'q'))
    with mock.patch.object(sys, 'argv', testargs):
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                gc.main()
        out, err = capsys.readouterr()
        print(err)
        check_list = ['Invalid input!', """12 + 12 + 12 - 12
12 × (12 + 12) ÷ 12
12 + 12 × 12 ÷ 12""", """Seems no solutions""", """
5 × 5 - 5 ÷ 5"""]
        for check in check_list:
            assert check in out


def test_main_3(capsys):
    """checking the 'main' function, when the user skips an
       equation that has no solution and exits the program"""
    answers = (i for i in ('1', 's', 'q'))
    with mock.patch.object(sys, 'argv', testargs):
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                gc.main()
        out, err = capsys.readouterr()
        print(err)
    assert 'Seems no solutions' in out


def test_main_4(capsys):
    """checking the 'main' function, when the user gives the correct answer,
       skips the task, gives the wrong answer and exits"""
    answers = (i for i in ('1', 's', '12 + 12 + 12 - 12',
                           '3', 'q'))
    with mock.patch.object(sys, 'argv', testargs):
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                gc.main()
        out, err = capsys.readouterr()
        print(err)
    assert """12 + 12 + 12 - 12
12 × (12 + 12) ÷ 12
12 + 12 × 12 ÷ 12""" in out


@pytest.mark.xfail
def test_main_5(capsys):
    """checking the 'main' function, when the user starts the
       game, gives an empty string and exits"""
    answers = (i for i in ('1', '', 'q'))
    with mock.patch.object(sys, 'argv', testargs):
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            gc.main()
            out, err = capsys.readouterr()
            print(err)
            assert 'Invalid input!' in out


@pytest.mark.xfail
@pytest.mark.parametrize('test', [('P'), ('C'), ('Q')])
def test_main_6(capsys, test):
    """checking the 'main' function when the user types
       capital letters from allowed characters"""
    answers = (i for i in (test, 'q'))
    with mock.patch.object(sys, 'argv', testargs):
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                gc.main()
            out, err = capsys.readouterr()
            print(err)
            assert 'Invalid input!' in out
