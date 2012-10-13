import random
from colors import (
    bcolors, print_dict, print_green,prepare_card_row,
    print_white, print_blue, print_purple, print_ordered_cards,
)
from constants import *

class Card(object):
    name = None
    worth = 0
    card_type = None
    faction = None
    abilities = None
    buy = 0
    kill = 0
    instant_worth = 0
    instant_kill = 0
    instant_buy = 0
    banishable = True

    def __init__(self, **kwargs):
        self.actions = []
        for k, v in kwargs.iteritems():
            if hasattr(self, k):
                setattr(self, k, v)

    def __repr__(self):
        return self.name

    def card_row(self, idx, player_card=False, game_phand=False):
        if player_card:
            instruction = (bcolors.WHITE, '%s:%s' % ('[c]ard', idx))
        else:
            instruction = (bcolors.WHITE, ' ')
        if ACTION_PLAY in self.actions:
            if player_card:
                instruction = (bcolors.WHITE, '%s:%s' % ('[c]ard', idx))
            elif game_phand:
                instruction = (bcolors.WHITE, '%s:%s' % ('[p]ers', idx))
            else:
                instruction = (bcolors.WHITE, '%s:%s' % (
                    self.kill_buy_acquire, idx)
                )

        attr_list = [
            instruction,
            (bcolors.PURPLE, self.card_type_string),
            self.card_faction,
            (bcolors.BLUE, self.name),
        ]

        attr_dict = {}

        numbered_attrs = [
            (bcolors.YELLOW, 'buy'),
            (bcolors.RED, 'kill'),
            (bcolors.GREEN, 'worth'),
            (bcolors.YELLOW, 'instant_buy'),
            (bcolors.RED, 'instant_kill'),
            (bcolors.GREEN, 'instant_worth'),
            (bcolors.BLUE, 'abilities'),
        ]

        for k, v in numbered_attrs:
            attr_list.append((k, getattr(self, v)))
        return prepare_card_row(attr_list)

    @property
    def card_type_string(self):
        str = ''
        if self.is_monster:
            str = 'MONSTER'
        elif self.is_hero:
            str = 'HERO'
        elif self.is_persistent:
            str = 'PERS'
        elif self.is_starting_card:
            str = 'STARTING'
        return str

    @property
    def card_faction(self):
        str = (bcolors.RED, 'MONSTER')
        if self.faction == VOID:
            str = (bcolors.PURPLE, 'VOID')
        elif self.faction == MECHANA:
            str = (bcolors.YELLOW, 'MECHANA')
        elif self.faction == ENLIGHTENED:
            str = (bcolors.BLUE, 'ENLIGHTENED')
        elif self.faction == LIFEBOUND:
            str = (bcolors.GREEN, 'LIFEBOUND')
        elif self.is_starting_card:
            str = (bcolors.WHITE, 'STARTING')
        return str

    @property
    def kill_buy_acquire(self):
        str = '[c]ard'
        if self.is_monster:
            str = '[k]ill'
        elif self.is_hero:
            str = '[b]uy'
        elif self.is_persistent:
            str = '[b]uy'
        return str

    def apply_card_tokens(self, game):
        kill = self.kill - game.token.get('minus_kill', 0)
        if kill < 0:
            kill = 0
        buy = self.buy - game.token.get('minus_buy', 0)
        if self.card_type == CARD_TYPE_PERSISTENT:
            buy -= game.token.get('minus_construct_buy', 0)
        if buy < 0:
            buy = 0
        return kill, buy

    def _determine_actions(self, game_action, game):
        kill, buy = self.apply_card_tokens(game)

        if game_action == ACTION_DISCARD_FROM_PLAYER_HAND:
            if self in game.active_player.hand:
                self.actions.append(ACTION_DISCARD_FROM_PLAYER_HAND)

        if game_action == ACTION_COPY:
            if self in game.played_user_cards:
                self.actions.append(ACTION_COPY)

        # unbanishable cards have a banishable token attached to them
        if game_action == ACTION_BANISH:
            if self.banishable:
                self.actions.append(ACTION_BANISH)

        if game_action == ACTION_DEFEAT:
            if self.card_type == CARD_TYPE_MONSTER:
                if game.token.get('killing_power', 0) >= kill:
                    self.actions.append(ACTION_DEFEAT)

        if game_action == ACTION_ACQUIRE_TO_TOP:
            if self.card_type != CARD_TYPE_MONSTER:
                if game.token.get('buying_power', 0) >= buy:
                    self.actions.append(ACTION_ACQUIRE_TO_TOP)

        if game_action == ACTION_PLAY:
            # if it's in the player's hand, it's always eligible
            if self in game.active_player.hand:
                self.actions.append(ACTION_PLAY)

        if self.card_type == CARD_TYPE_MONSTER:
            if game_action == ACTION_KILL:
            # check CAN KILL
                if game.active_player.killing_power >= kill:
                    self.actions.append(ACTION_KILL)
        else:
            if game_action == ACTION_BUY:
                # check CAN BUY
                if game.active_player.buying_power >= buy:
                    self.actions.append(ACTION_BUY)

    def check_actions(self, game):
        self.actions = []
        for action in game.actions:
            self._determine_actions(action, game)


    # lots of helpers below this

    def eligible(self, game):
        for action in game.actions:
            if action in self.actions:
                return True
        return False

    @property
    def is_monster(self):
        return self.card_type == CARD_TYPE_MONSTER

    @property
    def is_persistent(self):
        return self.card_type == CARD_TYPE_PERSISTENT

    @property
    def is_hero(self):
        return self.card_type == CARD_TYPE_HERO

    @property
    def is_starting_card(self):
        return self.faction == STARTING

    @property
    def can_buy(self):
        return self._is_eligible_for_action(ACTION_BUY)

    @property
    def can_kill(self):
        return self._is_eligible_for_action(ACTION_KILL)

    @property
    def can_banish(self):
        return self._is_eligible_for_action(ACTION_BANISH)

    @property
    def can_copy(self):
        return self._is_eligible_for_action(ACTION_COPY)

    @property
    def can_discard_from_player_hand(self):
        return self._is_eligible_for_action(ACTION_DISCARD_FROM_PLAYER_HAND)

    @property
    def can_defeat(self):
        return self._is_eligible_for_action(ACTION_DEFEAT)

    @property
    def can_acquire_to_top(self):
        return self._is_eligible_for_action(ACTION_ACQUIRE_TO_TOP)

    @property
    def can_acquire_to_discard(self):
        return self._is_eligible_for_action(ACTION_ACQUIRE_TO_DISCARD)

    @property
    def can_acquire_to_hand(self):
        return self._is_eligible_for_action(ACTION_ACQUIRE_TO_HAND)

    @property
    def can_banish_player_persistent(self):
        return self._is_eligible_for_action(ACTION_BANISH_PLAYER_PERSISTENT)

    @property
    def can_use(self):
        return self._is_eligible_for_action(ACTION_USE)

    def _is_eligible_for_action(self, action):
        if action in self.actions:
            return True
        return False

