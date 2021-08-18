#!usr/bin/python3
import pytest

from .gameconsole import GameConsole as gm


@pytest.mark.parametrize('title, result', 
                         [('12 + 12 + 12 - 12\n12 × (12 + 12) ÷ 12\n12 + 12 × 12 ÷ 12',
                         '\n12 + 12 + 12 - 12\n12 × (12 + 12) ÷ 12\n12 + 12 × 12 ÷ 12\n\n'),
                         ('4 × (1 + 2 + 3)\n1 × 2 × 3 × 4\n(1 + 3) × (2 + 4)',
                         '\n4 × (1 + 2 + 3)\n1 × 2 × 3 × 4\n(1 + 3) × (2 + 4)\n\n')])
def test_print_title(capsys, title, result):
    gm.print_title(title)
    out, err = capsys.readouterr()
    assert out == result


@pytest.mark.parametrize('title, result', [(None, None), ('4 × (5 + 9 - 8)\n8 + 4 × (9 - 5)',
                         '4 × (5 + 9 - 8)\n8 + 4 × (9 - 5)')])
def test_print_title_negativ(capsys, title, result):
    gm.print_title(title)
    out, err = capsys.readouterr()
    assert out != result

@pytest.mark.xfail
@pytest.mark.parametrize('input_output', [('name'), ('HeLlO'), (''), ('12')])
def test_raw_input_ex(input_output):
    with mock.patch.object(builtins, 'input', lambda _: input_output):
       assert gm.raw_input_ex() == input_output


@pytest.mark.xfail
@pytest.mark.parametrize('r', [('1'), ('2'), ('3'), ('p'), ('c'), ('q')])
def test_ui_menu(r):
    with mock.patch.object(builtins, 'input', lambda _: r):
       assert gm.ui_menu(menu, choices, eof = True) == r

