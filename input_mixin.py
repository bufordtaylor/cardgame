from colors import *
import os

from deck import (
    CARD_TYPE_MONSTER,
    CARD_TYPE_HERO,
    CARD_TYPE_PERSISTENT,
)

CANNOT_KILL_THIS_CARD = 'You cannot kill this card, it is a %s'
NOT_ENOUGH_KILL = 'Not enough kill'
NOT_ENOUGH_BUY = 'Not enough buy'
INVALID_SELECTION = 'No idea what you are doing, but it is wrong.'
NO_CARDS = 'You have no cards left. You should end your turn'
INVALID_CARD = 'Invalid card. Try a number 0 - %s. EX: c3 for the [c]ard with the 3 in front of it'

class InputMixin(object):

    def computer_inputs(self):
        print 'computer is doing shit'
        return

    def sanitize_selection(self, selection):
        return card_played

    def handle_gamephand_selection(self, selection):
        try:
            card_idx = int(selection[1:])
            card = self.phand[card_idx]
        except (ValueError, IndexError):
            card = None
            os.system(['clear','cls'][os.name == 'nt'])

        if not card:
            print_red(INVALID_CARD % (len(self.phand) - 1))
            return self.handle_inputs()
        os.system(['clear','cls'][os.name == 'nt'])

        if card.card_type == CARD_TYPE_MONSTER:
            if self.active_player.killing_power >= card.kill:
                self.active_player.points += card.instant_worth
                self.active_player.killing_power -= card.kill
                print_blue('KILLED CARD %s' % card)
            else:
                print_red(NOT_ENOUGH_KILL)
                return self.handle_inputs()
        else:
            if self.active_player.buying_power >= card.buy:
                self.active_player.discard.append(card)
                self.active_player.buying_power -= card.buy
                print_blue('BOUGHT CARD %s' % card)
            else:
                print_red(NOT_ENOUGH_BUY)
                return self.handle_inputs()

    def handle_kill_selection(self, selection):
        try:
            card_idx = int(selection[1:])
            card = self.hand[card_idx]
        except (ValueError, IndexError):
            card = None
            os.system(['clear','cls'][os.name == 'nt'])

        if not card:
            print_red(INVALID_CARD % (len(self.hand) - 1))
            return self.handle_inputs()
        if card.card_type != CARD_TYPE_MONSTER:
            print_red(CANNOT_KILL_THIS_CARD % card.card_type_string)
            return self.handle_inputs()
        os.system(['clear','cls'][os.name == 'nt'])

        if self.active_player.killing_power >= card.kill:
            self.active_player.points += card.instant_worth
            self.discard_card(card_idx)
            self.draw_card()
        else:
            print_red(NOT_ENOUGH_KILL)
        print_blue('KILLED CARD %s' % card)

    def handle_card_selection(self, selection):
        try:
            card_played = self.active_player.get_card(int(selection[1:]))
        except (ValueError, IndexError):
            card_played = None
            os.system(['clear','cls'][os.name == 'nt'])

        if not card_played:
            if len(self.active_player.hand) == 0:
                print_red(NO_CARDS)
            else:
                print_red(INVALID_CARD % (len(self.active_player.hand) - 1))
            return self.handle_inputs()
        os.system(['clear','cls'][os.name == 'nt'])

        self.play_card(card_played)
        self.played_user_cards.append(card_played)
        print_blue('PLAYED CARD %s' % card_played)

    def handle_inputs(self):
        if self.active_player.is_computer:
            return self.computer_inputs()

        self.print_phand()
        self.print_hand()
        self.print_user_hand()
        self.print_user_played_cards()
        self.print_user_status()
        selection = raw_input(
            'play [c]ard - game [p]ers - [k]ill enemy - [b]uy heroes - [e]nd turn:\n'
        )
        if selection == 'e':
            self.active_player.end_turn()
            return
        elif selection.startswith('c'):
            return self.handle_card_selection(selection)
        elif selection.startswith('k'):
            return self.handle_kill_selection(selection)
        elif selection.startswith('p'):
            return self.handle_gamephand_selection(selection)
        else:
            print_red(INVALID_SELECTION)
        print_blue('Press anykey to continue')
        raw_input()
