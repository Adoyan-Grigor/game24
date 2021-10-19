#!usr/bin/python3
'''test main "gameconsole"'''
import builtins
import readline
import sys

import mock

import pytest


from game24.game import Hand
from game24 import gameconsole as gc
from game24 import hhelp as hl


MSG_SELECT = gc.MSG_SELECT
INPUT_EOF = gc.INPUT_EOF


gc.GameConsole.new_hand = hl.MockGame_1.new_hand
gc.GameConsole.raw_input_ex = hl.GGameConsole.raw_input_ex


@pytest.mark.parametrize('test', [(1), (2), (3)])
def test_main_1(test, capsys):
    """test of the 'main' function"""
    if test == 1:
        answers = (i for i in ('1', 's', '12 + 12 + 12 - 12',
                               't', '12 + 12 * 12 / 12', 'n',
                               'n', 'h', 'n', 's', 'n', 'h',
                               '6 + 6 + 6 + 6', 'n', 's', 's',
                               's', '2 + 2 + 2 + 2', 's',
                               '12 + 12 + 12 - 12', 'n', 'q'))
        testargs = ['']
        with mock.patch.object(sys, 'argv', testargs):
            with mock.patch.object(builtins, 'input', lambda _: next(answers)):
                with pytest.raises(SystemExit):
                    gc.main()
            out, err = capsys.readouterr()
        assert '''Total 5 hands solved
Total 1 hands solved with hint
Total 7 hands failed to solve''' in out, err
    elif test == 2:
        answers = (i for i in ('2', '12 12 12',
                               '12 12 12 12', '2',
                               '2 2 2 2', '2',
                               '5 5 5 5', 'q'))
        testargs = ['']
        with mock.patch.object(sys, 'argv', testargs):
            with mock.patch.object(builtins, 'input', lambda _: next(answers)):
                with pytest.raises(SystemExit):
                    gc.main()
            out, err = capsys.readouterr()
            check_list = ['Invalid input!', """12 + 12 + 12 - 12
12 × (12 + 12) ÷ 12
12 + 12 × 12 ÷ 12""", """Seems no solutions""", """
5 × 5 - 5 ÷ 5"""]
            for check in check_list:
                assert check in out
    elif test == 3:
        answers = (i for i in ('1', 's', '12 + 12 + 12 - 12', 'q'))
        testargs = ['']
        with mock.patch.object(sys, 'argv', testargs):
            with mock.patch.object(builtins, 'input', lambda _: next(answers)):
                with pytest.raises(SystemExit):
                    gc.main()
            out, err = capsys.readouterr()
        assert """1. Try other solutions (t)
2. Next hand (n)
3. Show me the answers (s)
4. Quit the game (q)""" in out


@pytest.mark.xfail
@pytest.mark.parametrize('test', [(1), (2), (3)])
def test_main_2(test, capsys):
    """test of the 'main' function"""
    if test == 1:
        answers = (i for i in ('1', 's'))
        testargs = ['']
        with mock.patch.object(sys, 'argv', testargs):
            with mock.patch.object(builtins, 'input', lambda _: next(answers)):
                with pytest.raises(SystemExit):
                    gc.main()
            out, err = capsys.readouterr()
        assert 'Seems no solutions' in out, err
    elif test == 2:
        answers = (i for i in ('1', 's', '12 + 12 + 12 - 12',
                               '3', 'q'))
        testargs = ['']
        with mock.patch.object(sys, 'argv', testargs):
            with mock.patch.object(builtins, 'input', lambda _: next(answers)):
                with pytest.raises(SystemExit):
                    gc.main()
            out, err = capsys.readouterr()
        assert """12 + 12 + 12 - 12
12 × (12 + 12) ÷ 12
12 + 12 × 12 ÷ 12""" in out
    elif test == 3:
        answers = (i for i in ('1', 's', 's', 's',
                               '4 + 4 + 4 + 4 + 4 + 4'))
        testargs = ['']
        with mock.patch.object(sys, 'argv', testargs):
            with mock.patch.object(builtins, 'input', lambda _: next(answers)):
                with pytest.raises(SystemExit):
                    gc.main()
            out, err = capsys.readouterr()
            assert 'Good Jon' in out
