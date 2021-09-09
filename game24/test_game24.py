#!usr/bin/python3
import pytest
import mock
import builtins
import sys
import random


from game24.gameconsole import GameConsole as gc
from game24.game import Game as gm
from game24.game import Hand
from game24 import hellp as hl
from . import calc


@pytest.mark.parametrize('title, result', 
                         [('12 + 12 + 12 - 12\n12 × (12 + 12) ÷ 12\n12 + 12 × 12 ÷ 12',
                         '\n12 + 12 + 12 - 12\n12 × (12 + 12) ÷ 12\n12 + 12 × 12 ÷ 12\n\n'),
                         ('4 × (1 + 2 + 3)\n1 × 2 × 3 × 4\n(1 + 3) × (2 + 4)',
                         '\n4 × (1 + 2 + 3)\n1 × 2 × 3 × 4\n(1 + 3) × (2 + 4)\n\n'),
                         ('Good Job', '\nGood Job\n\n')])
def test_print_title(capsys, title, result):
    gc.print_title(title)
    out, err = capsys.readouterr()
    assert out == result


@pytest.mark.parametrize('title, result', [(None, None), ('4 × (5 + 9 - 8)\n8 + 4 × (9 - 5)',
                         '4 × (5 + 9 - 8)\n8 + 4 × (9 - 5)')])
def test_print_title_negativie(capsys, title, result):
    gc.print_title(title)
    out, err = capsys.readouterr()
    assert out != result


@pytest.mark.xfail
@pytest.mark.parametrize('input_output', [('name'), ('HeLlO'), (''), ('12')])
def test_raw_input_ex(input_output):
    with mock.patch.object(builtins, 'input', lambda _: input_output):
       assert gc.raw_input_ex() == input_output
    

@pytest.mark.xfail
@pytest.mark.parametrize('r', [('1'), ('2'), ('3'), ('p'), ('c'), ('q')])
def test_ui_menu(r):
    menu = '1. Play (p)\n2. Check answer (c)\n3. Quit (q)'
    choices = '1p2c3q'
    with mock.patch.object(builtins, 'input', lambda _: r):
       assert gc.ui_menu(menu, choices, eof = True) == r


@pytest.mark.xfail 
@pytest.mark.parametrize('r, result', [('12 12 12 12', '\n12 + 12 + 12 - 12\n12 × (12 + 12) ÷ 12\n12 + 12 × 12 ÷ 12\n\n'),
                         ('1 2 4 6', '\n4 × 6 × (2 - 1)\n(2 + 6) × (4 - 1)\n\n'),
                         ('1 2 3 4', '\n4 × (1 + 2 + 3)\n1 × 2 × 3 × 4\n(1 + 3) × (2 + 4)\n\n')])
def test_ui_check_answer(capsys, r, result):
    with mock.patch.object(builtins, 'input', lambda _: r):
        gc().ui_check_answer()
        out, err = capsys.readouterr()
        assert out == result


@pytest.mark.xfail
@pytest.mark.parametrize('test', [(1), (2), (3), (4), (5), ('h'), ('s'), ('b'), ('q')])
def test_ui_menu_and_expr(capsys, test):
    menu = '1. Definitely no solutions (n)\n2. Give me a hint (h)\n3. I gave up, show me the answer (s)\n4. Back to the main menu (b)\n5. Quit the game (q)'
    choices = '1n2h3s4b5q'
    gg = gc()
    hand = gg.new_hand()
    hand_ints = hand.integers
    hand_ui_check = ''
    result = ''
    final_result = ''
    if test in range(1, 6):
        for i in hand_ints:
            hand_ui_check += str(i) + ' '
        with mock.patch.object(builtins, 'input', lambda _: hand_ui_check):
            gg.ui_check_answer()
            out, err = capsys.readouterr()
            if out != '\nSeems no solutions\n\n':
                for l in out:
                    if l == '×':
                        result += '*'
                    elif l == '÷':
                        result += '/'
                    else:
                        result += l
                for k in result[1: ]:
                    if k == '\n':
                        break
                    final_result += k
                with mock.patch.object(builtins, 'input', lambda _: final_result):
                    assert gg.ui_menu_and_expr(menu, choices, eof = True) == calc.parse(final_result)
            else:
                with mock.patch.object(builtins, 'input', lambda _: 'n'):
                    assert gg.ui_menu_and_expr(menu, choices, eof = True) == 'n'
    else:
        with mock.patch.object(builtins, 'input', lambda _: test):
            assert gg.ui_menu_and_expr(menu, choices, eof = True) == test


@pytest.mark.parametrize('test', [(1), (2), (3), (4), (5)])
def test_print_result(capsys, test):
    gg = gc()
    hand = gg.new_hand()
    solved = 0
    failed = 0
    hinted = 0
    if hand.result == 's':
        solved += 1
    elif hand.result == 'h':
        hinted += 1
    elif hand.result == 'f':
        failed += 1
    gg.print_result()
    out, err = capsys.readouterr()
    assert out == '\nTotal %d hands solved' % solved + '\nTotal %d hands solved with hint' % hinted + '\nTotal %d hands failed to solve' % failed + '\n\n'



@pytest.mark.xfail
def test_play(capsys):
    class MockGame(gc, Hand):
        def new_hand(self):
            if self.is_set_end():
                return None

            cards = []
            self.cards = hl.hellp_new_hand_cards(self.cards)
            for i in range(self.count):
                idx = random.randint(0, len(self.cards) - 1)
                cards.append(self.cards.pop(idx))
            self.hand = Hand(cards, target=self.target)
            self.hands.append(self.hand)
            return self.hand


    gg = MockGame()
    gg.new_hand()
    sc = ' '.join([str(i) for i in gg.hand.integers])
    r = hl.hellp_ui_check_answer(capsys, sc) 
    answers = (i for i in (r, 'n', r, 'n', 's', 'n', r, 'n', r, 'n', 'h', r, 'n', r, 'n', r, 'n', r, 'n', r, 'n', r, 'n', r, 'b', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        assert gg.play() == None
