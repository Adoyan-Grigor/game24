#!usr/bin/python3
import pytest
import mock
import builtins
import sys


from game24.gameconsole import GameConsole as gc
from game24.game import Game as gm
from . import calc

def hellp_ui_check_answer(capsys, r):
    gg = gc()
    result = ''
    final_result = ''
    with mock.patch.object(builtins, 'input', lambda _: r):
        gg.ui_check_answer()
        out, err = capsys.readouterr()
        if out == '\nSeems no solutions\n\n':
            final_result = 'n'
        else:
            for i in out[1: ]:
                if i == '\n':
                    break
                result += i
            for i in result:
                if i == '×':
                    final_result += '*'
                elif i == '÷':
                    final_result += '/'
                else:
                    final_result += i
        return final_result


def hellp_new_hand():
    gg = gc()
    res_hand = ''
    hand = gg.new_hand()
    hand_ints = hand.integers
    for i in hand_ints:
        res_hand += str(i) + ' '
    return res_hand


def hellp_new_hand_cards(cards):
    llist = []
    for i in range(len(cards[44: 48])):
        llist.append(cards[i])
    cards = []
    while len(cards) < 53:
        for i in llist:
            cards.append(i)
    return cards
