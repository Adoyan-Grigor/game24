#!usr/bin/python3
import pytest
import mock
import builtins
import sys
import readline


from game24.gameconsole import GameConsole as gc
from game24.game import Hand
from game24.game import Game as gm
from . import calc


class GGameConsole(gc):
    def raw_input_ex(prompt='', default=''):
        '''enhance raw_input to support default input and also flat EOF'''
        return input(prompt)

gc = GGameConsole



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
            for i in out:
                if i == '\n':
                    break
                elif i == '×':
                    final_result += '*'
                elif i == '÷':
                    final_result += '/'
                else:
                    final_result += i
        return final_result


def hellp_new_hand_cards(cards):
    llist = []
    for i in range(len(cards[44: 48])):
        llist.append(cards[i])
    cards = []
    while len(cards) < 53:
        for i in llist:
            cards.append(i)
    return cards

def hellp_res_print():
    return '''Good Job!
\n--------------------------------------------------
1. Try other solutions (t)
2. Next hand (n)\n3. Show me the answers (s)
4. Quit the game (q)
--------------------------------------------------
\n--------------------------------------------------
1. Definitely no solutions (n)
2. Give me a hint (h)
3. I gave up, show me the answer (s)
4. Back to the main menu (b)
5. Quit the game (q)
--------------------------------------------------
\nGood Job!'''


class MockGame_1(gc, Hand):
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


class MockGame_5(gc, Hand):
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


def help_letters_and_numbers(a):
    res = ''
    for i in a:
        if i not in '123456789':
            return i
    return a
