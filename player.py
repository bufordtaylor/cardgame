import random
from deck import PlayerStartDeck, print_card_attrs
from shuffle_mixin import ShufflePlayerCardMixin
from colors import print_purple

class BasePlayer(object): pass

class Player(BasePlayer, ShufflePlayerCardMixin):
    name = None
    points = 0
    active = False
    buying_power = 0
    killing_power = 0

    def __init__(self, name):
        self.name = name
        self.deck = PlayerStartDeck().deck
        self.hand = []
        self.phand = []
        self.discard = []
        self.shuffle_deck()

    @property
    def is_computer(self):
        return False

    def __repr__(self):
        return "%(name)s Points:%(points)s" % dict(
            name=self.name,
            points=self.points,
        )

    def start_turn(self):
        self.active = True

    def end_turn(self):
        self.active = False

