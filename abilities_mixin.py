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
        self.change_action([ACTION_BANISH])
        self.must_banish_card(num=1, where=WHERE_PLAYER_HAND)

    def draw_1_banish_center(self, card=None):
        self.draw_1()
        self.change_action([ACTION_BANISH])
        self.can_banish_card(num=1, where=WHERE_GAME_HAND)

    def draw_1_if_control_gt_2_constructs(self, card=None):
        persistents = 0
        for c in self.active_player.phand:
            if c.card_type == CARD_TYPE_PERSISTENT:
                persistents += 1
        if persistents >= 2:
            self.active_player.draw_cards(num=1)

    def if_discard_draw_two(self, card=None):
        self.can_discard_card(num=1)
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
        self.must_copy_card()

    def defeat_monster_lt_4(self, card=None):
        self.change_action([ACTION_DEFEAT])
        self.can_defeat_card(killing_power=4)

    def defeat_monster_lt_6(self, card=None):
        self.change_action([ACTION_DEFEAT])
        self.can_defeat_card(killing_power=6)

    def acquire_any_center_hero(self, card=None):
        self.change_action([ACTION_ACQUIRE_TO_TOP])
        self.can_acquire_card(buying_power=1000)

    def if_lifebound_hero_plus_2_kill(self, card=None):
        add = False
        for c in self.played_user_cards:
            if c.in_faction(self, LIFEBOUND):
                add = True
        if add:
            self.active_player.killing_power += 2

    def acquire_hero_3_or_less_to_top_of_deck(self, card=None):
        self.set_token('hero_buying_power', 3, END_OF_ACTION)
        self.change_action([ACTION_ACQUIRE_TO_TOP])
        card, idx = self.handle_action_acquire_to_top(self.active_player)
        self.move_card(card, idx, WHERE_GAME_HAND)

    def cannot_be_banished_acquire_any_center_card(self, card=None):
        self.acquire_or_defeat_any(card)

    def acquire_or_defeat_any(self, card=None):
        self.change_action([ACTION_ACQUIRE_TO_TOP, ACTION_DEFEAT])
        self.active_player.killing_power += 1000
        self.active_player.buying_power += 1000
        self.select_card(1, where=WHERE_GAME_HAND, must=False)
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
        self.change_action(
            [ACTION_BANISH_PLAYER_HAND, ACTION_BANISH_PLAYER_DISCARD]
        )
        self.can_banish_card(num=1, where=None)

    def can_banish_1_hand_or_discard_and_center(self, card=None):
        self.change_action(
            [ACTION_BANISH_PLAYER_HAND, ACTION_BANISH_PLAYER_DISCARD]
        )
        self.can_banish_card(num=1, where=None)
        self.change_action([ACTION_BANISH])
        self.can_banish_card(num=1, where=WHERE_GAME_HAND)

    def opponents_keep_1_construct(self, card=None):
        for p in self.players:
            if p == self.active_player:
                continue

            if len(p.phand) > 1:
                card, deck, action, iid = self.handle_selection_inputs([ACTION_KEEP], p)
                for pcard in p.phand:
                    if card.iid != iid:
                        p.discard.append(pcard)
                p.phand = []
                p.phand.append(card)

    def can_banish_1_center(self, card=None):
        self.change_action([ACTION_BANISH])
        self.can_banish_card(num=1, where=WHERE_GAME_HAND)


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

