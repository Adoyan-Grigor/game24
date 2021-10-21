"""hhelp"""
import builtins
import random
import mock
import sys

import pytest


from game24.gameconsole import GameConsole as gc
from game24.game import Hand


class GGameConsole(gc):
    """analogue of the 'GameConsole' class with the modified
       'raw_input_ex' function for normal test work"""
    @staticmethod
    def raw_input_ex(prompt='', default=''):
        '''enhance raw_input to support default input and also flat EOF'''
        return input(prompt)


gc.raw_input_ex = GGameConsole.raw_input_ex
GC = gc
testargs = ['']


def help_ui_check_answer(capsys, r_input):
    """a function to calculate an equation from a combination of four numbers to get 24"""
    g_c = GC()
    final_result = ''
    with mock.patch.object(builtins, 'input', lambda _: r_input):
        g_c.ui_check_answer()
        out, err = capsys.readouterr()
        print(err)
        if out == '\nSeems no solutions\n\n':
            final_result = 'n'
        else:
            for i in out:
                if i == '\n':
                    break
                if i == '×':
                    final_result += '*'
                elif i == '÷':
                    final_result += '/'
                else:
                    final_result += i
        return final_result


def help_ui_check_answer_all(capsys, r_input):
    """function to calculate all equations from the combination of four numbers to get 24"""
    g_c = GC()
    with mock.patch.object(builtins, 'input', lambda _: r_input):
        g_c.ui_check_answer()
        out, err = capsys.readouterr()
        print(err)
    return out


def help_new_hand_cards(cards):
    """the modified 'new_hand_cards' function returns 12"""
    llist = []
    for i in range(len(cards[44: 48])):
        llist.append(cards[i])
    cards = []
    while len(cards) < 53:
        for i in llist:
            cards.append(i)
    return cards


class MockGameNone(GC, Hand):
    """Creating an analogue of the 'GameConsole'
    class with modified functions 'new_hand'"""
    def new_hand(self):
        """"modified function 'new_hand'"""
        return None


class MockGame0(GC, Hand):
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


class MockGame1(GC, Hand):
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


class MockGame5(GC, Hand):
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


def help_letters_and_numbers(arg):
    """a function to calculate a letter from a string"""
    for i in arg:
        if i not in '123456789':
            return i
    return arg


class MockGamePrintresult(GC, Hand):
    """Creating an analogue of the 'GameConsole'
    class with modified functions 'new_hand'"""
    def new_hand(self):
        if self.is_set_end():
            return None

        for i in range(0, 13):
            cards = []
            for ind in range(self.count):
                print(ind)
                idx = random.randint(0, len(self.cards) - 1)
                cards.append(self.cards.pop(idx))
            hand = Hand(cards, target=self.target)
            self.hands.append(hand)
        for i in range(0, 5):
            self.hands[i].result = 's'
        for i in range(5, 9):
            self.hands[i].result = 'h'
        for i in range(9, 13):
            self.hands[i].result = 'f'
        return hand


def test_help_play_1(capsys):
    """checking the 'play' function when the program skips all tasks"""
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
        print(err)
        return out


def test_help_play_2(capsys, test):
    """checking the 'play' function when the program responds
       correctly that there is no correct answer"""
    g_c = MockGame0()
    g_c.new_hand()
    answers = (i for i in (test, 'b', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.play()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_play_3(capsys, test):
    """checking the play function when the user turns to the program for
       help in solving the equation when there is no solution"""
    g_c = MockGame0()
    g_c.new_hand()
    answers = (i for i in (test, 'b', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.play()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_play_4(test):
    """checking the 'play' function when the user
       wants to go to the main menu"""
    g_c = MockGame0()
    g_c.new_hand()
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        return g_c.play()


def test_help_play_5(test):
    """checking the 'play' function when the user wants to log out"""
    g_c = MockGame0()
    g_c.new_hand()
    with mock.patch.object(builtins, 'input', lambda _: test):
        with pytest.raises(SystemExit):
            assert g_c.play().type == SystemExit


def test_help_play_6(test):
    """checking the 'play' function, check if MSG_MENU_SET_END is working"""
    g_c = MockGame0()
    g_c.new_hand()
    answers = (i for i in ('s', 's', 's', 's', 's', 's', 's', 's', 's',
                           's', 's', 's', 's', test, 's', 's', 's', 's',
                           's', 's', 's', 's', 's',
                           's', 's', 's', 's', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        with pytest.raises(SystemExit):
            assert g_c.play().type == SystemExit


def test_help_play_7(test):
    """checking the "play" function, when the user wants to go
       to the main menu via MSG_MENU_SET_END"""
    g_c = MockGame0()
    g_c.new_hand()
    answers = (i for i in ('s', 's', 's', 's', 's',
                           's', 's', 's', 's', 's',
                           's', 's', 's', test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.play()


def test_help_play_8(test):
    """checking the "play" function, when the user wants to
       exit the program via MSG_MENU_SET_END"""
    g_c = MockGame0()
    g_c.new_hand()
    answers = (i for i in ('s', 's', 's', 's', 's',
                           's', 's', 's', 's', 's',
                           's', 's', 's', test))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        with pytest.raises(SystemExit):
            assert g_c.play().type == SystemExit


def test_help_play_9(capsys):
    """checking the "play" function, when hand is empty"""
    g_c = MockGameNone()
    g_c.new_hand()
    answers = (i for i in ('1', 'b', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.play()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_play_10(capsys):
    """checking the "play" function, when the user has correctly
       solved the same equation twice"""
    g_c = MockGame0()
    answers = (i for i in ('s', 's', 's', 's', 's',
                           '6 + 6 + 6 + 6', 't',
                           '6 + 6 + 6 + 6', 'n',
                           's', 's', 's', 's', 's',
                           's', 's', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        with pytest.raises(SystemExit):
            g_c.play()
    out, err = capsys.readouterr()
    print(err)
    return out


def test_help_play_11(capsys):
    """checking the "play" function, when the user correctly solved
       the same equation twice, but in different ways"""
    g_c = MockGame0()
    answers = (i for i in ('s', 's', 's', 's', 's',
                           '6 + 6 + 6 + 6', 't',
                           '6 * 6 - 6 - 6', 'n',
                           's', 's', 's', 's', 's',
                           's', 's', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        with pytest.raises(SystemExit):
            g_c.play()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_play_12(capsys):
    """checking the "play" function, when the user skips the task
       after receiving help from the program"""
    g_c = MockGame0()
    answers = (i for i in ('h', 's', 'h', 's', 'h', 's', 'h', 's', 'h',
                           's', 'h', 's', 'h', 's', 'h', 's', 'h', 's',
                           'h', 's', 'h', 's', 'h', 's',
                           'h', 's', 'b', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.play()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_play_13(capsys):
    """checking the "play" function, when the user asks for the rest
       of the answer options after the correct answer"""
    g_c = MockGame5()
    answers = (i for i in ('12 + 12 + 12 - 12', 's', 'b', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.play()
    out, err = capsys.readouterr()
    print(err)
    return out


def test_help_play_14(capsys):
    """checking the "play" function, when the user finds a bug
       by entering more numbers than allowed"""
    g_c = MockGame5()
    answers = (i for i in ('12 + 12 + 12 + 12 - 12 - 12', 'n', 'b', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.play()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_play_15(test):
    """checking the "play" function, when, after the correct answer,
       the user wants to exit the program"""
    g_c = MockGame5()
    answers = (i for i in ('12 + 12 + 12 - 12', test))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        with pytest.raises(SystemExit):
            assert g_c.play().type == SystemExit


def test_help_play_16(capsys, test):
    """checking the 'play' function when the program
       receives an incorrect response"""
    g_c = MockGame5()
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        with pytest.raises(SystemExit):
            g_c.play()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_play_17(capsys, test):
    """checking the function 'play' when the program gets the correct
       equation, but more numbers are used than allowed"""
    g_c = MockGame5()
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        with pytest.raises(SystemExit):
            g_c.play()
        out, err = capsys.readouterr()
        print(err)
        return out

def test_help_main_1(capsys):
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
                MockGame1().main()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_main_2(capsys):
    """checking the 'main' function, when the user wants
       to use the 'ui_check_answer' function"""
    answers = (i for i in ('2', '12 12 12',
                           '12 12 12 12', '2',
                           '2 2 2 2', '2',
                           '5 5 5 5', 'q'))
    with mock.patch.object(sys, 'argv', testargs):
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            MockGame1().main()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_main_3(capsys):
    """checking the 'main' function, when the user skips an
       equation that has no solution and exits the program"""
    answers = (i for i in ('1', 's', 'q'))
    with mock.patch.object(sys, 'argv', testargs):
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                MockGame1().main()
        out, err = capsys.readouterr()
        print(err)
    return out


def test_help_main_4(capsys):
    """checking the 'main' function, when the user gives the correct answer,
       skips the task, gives the wrong answer and exits"""
    answers = (i for i in ('1', 's', '12 + 12 + 12 - 12',
                           '3', 'q'))
    with mock.patch.object(sys, 'argv', testargs):
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                MockGame1().main()
        out, err = capsys.readouterr()
        print(err)
        return out


@pytest.mark.xfail
def test_help_main_5(capsys):
    """checking the 'main' function, when the user starts the
       game, gives an empty string and exits"""
    answers = (i for i in ('1', '', 'q'))
    with mock.patch.object(sys, 'argv', testargs):
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            MockGame1().main()
            out, err = capsys.readouterr()
            print(err)
            return out


@pytest.mark.xfail
@pytest.mark.parametrize('test', [('P'), ('C'), ('Q')])
def test_help_main_6(capsys, test):
    """checking the 'main' function when the user types
       capital letters from allowed characters"""
    answers = (i for i in (test, 'q'))
    with mock.patch.object(sys, 'argv', testargs):
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                MockGame1().main()
            out, err = capsys.readouterr()
            print(err)
            return out
