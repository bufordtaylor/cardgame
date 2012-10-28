import random
from constants import *
from abilities_constants import *

class AbilitiesMixin(object):

    def draw_1(self, card=None):
        self.active_player.draw_cards(num=1)

    def draw_2(self, card=None):
        self.active_player.draw_cards(num=2)

    def draw_3(self, card=None):
        self.active_player.draw_cards(num=3)

    def draw_2_then_banish_1_hand(self, card=None):
        self.draw_2()
        card, deck, action, iid = self.handle_selection_inputs(
            [ACTION_BANISH_PLAYER_HAND], self.active_player)
        self.remove_card(card, self.active_player.hand)
        self.discard.append(card)

    def draw_1_banish_center(self, card=None):
        self.draw_1()
        card, deck, action, iid = self.handle_selection_inputs(
            [ACTION_BANISH_CENTER], self.active_player)
        if card:
            self.remove_card(card, self.hand)
            self.discard.append(card)

    def draw_1_if_control_gt_2_constructs(self, card=None):
        persistents = 0
        for c in self.active_player.phand:
            if c.card_type == CARD_TYPE_PERSISTENT:
                persistents += 1
        if persistents >= 2:
            self.active_player.draw_cards(num=1)

    def if_discard_draw_two(self, card=None):
        self.action_perform([ACTION_DISCARD_FROM_PLAYER_HAND])
        if self.selected_card:
            self.draw_2()

    def banish_this_extra_turn(self, card=None, action=None):
        if action == ACTION_USE:
            for idx, c in enumerate(self.active_player.phand):
                if c == card:
                    banish_card = self.active_player.get_card(
                        idx,
                        persistent=True,
                        move=True
                    )
                    self.discard.append(banish_card)
                    self.use_token(card.abilities)
                    self.extra_turn = True
                    break
        else:
            self.set_token(card.abilities, card, END_OF_TURN)

    def copy_effect(self, card=None):
        self.action_perform([ACTION_COPY])

    def defeat_monster_lt_4(self, card=None):
        self.set_token('minus_kill', 4, END_OF_ACTION)
        self.action_perform([ACTION_DEFEAT])

    def defeat_monster_lt_6(self, card=None):
        self.set_token('minus_kill', 6, END_OF_ACTION)
        self.action_perform([ACTION_DEFEAT])

    def acquire_any_center_hero(self, card=None):
        self.set_token('hero_buying_power', 1000, END_OF_ACTION)
        self.action_perform([ACTION_ACQUIRE_TO_TOP])

    def if_lifebound_hero_plus_2_kill(self, card=None):
        add = False
        for c in self.played_user_cards:
            if c.in_faction(self, LIFEBOUND):
                add = True
        if add:
            self.active_player.killing_power += 2

    def acquire_hero_3_or_less_to_top_of_deck(self, card=None):
        self.set_token('hero_buying_power', 3, END_OF_ACTION)
        self.action_perform([ACTION_ACQUIRE_TO_TOP])

    def cannot_be_banished_acquire_any_center_card(self, card=None):
        self.acquire_or_defeat_any(card)

    def acquire_or_defeat_any(self, card=None):
        self.active_player.killing_power += 1000
        self.active_player.buying_power += 1000
        self.action_perform([ACTION_ACQUIRE_TO_TOP, ACTION_DEFEAT])
        self.active_player.killing_power -= 1000
        self.active_player.buying_power -= 1000

    def plus_1_buy_or_1_kill(self, card=None):
        self.change_action([ACTION_THIS_OR_THAT])
        choice = self.handle_this_or_that(BUY_1, KILL_1)
        if choice == BUY_1:
            self.active_player.buying_power += 1
        else:
            self.active_player.killing_power += 1

    def plus_1_point_per_controlled_construct(self, card=None):
        factions = []
        for c in self.active_player.phand:
            if c.faction not in factions:
                factions.append(c.faction)
        self.active_player.points += len(factions)

    def next_construct_1_less_buy(self, card=None):
        # TODO: Actually display 1 less buy
        # right now it is only doing it on the back end
        self.set_token('minus_construct_buy', 1, END_OF_TURN)

    def can_banish_1_hand_or_discard(self, card=None):
        self.action_perform([ACTION_BANISH_PLAYER_HAND, ACTION_BANISH_PLAYER_DISCARD])

    def can_banish_1_hand_or_discard_and_center(self, card=None):
        self.can_banish_1_hand_or_discard()
        self.can_banish_1_center()

    def can_banish_1_center(self, card=None):
        self.action_perform([ACTION_BANISH])


    def opponents_destroy_1_construct(self, card=None):
        for p in self.players:
            if p == self.active_player:
                continue

            if len(p.phand) == 1:
                p.discard.append(p.phand.pop())

            if len(p.phand) > 1:
                self.change_action([ACTION_BANISH_PLAYER_PERSISTENT])
                destroy_card, destroy_idx = self.handle_destroy_one_construct(p)
                card = p.get_card(destroy_idx, persistent=True, move=True)
                p.discard.append(card)

    def add_random_card_to_hand_from_each_opponent(self, card=None):
        for p in self.players:
            if p != self.active_player:
                card = p.get_card(random.randint(0, len(p.hand)-1))
                self.active_player.hand.append(card)

    def per_turn_draw_1(self, card=None, action=None):
        if action == ACTION_USE:
            self.draw_1()
            self.use_token(card.abilities)
        else:
            self.set_token(card.abilities, card, END_OF_TURN)

    def per_turn_plus_1_kill_can_spend_4_to_buy_3_points(self, card=None, action=None):
        if action == ACTION_USE:
            self.active_player.buying_power -= 4
            self.active_player.points += 3
            self.use_token(card.abilities)
        else:
            if self.active_player.buying_power >= 4:
                self.set_token(card.abilities, card, END_OF_TURN)
            elif self.token.get(card.abilities):
                self.remove_token(card.abilities)

    def per_turn_plus_1_buy_first_lifebound_hero_plus_1_point(self, card=None):
        self.active_player.buying_power += 1
        self.set_token(PER_TURN_PLUS_1_BUY_FIRST_LIFEBOUND_HERO_PLUS_1_POINT, 1, END_OF_TURN)

    def per_turn_when_play_mechana_construct_draw_1_including_this_one(self, card=None):
        self.set_token(PER_TURN_WHEN_PLAY_MECHANA_CONSTRUCT_DRAW_1_INCLUDING_THIS_ONE, 1, END_OF_TURN)

    def per_turn_plus_1_buy_for_mechana_construct_only(self, card=None):
        self.set_token('minus_mechana_construct_buy', 1, END_OF_TURN)

    def per_turn_when_acquire_mechana_construct_put_in_play(self, card=None):
        self.set_token(PER_TURN_WHEN_ACQUIRE_MECHANA_CONSTRUCT_PUT_IN_PLAY, 1, END_OF_TURN)

    def per_turn_plus_2_buy_for_mechana_construct_only(self, card=None):
        self.set_token('minus_mechana_construct_buy', 2, END_OF_TURN)

    def per_turn_plus_1_kill_per_controlled_mechana_contruct(self, card=None):
        # adding one for card if self not in the phand already
        if card not in self.active_player.phand:
            self.active_player.killing_power += 1
        for card in self.active_player.phand:
            if card.in_faction(self,MECHANA):
                self.active_player.killing_power += 1

    def per_turn_plus_1_kill_first_monster_defeat_plus_1_point(self, card=None):
        self.active_player.killing_power += 1
        self.set_token(PER_TURN_PLUS_1_KILL_FIRST_MONSTER_DEFEAT_PLUS_1_POINT, 1, END_OF_TURN)

    def per_turn_plus_3_kill(self, card=None):
        self.active_player.killing_power += 3

    def per_turn_plus_1_kill(self, card=None):
        self.active_player.killing_power += 1

    def all_contructs_are_mechana(self, card=None):
        self.set_token(ALL_CONTRUCTS_ARE_MECHANA, 1, END_OF_TURN)

    def opponents_keep_1_construct(self, card=None):
        for p in self.players:
            if p == self.active_player:
                continue

            if len(p.phand) > 1:
                results = self.handle_selection_inputs([ACTION_KEEP], p)
                card, deck, action, iid = results
                for pcard in p.phand:
                    if card.iid != iid:
                        p.discard.append(pcard)
                p.phand = []
                p.phand.append(card)


########### regular abilities
    def normal_action(self):
        card, deck, action, iid = self.handle_selection_inputs(
            ACTION_NORMAL, self.active_player)

        # card is now not in any deck. it is active
        self.active_card.append(card)

        if action == ACTION_USE:
            getattr(self,ABILITY_MAP.get(card.abilities)
                )(card=card, action=action)

        # if playing card, remove card from player hand
        if action == ACTION_PLAY:
            self.remove_card(card, self.active_player.hand)

            # play user card effects
            self.play_user_card_effects(card)

            # depending on what type of card it is, determine where it
            # should go, persistent hand or played user cards
            if card.card_type == CARD_TYPE_PERSISTENT:
                self.active_player.phand.append(card)
                #TODO we are calling this in play_user_card_effects
                self.check_cards_eligibility()
            else:
                self.played_user_cards.append(card)

        if action == ACTION_BUY or action == ACTION_ACQUIRE_TO_PHAND:
            if not card.faction == STARTING:
                self.remove_card(card, self.hand)
                self.draw_card()
            else:
                card.pop_card_from_persistent_game_backup(self)

            kill, buy = card.apply_card_tokens(self)
            self.remove_token('minus_buy')
            self.active_player.buying_power -= buy

            if card.card_type == CARD_TYPE_PERSISTENT:
                self.remove_token('minus_construct_buy')

            if (
                card.in_faction(self, MECHANA) and
                card.card_type == CARD_TYPE_PERSISTENT
            ):
                self.remove_token('minus_mechana_construct_buy')


            if action == ACTION_BUY:
                self.active_player.discard.append(card)
            if action == ACTION_ACQUIRE_TO_PHAND:
                self.play_user_card_effects(card)
                self.active_player.phand.append(card)

        if action == ACTION_KILL:
            self._action_perform_defeat(card, deck)

        self.active_card = []
        return card

    def action_perform(self, actions, player=None):
        """performs all the unusual things like copying, banishing, discarding
        acquiring, defeating, etc"""
        if player is None:
            player = self.active_player

        card, deck, action, iid = self.handle_selection_inputs(actions, player)
        if not card:
            return

        if action in [
            ACTION_BANISH_PLAYER_HAND,
            ACTION_BANISH_PLAYER_DISCARD,
            ACTION_BANISH_CENTER,
        ]:
            if deck == DECK_GAME_DECK:
                self.remove_card(card, self.hand)
            elif deck == DECK_PLAYER_DISCARD:
                self.remove_card(card, player.discard)
            elif deck == DECK_PLAYER_HAND:
                self.remove_card(card, player.hand)
            self.discard.append(card)

        if action == ACTION_BANISH_PLAYER_PERSISTENT:
            self.remove_card(card, player.phand)
            player.discard.append(card)

        if action == ACTION_DISCARD_FROM_PLAYER_HAND:
            self.remove_card(card, player.hand)
            player.discard.append(card)

        if action == ACTION_ACQUIRE_TO_TOP:
            self.remove_card(card, self.hand)
            player.deck.append(card)

        if action == ACTION_DEFEAT:
            self._action_perform_defeat(card, deck)

    def _action_perform_defeat(self, card, deck):
        if not card.faction == STARTING:
            self.remove_card(card, self.hand)
            self.draw_card()
        else:
            card.pop_card_from_persistent_game_backup(self)

        kill, buy = card.apply_card_tokens(self)
        self.remove_token('minus_kill')
        print 'points', self.active_player.points, card.instant_worth, card
        self.active_player.points += card.instant_worth
        self.active_player.killing_power -= kill

        if PER_TURN_PLUS_1_KILL_FIRST_MONSTER_DEFEAT_PLUS_1_POINT in self.token:
            self.active_player.points += 1
            self.use_token(PER_TURN_PLUS_1_KILL_FIRST_MONSTER_DEFEAT_PLUS_1_POINT)

        self.discard.append(card)

        self.play_abilities(card)
        self.check_tokens_for_use_once()
