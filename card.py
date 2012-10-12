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
    eligible = False
    banishable = True

    def __init__(self, **kwargs):
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
        if self.eligible:
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

    def is_eligible(self, game):
        """depending upon the situation and where the card is, it becomes
        eligible for selection"""

        self.eligible = False

        if game.action == ACTION_DISCARD:
            if self in game.active_player.hand:
                self.eligible = True

        if game.action == ACTION_COPY:
            if self in game.played_user_cards:
                self.eligible = True

        # unbanishable cards have a banishable token attached to them
        if game.action == ACTION_BANISH:
            self.eligible = self.banishable

        if game.action == ACTION_DEFEAT:
            if self.card_type == CARD_TYPE_MONSTER:
                if game.token.get('killing_power') >= self.kill:
                    self.eligible = True

        if game.action == ACTION_ACQUIRE_TO_TOP:
            if self.card_type != CARD_TYPE_MONSTER:
                if game.token.get('buying_power') >= self.buy:
                    self.eligible = True

        if game.action == ACTION_NORMAL:
            # if it's in the player's hand, it's always eligible
            if self in game.active_player.hand:
                self.eligible = True
            # check CAN KILL
            if self.card_type == CARD_TYPE_MONSTER:
                if game.active_player.killing_power >= self.kill:
                    self.eligible = True
            # check CAN BUY
            else:
                if game.active_player.buying_power >= self.buy:
                    self.eligible = True
        return self.eligible

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

