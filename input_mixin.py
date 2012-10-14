import os
from colors import *
from constants import *


class InputMixin(object):

    def sanitize(self,
        selection,
        persistent=False,
        player_card=False,
        played_card=False,
    ):
        try:
            card_idx = int(selection[1:])
            if player_card:
                if persistent:
                    card = self.active_player.phand[card_idx]
                else:
                    card = self.active_player.hand[card_idx]
            elif played_card:
                card = self.played_user_cards[card_idx]
            else:
                if persistent:
                    card = self.phand[card_idx]
                else:
                    card = self.hand[card_idx]
        except (ValueError, IndexError):
            card = None
            card_idx = None
            os.system(['clear','cls'][os.name == 'nt'])

        # TODO this is horrible, do something with this
        if not card:
            if player_card:
                if persistent:
                    if len(self.active_player.phand) == 0:
                        print_red(NO_CARDS)
                    else:
                        print_red(INVALID_CARD % (len(self.active_player.phand) - 1))
                else:
                    if len(self.active_player.phand) == 0:
                        print_red(NO_CARDS)
                    else:
                        print_red(INVALID_CARD % (len(self.active_player.hand) - 1))
            elif played_card:
                print_red(INVALID_CARD % (len(self.played_user_cards) - 1))
            else:
                if persistent:
                    print_red(INVALID_CARD % (len(self.phand) - 1))
                else:
                    print_red(INVALID_CARD % (len(self.hand) - 1))

        return card, card_idx

    def handle_select_inputs(self, where, must):
        """
        select card from a location in play,
        must indicates that they must select a card
        """
        player_card=False
        played_card=False
        persistent=False

        if ACTION_BANISH_PLAYER_HAND in self.actions:
            self.print_user_hand()

        if ACTION_BANISH_PLAYER_DISCARD in self.actions:
            self.print_user_hand_discard()

        # determine if there are any persistents that are useable
        if (
            ACTION_PLAY in self.actions
            and ACTION_USE in self.active_player.phand
        ):
            self.print_user_phand()

        if where == WHERE_GAME_HAND:
            if must:
                if len(self.hand) == 0:
                    return None, None
                elif len(self.hand) == 1:
                    return self.hand[0]
            self.print_hand()
        elif where == WHERE_PLAYER_HAND:
            if must:
                if len(self.active_player.hand) == 0:
                    return None, None
                elif len(self.active_player.hand) == 1:
                    return self.active_player.hand[0], 0
            self.print_user_hand()
            player_card=True
        elif where == WHERE_PLAYED:
            if must:
                if len(self.played_user_cards) == 0:
                    return None, None
                elif len(self.played_user_cards) == 1:
                    return self.played_user_cards[0], 0
            self.print_user_played_cards()
            played_card=True
        elif where == WHERE_PERSISTENT:
            if must:
                if len(self.active_player.phand) == 0:
                    return None, None
                elif len(self.active_player.phand) == 1:
                    return self.active_player.phand[0], 0
            self.print_user_phand()
            player_card=True
            persistent=True
        selection = self.active_player.make_selection(must=must)
        if selection == 'n' and not must:
            return None, None

        card, card_idx = self.sanitize(
            selection,
            persistent=persistent,
            player_card=player_card,
            played_card=played_card,
        )
        if not card:
            self.debug_counter += 1
            if self.debug_counter > 5:
                raise 'something is wrong'
                return None, None
            return self.handle_select_inputs(where, must)

        if not card.eligible(self) and not where == WHERE_PLAYER_HAND:
            print_red('%s - Card not eligible for selection' % card.name)
            self.debug_counter += 1
            if self.debug_counter > 5:
                return None, None
            return self.handle_select_inputs(where, must)

        os.system(['clear','cls'][os.name == 'nt'])
        self.debug_counter = 0
        return card, card_idx

    def handle_inputs(self):
        """for the main loop, when a player is playing cards"""
        self.check_cards_eligibility()
        self.print_user_status()
        self.print_phand()
        self.print_hand()
        self.print_user_hand()
        selection = self.active_player.make_selection()
        if selection == 'e':
            self.active_player.end_turn()
            return
        elif selection.startswith('c'):
            return self.play_user_card(selection)
        elif selection.startswith('t'):
            return self.play_user_card_persistent(selection)
        elif selection.startswith('a'):
            return self.play_all_user_cards(selection)
        elif selection.startswith('l'):
            return self.show_played_cards(selection)
        elif selection.startswith('k'):
            return self.defeat_or_acquire(selection)
        elif selection.startswith('b'):
            return self.defeat_or_acquire(selection)
        elif selection.startswith('p'):
            return self.defeat_or_acquire(selection, persistent=True)
        else:
            print_red(INVALID_SELECTION)
