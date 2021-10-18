#!usr/bin/python3
'''test main "gameconsole"'''
import builtins
import readline
import sys

import mock

import pytest


from game24.game import Hand
from game24 import gameconsole as gc


GC = gc.GameConsole


class GGameConsole(GC):
    """Creating an analogue of the 'GameConsole' class
    with modified functions 'raw_input' and 'ui_menu'"""
    def __init__(self, target=24, count=4, face2ten=False, showcard=False):
        super(GC, self).__init__(target, count, face2ten)
        self.showcard = showcard

    def raw_input_ex(self, prompt='', default=''):
        '''enhance raw_input to support default input and also flat EOF'''
        try:
            readline.set_startup_hook(lambda: readline.insert_text(default))
            try:
                return input(prompt)
            finally:
                readline.set_startup_hook()

        except EOFError:
            input_eof = '\x00'
            return input_eof


GC = GGameConsole
MSG_SELECT = gc.MSG_SELECT
INPUT_EOF = gc.INPUT_EOF


class MockGame(GC, Hand):
    """Creating an analogue of the 'GameConsole'
    class with modified functions 'new_hand'"""
    def new_hand(self):
        """"modified function 'new_hand'"""
        if self.is_set_end():
            return None

        cards = []
        for i in range(self.count):
            print(i)
            idx = -1
            cards.append(self.cards.pop(idx))
        hand = Hand(cards, target=self.target)
        self.hands.append(hand)
        return hand


@pytest.mark.parametrize('test', [(1), (2), (3), (4), (5)])
def test_main(test, capsys):
    """test of the 'main' function"""
    gc.GameConsole.new_hand = MockGame.new_hand
    gc.GameConsole.raw_input_ex = GGameConsole.raw_input_ex
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
    elif test == 4:
        answers = (i for i in ('1', 's'))
        testargs = ['']
        with mock.patch.object(sys, 'argv', testargs):
            with mock.patch.object(builtins, 'input', lambda _: next(answers)):
                with pytest.raises(SystemExit):
                    gc.main()
            out, err = capsys.readouterr()
        assert 'Seems no solutions' in out
    elif test == 5:
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
