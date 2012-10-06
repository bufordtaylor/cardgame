import random
from colors import (
    bcolors, print_dict, print_green,prepare_card_row,
    print_white, print_blue, print_purple, print_ordered_cards,
)
from deck import (
    CARD_TYPE_MONSTER,
    CARD_TYPE_HERO,
    CARD_TYPE_PERSISTENT,
)


class Card(object):
    name = None
    worth = 0
    card_type = None
    abilities = {}
    buy = 0
    kill = 0

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            if hasattr(self, k):
                setattr(self, k, v)

    def __repr__(self):
        return self.name

    def card_row(self, idx, player_card=False):
        if not player_card:
            instruction = (bcolors.WHITE, '%s:%s' % (self.kill_buy_acquire, idx))
        else:
            instruction = (bcolors.WHITE, '%s:%s' % ('[c]ard', idx))

        attr_list = [
            instruction,
            (bcolors.PURPLE, self.card_type_string),
            (bcolors.BLUE, self.name),
        ]

        attr_dict = {}

        numbered_attrs = {
            bcolors.GREEN: 'worth',
            bcolors.YELLOW: 'buy',
            bcolors.RED: 'kill'
        }

        for k, v in numbered_attrs.iteritems():
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

    @property
    def is_monster(self):
        return self.card_type == CARD_TYPE_MONSTER

    @property
    def is_persistent(self):
        return self.card_type == CARD_TYPE_PERSISTENT

    @property
    def is_hero(self):
        return self.card_type == CARD_TYPE_HERO

