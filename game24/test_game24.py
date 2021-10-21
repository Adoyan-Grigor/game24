"""test_game24"""
import builtins
import sys

import mock

import pytest


from game24 import calc
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
    print(err)
    assert out == result


@pytest.mark.parametrize('title, result', [(None, None),
                         ('4 × (5 + 9 - 8)\n8 + 4 × (9 - 5)',
                         '4 × (5 + 9 I- 8)\n8 + 4 × (9 - 5)')])
def test_print_title_negativie(capsys, title, result):
    """negative test of print_title function"""
    GC.print_title(title)
    out, err = capsys.readouterr()
    print(err)
    assert out != result


@pytest.mark.parametrize('input_output', [('name'), ('HeLlO'), (''), ('12')])
def test_raw_input_ex(input_output):
    """test of the 'raw_input_ex' function"""
    with mock.patch.object(builtins, 'input', lambda _: input_output):
        assert GC().raw_input_ex() == input_output


gc.GameConsole.raw_input_ex = hl.GGameConsole.raw_input_ex
GC = hl.GGameConsole


@pytest.mark.parametrize('test', [('1'), ('2'), ('3'),
                                  ('p'), ('c'), ('q')])
def test_ui_menu(test):
    """checking the 'ui_menu' function when the program
       receives characters from 'choises'"""
    g_c = GC()
    menu = '1. Play (p)\n2. Check answer (c)\n3. Quit (q)'
    choices = '1p2c3q'
    with mock.patch.object(builtins, 'input', lambda _: test):
        assert g_c.ui_menu(menu, choices, eof=True) == test


@pytest.mark.parametrize('test', [('w'), ('T'), ('#'),
                                  ('ccs'), ('8'), ('78')])
def test_ui_menu_negative_1(test, capsys):
    """checking the 'ui_menu' function when the program
       receives unresolved characters"""
    g_c = GC()
    menu = '1. Play (p)\n2. Check answer (c)\n3. Quit (q)'
    choices = '1p2c3q'
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_menu(menu, choices, eof=True)
        out, err = capsys.readouterr()
        print(err)
        assert 'Invalid input!' in out


@pytest.mark.xfail
@pytest.mark.parametrize('test', [('P'), ('C'), ('Q')])
def test_ui_menu_negative_2(test, capsys):
    """checking the 'ui_menu' function when the program gets
       capital letters from the 'choices' letters"""
    g_c = GC()
    menu = '1. Play (p)\n2. Check answer (c)\n3. Quit (q)'
    choices = '1p2c3q'
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_menu(menu, choices, eof=True)
        out, err = capsys.readouterr()
        print(err)
        assert 'Invalid input' in out


@pytest.mark.xfail
def test_ui_menu_negative_3(capsys):
    """checking the 'ui_menu' function when the program
       receives an empty string"""
    g_c = GC()
    menu = '1. Play (p)\n2. Check answer (c)\n3. Quit (q)'
    choices = '1p2c3q'
    answers = (i for i in ('', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_menu(menu, choices, eof=True)
        out, err = capsys.readouterr()
        print(err)
        assert 'Invalid input!' in out


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
    """checking the ui_check_answer function when the program
      receives the usual input for the function"""
    with mock.patch.object(builtins, 'input', lambda _: test_input):
        GC().ui_check_answer()
        out, err = capsys.readouterr()
        print(err)
        assert out, err == result


@pytest.mark.parametrize('test', [('1 1 1'), ('adwada'),
                                  ('/'), ('1111'), ('P'), ('')])
def test_ui_check_answer_negative(capsys, test):
    """checking function 'ui_check_answer' when
       program receives invalid input"""
    g_c = GC()
    answers = (i for i in (test, '1 1 1 1'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_check_answer()
        out, err = capsys.readouterr()
        print(err)
        assert 'Invalid input' in out, err


@pytest.mark.parametrize('test', [('12 + 12 + 12 - 12'),
                                  ('(12 + 12) / 12 * 12'),
                                  ('12 * 12 / 12 + 12')])
def test_ui_menu_and_expr_1(test):
    """checking the function 'ui_emnu_and_expr' when we give an
       equation that consists of the allowed numbers"""
    menu = '''1. Definitely no solutions (n)\n2. Give me a hint (h)
3. I gave up, show me the answer (s)
4. Back to the main menu (b)
5. Quit the game (q)'''
    choices = '1n2h3s4b5q'
    g_c = hl.MockGame5()
    g_c.new_hand()
    with mock.patch.object(builtins, 'input', lambda _: test):
        assert g_c.ui_menu_and_expr(menu, choices,
                                    eof=True) == calc.parse(test)


@pytest.mark.parametrize('test', [('1'), ('n'), ('2'), ('h'), ('3'), ('s'),
                                  ('4'), ('b'), ('5'), ('q')])
def test_ui_menu_and_expt_2(test):
    """checking the ui_emnu_and_expr function when
       we give characters from 'choices'"""
    menu = '''1. Definitely no solutions (n)\n2. Give me a hint (h)
3. I gave up, show me the answer (s)
4. Back to the main menu (b)
5. Quit the game (q)'''
    choices = '1n2h3s4b5q'
    g_c = hl.MockGame5()
    g_c.new_hand()
    with mock.patch.object(builtins, 'input', lambda _: test):
        assert g_c.ui_menu_and_expr(menu, choices, eof=True) == test


@pytest.mark.parametrize('test', [('12 - 12 + 12 + 12 - 12 + 12'),
                                  ('12 + 12 * 12 / 12 + 12 - 12'),
                                  ('12 + 12 + 12 + 12 - 12 - 12')])
def test_ui_menu_and_expr_negative_1(test):
    """checking the function 'ui_emnu_and_expr' when the program gets
       the correct equation, but more numbers are used than allowed"""
    g_c = hl.MockGame5()
    menu = '''1. Definitely no solutions (n)\n2. Give me a hint (h)
3. I gave up, show me the answer (s)
4. Back to the main menu (b)
5. Quit the game (q)'''
    choices = '1n2h3s4b5q'
    g_c.new_hand()
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        assert g_c.ui_menu_and_expr(menu, choices) == calc.parse(test)


@pytest.mark.parametrize('test', [('a'), ('A'), ('aA'),
                                  ('ggs'), ('AFAW'), ('ASffdS'),
                                  ('8s'), ('8S'), ('4dsf'),
                                  ('3FSE'), ('4GdsAd')])
def test_ui_menu_and_expr_negative_2(capsys, test):
    """checking the ui_emnu_and_expr function
       when we give unresolved characters"""
    g_c = hl.MockGame5()
    menu = '''1. Definitely no solutions (n)\n2. Give me a hint (h)
3. I gave up, show me the answer (s)
4. Back to the main menu (b)
5. Quit the game (q)'''
    choices = '1n2h3s4b5q'
    g_c.new_hand()
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_menu_and_expr(menu, choices)
        out, err = capsys.readouterr()
        print(err)
        check_symbol = hl.help_letters_and_numbers(test)
        assert 'Invalid character: ' + check_symbol in out


@pytest.mark.parametrize('test', [('6'), ('7'), ('67'), ('12'), ('12345')])
def test_ui_menu_and_expr_negative_3(capsys, test):
    """checking the ui_emnu_and_expr function when
       we give numbers not from 'choices'"""
    g_c = hl.MockGame5()
    menu = '''1. Definitely no solutions (n)\n2. Give me a hint (h)
3. I gave up, show me the answer (s)
4. Back to the main menu (b)
5. Quit the game (q)'''
    choices = '1n2h3s4b5q'
    g_c.new_hand()
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_menu_and_expr(menu, choices)
        out, err = capsys.readouterr()
        print(err)
        assert 'Invalid expression: operator missed' in out


@pytest.mark.xfail
def test_ui_menu_and_expr_negative_4(capsys):
    """if you give 'ui_menu_and_expr' an empty string"""
    g_c = hl.MockGame5()
    menu = '''1. Definitely no solutions (n)\n2. Give me a hint (h)
3. I gave up, show me the answer (s)
4. Back to the main menu (b)
5. Quit the game (q)'''
    choices = '1n2h3s4b5q'
    g_c.new_hand()
    answers = (i for i in ('', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_menu_and_expr(menu, choices)
        out, err = capsys.readouterr()
        print(err)
        assert """Invalid expression: operator missed
""" in out or 'Invalid character:' in out


@pytest.mark.xfail
@pytest.mark.parametrize('test', [('1n'), ('n2'), ('2h'), ('h3'),
                                  ('3s'), ('s4'), ('4b'), ('b5'),
                                  ('5q'), ('1n2h3s4b5q')])
def test_ui_menu_and_expr_negative_5(capsys, test):
    """if you give ui_menu_and_expr invalid input but found in 'choices'"""
    g_c = hl.MockGame5()
    menu = '''1. Definitely no solutions (n)\n2. Give me a hint (h)
3. I gave up, show me the answer (s)
4. Back to the main menu (b)
5. Quit the game (q)'''
    choices = '1n2h3s4b5q'
    g_c.new_hand()
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_menu_and_expr(menu, choices)
        out, err = capsys.readouterr()
        print(err)
        check_symbol = hl.help_letters_and_numbers(test)
        assert 'Invalid character: ' + check_symbol in out


@pytest.mark.xfail
@pytest.mark.parametrize('test', [('N'), ('H'), ('S'), ('B'), ('Q')])
def test_ui_menu_and_expr_negative_6(capsys, test):
    """checking the 'ui_menu_and_expr' function when the
       program receives large letters of allowed characters"""
    g_c = hl.MockGame5()
    menu = '''1. Definitely no solutions (n)\n2. Give me a hint (h)
3. I gave up, show me the answer (s)
4. Back to the main menu (b)
5. Quit the game (q)'''
    choices = '1n2h3s4b5q'
    g_c.new_hand()
    answers = (i for i in (test, 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.ui_menu_and_expr(menu, choices)
        out, err = capsys.readouterr()
        print(err)
        assert 'Invalid character: ' + test in out


def test_print_result(capsys):
    """test of the 'print_result' function"""
    g_c = hl.MockGamePrintresult()
    g_c.new_hand()
    g_c.print_result()
    out, err = capsys.readouterr()
    print(err)
    assert """Total 5 hands solved
Total 4 hands solved with hint
Total 4 hands failed to solve""" in out


@pytest.mark.parametrize('test', [('1'), ('p')])
def test_main_gc_1(test):
    """checking the "main" function in the 'GameConsole'
       class when the user wants to start the game"""
    g_c = GC()
    answers = (i for i in (test, 'b', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.main()


@pytest.mark.parametrize('test', [('2'), ('c')])
def test_main_gc_2(test):
    """checking the 'main' function from the 'GameConsole' class when
       the user wants to use the 'ui_check_answer' function"""
    g_c = GC()
    answers = (i for i in (test, '1 1 1 1', 'q'))
    with mock.patch.object(builtins, 'input', lambda _: next(answers)):
        g_c.main()


@pytest.mark.parametrize('test', [('3'), ('q')])
def test_main_gc_3(test):
    """checking the 'main' function from the 'GameConsole' class when
       the user wants to exit the program"""
    g_c = GC()
    with mock.patch.object(builtins, 'input', lambda _: test):
        g_c.main()


@pytest.mark.parametrize('test, result', [('12 + 12 + 12 - 12',
                                           '12 + 12 + 12 - 12\n'),
                                          ('12 + 12 + (12 - 12)',
                                           '12 + 12 + 12 - 12\n'),
                                          ('5 + 5 + 5 + 5',
                                           '5 + 5 + 5 + 5\n'),
                                          ('13 + (10 * 12) / 2',
                                           '13 + 10 × 12 ÷ 2\n'),
                                          ('12 + 12 + 12',
                                           '12 + 12 + 12\n')])
def test_parse(test, result, capsys):
    """test of the 'parse' function"""
    print(calc.parse(test))
    out, err = capsys.readouterr()
    print(err)
    assert out == result


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
