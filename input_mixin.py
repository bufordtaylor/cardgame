import os
from colors import *
from constants import *
from card import get_card_by_iid, get_card_and_deck


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

        if selection.startswith('u'):
            if ACTION_ACQUIRE_TO_PHAND in card.actions:
                card.move_to = WHERE_PLAYER_PERSISTENT
            else:
                os.system(['clear','cls'][os.name == 'nt'])
                print_red(INVALID_SELECTION)
                card = None
                card_idx = None

        return card, card_idx



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

    def handle_select_inputs(self, where, must):
        """
        select card from a location in play,
        must indicates that they must select a card
        """
        print 'ACTIONS:', ','.join([ACTION_DICT[a] for a in self.actions]), 'WHERE:', where, 'must:', must
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
        print 'ACTIONS:', ','.join([ACTION_DICT[a] for a in self.actions])
        self.check_cards_eligibility()
        self.print_user_status()
        self.print_phand()
        self.print_hand()
        self.print_user_hand()
        self.print_user_phand()
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
        elif selection.startswith('u'):
            return self.defeat_or_acquire(selection)
        elif selection.startswith('p'):
            return self.defeat_or_acquire(selection, persistent=True)
        else:
            print_red(INVALID_SELECTION)

    def handle_selection_inputs(self, actions, player):
        self.change_action(actions)
        self.display_proper_deck(player)
        try:
            raw_card_selection = int(player.raw_card_selection())
        except ValueError:
            print 'must be integer'
            return self.handle_selection_inputs(actions, player)

        card, deck, action, iid = self.select_card_for_action(
            raw_card_selection, player
        )
        print card, deck, action, iid
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
