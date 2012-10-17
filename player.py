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

    def make_selection(self, must=False, this=None, that=None):
        none_choice = ''
        if not must:
            none_choice = '[n]one '

        end_turn = True

        input_string = ['show p[l]ayed cards']
        if ACTION_PLAY in self.game.actions:
            input_string.append('play [c]ard')
            input_string.append('play [a]ll card')
        if ACTION_BUY in self.game.actions:
            input_string.append('[b]uy heroes')
            input_string.append('buy [p]ersistent')
        if ACTION_ACQUIRE_TO_PHAND in self.game.actions:
            input_string.append('p[u]t in play')
        if ACTION_KILL in self.game.actions:
            input_string.append('[k]ill enemy')
        if ACTION_BANISH in self.game.actions:
            input_string.append('[b]anish card %s' % (none_choice))
        if ACTION_DISCARD_FROM_PLAYER_HAND in self.game.actions:
            input_string.append('[d]iscard card %s' % (none_choice))
        if ACTION_THIS_OR_THAT in self.game.actions:
            input_string.append('[s0]-%s or [s1]-%s' % (this, that))
            end_turn = False
        if end_turn:
            input_string.append('[e]nd turn')
        return raw_input(' | '.join(input_string))

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

        # check the persistents
        for card in self.phand:
            self.game.play_user_card(card)

    def end_turn(self):

        self.active = False
        self.new_hand()
        self.buying_power = 0
        self.killing_power = 0
        self.game.token = {}
        self.game.token_erasers = {}
        self.game.used_tokens = {}
        os.system(['clear','cls'][os.name == 'nt'])

class Computer(Player, ShufflePlayerCardMixin):

    @property
    def is_computer(self):
        return True

    def make_selection(self, must=False, this=None, that=None):
        selection = 'a'
        # order is important here for unit tests
        if ACTION_BUY in self.game.actions or ACTION_KILL in self.game.actions:
            if len(self.hand) == 0:
                selection = 'p0'
        elif ACTION_BANISH in self.game.actions:
            selection = 'b0'
        elif ACTION_DISCARD_FROM_PLAYER_HAND in self.game.actions:
            selection = 'd0'
        elif ACTION_BANISH_PLAYER_DISCARD in self.game.actions:
            selection = 'b0'
        elif ACTION_BANISH_PLAYER_HAND in self.game.actions:
            selection = 'b0'
        elif ACTION_COPY in self.game.actions:
            selection = 'c0'
        elif ACTION_ACQUIRE_TO_TOP in self.game.actions:
            for idx, card in enumerate(self.game.hand):
                if card.card_type == CARD_TYPE_MONSTER:
                    continue

                selection = 'b' + str(idx)
                break

            if not selection.startswith('b'):
                selection = 'p0'
        elif ACTION_THIS_OR_THAT in self.game.actions:
            selection = 's0'
        return selection

