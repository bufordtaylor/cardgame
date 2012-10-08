import random
import os
from deck import PlayerStartDeck, print_card_attrs
from shuffle_mixin import ShufflePlayerCardMixin
from colors import print_purple
from constants import *

class BasePlayer(object): pass

class Player(BasePlayer, ShufflePlayerCardMixin):
    name = None
    points = 0
    active = False
    buying_power = 0
    killing_power = 0
    game = None

    def __init__(self, name):
        self.name = name
        self.deck = PlayerStartDeck().deck
        self.hand = []
        self.phand = []
        self.discard = []
        self.shuffle_deck()

    def make_selection(self, must=False):
        none_choice = ''
        if not must:
            none_choice = '[n]one '

        if self.game.action == ACTION_NORMAL:
            input_string = "COMMANDS: acquire [p]ersistent | [k]ill enemy | [b]uy heroes | play [c]ard | play [a]ll | play pe[r]sistent | show p[l]ayed cards | [e]nd turn "
        elif self.game.action == ACTION_BANISH:
            input_string = "COMMANDS: [b]anish card %s" % (none_choice)
        elif self.game.action == ACTION_DISCARD:
            input_string = "COMMANDS: [d]iscard card %s" % (none_choice)
        return raw_input(input_string)

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
        self.new_hand()
        self.buying_power = 0
        self.killing_power = 0
        os.system(['clear','cls'][os.name == 'nt'])

class Computer(Player, ShufflePlayerCardMixin):

    @property
    def is_computer(self):
        return True

    def make_selection(self, must=False):
        selection = 'a'
        if self.game.action == ACTION_NORMAL:
            if len(self.hand) == 0:
                selection = 'p0'
        elif self.game.action == ACTION_BANISH:
            selection = 'b0'
        elif self.game.action == ACTION_DISCARD:
            selection = 'd0'
        elif self.game.action == ACTION_COPY:
            selection = 'c0'

        return selection

