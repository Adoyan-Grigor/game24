#!usr/bin/python3
'''test file "gameconsole"'''
import pytest
import mock
import builtins
import sys
import random
import readline


from game24.gameconsole import *
from game24.game import Game as gm
from game24.game import Hand
from game24 import hellp as hl
from game24 import calc

gc = GameConsole


@pytest.mark.parametrize('title, result',
                         [('12 + 12 + 12 - 12\n12 × (12 + 12) ÷ 12\n12 + 12 × 12 ÷ 12',
                           '\n12 + 12 + 12 - 12\n12 × (12 + 12) ÷ 12\n12 + 12 × 12 ÷ 12\n\n'),
                          ('4 × (1 + 2 + 3)\n1 × 2 × 3 × 4\n(1 + 3) × (2 + 4)',
                           '\n4 × (1 + 2 + 3)\n1 × 2 × 3 × 4\n(1 + 3) × (2 + 4)\n\n'),
                          ('Good Job', '\nGood Job\n\n')])
def test_print_title(capsys, title, result):
    """test of the print_title function"""
    gc.print_title(title)
    out, err = capsys.readouterr()
    assert out == result


@pytest.mark.parametrize('title, result', [(None, None), ('4 × (5 + 9 - 8)\n8 + 4 × (9 - 5)',
                         '4 × (5 + 9 I- 8)\n8 + 4 × (9 - 5)')])
def test_print_title_negativie(capsys, title, result):
    """negative test of print_title function"""
    gc.print_title(title)
    out, err = capsys.readouterr()
    assert out != result


@pytest.mark.parametrize('input_output', [('name'), ('HeLlO'), (''), ('12')])
def test_raw_input_ex(input_output):
    """test of the 'raw_input_ex' function"""
    with mock.patch.object(builtins, 'input', lambda _: input_output):
        assert gc().raw_input_ex() == input_output


class GGameConsole(gc):
    """Creating an analogue of the 'GameConsole' class with modified functions 'raw_input' and 'ui_menu'"""
    def __init__(self, target=24, count=4, face2ten=False, showcard=False):
        super(gc, self).__init__(target, count, face2ten)
        self.showcard = showcard

    def raw_input_ex(prompt='', default=''):
        try:
            readline.set_startup_hook(lambda: readline.insert_text(default))
            try:
                return input(prompt)
            finally:
                readline.set_startup_hook()

        except EOFError:
            return INPUT_EOF

    @staticmethod
    def ui_menu(menu, choices, eof=True):
        MSG_INVALID_INPUT = 'Invalid input!'
        INPUT_EOF = '\x00'
        MSG_SELECT = 'Your choice: '
        '''show a menu, and return the selection'''
        GGameConsole.print_title(menu, dechar='-')
        while True:
            r = GGameConsole.raw_input_ex(MSG_SELECT).strip()
            if r.lower() in choices or (eof and r == INPUT_EOF):
                print()
                return r
            print(MSG_INVALID_INPUT)


gc = GGameConsole


@pytest.mark.parametrize('r', [('1'), ('2'), ('3'), ('p'), ('c'), ('q'), ('P'), ('C'), ('Q')])
def test_ui_menu(r):
    """test of the 'ui_menu' function"""
    gg = gc()
    menu = '1. Play (p)\n2. Check answer (c)\n3. Quit (q)'
    choices = '1p2c3q'
    with mock.patch.object(builtins, 'input', lambda _: r):
        assert gg.ui_menu(menu, choices, eof=True) == r


@pytest.mark.xfail
@pytest.mark.parametrize('r', [('w'), ('T'), (''), ('#'), ('ccs'), ('8'), ('78')])
def test_ui_menu_negative(r, capsys):
    """negative test of the 'ui_menu' function"""
    gg = gc()
    menu = '1. Play (p)\n2. Check answer (c)\n3. Quit (q)'
    choices = '1p2c3q'
    answers = (i for i in (r, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        gg.ui_menu(menu, choices, eof=True)
        out, err = capsys.readouterr()
        assert out == ('-' * 50) + '\n' + menu + '\n' + ('-' * 50) + '\nInvalid input!\n\n'


@pytest.mark.parametrize('r, result', [('12 12 12 12', '\n12 + 12 + 12 - 12\n12 × (12 + 12) ÷ 12\n12 + 12 × 12 ÷ 12\n\n'),
                         ('1 2 4 6', '\n4 × 6 × (2 - 1)\n(2 + 6) × (4 - 1)\n\n'),
                         ('1 2 3 4', '\n4 × (1 + 2 + 3)\n1 × 2 × 3 × 4\n(1 + 3) × (2 + 4)\n\n'),
                         ('1 1 1 1', '\nSeems no solutions\n\n')])
def test_ui_check_answer(capsys, r, result):
    """test of the 'ui_check_answer' function"""
    with mock.patch.object(builtins, 'input', lambda _: r):
        gc().ui_check_answer()
        out, err = capsys.readouterr()
        assert out == result


@pytest.mark.parametrize('r', [('1 1 1'), ('adwada'), ('/'), ('1111'), ('P')])
def test_ui_check_answer_negative(capsys, r):
    """negative test of the 'ui_check_answer' function"""
    gg = gc()
    answers = (i for i in (r, '1 1 1 1'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        gg.ui_check_answer()
        out, err = capsys.readouterr()
        assert 'Invalid input' in out


@pytest.mark.parametrize('test', [(1), (2), (3), (4), (5), ('h'), ('s'), ('b'), ('q'), ('n')])
def test_ui_menu_and_expr(capsys, test):
    """test of the 'ui_menu_and_expr' function"""
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
                for ind in out:
                    if ind == '×':
                        result += '*'
                    elif ind == '÷':
                        result += '/'
                    else:
                        result += ind
                for k in result[1:]:
                    if k == '\n':
                        break
                    final_result += k
                with mock.patch.object(builtins, 'input', lambda _: final_result):
                    assert gg.ui_menu_and_expr(menu, choices, eof=True) == calc.parse(final_result)
            else:
                with mock.patch.object(builtins, 'input', lambda _: 'n'):
                    assert gg.ui_menu_and_expr(menu, choices, eof=True) == 'n'
    else:
        with mock.patch.object(builtins, 'input', lambda _: test):
            assert gg.ui_menu_and_expr(menu, choices, eof=True) == test


@pytest.mark.xfail
@pytest.mark.parametrize('r, err_type', [('1 + 1 + 1 + 1', 1), ('1 + 1 + 1 + 1 + 1', 2), ('1111', 3), ('R', 4), ('rfwg', 4), ('12 + 12 + 12 + 12', 2), ('1 1 1 1', 5)])
def test_ui_menu_and_expr_negative(capsys, r, err_type):
    """negative test of the 'ui_menu_and_expr' function"""
    class MockGame(gc, Hand):
        def new_hand(self):
            if self.is_set_end():
                return None

            cards = []
            for i in range(self.count):
                idx = 0
                cards.append(self.cards.pop(idx))
            hand = Hand(cards, target=self.target)
            self.hands.append(hand)
            self.hand = hand
            return self.hand

    gg = MockGame()
    answers = (i for i in (r, 'b', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        gg.play()
        out, err = capsys.readouterr()
        if err_type == 1:
            assert "Sorry! It's not correct!" in out
        elif err_type == 2:
            assert 'Invalid integer: ' in out
        elif err_type == 3:
            assert 'Invalid expression: operator missed' in out
        elif err_type == 4:
            assert 'Invalid character: ' + r[0] in out
        elif err_type == 5:
            assert 'Invalid token' in out


@pytest.mark.parametrize('test', [(1), (2), (3), (4), (5)])
def test_print_result(capsys, test):
    """test of the 'print_result' function"""
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


def test_play_1(capsys):
    """test of the 'play' function"""
    class MockGame(gc, Hand):
        """Creating an analogue of the 'GameConsole' class with modified functions 'new_hand'"""
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
        gg.play()


@pytest.mark.xfail
@pytest.mark.parametrize('r, t_type', [('1', 1), ('n', 1), ('N', 1), ('2', 2), ('h', 2), ('H', 2), ('3', 3), ('s', 3), ('S', 3), ('4', 4), ('q', 4), ('Q', 4)])
def test_play_2(capsys, r, t_type):
    """test of the 'play' function"""
    class MockGame(gc, Hand):
        """Creating an analogue of the 'GameConsole' class with modified functions 'new_hand'"""
        def new_hand(self):
            if self.is_set_end():
                return None

            cards = []
            self.cards = hl.hellp_new_hand_cards(self.cards)
            for i in range(self.count):
                idx = 0
                cards.append(self.cards.pop(idx))
            self.hand = Hand(cards, target=self.target)
            self.hands.append(self.hand)
            return self.hand

    gg = MockGame()
    gg.new_hand()
    cs = ' '.join([str(i) for i in gg.hand.integers])
    sc = hl.hellp_ui_check_answer(capsys, cs)
    if t_type == 1:
        answers = (i for i in (r, 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            gg.play()
            out, err = capsys.readouterr()
            assert 'Good Job' in out
    elif t_type == 2:
        answers = (i for i in (r, 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            gg.play()
            out, err = capsys.readouterr()
            assert "Seems no solutions" in out
    elif t_type == 3:
        answers = (i for i in (r, r, r, r, 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            gg.play()
            out, err = capsys.readouterr()
            assert "Seems no solutions" in out
    elif t_type == 4:
        answers = (i for i in (r, 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            gg.play()


def test_play_3(capsys):
    """test of the 'play' function"""
    class MockGame(gc, Hand):
        def new_hand(self):
            return None

    gg = MockGame()
    gg.new_hand()
    answers = (i for i in ('1', 'b', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        gg.play()
        out, err = capsys.readouterr()
        assert 'Set end, your result' in out


@pytest.mark.xfail
@pytest.mark.parametrize('r', [(1), (2), (3), (4), (5), (6)])
def test_play_4(capsys, r):
    """test of the 'play' function"""
    class MockGame(gc, Hand):
        """Creating an analogue of the 'GameConsole' class with modified functions 'new_hand'"""
        def new_hand(self):
            if self.is_set_end():
                return None

            cards = []
            for i in range(self.count):
                idx = -5
                cards.append(self.cards.pop(idx))
            hand = Hand(cards, target=self.target)
            self.hands.append(hand)
            return hand

    gg = gc()
    if r == 1:
        answers = (i for i in ('s', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            gg.play()
            out, err = capsys.readouterr()
            assert 'Total 0 hands solved\nTotal 0 hands solved with hint\nTotal 13 hands failed to solve' in out
    elif r == 2:
        answers = (i for i in ('h', 's', 'h', 's', 'h', 's', 'h', 's', 'h',
                               's', 'h', 's', 'h', 's', 'h', 's', 'h', 's',
                               'h', 's', 'h', 's', 'h', 's', 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            gg.play()
            out, err = capsys.readouterr()
            assert 'Total 0 hands solved\nTotal 0 hands solved with hint\nTotal 13 hands failed to solve' in out
    elif r == 3:
        gg = MockGame()
        answers = (i for i in ('12 + 12 + 12 - 12', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            gg.play()
    elif r == 4:
        gg = MockGame()
        answers = (i for i in ('12 + 12 + 12 - 12', 't', '12 * (12 + 12) / 12', 'n', 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            gg.play()
            out, err = capsys.readouterr()
            assert hl.hellp_res_print() in out
    elif r == 5:
        gg = MockGame()
        answers = (i for i in ('12 + 12 + 12 - 12', 's', 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: '12 12 12 12'):
            gg.ui_check_answer()
            out, err = capsys.readouterr()
            ass_res = out
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            gg.play()
            out, err = capsys.readouterr()
            assert ass_res in out
    elif r == 6:
        gg = MockGame()
        answers = (i for i in ('12 + 12 + 12 + 12 - 12 - 12', 'n', 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            gg.play()
            out, err = capsys.readouterr()
            assert "You not only solved the problem, but also found a bug!\nPlease report to me with the cards and your solution if you don't mind." in out


@pytest.mark.xfail
@pytest.mark.parametrize('r', [('a'), ('A'), ('5'), ('safg'), ('')])
def test_play_6(capsys, r):
    """test of the 'play' function"""
    class MockGame(gc, Hand):
        """Creating an analogue of the 'GameConsole' class with modified functions 'new_hand'"""
        def new_hand(self):
            if self.is_set_end():
                return None

            cards = []
            for i in range(self.count):
                idx = -5
                cards.append(self.cards.pop(idx))
            hand = Hand(cards, target=self.target)
            self.hands.append(hand)
            return hand

    gg = MockGame()
    answers = (i for i in ('12 + 12 + 12 - 12', r, 'n', 'b', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        gg.play()
        out, err = capsys.readouterr()
        print(out)
        assert 'Invalid input!' in out


@pytest.mark.xfail
@pytest.mark.parametrize('r, t_type', [('1', 1), ('p', 1), ('P', 1), ('2', 2), ('c', 2), ('C', 2), ('3', 3), ('q', 3), ('Q', 3)])
def test_main(r, t_type):
    """test of the 'play' function"""
    gg = gc()
    if t_type == 1:
        answers = (i for i in (r, 'b', 'q'))
    elif t_type == 2:
        answers = (i for i in (r, '1 1 1 1', 'q'))
    elif t_type == 3:
        answers = (i for i in (r))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        gg.main()


@pytest.mark.xfail
@pytest.mark.parametrize('r', [('4'), ('5'), ('s'), ('S'), ('adaf'), ('AFSF'), ('FSsfA'), ('')])
def test_main_negative(capsys, r):
    """negative test of the 'main' function"""
    gg = gc()
    answers = (i for i in (r, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        gg.main()
        out, err = capsys.readouterr()
        assert 'Invalid input!' in out
