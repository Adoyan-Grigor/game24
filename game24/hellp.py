#!usr/bin/python3
import pytest
import mock
import builtins
import sys
import readline


from game24.gameconsole import GameConsole as gc
from game24.game import Game as gm
from . import calc


class GGameConsole(gc):
    def raw_input_ex(prompt='', default=''):
        '''enhance raw_input to support default input and also flat EOF'''
        try:
            readline.set_startup_hook(lambda: readline.insert_text(default))
            try:
                return input(prompt)
            finally:
                readline.set_startup_hook()

        except EOFError:
            return INPUT_EOF

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


class Play(gc):
    def play(self, x):
        MSG_PLAY_NEW_SET = 'Set %d'
        MSG_PLAY_NEW_HAND = 'Hand %d: %s'
        MSG_MENU_PLAY = '''1. Definitely no solutions (n)
        2. Give me a hint (h)
        3. I gave up, show me the answer (s)
        4. Back to the main menu (b)
        5. Quit the game (q)'''
        MSG_PLAY_NO_ANSWER = 'Seems no solutions'
        INPUT_EOF = '\x00'
        while True:
            if not self.hands:
                self.print_title(MSG_PLAY_NEW_SET % self.seti, dechar='*')

            hand = self.new_hand()
            if not hand:
                # no enough cards for a new hand
                self.print_title(MSG_PLAY_NO_CARDS, dechar='*')
                self.print_result()

                choices = '1n2b3q'
                r = self.ui_menu(MSG_MENU_SET_END, choices)
                if r in '1n':
                    # renew the set
                    self.reset()
                    continue

                elif r in ('2b' + INPUT_EOF):
                    # back to the main menu
                    return

                elif r in '3q':
                    sys.exit(0)

            print()
            if self.showcard:
                sc = hand.str_cards()
            else:
                sc = x 
            self.print_title(MSG_PLAY_NEW_HAND % (len(self.hands), sc),
                                                            dechar='+')
            print()
            while True:
                choices = '1n2h3s4b5q'
                r = self.ui_menu_and_expr(MSG_MENU_PLAY, choices)
                if isinstance(r, calc.Expr):
                    expr = r
                    if expr.value == self.target:
                        hand.solved()
                        if expr not in hand.answers:
                            s = MSG_PLAY_FIND_BUG
                        else:
                            s = MSG_PLAY_RIGHT
                        self.print_title(s)

                        choices = '1t2n3s4q'
                        r = self.ui_menu(MSG_MENU_PLAY_RIGHT, choices, eof=False)
                        if r in '1t':
                            continue
                        elif r in '2n':
                            break
                        elif r in '3s':
                            self.print_title(hand.str_answer())
                        elif r in '4q':
                            sys.exit(0)

                    else:
                        self.print_title(MSG_PLAY_WRONG)
                        continue

                elif r in '1n':
                    # no answer
                    if hand.answers:
                        self.print_title(MSG_PLAY_WRONG)
                        continue
                    else:
                        hand.solved()
                        self.print_title(MSG_PLAY_RIGHT)

                elif r in '2h':
                    # show a hint
                    if hand.answers:
                        hand.hinted()
                        self.print_title(hand.str_hint())
                        continue
                    else:
                        self.print_title(MSG_PLAY_NO_ANSWER)

                elif r in '3s':
                    # show the answer
                    if hand.answers:
                        s = hand.str_answer()
                    else:
                        s = MSG_PLAY_NO_ANSWER
                    self.print_title(s)

                elif r in ('4b' + INPUT_EOF):
                    # back to the main menu
                    return

                elif r in '5q':
                    sys.exit(0)

                # this hand is end
                break
