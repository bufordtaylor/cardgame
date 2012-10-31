import os
from colors import *
from constants import *
from card import get_card_by_iid, get_card_and_deck


class InputMixin(object):

    def handle_this_or_that(self, this, that):

        print 'ACTIONS:', ','.join([ACTION_DICT[a] for a in self.actions])
        selection = self.active_player.make_selection(this=this, that=that)
        if selection == 's0':
            return this
        elif selection == 's1':
            return that
        print_red(INVALID_SELECTION)
        return self.handle_this_or_that(this, that)

    def handle_destroy_one_construct(self, player):
        print 'ACTIONS:', ','.join([ACTION_DICT[a] for a in self.actions])
        #player.print_phand()
        selection = player.make_selection(must=True)
        try:
            card_idx = int(selection[1:])
            card = player.phand[card_idx]
            return card, card_idx
        except (ValueError, IndexError):
            card = None
            card_idx = None
            os.system(['clear','cls'][os.name == 'nt'])
            print_red(INVALID_SELECTION)
        return self.handle_destroy_one_construct(player)


    def handle_action_acquire_to_top(self, player):
        print 'ACTIONS:', ','.join([ACTION_DICT[a] for a in self.actions])
        self.print_hand()
        self.print_phand()
        selection = player.make_selection(must=True)
        try:
            card_idx = int(selection[1:])
            if selection.startswith('s'):
                card = self.hand[card_idx]
            else:
                card = self.phand[card_idx]
            return card, card_idx
        except (ValueError, IndexError):
            card = None
            card_idx = None
            os.system(['clear','cls'][os.name == 'nt'])
            print_red(INVALID_SELECTION)
        return self.handle_action_acquire_to_top(player)

    def handle_selection_inputs(self, actions, player):
        self.change_action(actions)
        if self.debug:
            print 'debug', actions == ACTION_NORMAL, self.player_can_do_actions(), player
            if not self.player_can_do_actions():
                player.end_turn()
                return (None, None, None, None)

        self.display_proper_deck(player)
        try:
            raw_input = player.raw_card_selection()

            if raw_input == 'end turn':
                player.end_turn()
                return (None, None, None, None)
            # in this case, there is no eligible card to select
            # therefore nothing can be done
            if raw_input is None:
                self.log_action(None, None, None, None)
                return (None, None, None, None)
            else:
                raw_card_selection = int(raw_input)
        except ValueError:
            print 'must be integer'
            return self.handle_selection_inputs(actions, player)


        card, deck, action, iid = self.select_card_for_action(
            raw_card_selection, player
        )
        if not card or action == ACTION_DESELECT:
            self.handle_selection_inputs(actions, player)

        return (card, deck, action, iid)

    def display_proper_deck(self, player):
        self.print_user_status()
        if ACTION_BUY in self.actions or ACTION_KILL in self.actions:
            self.print_phand()
            self.print_hand()
            self.print_user_hand()
            self.print_user_phand(player)
        if ACTION_BANISH in self.actions:
            self.print_hand()
        if ACTION_BANISH_CENTER in self.actions:
            self.print_hand()
        if ACTION_DISCARD_FROM_PLAYER_HAND in self.actions:
            self.print_user_hand()
        if ACTION_BANISH_PLAYER_DISCARD in self.actions:
            self.print_user_hand_discard()
        if ACTION_BANISH_PLAYER_HAND in self.actions:
            self.print_user_hand()
        if ACTION_COPY in self.actions:
            self.print_user_played_cards()
        if (
            ACTION_ACQUIRE_TO_TOP in self.actions or
            ACTION_ACQUIRE_TO_PHAND in self.actions
        ):
            self.print_hand()
            self.print_phand()
        if ACTION_THIS_OR_THAT in self.actions:
            print 'this or that'
        if ACTION_KEEP in self.actions:
            self.print_user_phand(player)
        if ACTION_BANISH_PLAYER_PERSISTENT in self.actions:
            self.print_user_phand(player)

    def select_card_for_action(self, iid, player):
        """select card for an action"""
        card, deck = get_card_and_deck(self, iid)
        if not card:
            return card, deck, None, iid
        card.list_eligible_actions()
        action = player.select_card_action(card.actions)
        return card, deck, action, iid
