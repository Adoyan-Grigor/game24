"""hhelp"""
import builtins
import random
import sys
import mock

import pytest


from game24 import gameconsole as gc
from game24.game import Hand

GC = gc.GameConsole
g_c = GC()
testargs = ['']


def help_ui_check_answer(capsys, r_input):
    """a function to calculate an equation from a combination
       of four numbers to get 24"""
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
    """function to calculate all equations from the combination
       of four numbers to get 24"""
    with mock.patch.object(builtins, 'input', lambda _: r_input):
        g_c.ui_check_answer()
        out, err = capsys.readouterr()
        print(err)
    return out


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
    g_g = MockGame0()
    g_g.new_hand()
    answers = (i for i in (test, 'b', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_g.play()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_play_3(capsys, test):
    """checking the play function when the user turns to the program for
       help in solving the equation when there is no solution"""
    g_g = MockGame0()
    g_g.new_hand()
    answers = (i for i in (test, 'b', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_g.play()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_play_4(test):
    """checking the 'play' function when the user
       wants to go to the main menu"""
    g_g = MockGame0()
    g_g.new_hand()
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        return g_g.play()


def test_help_play_5(test):
    """checking the 'play' function when the user wants to log out"""
    g_g = MockGame0()
    g_g.new_hand()
    with mock.patch.object(builtins, 'input', lambda _: test):
        with pytest.raises(SystemExit):
            assert g_g.play().type == SystemExit


def test_help_play_6(test):
    """checking the 'play' function, check if MSG_MENU_SET_END is working"""
    g_g = MockGame0()
    g_g.new_hand()
    answers = (i for i in ('s', 's', 's', 's', 's', 's', 's', 's', 's',
                           's', 's', 's', 's', test, 's', 's', 's', 's',
                           's', 's', 's', 's', 's',
                           's', 's', 's', 's', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        with pytest.raises(SystemExit):
            assert g_g.play().type == SystemExit


def test_help_play_7(test):
    """checking the "play" function, when the user wants to go
       to the main menu via MSG_MENU_SET_END"""
    g_g = MockGame0()
    g_g.new_hand()
    answers = (i for i in ('s', 's', 's', 's', 's',
                           's', 's', 's', 's', 's',
                           's', 's', 's', test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_g.play()


def test_help_play_8(test):
    """checking the "play" function, when the user wants to
       exit the program via MSG_MENU_SET_END"""
    g_g = MockGame0()
    g_g.new_hand()
    answers = (i for i in ('s', 's', 's', 's', 's',
                           's', 's', 's', 's', 's',
                           's', 's', 's', test))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        with pytest.raises(SystemExit):
            assert g_g.play().type == SystemExit


def test_help_play_9(capsys):
    """checking the "play" function, when hand is empty"""
    g_g = MockGameNone()
    g_g.new_hand()
    answers = (i for i in ('1', 'b', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_g.play()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_play_10(capsys):
    """checking the "play" function, when the user has correctly
       solved the same equation twice"""
    g_g = MockGame0()
    answers = (i for i in ('s', 's', 's', 's', 's',
                           '6 + 6 + 6 + 6', 't',
                           '6 + 6 + 6 + 6', 'n',
                           's', 's', 's', 's', 's',
                           's', 's', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        with pytest.raises(SystemExit):
            g_g.play()
    out, err = capsys.readouterr()
    print(err)
    return out


def test_help_play_11(capsys):
    """checking the "play" function, when the user correctly solved
       the same equation twice, but in different ways"""
    g_g = MockGame0()
    answers = (i for i in ('s', 's', 's', 's', 's',
                           '6 + 6 + 6 + 6', 't',
                           '6 * 6 - 6 - 6', 'n',
                           's', 's', 's', 's', 's',
                           's', 's', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        with pytest.raises(SystemExit):
            g_g.play()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_play_12(capsys):
    """checking the "play" function, when the user skips the task
       after receiving help from the program"""
    g_g = MockGame0()
    answers = (i for i in ('h', 's', 'h', 's', 'h', 's', 'h', 's', 'h',
                           's', 'h', 's', 'h', 's', 'h', 's', 'h', 's',
                           'h', 's', 'h', 's', 'h', 's',
                           'h', 's', 'b', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_g.play()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_play_13(capsys):
    """checking the "play" function, when the user asks for the rest
       of the answer options after the correct answer"""
    g_g = MockGame5()
    answers = (i for i in ('12 + 12 + 12 - 12', 's', 'b', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_g.play()
    out, err = capsys.readouterr()
    print(err)
    return out


def test_help_play_14(test):
    """checking the "play" function, when, after the correct answer,
       the user wants to exit the program"""
    g_g = MockGame5()
    answers = (i for i in ('12 + 12 + 12 - 12', test))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        with pytest.raises(SystemExit):
            assert g_g.play().type == SystemExit


def test_help_play_15(capsys, test):
    """checking the 'play' function when the program
       receives an incorrect response"""
    g_g = MockGame5()
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        with pytest.raises(SystemExit):
            g_g.play()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_play_16(capsys, test):
    """checking the function 'play' when the program gets the correct
       equation, but more numbers are used than allowed"""
    g_g = MockGame5()
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        with pytest.raises(SystemExit):
            g_g.play()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_play_17(capsys):
    """checking the 'play' function when the user enters an empty string"""
    g_g = MockGame5()
    answers = (i for i in ('', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        with pytest.raises(SystemExit):
            g_g.play()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_play_18(capsys, test):
    """checking the 'play' function when the user enters a
       wrong answer twice and exits"""
    g_g = MockGame5()
    answers = (i for i in (test, test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        with pytest.raises(SystemExit):
            g_g.play()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_play_19(capsys):
    """checking the "main" function when the user skips a problem,
    solves the equation correctly, cannot solve the same equation
    again, asks for help, solves the equation correctly, skips the
    remaining problems, and quits the game"""
    g_g = MockGame1()
    answers = (i for i in ('s', '12 + 12 + 12 - 12',
                           't', '12 + 12 + 12 + 12',
                           'h', '12 + 12 * 12 / 12',
                           's', 's', 's', 's', 's', 's',
                           's', 's', 's', 's', 's', 's', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        with pytest.raises(SystemExit):
            g_g.play()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_play_20(capsys):
    """checking the 'play' function, when the user skips the task,
       asks the program for help twice, gives the correct answer,
       skips the rest of the tasks and exits"""
    g_g = MockGame1()
    answers = (i for i in ('s', 'h', 'h',
                           '12 + 12 + 12 - 12',
                           's', 's', 's', 's', 's', 's',
                           's', 's', 's', 's', 's', 's', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        with pytest.raises(SystemExit):
            g_g.play()
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


def test_help_main_5(capsys):
    """checking the 'main' function when the user starts the game and correctly
       solves the equation but using more numbers than allowed"""
    answers = (i for i in ('1', '12 + 12 + 12 + 12 - 12', 'q'))
    with mock.patch.object(sys, 'argv', testargs):
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                MockGame5().main()
            out, err = capsys.readouterr()
            print(err)
            return out


def test_help_main_6(capsys):
    """checking the 'main' function, when the user starts the
       game, gives an empty string and exits"""
    answers = (i for i in ('1', '', 'q'))
    with mock.patch.object(sys, 'argv', testargs):
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                MockGame1().main()
            out, err = capsys.readouterr()
            print(err)
            return out


def test_help_main_7(capsys, test):
    """checking the 'main' function when the user types
       capital letters from allowed characters"""
    answers = (i for i in (test, 'q'))
    with mock.patch.object(sys, 'argv', testargs):
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            MockGame1().main()
            out, err = capsys.readouterr()
            print(err)
            return out


def test_help_main_8(capsys):
    """checking the 'main' function when the user starts
      the game, enters a blank line and exits"""
    answers = (i for i in ('1', '', 'q'))
    with mock.patch.object(sys, 'argv', testargs):
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                MockGame1().main()
            out, err = capsys.readouterr()
            print(err)
            return out


def test_help_main_9(capsys, test):
    """checking the 'main' function when the user starts the
       game first gives an incorrect answer, then he gives a
       correct answer and exits"""
    answers = (i for i in ('1', test, '12 + 12 + 12 - 12',
                           'n', 'q'))
    with mock.patch.object(sys, 'argv', testargs):
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                MockGame5().main()
            out, err = capsys.readouterr()
            print(err)
            return out


def test_help_main_10(capsys):
    """checking the 'main' function, when the user starts
       the game, gives the wrong answer several times and exits"""
    answers = (i for i in ('1', '12 + 12 + 12 + 12',
                           '12 * 12 * 12 * 12', '12 + 12 - 12 - 12',
                           '12 / 12 * 12 * 12', '12 - 12 * 12 - 12', 'q'))
    with mock.patch.object(sys, 'argv', testargs):
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                MockGame5().main()
            out, err = capsys.readouterr()
            print(err)
            return out


def test_help_main_11_12(capsys, test):
    """checking the 'main' function when the user gives unauthorized input"""
    answers = (i for i in ('1', test, 'q'))
    with mock.patch.object(sys, 'argv', testargs):
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                MockGame5().main()
            out, err = capsys.readouterr()
            print(err)
            return out


def test_help_main_13(capsys, test):
    """checking the "main" function when the user gives
       an unauthorized input in the main menu"""
    answers = (i for i in (test, 'q'))
    with mock.patch.object(sys, 'argv', testargs):
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            MockGame5().main()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_main_14(capsys):
    """checking the 'main' function, when the user starts the game,
    skips the task, solves the equation correctly, fails to solve
    the same equation again, asks for help, solves the equation
    correctly, skips the remaining tasks and exits the game"""
    answers = (i for i in ('1', 's', '12 + 12 + 12 - 12',
                           't', '12 + 12 + 12 + 12',
                           'h', '12 + 12 * 12 / 12',
                           's', 's', 's', 's', 's', 's',
                           's', 's', 's', 's', 's', 's', 'q'))
    with mock.patch.object(sys, 'argv', testargs):
        with mock.patch.object(builtins, 'input', lambda _: next(answers)):
            with pytest.raises(SystemExit):
                MockGame1().main()
            out, err = capsys.readouterr()
            print(err)
            return out


def test_help_ui_menu_and_expr_1(test, menu, choices):
    """checking the function 'ui_emnu_and_expr' when we give an
       equation that consists of the allowed numbers"""
    g_g = MockGame5()
    g_g.new_hand()
    with mock.patch.object(builtins, 'input', lambda _: test):
        return g_g.ui_menu_and_expr(menu, choices,
                                    eof=True)


def test_help_ui_menu_and_expr_2(test, menu, choices):
    """checking the ui_emnu_and_expr function when
       we give characters from 'choices'"""
    g_g = MockGame5()
    g_g.new_hand()
    with mock.patch.object(builtins, 'input', lambda _: test):
        return g_g.ui_menu_and_expr(menu, choices, eof=True)


def test_help_ui_menu_and_expr_negative_1(test, menu, choices):
    """checking the function 'ui_emnu_and_expr' when the program gets
       the correct equation, but more numbers are used than allowed"""
    g_g = MockGame5()
    g_g.new_hand()
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        return g_g.ui_menu_and_expr(menu, choices)


def test_help_ui_menu_and_expr_negative_2(capsys, test, menu, choices):
    """checking the ui_emnu_and_expr function
       when we give unresolved characters"""
    g_g = MockGame5()
    g_g.new_hand()
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_menu_and_expr(menu, choices)
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_ui_menu_and_expr_negative_3(capsys, test, menu, choices):
    """checking the ui_emnu_and_expr function when
       we give numbers not from 'choices'"""
    g_g = MockGame5()
    g_g.new_hand()
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_g.ui_menu_and_expr(menu, choices)
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_ui_menu_and_expr_negative_4(capsys, menu, choices):
    """if you give 'ui_menu_and_expr' an empty string"""
    g_g = MockGame5()
    g_g.new_hand()
    answers = (i for i in ('', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_g.ui_menu_and_expr(menu, choices)
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_ui_menu_and_expr_negative_5(capsys, test, menu, choices):
    """if you give ui_menu_and_expr invalid input but found in 'choices'"""
    g_g = MockGame5()
    g_g.new_hand()
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_g.ui_menu_and_expr(menu, choices)
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_ui_menu_and_expr_negative_6(capsys, test, menu, choices):
    """checking the 'ui_menu_and_expr' function when the
       program receives large letters of allowed characters"""
    g_g = MockGame5()
    g_g.new_hand()
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_g.ui_menu_and_expr(menu, choices)
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_ui_menu(test):
    """checking the 'ui_menu' function when the program
       receives characters from 'choises'"""
    menu = '1. Play (p)\n2. Check answer (c)\n3. Quit (q)'
    choices = '1p2c3q'
    with mock.patch.object(builtins, 'input', lambda _: test):
        return g_c.ui_menu(menu, choices, eof=True)


def test_help_ui_menu_negative_1(test, capsys):
    """checking the 'ui_menu' function when the program
       receives unresolved characters"""
    menu = '1. Play (p)\n2. Check answer (c)\n3. Quit (q)'
    choices = '1p2c3q'
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_menu(menu, choices, eof=True)
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_ui_menu_negative_2(test, capsys):
    """checking the 'ui_menu' function when the program gets
       capital letters from the 'choices' letters"""
    menu = '1. Play (p)\n2. Check answer (c)\n3. Quit (q)'
    choices = '1p2c3q'
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_menu(menu, choices, eof=True)
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_ui_menu_negative_3(capsys):
    """checking the 'ui_menu' function when the program
       receives an empty string"""
    menu = '1. Play (p)\n2. Check answer (c)\n3. Quit (q)'
    choices = '1p2c3q'
    answers = (i for i in ('', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_menu(menu, choices, eof=True)
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_ui_check_answer(capsys, test_input):
    """checking the ui_check_answer function when the program
      receives the usual input for the function"""
    with mock.patch.object(builtins, 'input', lambda _: test_input):
        GC().ui_check_answer()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_ui_check_answer_negative(capsys, test):
    """checking function 'ui_check_answer' when
       program receives invalid input"""
    answers = (i for i in (test, '1 1 1 1'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_check_answer()
        out, err = capsys.readouterr()
        print(err)
        return out


def test_help_print_result(capsys):
    """test of the 'print_result' function"""
    c_g = MockGamePrintresult()
    c_g.new_hand()
    c_g.print_result()
    out, err = capsys.readouterr()
    print(err)
    return out
