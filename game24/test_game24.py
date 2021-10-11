#!usr/bin/python3
'''test file "gameconsole"'''
import pytest
import mock
import builtins
import sys
import random
import readline


from .gameconsole import *
from game24.game import Game as gm
from game24.game import Hand
from . import help as hl
from game24 import calc

GC = GameConsole


@pytest.mark.parametrize('title, result',
                         [('12 + 12 + 12 - 12\n12 × (12 + 12) ÷ 12\n12 + 12 × 12 ÷ 12',
                           '\n12 + 12 + 12 - 12\n12 × (12 + 12) ÷ 12\n12 + 12 × 12 ÷ 12\n\n'),
                          ('4 × (1 + 2 + 3)\n1 × 2 × 3 × 4\n(1 + 3) × (2 + 4)',
                           '\n4 × (1 + 2 + 3)\n1 × 2 × 3 × 4\n(1 + 3) × (2 + 4)\n\n'),
                          ('Good Job', '\nGood Job\n\n')])
def test_print_title(capsys, title, result):
    """test of the print_title function"""
    GC.print_title(title)
    out, err = capsys.readouterr()
    assert out, err == result


@pytest.mark.parametrize('title, result', [(None, None), ('4 × (5 + 9 - 8)\n8 + 4 × (9 - 5)',
                         '4 × (5 + 9 I- 8)\n8 + 4 × (9 - 5)')])
def test_print_title_negativie(capsys, title, result):
    """negative test of print_title function"""
    GC.print_title(title)
    out, err = capsys.readouterr()
    assert out, err != result


@pytest.mark.parametrize('input_output', [('name'), ('HeLlO'), (''), ('12')])
def test_raw_input_ex(input_output):
    """test of the 'raw_input_ex' function"""
    with mock.patch.object(builtins, 'input', lambda _: input_output):
        assert GC().raw_input_ex() == input_output


class GGameConsole(GC):
    """Creating an analogue of the 'GameConsole' class with modified functions 'raw_input' and 'ui_menu'"""
    def __init__(self, target=24, count=4, face2ten=False, showcard=False):
        super(GC, self).__init__(target, count, face2ten)
        self.showcard = showcard

    def raw_input_ex(prompt='', default=''):
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

    @staticmethod
    def ui_menu(menu, choices, eof=True):
        '''show a menu, and return the selection'''
        msg_invalid_input = 'Invalid input!'
        GGameConsole.print_title(menu, dechar='-')
        while True:
            result = GGameConsole.raw_input_ex(MSG_SELECT).strip()
            if result.lower() in choices or (eof and result == INPUT_EOF):
                print()
                return result
            print(msg_invalid_input)


GC = GGameConsole


@pytest.mark.parametrize('test', [('1'), ('2'), ('3'), ('p'), ('c'), ('q'), ('P'), ('C'), ('Q')])
def test_ui_menu(test):
    """test of the 'ui_menu' function"""
    g_c = GC()
    menu = '1. Play (p)\n2. Check answer (c)\n3. Quit (q)'
    choices = '1p2c3q'
    with mock.patch.object(builtins, 'input', lambda _: test):
        assert g_c.ui_menu(menu, choices, eof=True) == test


@pytest.mark.parametrize('test', [('w'), ('T'), (''), ('#'), ('ccs'), ('8'), ('78')])
def test_ui_menu_negative(test, capsys):
    """negative test of the 'ui_menu' function"""
    g_c = GC()
    menu = '1. Play (p)\n2. Check answer (c)\n3. Quit (q)'
    choices = '1p2c3q'
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_menu(menu, choices, eof=True)
        out, err = capsys.readouterr()
        assert out, err == ('-' * 50) + '\n' + menu + '\n' + ('-' * 50) + '\nInvalid input!\n\n'


@pytest.mark.parametrize('test_input, result', [('12 12 12 12', '\n12 + 12 + 12 - 12\n12 × (12 + 12) ÷ 12\n12 + 12 × 12 ÷ 12\n\n'),
                         ('1 2 4 6', '\n4 × 6 × (2 - 1)\n(2 + 6) × (4 - 1)\n\n'),
                         ('1 2 3 4', '\n4 × (1 + 2 + 3)\n1 × 2 × 3 × 4\n(1 + 3) × (2 + 4)\n\n'),
                         ('1 1 1 1', '\nSeems no solutions\n\n'), ('0 0 0 0', '\nSeems no solutions\n\n')])
def test_ui_check_answer(capsys, test_input, result):
    """test of the 'ui_check_answer' function"""
    with mock.patch.object(builtins, 'input', lambda _: test_input):
        GC().ui_check_answer()
        out, err = capsys.readouterr()
        assert out, err == result


@pytest.mark.parametrize('test', [('1 1 1'), ('adwada'), ('/'), ('1111'), ('P')])
def test_ui_check_answer_negative(capsys, test):
    """negative test of the 'ui_check_answer' function"""
    g_c = GC()
    answers = (i for i in (test, '1 1 1 1'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_check_answer()
        out, err = capsys.readouterr()
        assert 'Invalid input' in out, err


@pytest.mark.parametrize('test', [(1), (2), (3), (4), (5), ('h'), ('s'), ('b'), ('q'), ('n')])
def test_ui_menu_and_expr(capsys, test):
    """test of the 'ui_menu_and_expr' function"""
    menu = '1. Definitely no solutions (n)\n2. Give me a hint (h)\n3. I gave up, show me the answer (s)\n4. Back to the main menu (b)\n5. Quit the game (q)'
    choices = '1n2h3s4b5q'
    g_c = GC()
    hand = g_c.new_hand()
    hand_ints = hand.integers
    hand_ui_check = ''
    result = ''
    final_result = ''
    if test in range(1, 6):
        for i in hand_ints:
            hand_ui_check += str(i) + ' '
        with mock.patch.object(builtins, 'input', lambda _: hand_ui_check):
            g_c.ui_check_answer()
            out, err = capsys.readouterr()
            if out != '\nSeems no solutions\n\n' and err != '\nSeems no solutions\n\n':
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
                    assert g_c.ui_menu_and_expr(menu, choices, eof=True) == calc.parse(final_result)
            else:
                with mock.patch.object(builtins, 'input', lambda _: 'n'):
                    assert g_c.ui_menu_and_expr(menu, choices, eof=True) == 'n'
    else:
        with mock.patch.object(builtins, 'input', lambda _: test):
            assert g_c.ui_menu_and_expr(menu, choices, eof=True) == test


@pytest.mark.xfail
@pytest.mark.parametrize('test, err_type', [('1 + 1 + 1 + 1', 1), ('1 + 1 + 1 + 1 + 1', 2), ('1111', 3), ('R', 4), ('rfwg', 4), ('12 + 12 + 12 + 12', 2), ('1 1 1 1', 5)])
def test_ui_menu_and_expr_negative(capsys, test, err_type):
    """negative test of the 'ui_menu_and_expr' function"""
    class MockGame(GC, Hand):
        """Creating an analogue of the 'GameConsole' class with modified functions 'new_hand'"""
        def new_hand(self):
            """"modified function 'new_hand'"""
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

    g_c = MockGame()
    answers = (i for i in (test, 'b', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.play()
        out, err = capsys.readouterr()
        if err_type == 1:
            assert "Sorry! It's not correct!" in out, err
        elif err_type == 2:
            assert 'Invalid integer: ' in out
        elif err_type == 3:
            assert 'Invalid expression: operator missed' in out
        elif err_type == 4:
            assert 'Invalid character: ' + test[0] in out
        elif err_type == 5:
            assert 'Invalid token' in out


@pytest.mark.parametrize('test', [(1), (2), (3), (4), (5)])
def test_print_result(capsys, test):
    """test of the 'print_result' function"""
    g_c = GC()
    hand = g_c.new_hand()
    solved = 0
    failed = 0
    hinted = 0
    if hand.result == 's':
        solved += 1
    elif hand.result == 'h':
        hinted += 1
    elif hand.result == 'f':
        failed += 1
    g_c.print_result()
    out, err = capsys.readouterr()
    assert out, err == '\nTotal %d hands solved' % solved + '\nTotal %d hands solved with hint' % hinted + '\nTotal %d hands failed to solve' % failed + '\n\n'


@pytest.mark.xfail
def test_play_1(capsys):
    """test of the 'play' function"""
    class MockGame(GC, Hand):
        """Creating an analogue of the 'GameConsole' class with modified functions 'new_hand'"""
        def new_hand(self):
            """"modified function 'new_hand'"""
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

    g_c = MockGame()
    g_c.new_hand()
    s_c = ' '.join([str(i) for i in g_c.hand.integers])
    hl_res = hl.hellp_ui_check_answer(capsys, s_c)
    answers = (i for i in (hl_res, 'n', hl_res, 'n', 's', 'n', hl_res, 'n', hl_res, 'n', 'h', hl_res, 'n', hl_res, 'n', hl_res, 'n', hl_res, 'n', hl_res, 'n', hl_res, 'n', hl_res, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.play()


@pytest.mark.xfail
@pytest.mark.parametrize('test, t_type', [('1', 1), ('n', 1), ('N', 1), ('2', 2), ('h', 2), ('H', 2), ('3', 3), ('s', 3), ('S', 3), ('4', 4), ('b', 4), ('B', 4), ('5', 5), ('q', 5), ('Q', 5), ('1', 6), ('n', 6), ('N', 6), ('3', 7), ('q', 7), ('Q', 7)])
def test_play_2(capsys, test, t_type):
    """test of the 'play' function"""
    class MockGame(GC, Hand):
        """"modified function 'new_hand'"""
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

    g_c = MockGame()
    g_c.new_hand()
    cs = ' '.join([str(i) for i in g_c.hand.integers])
    sc = hl.hellp_ui_check_answer(capsys, cs)
    if t_type == 1:
        answers = (i for i in (test, 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
            out, err = capsys.readouterr()
            assert 'Good Job' in out
    elif t_type == 2:
        answers = (i for i in (test, 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
            out, err = capsys.readouterr()
            assert "Seems no solutions" in out
    elif t_type == 3:
        answers = (i for i in (test, test, test, test, 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
            out, err = capsys.readouterr()
            assert "Seems no solutions" in out
    elif t_type == 4:
        answers = (i for i in (test, 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
    elif t_type == 5:
        g_c = GC()
        answers = (i for i in (test))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
    elif t_type == 6:
        g_c = GC()
        answers = (i for i in ('s', 's', 's', 's', 's', 's', 's', 's', 's',
                               's', 's', 's', 's', test, 's', 's', 's', 's',
                               's', 's', 's', 's', 's', 's', 's', 's', 's', 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
    elif t_type == 7:
        g_c = GC()
        answers = (i for i in ('s', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', test))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()


def test_play_3(capsys):
    """test of the 'play' function"""
    class MockGame(GC, Hand):
        def new_hand(self):
            return None

    g_c = MockGame()
    g_c.new_hand()
    answers = (i for i in ('1', 'b', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.play()
        out, err = capsys.readouterr()
        assert 'Set end, your result' in out


@pytest.mark.xfail
@pytest.mark.parametrize('r', [(1), (2), (3), (4), (5), (6), (7), (8), (9), (10), (11), (12), (13)])
def test_play_4(capsys, r):
    """test of the 'play' function"""
    class MockGame(GC, Hand):
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

    g_c = GC()
    if r == 1:
        answers = (i for i in ('s', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
            out, err = capsys.readouterr()
            assert 'Total 0 hands solved\nTotal 0 hands solved with hint\nTotal 13 hands failed to solve' in out
    elif r == 2:
        answers = (i for i in ('h', 's', 'h', 's', 'h', 's', 'h', 's', 'h',
                               's', 'h', 's', 'h', 's', 'h', 's', 'h', 's',
                               'h', 's', 'h', 's', 'h', 's', 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
            out, err = capsys.readouterr()
            assert 'Total 0 hands solved\nTotal 0 hands solved with hint\nTotal 13 hands failed to solve' in out
    elif r == 3:
        g_c = MockGame()
        answers = (i for i in ('12 + 12 + 12 - 12', 't', '12 * (12 + 12) / 12', 'n', 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
            out, err = capsys.readouterr()
            assert hl.hellp_res_print() in out
    elif r == 4:
        g_c = MockGame()
        answers = (i for i in ('12 + 12 + 12 - 12', 's', 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: '12 12 12 12'):
            g_c.ui_check_answer()
        out, err = capsys.readouterr()
        ass_res = out
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
            out, err = capsys.readouterr()
            assert ass_res in out
    elif r == 5:
        g_c = MockGame()
        answers = (i for i in ('12 + 12 + 12 + 12 - 12 - 12', 'n', 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
            out, err = capsys.readouterr()
            assert "You not only solved the problem, but also found a bug!\nPlease report to me with the cards and your solution if you don't mind." in out
    elif r == 6:
        g_c = MockGame()
        answers = (i for i in ('12 + 12 + 12 - 12', '4'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
    elif r == 7:
        g_c = MockGame()
        answers = (i for i in ('12 + 12 + 12 - 12', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
    elif r == 8:
        g_c = MockGame()
        answers = (i for i in ('12 + 12 + 12 - 12', 'Q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
    elif r == 9:
        g_c = MockGame()
        answers = (i for i in ('12 + 12 + 12 - 12', '', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
        out, err = capsys.readouterr()
        assert 'Invalid input!' in out
    elif r == 10:
        g_c = MockGame()
        answers = (i for i in ('12 + 12 + 12 - 12', '4'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
    elif r == 11:
        g_c = MockGame()
        answers = (i for i in ('12 + 12 + 12 - 12', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
    elif r == 12:
        g_c = MockGame()
        answers = (i for i in ('12 + 12 + 12 - 12', 'Q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
    elif r == 13:
        g_c = MockGame()
        answers = (i for i in ('12 + 12 + 12 - 12', '', '1', '4', '5'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
            out, err = capsys.readouterr()
        assert 'Invalid input!' in out, err
    


@pytest.mark.xfail
@pytest.mark.parametrize('r', [('a'), ('A'), ('5'), ('safg'), ('')])
def test_play_5(capsys, r):
    """test of the 'play' function"""
    class MockGame(GC, Hand):
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

    g_c = MockGame()
    answers = (i for i in ('12 + 12 + 12 - 12', r, 'n', 'b', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.play()
        out, err = capsys.readouterr()
        assert 'Invalid input!' in out


@pytest.mark.xfail
@pytest.mark.parametrize('test, t_type', [('1', 1), ('p', 1), ('P', 1), ('2', 2), ('c', 2), ('C', 2), ('3', 3), ('q', 3), ('Q', 3)])
def test_main(test, t_type):
    """test of the 'play' function"""
    g_c = GC()
    if t_type == 1:
        answers = (i for i in (test, 'b', 'q'))
    elif t_type == 2:
        answers = (i for i in (test, '1 1 1 1', 'q'))
    elif t_type == 3:
        answers = (i for i in (test))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.main()


@pytest.mark.xfail
@pytest.mark.parametrize('r', [('4'), ('5'), ('s'), ('S'), ('adaf'), ('AFSF'), ('FSsfA'), ('')])
def test_main_negative(capsys, r):
    """negative test of the 'main' function"""
    g_c = GC()
    answers = (i for i in (r, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.main()
        out, err = capsys.readouterr()
        assert 'Invalid input!' in out


@pytest.mark.parametrize('test', [('12 + 12 + 12 - 12'), ('12 + 12 + (12 - 12)'), ('5 + 5 + 5 + 5'), ('13 + (10 + 12) / 2'), ('12 + 12 + 12')])
def test_parse(test, capsys):
    print(calc.parse(test))
    out, err = capsys.readouterr()
    if test == '12 + 12 + (12 - 12)':
        assert out == '12 + 12 + 12 - 12\n'
    elif test == '13 + (10 + 12) / 2':
        assert out == '13 + (10 + 12) ÷ 2\n'
    else:
        assert out == test + '\n'



@pytest.mark.parametrize('test, test_targ, result',
                         [([12, 12, 12, 12], 24, '[<+ [12, 12, 12, ^12]>, <* [12, <+ [12, 12]>, ^12]>, <+ [12, <* [12, 12, ^12]>]>]'),
                         ([12, 12, 12], 24, '[]'), ([5, 5, 5, 5, 5], 25, '[<+ [5, 5, 5, 5, 5]>, <+ [<* [5, <+ [5, 5]>]>, ^<* [5, 5]>]>, <+ [<* [5, 5]>, <* [5, <+ [5, ^5]>]>]>, <* [5, <+ [5, <* [5, <+ [5, ^5]>]>]>]>, <+ [<* [5, <+ [5, <* [5, ^5]>]>]>, ^5]>, <+ [5, <* [5, <+ [5, ^<* [5, ^5]>]>]>]>]')])
def test_solve(test, test_targ, result):
    assert str(calc.solve(test, test_targ)) == result



@pytest.mark.xfail
@pytest.mark.parametrize('n', [(1), (2), (3)])
def test_arg_parse(n):
    """negative test of the 'arg_parse' function"""
    if n == 1:
        r = 'namespace.integers = []'
    elif n == 2:
        r = "namespace.integers.append('a')"
    elif n == 3:
        r = "namespace.integers.append('a', 'b', 'g')"
    answers = (i for i in ('s', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                           'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                           'n', 'n', 'n', 'n', 's', 'n', 's', 'n', 'n',
                           'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                           'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                           'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                           'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                           'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                           'n', r, 'n', 'n', 'n', 'argv = None', 'c'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        if n == 1:
            breakpoint()
            assert arg_parse().interactive == True
        elif n == 2:
            breakpoint()
            arg_parse()
        elif n == 3:
            breakpoint()
            arg_parse()


@pytest.mark.xfail
@pytest.mark.parametrize('n', [(1), (2), (3), (4), (5), (6)])
def test_main(n, capsys):
    """test function 'main' in non-function"""
    if n == 1:
        answers = (i for i in ('s', 'n', 's', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'n', 'n', 'n', 's', 'n', 's', 'n', 'n',
                               'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'namespace.interactive == True',
                               'namespace.integers = []', 'n', 'n', 'n', 'argv = None',
                               'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 's', 'n', 'n', 's', 'n', 'n',
                               'GameConsole.raw_input_ex = input', 'c', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            breakpoint()
            main()
    elif n == 2:
        answers = (i for i in ('s', 'n', 's', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'n', 'n', 'n', 's', 'n', 's', 'n', 'n',
                               'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'namespace.integers = ["12 + 12 + 12 + 12"]',
                               'namespace.debug = True', 'n', 'n', 'n', 'argv = None', 'c'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            breakpoint()
            main()
            out, err = capsys.readouterr()
            assert '<+ [12, 12, 12, 12]>\n12 + 12 + 12 + 12\n48\n' == out
    elif 3 <= n <= 6:
        if n == 3:
            r = '1, 2, 3, 4'
        elif n == 4:
            r = '5, 5, 5, 5'
        elif n == 5:
            r = '3, 2, 8, 3'
        elif n == 6:
            r = '1, 1, 1, 1'
        answers = (i for i in ('s', 'n', 's', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'n', 'n', 'n', 's', 'n', 's', 'n', 'n',
                               'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',
                               'n', 'namespace.integers = [' + r + ']',
                               'n', 'n', 'n', 'argv = None', 'c'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            breakpoint()
            main()
            out, err = capsys.readouterr()
            if n == 3:
                assert out == '4 × (1 + 2 + 3)\n1 × 2 × 3 × 4\n(1 + 3) × (2 + 4)\n'
            elif n == 4:
                assert out == '5 × 5 - 5 ÷ 5\n'
            elif n == 5:
                assert out == '3 × 8 × (3 - 2)\n8 × (2 × 3 - 3)\n8 × (3 + 3) ÷ 2\n8 × (2 + 3 ÷ 3)\n'
            elif n == 6:
                assert out == 'Seems no solutions\n'
