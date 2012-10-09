from constants import *

class AbilitiesMixin(object):

    def draw_1(self):
        self.active_player.draw_cards(num=1)

    def draw_2(self):
        self.active_player.draw_cards(num=2)

    def draw_3(self):
        self.active_player.draw_cards(num=3)

    def draw_2_then_banish_1_hand(self):
        self.draw_2()
        self.must_banish_card(num=1, where=WHERE_PLAYER_HAND)

    def draw_1_banish_center(self):
        self.draw_1()
        self.can_banish_card(num=1, where=WHERE_GAME_HAND)

    def draw_1_if_control_gt_2_constructs(self):
        persistents = 0
        for c in self.active_player.phand:
            if c.card_type == CARD_TYPE_PERSISTENT:
                persistents += 1
        if persistents >= 2:
            self.active_player.draw_cards(num=1)

    def if_discard_draw_two(self):
        self.can_discard_card(num=1)
        if self.selected_card:
            self.draw_2()

    def banish_this_extra_turn(self):
        raise 'Not implemented'

    def copy_effect(self):
        self.must_copy_card()

    def defeat_monster_lt_4(self):
        raise 'Not implemented'

    def defeat_monster_lt_6(self):
        raise 'Not implemented'

    def acquire_any_center_hero(self):
        raise 'Not implemented'

    def if_lifebound_hero_plus_2_kill(self):
        raise 'Not implemented'

    def acquire_hero_3_or_less_to_top_of_deck(self):
        raise 'Not implemented'

    def plus_1_buy_or_1_kill(self):
        raise 'Not implemented'

    def plus_1_point_per_controlled_construct(self):
        raise 'Not implemented'

    def next_construct_1_less_buy(self):
        raise 'Not implemented'

    def can_banish_1_hand_or_discard_and_center(self):
        raise 'Not implemented'

    def opponents_keep_1_construct(self):
        raise 'Not implemented'

    def can_banish_1_center(self):
        raise 'Not implemented'

    def cannot_be_banished_acquire_any_center_card(self):
        raise 'Not implemented'

    def opponents_destroy_1_construct(self):
        raise 'Not implemented'

    def add_random_card_to_hand_from_each_opponent(self):
        raise 'Not implemented'

    def per_turn_draw_1(self):
        raise 'Not implemented'

    def per_turn_plus_1_kill_can_spend_4_to_buy_3_points(self):
        raise 'Not implemented'

    def per_turn_plus_1_buy_first_lifebound_hero_plus_1_point(self):
        raise 'Not implemented'

    def per_turn_when_play_mechana_construct_draw_1_including_this_one(self):
        raise 'Not implemented'

    def per_turn_plus_1_buy_for_mechana_construct_only(self):
        raise 'Not implemented'

    def per_turn_when_acquire_mechana_construct_put_in_play(self):
        raise 'Not implemented'

    def per_turn_plus_2_buy_for_mechana_construct_only(self):
        raise 'Not implemented'

    def per_turn_plus_1_kill_per_controlled_mechana_contruct(self):
        raise 'Not implemented'

    def per_turn_plus_1_kill_first_monster_defeat_plus_1_point(self):
        raise 'Not implemented'

    def per_turn_plus_3_kill(self):
        raise 'Not implemented'

    def all_contructs_are_mechana(self):
        raise 'Not implemented'

    def per_turn_plus_1_kill(self):
        raise 'Not implemented'

    def acquire_or_defeat_any(self):
        raise 'Not implemented'
