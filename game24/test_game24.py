#!usr/bin/python3
'''test file "gameconsole"'''
import builtins
import readline
import sys

import mock

import pytest


from game24 import calc
from game24.game import Hand
from game24 import gameconsole as gc
from game24 import hhelp as hl

GC = gc.GameConsole
MSG_SELECT = gc.MSG_SELECT
INPUT_EOF = gc.INPUT_EOF


@pytest.mark.parametrize('title, result',
                         [('''12 + 12 + 12 - 12
12 × (12 + 12) ÷ 12\n12 + 12 × 12 ÷ 12''',
                           '''\n12 + 12 + 12 - 12\n12 × (12 + 12) ÷ 12
12 + 12 × 12 ÷ 12\n\n'''),
                          ('4 × (1 + 2 + 3)\n1 × 2 × 3 × 4\n(1 + 3) × (2 + 4)',
                           '''\n4 × (1 + 2 + 3)\n1 × 2 × 3 × 4
(1 + 3) × (2 + 4)\n\n'''),
                          ('Good Job', '\nGood Job\n\n')])
def test_print_title(capsys, title, result):
    """test of the print_title function"""
    GC.print_title(title)
    out, err = capsys.readouterr()
    assert out, err == result


@pytest.mark.parametrize('title, result', [(None, None),
                         ('4 × (5 + 9 - 8)\n8 + 4 × (9 - 5)',
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


gc.GameConsole.raw_input_ex = hl.GGameConsole.raw_input_ex
GC = hl.GGameConsole


@pytest.mark.parametrize('test', [('1'), ('2'), ('3'),
                                  ('p'), ('c'), ('q'),
                                  ('P'), ('C'), ('Q')])
def test_ui_menu(test):
    """test of the 'ui_menu' function"""
    g_c = GC()
    menu = '1. Play (p)\n2. Check answer (c)\n3. Quit (q)'
    choices = '1p2c3q'
    with mock.patch.object(builtins, 'input', lambda _: test):
        assert g_c.ui_menu(menu, choices, eof=True) == test


@pytest.mark.parametrize('test', [('w'), ('T'), (''), ('#'),
                                  ('ccs'), ('8'), ('78')])
def test_ui_menu_negative(test, capsys):
    """negative test of the 'ui_menu' function"""
    g_c = GC()
    menu = '1. Play (p)\n2. Check answer (c)\n3. Quit (q)'
    choices = '1p2c3q'
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_menu(menu, choices, eof=True)
        out, err = capsys.readouterr()
        assert out, err == ('-' * 50) + '\n' + menu + '\n' + ('-' * 50) + '''
Invalid input!\n\n'''


@pytest.mark.parametrize('test_input, result', [('12 12 12 12',
                         '''\n12 + 12 + 12 - 12\n12 × (12 + 12) ÷ 12
12 + 12 × 12 ÷ 12\n\n'''),
                                                ('1 2 4 6',
                                                 '''\n4 × 6 × (2 - 1)
(2 + 6) × (4 - 1)\n\n'''),
                                                ('1 2 3 4',
                                                 '''\n4 × (1 + 2 + 3)
1 × 2 × 3 × 4\n(1 + 3) × (2 + 4)\n\n'''),
                                                ('1 1 1 1',
                                                 '\nSeems no solutions\n\n'),
                                                ('0 0 0 0',
                                                 '\nSeems no solutions\n\n')])
def test_ui_check_answer(capsys, test_input, result):
    """test of the 'ui_check_answer' function"""
    with mock.patch.object(builtins, 'input', lambda _: test_input):
        GC().ui_check_answer()
        out, err = capsys.readouterr()
        assert out, err == result


@pytest.mark.parametrize('test', [('1 1 1'), ('adwada'),
                                  ('/'), ('1111'), ('P')])
def test_ui_check_answer_negative(capsys, test):
    """negative test of the 'ui_check_answer' function"""
    g_c = GC()
    answers = (i for i in (test, '1 1 1 1'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_check_answer()
        out, err = capsys.readouterr()
        assert 'Invalid input' in out, err


@pytest.mark.parametrize('test', [('12 + 12 + 12 - 12'), ('(12 + 12) / 12 * 12'),
                                  ('12 * 12 / 12 + 12')])
def test_ui_menu_and_expr_1(capsys, test):
    """checking the function 'ui_emnu_and_expr' when we give an equation that consists of the allowed numbers"""
    menu = '''1. Definitely no solutions (n)\n2. Give me a hint (h)
3. I gave up, show me the answer (s)
4. Back to the main menu (b)
5. Quit the game (q)'''
    choices = '1n2h3s4b5q'
    g_c = hl.MockGame_5()
    hand = g_c.new_hand()
    hand_ints = hand.integers
    with mock.patch.object(builtins, 'input', lambda _: test):
        assert g_c.ui_menu_and_expr(menu, choices, eof=True) == calc.parse(test)


@pytest.mark.parametrize('test', [('1'), ('n'), ('2'), ('h'), ('3'), ('s'),
                                  ('4'), ('b'), ('5'), ('q')])
def test_ui_menu_and_expt_2(test):
    """checking the ui_emnu_and_expr function when we give characters from 'choices'"""
    menu = '''1. Definitely no solutions (n)\n2. Give me a hint (h)
3. I gave up, show me the answer (s)
4. Back to the main menu (b)
5. Quit the game (q)'''
    choices = '1n2h3s4b5q'
    g_c = hl.MockGame_5()
    hand = g_c.new_hand()
    hand_ints = hand.integers
    with mock.patch.object(builtins, 'input', lambda _: test):
        assert g_c.ui_menu_and_expr(menu, choices, eof=True) == test


@pytest.mark.parametrize('test', [('12 - 12 + 12 + 12 - 12 + 12'),
                                  ('12 + 12 * 12 / 12 + 12 - 12'),
                                  ('12 + 12 + 12 + 12 - 12 - 12')])
def test_ui_menu_and_expr_negative_1(capsys, test):
    """checking the ui_emnu_and_expr function when we give the correct equation but using more numbers than allowed"""
    g_c = hl.MockGame_5()
    menu = '''1. Definitely no solutions (n)\n2. Give me a hint (h)
3. I gave up, show me the answer (s)
4. Back to the main menu (b)
5. Quit the game (q)'''
    choices = '1n2h3s4b5q'
    hand = g_c.new_hand()
    hand_ints = hand.integers
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        assert g_c.ui_menu_and_expr(menu, choices) == calc.parse(test)


@pytest.mark.parametrize('test', [('a'), ('A'), ('aA'), ('ggs'), ('AFAW'), ('ASffdS'),
                                  ('8s'), ('8S'), ('4dsf'), ('3FSE'), ('4GdsAd')])
def test_ui_menu_and_expr_negative_2(capsys, test):
    """checking the ui_emnu_and_expr function when we give unresolved characters"""
    g_c = hl.MockGame_5()
    menu = '''1. Definitely no solutions (n)\n2. Give me a hint (h)
3. I gave up, show me the answer (s)
4. Back to the main menu (b)
5. Quit the game (q)'''
    choices = '1n2h3s4b5q'
    hand = g_c.new_hand()
    hand_ints = hand.integers
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_menu_and_expr(menu, choices)
        out, err = capsys.readouterr()
        check_symbol = hl.help_letters_and_numbers(test)
        assert 'Invalid character: ' + check_symbol in out


@pytest.mark.parametrize('test', [('6'), ('7'), ('67'), ('12'), ('12345')])
def test_ui_menu_and_expr_negative_3(capsys, test):
    """checking the ui_emnu_and_expr function when we give numbers not from 'choices'"""
    g_c = hl.MockGame_5()
    menu = '''1. Definitely no solutions (n)\n2. Give me a hint (h)
3. I gave up, show me the answer (s)
4. Back to the main menu (b)
5. Quit the game (q)'''
    choices = '1n2h3s4b5q'
    hand = g_c.new_hand()
    hand_ints = hand.integers
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_menu_and_expr(menu, choices)
        out, err = capsys.readouterr()
        assert 'Invalid expression: operator missed' in out


@pytest.mark.xfail
def test_ui_menu_and_expr_negative_4(capsys):
    """if you give 'ui_menu_and_expr' an empty string"""
    g_c = hl.MockGame_5()
    menu = '''1. Definitely no solutions (n)\n2. Give me a hint (h)
3. I gave up, show me the answer (s)
4. Back to the main menu (b)
5. Quit the game (q)'''
    choices = '1n2h3s4b5q'
    hand = g_c.new_hand()
    hand_ints = hand.integers
    answers = (i for i in ('', 'q'))
    with mock.patch.object(builtins, 'input', lambda _:next(answers)):
        g_c.ui_menu_and_expr(menu, choices)
        out, err = capsys.readouterr()
        assert """Invalid expression: operator missed
""" in out or 'Invalid character:' in out


@pytest.mark.xfail
@pytest.mark.parametrize('test', [('1n'), ('n2'), ('2h'), ('h3'),
                                  ('3s'), ('s4'), ('4b'), ('b5'),
                                  ('5q'), ('1n2h3s4b5q')])
def test_ui_menu_and_expr_negative_5(capsys, test):
    """if you give ui_menu_and_expr invalid input but found in 'choices'"""
    g_c = hl.MockGame_5()
    menu = '''1. Definitely no solutions (n)\n2. Give me a hint (h)
3. I gave up, show me the answer (s)
4. Back to the main menu (b)
5. Quit the game (q)'''
    choices = '1n2h3s4b5q'
    hand = g_c.new_hand()
    hand_ints = hand.integers
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_menu_and_expr(menu, choices)
        out, err = capsys.readouterr()
        check_symbol = hl.help_letters_and_numbers(test)
        assert 'Invalid character: ' + check_symbol in out


def test_print_result(capsys):
    """test of the 'print_result' function"""
    g_c = hl.MockGamePrintresult()
    g_c.new_hand()
    g_c.print_result()
    out, err = capsys.readouterr()
    assert """Total 5 hands solved
Total 4 hands solved with hint
Total 4 hands failed to solve""" in out

def test_play_1(capsys):
    """test of the 'play' function"""
    g_c = GC()
    answers = (i for i in ('s', 's', 's',
                           's', 's', 's',
                           's', 's', 's',
                           's', 's', 's',
                           's', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        with pytest.raises(SystemExit):
            g_c.play()
        out, err = capsys.readouterr()
        assert """1. One more set (n)
2. Back to the main menu (b)
3. Quit the game (q)""" in out, err


@pytest.mark.xfail
@pytest.mark.parametrize('test, t_type', [('1', 1), ('n', 1), ('N', 1),
                                          ('2', 2), ('h', 2), ('H', 2),
                                          ('3', 3), ('s', 3), ('S', 3),
                                          ('4', 4), ('b', 4), ('B', 4),
                                          ('5', 5), ('q', 5), ('Q', 5),
                                          ('1', 6), ('n', 6), ('N', 6),
                                          ('3', 7), ('q', 7), ('Q', 7)])
def test_play_2(capsys, test, t_type):
    """test of the 'play' function"""
    class MockGame(GC, Hand):
        """Creating an analogue of the 'GameConsole'
        class with modified functions 'new_hand'"""
        def new_hand(self):
            """"modified function 'new_hand'"""
            if self.is_set_end():
                return None

            cards = []
            self.cards = hl.hellp_new_hand_cards(self.cards)
            for i in range(self.count):
                print(i)
                idx = 0
                cards.append(self.cards.pop(idx))
            hand = Hand(cards, target=self.target)
            self.hands.append(hand)
            return hand

    g_c = MockGame()
    g_c.new_hand()
    if t_type == 1:
        answers = (i for i in (test, 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
            out, err = capsys.readouterr()
            assert 'Good Job' in out, err
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
            with pytest.raises(SystemExit):
                assert g_c.play().type == SystemExit
    elif t_type == 6:
        g_c = GC()
        answers = (i for i in ('s', 's', 's', 's', 's', 's', 's', 's', 's',
                               's', 's', 's', 's', test, 's', 's', 's', 's',
                               's', 's', 's', 's', 's',
                               's', 's', 's', 's', 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
    elif t_type == 7:
        g_c = GC()
        answers = (i for i in ('s', 's', 's', 's', 's',
                               's', 's', 's', 's', 's',
                               's', 's', 's', test))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                assert g_c.play().type == SystemExit


@pytest.mark.xfail
@pytest.mark.parametrize('test', [(1), (2), (3), (4)])
def test_play_3(test, capsys):
    """test of the 'play' function"""
    class MockGame(GC, Hand):
        """Creating an analogue of the 'GameConsole'
        class with modified functions 'new_hand'"""
        def new_hand(self):
            """"modified function 'new_hand'"""
            return None
    if test == 1:
        g_c = MockGame()
        g_c.new_hand()
        answers = (i for i in ('1', 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
            out, err = capsys.readouterr()
            assert 'Set end, your result' in out, err

    class GameMock(GC, Hand):
        """Creating an analogue of the 'GameConsole'
        class with modified functions 'new_hand'"""
        def new_hand(self):
            """"modified function 'new_hand'"""
            if self.is_set_end():
                return None

            cards = []
            for i in range(self.count):
                print(i)
                idx = 0
                cards.append(self.cards.pop(idx))
            hand = Hand(cards, target=self.target)
            self.hands.append(hand)
            return hand

    if test == 2:
        g_c = GameMock()
        answers = (i for i in ('s', 's', 's', 's', 's',
                               '6 + 6 + 6 + 6', 't',
                               '6 + 6 + 6 + 6', 'n',
                               's', 's', 's', 's', 's',
                               's', 's', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                g_c.play()
        out, err = capsys.readouterr()
        assert """Total 1 hands solved
Total 0 hands solved with hint
Total 12 hands failed to solve""" in out
    elif test == 3:
        g_c = GameMock()
        answers = (i for i in ('s', 's', 's', 's', 's',
                               '6 + 6 + 6 + 6', 't',
                               '6 * 6 - 6 - 6', 'n',
                               's', 's', 's', 's', 's',
                               's', 's', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                g_c.play()
        out, err = capsys.readouterr()
        assert """Total 1 hands solved
Total 0 hands solved with hint
Total 12 hands failed to solve""" in out
    elif test == 4:
        g_c = GameMock()
        answers = (i for i in ('s', 's', 's', 's', 's',
                               '6 + 6 + 6 + 6', 't', 'h',
                               '6 * 6 - 6 - 6', 'n',
                               's', 's', 's', 's', 's',
                               's', 's', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                g_c.play()
        out, err = capsys.readouterr()
        assert """Total 1 hands solved
Total 0 hands solved with hint
Total 12 hands failed to solve""" in out


@pytest.mark.xfail
@pytest.mark.parametrize('test', [(1), (2), (3), (4), (5)])
def test_play_4(capsys, test):
    """test of the 'play' function"""
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
                idx = -5
                cards.append(self.cards.pop(idx))
            hand = Hand(cards, target=self.target)
            self.hands.append(hand)
            return hand

    g_c = GC()
    if test == 1:
        answers = (i for i in ('s', 's', 's', 's', 's',
                               's', 's', 's', 's', 's',
                               's', 's', 's', 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
            out, err = capsys.readouterr()
            check_coment = 'Total 0 hands solved\nTotal 0 hands solved '
            check_coment += 'with hint\nTotal 13 hands failed to solve'
            assert check_coment in out, err
    elif test == 2:
        answers = (i for i in ('h', 's', 'h', 's', 'h', 's', 'h', 's', 'h',
                               's', 'h', 's', 'h', 's', 'h', 's', 'h', 's',
                               'h', 's', 'h', 's', 'h', 's',
                               'h', 's', 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
            out, err = capsys.readouterr()
            check_coment = 'Total 0 hands solved\nTotal 0 '
            check_coment += '''hands solved with hint
Total 13 hands failed to solve'''
            assert check_coment in out
    elif test == 3:
        g_c = MockGame()
        answers = (i for i in ('12 + 12 + 12 - 12', 't',
                               '12 * (12 + 12) / 12', 'n', 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
            out, err = capsys.readouterr()
            assert hl.hellp_res_print() in out
    elif test == 4:
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


@pytest.mark.xfail
@pytest.mark.parametrize('test', [(1), (2), (3), (4), (5)])
def test_play_5(capsys, test):
    """test of the 'play' function"""
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
                idx = -5
                cards.append(self.cards.pop(idx))
            hand = Hand(cards, target=self.target)
            self.hands.append(hand)
            return hand

    g_c = GC()
    if test == 1:
        g_c = MockGame()
        answers = (i for i in ('12 + 12 + 12 + 12 - 12 - 12', 'n', 'b', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            g_c.play()
            out, err = capsys.readouterr()
            check_coment = 'You not only solved the problem, but '
            check_coment += """also found a bug!
Please report to me with the cards and your solution if you don't mind."""
            assert check_coment in out, err
    if test == 2:
        g_c = MockGame()
        answers = (i for i in ('12 + 12 + 12 - 12', '4'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                assert g_c.play().type == SystemExit
    elif test == 3:
        g_c = MockGame()
        answers = (i for i in ('12 + 12 + 12 - 12', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                assert g_c.play().type == SystemExit
    elif test == 4:
        g_c = MockGame()
        answers = (i for i in ('12 + 12 + 12 - 12', 'Q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                assert g_c.play().type == SystemExit
    elif test == 5:
        g_c = MockGame()
        answers = (i for i in ('12 + 12 + 12 - 12', '', 'q'))
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                assert g_c.play().type == SystemExit
        out, err = capsys.readouterr()
        assert 'Invalid input!' in out


@pytest.mark.xfail
@pytest.mark.parametrize('test', [('a'), ('A'), ('5'), ('safg'), ('')])
def test_play_6(capsys, test):
    """test of the 'play' function"""
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
                idx = -5
                cards.append(self.cards.pop(idx))
            hand = Hand(cards, target=self.target)
            self.hands.append(hand)
            return hand

    g_c = MockGame()
    answers = (i for i in ('12 + 12 + 12 - 12', test, 'n', 'b', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.play()
        out, err = capsys.readouterr()
        assert 'Invalid input!' in out, err


@pytest.mark.xfail
@pytest.mark.parametrize('test, t_type', [('1', 1), ('p', 1),
                                          ('P', 1), ('2', 2),
                                          ('c', 2), ('C', 2),
                                          ('3', 3), ('q', 3), ('Q', 3)])
def test_main_gc(test, t_type):
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
@pytest.mark.parametrize('test', [('4'), ('5'), ('s'),
                                  ('S'), ('adaf'),
                                  ('AFSF'), ('FSsfA'), ('')])
def test_main_negative(capsys, test):
    """negative test of the 'main' function"""
    g_c = GC()
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.main()
        out, err = capsys.readouterr()
        assert 'Invalid input!' in out, err


@pytest.mark.parametrize('test', [('12 + 12 + 12 - 12'),
                                  ('12 + 12 + (12 - 12)'),
                                  ('5 + 5 + 5 + 5'),
                                  ('13 + (10 + 12) / 2'),
                                  ('12 + 12 + 12')])
def test_parse(test, capsys):
    """test of the 'parse' function"""
    print(calc.parse(test))
    out, err = capsys.readouterr()
    if test == '12 + 12 + (12 - 12)':
        assert out, err == '12 + 12 + 12 - 12\n'
    elif test == '13 + (10 + 12) / 2':
        assert out, err == '13 + (10 + 12) ÷ 2\n'
    else:
        assert out, err == test + '\n'


CHECK_TEST_PARSE = '[<+ [12, 12, 12, ^12]>, <* [12, <+ [12, 12]>'


CHECK_TEST_PARSE += ', ^12]>, <+ [12, <* [12, 12, ^12]>]>]'


@pytest.mark.parametrize('test, test_targ, result',
                         [([12, 12, 12, 12], 24,
                             CHECK_TEST_PARSE),
                          ([12, 12, 12], 24, '[]')])
def test_solve(test, test_targ, result):
    """test of the 'solve' function"""
    assert str(calc.solve(test, test_targ)) == result


@pytest.mark.parametrize('test', [(1), (2), (3)])
def test_arg_parse(test):
    """negative test of the 'arg_parse' function"""
    print(test)
    testargs = ['']
    with mock.patch.object(sys, 'argv', testargs):
        assert gc.arg_parse().interactive
