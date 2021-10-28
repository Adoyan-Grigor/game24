"""test_game24_play"""
import pytest


from game24 import gameconsole as gc
from game24.tests import hhelp as hl


def test_play_1(capsys):
    """checking the 'play' function when the program skips all tasks"""
    assert """1. One more set (n)
2. Back to the main menu (b)
3. Quit the game (q)""" in hl.test_help_play_1(capsys)


@pytest.mark.parametrize('test', [('1'), ('n')])
def test_play_2(capsys, test):
    """checking the 'play' function when the program responds
       correctly that there is no correct answer"""
    assert 'Good Job' in hl.test_help_play_2(capsys, test)


@pytest.mark.parametrize('test', [('2'), ('h')])
def test_play_3(capsys, test):
    """checking the play function when the user turns to the program for
       help in solving the equation when there is no solution"""
    assert "Seems no solutions" in hl.test_help_play_3(capsys, test)


@pytest.mark.parametrize('test', [('4'), ('b')])
def test_play_4(test):
    """checking the 'play' function when the user
       wants to go to the main menu"""
    hl.test_help_play_4(test)


@pytest.mark.parametrize('test', [('5'), ('q')])
def test_play_5(test):
    """checking the 'play' function when the user wants to log out"""
    hl.test_help_play_5(test)


@pytest.mark.parametrize('test', [('1'), ('n')])
def test_play_6(test):
    """checking the 'play' function, check if MSG_MENU_SET_END is working"""
    hl.test_help_play_6(test)


@pytest.mark.parametrize('test', [('2'), ('b')])
def test_play_7(test):
    """checking the "play" function, when the user wants to go
       to the main menu via MSG_MENU_SET_END"""
    hl.test_help_play_7(test)


@pytest.mark.parametrize('test', [('3'), ('q')])
def test_play_8(test):
    """checking the "play" function, when the user wants to
       exit the program via MSG_MENU_SET_END"""
    hl.test_help_play_8(test)


def test_play_9(capsys):
    """checking the "play" function, when hand is empty"""
    assert 'Set end, your result' in hl.test_help_play_9(capsys)


def test_play_10(capsys):
    """checking the "play" function, when the user has correctly
       solved the same equation twice"""
    assert """Total 1 hands solved
Total 0 hands solved with hint
Total 12 hands failed to solve""" in hl.test_help_play_10(capsys)


def test_play_11(capsys):
    """checking the "play" function, when the user correctly solved
       the same equation twice, but in different ways"""
    assert """Total 1 hands solved
Total 0 hands solved with hint
Total 12 hands failed to solve""" in hl.test_help_play_11(capsys)


def test_play_12(capsys):
    """checking the "play" function, when the user skips the task
       after receiving help from the program"""
    assert """Total 0 hands solved
Total 0 hands solved with hint
Total 13 hands failed to solve""" in hl.test_help_play_12(capsys)


def test_play_13(capsys):
    """checking the "play" function, when the user asks for the rest
       of the answer options after the correct answer"""
    check = hl.help_ui_check_answer_all(capsys, '12 12 12 12')
    assert check in hl.test_help_play_13(capsys)


@pytest.mark.parametrize('test', [('4'), ('q')])
def test_play_14(test):
    """checking the 'play' function when the program
       receives an incorrect response"""
    hl.test_help_play_14(test)


@pytest.mark.parametrize('test', [('12 + 12 + 12 + 12'), ('12 - 12 * 12 / 12'),
                                  ('12 - 12 - 12 + 12')])
def test_play_15(capsys, test):
    """checking the 'play' function when the program
       receives an incorrect response"""
    assert gc.MSG_PLAY_WRONG in hl.test_help_play_15(capsys, test)


@pytest.mark.parametrize('test', [('12 - 12 + 12 + 12 - 12 + 12'),
                                  ('12 + 12 * 12 / 12 + 12 - 12'),
                                  ('12 + 12 + 12 + 12 - 12 - 12')])
def test_play_16(capsys, test):
    """checking the function 'play' when the program gets the correct
       equation, but more numbers are used than allowed"""
    assert gc.MSG_MENU_PLAY_RIGHT not in hl.test_help_play_16(capsys, test)


def test_play_17(capsys):
    """checking the 'play' function when the user enters an empty string"""
    assert gc.MSG_INVALID_INPUT in hl.test_help_play_17(capsys)


@pytest.mark.parametrize('test', [('12 + 12 + 12 + 12'), ('12 - 12 * 12 / 12'),
                                  ('12 - 12 - 12 + 12')])
def test_play_18(capsys, test):
    """checking the 'play' function when the user enters a
       wrong answer twice and exits"""
    assert gc.MSG_MENU_PLAY_RIGHT not in hl.test_help_play_18(capsys,
                                                              test)


@pytest.mark.xfail
def test_play_19(capsys):
    """checking the "main" function when the user skips a problem,
    solves the equation correctly, cannot solve the same equation
    again, asks for help, solves the equation correctly, skips the
    remaining problems, and quits the game"""
    check = """Total 1 hands solved
Total 0 hands solved with hint
Total 11 hands failed to solve"""
    assert check in hl.test_help_play_19(capsys)


def test_play_20(capsys):
    """checking the 'play' function, when the user skips the task,
       asks the program for help twice, gives the correct answer,
       skips the rest of the tasks and exits"""
    check = """Total 0 hands solved
Total 1 hands solved with hint
Total 12 hands failed to solve"""
    assert check in hl.test_help_play_20(capsys), hl.test_help_play_20(capsys)
