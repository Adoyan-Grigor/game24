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
