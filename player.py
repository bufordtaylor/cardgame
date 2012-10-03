import random
from deck import PlayerStartDeck, print_card_attrs
from shuffle_mixin import ShuffleMixin
from colors import print_purple

class BasePlayer(object): pass

class Player(BasePlayer, ShuffleMixin):
    name = None
    deck = [] # player's deck of cards unplayed
    discard = [] # player's deck of cards played
    hand = [] # player's hand of cards in play
    phand = [] # persistant hand (i.e constructs) of cards in play
    points = 0
    active = False

    def __init__(self, name):
        self.name = name
        self.deck = PlayerStartDeck().deck

    @property
    def is_computer(self):
        return False

    def __repr__(self):
        return "%(name)s Points:%(points)s" % dict(
            name=self.name,
            points=self.points,
        )

    def print_hand(self):
        print_purple(
            '------------PLAYER %s HAND------------------' % self.name
        )
        print_card_attrs()
        for idx,card in enumerate(self.hand):
            card.print_card(idx, player_card=True)

    def start_turn(self):
        self.active = True

    def end_turn(self):
        self.active = False

