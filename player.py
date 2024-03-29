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

    @property
    def hand_iids(self):
        return [c.iid for c in self.hand]

    @property
    def phand_iids(self):
        return [c.iid for c in self.phand]

    @property
    def discard_iids(self):
        return [c.iid for c in self.discard]

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
        if action_list == ACTION_NORMAL:
            input_string.append('end turn')
        for k,v in ACTION_DICT_DISPLAY.iteritems():
            if k in action_list:
                input_string.append(v)

        selection = self._make_selection(input_string)
        for k,v in ACTION_DICT_DISPLAY.iteritems():
            if selection == v:
                return k
        return ACTION_DESELECT

class Computer(Player, ShufflePlayerCardMixin):
    """computer is a dumb machine that always chooses the first available
    action without thinking ahead"""

    @property
    def is_computer(self):
        return True

    def _make_selection(self, display_list):
        print display_list
        return display_list[len(display_list) - 1]

    def raw_card_selection(self):

        # built in for testing purposes to override an action
        if hasattr(self.game, '_force_actions'):
            self.game.actions = self.game._force_actions
            delattr(self.game, '_force_actions')

        if ACTION_KEEP in self.game.actions:
            for card in self.phand:
                return card.iid

        # play all cards before deciding to action_kill or action_buy
        if ACTION_PLAY in self.game.actions:

            # if we can use a persistent, use it first
            for idx, c in enumerate(self.phand):
                if c.can_use:
                    return c.iid

            for c in self.hand:
                if c.can_play:
                    return c.iid

        if ACTION_ACQUIRE_TO_TOP in self.game.actions:
            for c in self.game.hand:
                if c.can_acquire_to_top:
                    return c.iid

        if ACTION_DISCARD_FROM_PLAYER_HAND in self.game.actions:
            return self.hand[0].iid

        if ACTION_BANISH_PLAYER_HAND in self.game.actions:
            return self.hand[0].iid

        if ACTION_COPY in self.game.actions:
            try:
                return self.game.played_user_cards[0].iid
            except IndexError:
                return None

        if ACTION_BANISH_CENTER in self.game.actions:
            for idx, c in enumerate(self.game.hand):
                if c.banishable:
                    return c.iid

        if ACTION_ACQUIRE_TO_PHAND in self.game.actions:
            for card in self.game.hand:
                if card.can_acquire_to_phand:
                    return card.iid

        if ACTION_BUY in self.game.actions:
            if hasattr(self.game, '_override_buy') and getattr(self.game,'_override_buy') == 'mystic':
                for idx, c in enumerate(self.game.phand):
                    if c.name == 'mystic':
                        delattr(self.game, '_override_buy')
                        return c.iid

            if hasattr(self, '_override_buy') == 'heavy infantry':
                for idx, c in enumerate(self.game.phand):
                    if c.name == 'heavy infantry':
                        delattr(self.game, '_override_buy')
                        return c.iid

            for idx, c in enumerate(self.game.hand):
                if c.can_buy:
                    return c.iid

            if len(self.game.buy_3_deck) == 1 or len(self.game.buy_2_deck) == 1:
                return None

            for idx, c in enumerate(self.game.phand):
                if c.can_buy:
                    return c.iid

        if ACTION_DEFEAT in self.game.actions:
            # if override, kill cultist
            if hasattr(self.game, '_override_kill') and getattr(self.game, '_override_kill') == 'cultist':
                for idx, c in enumerate(self.game.phand):
                    if c.name == 'cultist' and c.can_defeat:
                        delattr(self.game, '_override_kill')
                        return c.iid

            # kill first available monster
            for idx, c in enumerate(self.game.hand):
                if c.can_defeat:
                    return c.iid

            if len(self.game.kill_1_deck) == 1:
                return None

            # fall through to kill cultist anyway
            for idx, c in enumerate(self.game.phand):
                if c.name == 'cultist' and c.can_defeat:
                    return c.iid

        if ACTION_KILL in self.game.actions:
            # if override, kill cultist
            if hasattr(self.game, '_override_kill') and getattr(self.game, '_override_kill') == 'cultist':
                for idx, c in enumerate(self.game.phand):
                    if c.name == 'cultist' and c.can_kill:
                        delattr(self.game, '_override_kill')
                        return c.iid

            # kill first available monster
            for idx, c in enumerate(self.game.hand):
                if c.can_kill:
                    return c.iid

            if len(self.game.kill_1_deck) == 1:
                return None

            # fall through to kill cultist anyway
            for idx, c in enumerate(self.game.phand):
                if c.name == 'cultist' and c.can_kill:
                    return c.iid

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

