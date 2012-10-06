from colors import *
import os


INVALID_SELECTION = 'No idea what you are doing, but it is wrong.'
NO_CARDS = 'You have no cards left. You should end your turn'
INVALID_CARD = 'Invalid card. Try a number 0 - %s. EX: c3 for the [c]ard with the 3 in front of it'

class InputMixin(object):

    def computer_inputs(self):
        print 'computer is doing shit'
        return

    def sanitize_selection(self, selection):
        try:
            card_played = self.active_player.get_card(int(selection[1:]))
        except (ValueError, IndexError):
            card_played = None
            os.system(['clear','cls'][os.name == 'nt'])
        return card_played

    def handle_kill_selection(self, selection):
        print 'killing'

    def handle_card_selection(self, selection):
        card_played = self.sanitize_selection(selection)

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

        self.print_hand()
        self.print_user_hand()
        self.print_user_status()
        self.print_user_played_cards()
        selection = raw_input(
            'play [c]ard - [k]ill enemy - [b]uy heroes - [e]nd turn:\n'
        )
        if selection == 'e':
            self.active_player.end_turn()
            return
        elif selection.startswith('c'):
            return self.handle_card_selection(selection)
        elif selection.startswith('k'):
            return self.handle_kill_selection(selection)
        else:
            print_red(INVALID_SELECTION)
        print_blue('Press anykey to continue')
        raw_input()
