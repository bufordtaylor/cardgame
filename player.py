import random
import os
from deck import PlayerStartDeck, print_card_attrs, starter_cards
from shuffle_mixin import ShufflePlayerCardMixin
from colors import print_purple
from constants import *
from card import Card

class BasePlayer(object): pass

class Player(BasePlayer, ShufflePlayerCardMixin):
    name = None
    points = 0
    active = False
    buying_power = 0
    killing_power = 0
    game = None

    def __init__(self, name, game):
        self.name = name
        self.deck = []
        self.hand = []
        self.phand = []
        self.discard = []
        self.shuffle_deck()

    def init_deck(self, game):
        for i in xrange(0,2):
            card_dict = starter_cards[i]
            for x in xrange(0,8 if i == 0 else 2):
                card = Card(
                    iid=game.next_iid,
                    name=card_dict['name'],
                    worth=card_dict['worth'],
                    card_type=card_dict['card_type'],
                    buy=card_dict['buy'],
                    kill=card_dict['kill'],
                    instant_worth=card_dict['instant_worth'],
                    instant_buy=card_dict['instant_buy'],
                    instant_kill=card_dict['instant_kill'],
                    faction=card_dict['faction'],
                )
                self.deck.append(card)


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
        if ACTION_COPY in self.game.actions:
            input_string.append('[s]elect card to copy')
        if ACTION_ACQUIRE_TO_PHAND in self.game.actions:
            input_string.append('p[u]t in play')
        if ACTION_KILL in self.game.actions:
            input_string.append('[k]ill enemy')
        if ACTION_USE in self.game.actions:
            input_string.append('[t] use pers')
        if ACTION_BANISH in self.game.actions:
            input_string.append('[b]anish card %s' % (none_choice))
        if ACTION_DISCARD_FROM_PLAYER_HAND in self.game.actions:
            input_string.append('[d]iscard card %s' % (none_choice))
        if ACTION_THIS_OR_THAT in self.game.actions:
            input_string.append('[s0]-%s or [s1]-%s' % (this, that))
            end_turn = False
        if ACTION_KEEP in self.game.actions:
            input_string.append('[k]eep one persistent')
            end_turn = False
        if ACTION_BANISH_PLAYER_PERSISTENT in self.game.actions:
            input_string.append('[d]iscard one persistent')
            end_turn = False
        if ACTION_BANISH_PLAYER_HAND in self.game.actions:
            input_string.append('[b]anish card %s' % (none_choice))
        if ACTION_BANISH_PLAYER_DISCARD in self.game.actions:
            input_string.append('[b]anish card %s' % (none_choice))
        if ACTION_ACQUIRE_TO_TOP in self.game.actions:
            input_string.append('[s]elect card %s' % (none_choice))
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
        #self.buying_power += 1000
        #self.killing_power += 1000

        # check the persistents
        for card in self.phand:
            self.game.play_user_card_effects(card)

    def end_turn(self):
        self.active = False
        self.new_hand()
        self.buying_power = 0
        self.killing_power = 0
        self.game.token = {}
        self.game.token_erasers = {}
        self.game.used_tokens = {}
        os.system(['clear','cls'][os.name == 'nt'])

    def _make_selection(self, display_list):
        selection = raw_input(' | '.join(display_list))
        if selection not in display_list:
            return self._make_selection(display_list)
        return selection

    def raw_card_selection(self):
        return raw_input('select a card ')


    def select_card_action(self, action_list=None):
        input_string = ['deselect']
        for k,v in ACTION_DICT_DISPLAY.iteritems():
            if k in action_list:
                input_string.append(v)

        selection = self._make_selection(input_string)
        for k,v in ACTION_DICT_DISPLAY.iteritems():
            if selection == v:
                return k
        return ACTION_DESELECT



class Computer(Player, ShufflePlayerCardMixin):

    @property
    def is_computer(self):
        return True

    def _make_selection(self, display_list):
        return display_list[len(display_list) - 1]

    def raw_card_selection(self):
        if ACTION_KEEP in self.game.actions:
            for card in self.phand:
                return card.iid

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
            selection = 's0'
        elif ACTION_ACQUIRE_TO_TOP in self.game.actions:
            selection = None
            for idx, card in enumerate(self.game.hand):
                if card.can_acquire_to_top:
                    selection = 's' + str(idx)
                    break

            if not selection:
                selection = 'p0'
        elif ACTION_THIS_OR_THAT in self.game.actions:
            selection = 's0'
        elif ACTION_KEEP in self.game.actions:
            selection = 'k0'
        elif ACTION_BANISH_PLAYER_PERSISTENT in self.game.actions:
            selection = 'd0'
        return selection

