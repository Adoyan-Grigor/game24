"""hhelp"""
import mock
import builtins
import random


from game24.gameconsole import GameConsole as gc
from game24.game import Hand
from game24.game import Game as gm
from game24 import calc


class GGameConsole(gc):
    """analogue of the 'GameConsole' class with the modified
       'raw_input_ex' function for normal test work"""
    @staticmethod
    def raw_input_ex(prompt='', default=''):
        '''enhance raw_input to support default input and also flat EOF'''
        return input(prompt)


GC = GGameConsole


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
