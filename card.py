import random
from abilities_constants import *
from constants import *
from colors import (
    bcolors, print_dict, print_green,prepare_card_row,
    print_white, print_blue, print_purple, print_ordered_cards,
)

def get_card_and_deck(game, iid):
    if game.selected_card:
        if game.selected_card.iid == iid:
            return game.selected_card, DECK_SELECTED_CARD
    for c in game.deck:
        if c.iid == iid:
            return c, DECK_GAME_DECK
    for c in game.hand:
        if c.iid == iid:
            return c, DECK_GAME_HAND
    for c in game.phand:
        if c.iid == iid:
            return c, DECK_GAME_PHAND
    for c in game.discard:
        if c.iid == iid:
            return c, DECK_GAME_DISCARD
    for c in game.played_user_cards:
        if c.iid == iid:
            return c, DECK_GAME_PLAYED_USER_CARDS
    for c in game.active_card:
        if c.iid == iid:
            return c, DECK_GAME_ACTIVE_CARD
    for p in game.players:
        for c in p.deck:
            if c.iid == iid:
                return c, DECK_PLAYER_DECK
        for c in p.phand:
            if c.iid == iid:
                return c, DECK_PLAYER_PHAND
        for c in p.hand:
            if c.iid == iid:
                return c, DECK_PLAYER_HAND
        for c in p.discard:
            if c.iid == iid:
                return c, DECK_PLAYER_DISCARD
    for c in game.buy_2_deck:
        if c.iid == iid:
            return c, DECK_GAME_PHAND
    for c in game.buy_3_deck:
        if c.iid == iid:
            return c, DECK_GAME_PHAND
    for c in game.kill_1_deck:
        if c.iid == iid:
            return c, DECK_GAME_PHAND
    return None, None

def get_card_by_iid(game, iid):
    card, deck = get_card_and_deck(game, iid)
    return card

class Card(object):
    cid = -1 # card ID
    iid = -1 # instance ID
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
    move_to = None

    def __init__(self, **kwargs):
        self.actions = []
        for k, v in kwargs.iteritems():
            if hasattr(self, k):
                setattr(self, k, v)

    def __repr__(self):
        return self.name

    def card_row(self, idx, game, player_card=False, game_phand=False):
        """this is for printing purposes only"""
        print 'name:', self.name, ','.join([ACTION_DICT[a] for a in self.actions])
        color = bcolors.WHITE
        if self.mark_for_action:
            color = bcolors.GREEN
        elif self.mark_for_kill:
            color = bcolors.RED
        instruction = (color, self.iid)

        attr_list = [
            instruction,
            (color, self.card_type_string),
            self.card_faction(color),
            (color, self.name),
        ]

        attr_dict = {}

        numbered_attrs = [
            (color, 'buy'),
            (color, 'kill'),
            (color, 'worth'),
            (color, 'instant_buy'),
            (color, 'instant_kill'),
            (color, 'instant_worth'),
            (color, 'abilities'),
        ]

        for k, v in numbered_attrs:
            value = getattr(self, v)
            if v == 'buy':
                if game.token.get('minus_buy', 0) > 0:
                    value = "%s (-%s)" % (value, game.token.get('minus_buy', 0))

                if (self.card_type == CARD_TYPE_PERSISTENT and game.token.get('minus_construct_buy', 0) > 0):
                    value = "%s (-%s)" % (value, game.token.get('minus_construct_buy', 0))

                if (
                    self.card_type == CARD_TYPE_PERSISTENT and
                    self.in_faction(game, MECHANA) and
                    game.token.get('minus_mechana_construct_buy', 0) > 0
                ):
                    value = "%s (-%s)" % (value, game.token.get('minus_buy', 0))
            if v == 'kill' and game.token.get('minus_kill', 0) > 0:
                value = "%s (-%s)" % (value, game.token.get('minus_kill', 0))

            attr_list.append((k, value))
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

    def pop_card_from_persistent_game_backup(self, game):
        popped = None
        if self.cid == STARTING_CARD_BUY_3:
            popped = game.buy_3_deck.pop()
            game.phand[0] = game.buy_3_deck[len(game.buy_3_deck)-1]
        elif self.cid == STARTING_CARD_BUY_2:
            popped = game.buy_2_deck.pop()
            game.phand[1] = game.buy_2_deck[len(game.buy_2_deck)-1]
        else:
            popped = game.kill_1_deck.pop()
            game.phand[2] = game.kill_1_deck[len(game.kill_1_deck)-1]
        return popped

    def card_faction(self, color):
        str = (color, 'MONSTER')
        if self.faction == VOID:
            str = (color, 'VOID')
        elif self.faction == MECHANA:
            str = (color, 'MECHANA')
        elif self.faction == ENLIGHTENED:
            str = (color, 'ENLIGHTENED')
        elif self.faction == LIFEBOUND:
            str = (color, 'LIFEBOUND')
        elif self.is_starting_card:
            str = (color, 'STARTING')
        return str

    def kill_buy_acquire(self, game):
        str = '[c]ard'
        if ACTION_BUY in game.actions or ACTION_KILL in game.actions:
            if self.is_monster:
                str = '[k]ill'
            elif self.is_hero:
                str = '[b]uy'
            elif self.is_persistent:
                str = '[b]uy'
        else:
            str = '[s]elect'
        return str

    def in_faction(self, game, faction):

        if (ALL_CONTRUCTS_ARE_MECHANA in game.token and
            self.card_type == CARD_TYPE_PERSISTENT and
            faction == MECHANA
        ):
            return True

        return faction == self.faction

    def apply_card_tokens(self, game):
        kill = self.kill - game.token.get('minus_kill', 0)
        if kill < 0:
            kill = 0
        buy = self.buy - game.token.get('minus_buy', 0)
        if self.card_type == CARD_TYPE_PERSISTENT:
            buy -= game.token.get('minus_construct_buy', 0)

        if self.in_faction(game, MECHANA) and self.card_type == CARD_TYPE_PERSISTENT:
            buy -= game.token.get('minus_mechana_construct_buy', 0)

        if buy < 0:
            buy = 0

        return kill, buy

    def _determine_actions(self, game_action, game):
        kill, buy = self.apply_card_tokens(game)

        if game_action == ACTION_KEEP:
            for p in game.players:
                if id(self) in [id(c) for c in p.phand]:
                    self.actions.append(ACTION_KEEP)
            return

        if game_action == ACTION_DISCARD_FROM_PLAYER_HAND:
            if self in game.active_player.hand:
                self.actions.append(ACTION_DISCARD_FROM_PLAYER_HAND)

        if game_action == ACTION_COPY:
            if id(self) in [id(c) for c in game.played_user_cards]:
                self.actions.append(ACTION_COPY)

        # unbanishable cards have a banishable token attached to them
        if game_action == ACTION_BANISH:
            if self.banishable:
                self.actions.append(ACTION_BANISH)

        if game_action == ACTION_BANISH_CENTER:
            if self.iid in [c.iid for c in game.hand] and self.banishable:
                self.actions.append(ACTION_BANISH_CENTER)

        if game_action == ACTION_BANISH_PLAYER_HAND:
            if self.iid in [c.iid for c in game.active_player.hand]:
                self.actions.append(ACTION_BANISH_PLAYER_HAND)

        if game_action == ACTION_DEFEAT:
            if self.card_type == CARD_TYPE_MONSTER:
                if game.active_player.killing_power >= kill:
                    self.actions.append(ACTION_DEFEAT)

        if game_action == ACTION_ACQUIRE_TO_TOP:
            if self.card_type == CARD_TYPE_HERO:
                if game.token.get('hero_buying_power', 0) >= buy:
                    self.actions.append(ACTION_ACQUIRE_TO_TOP)

            if self.card_type != CARD_TYPE_MONSTER:
                if game.token.get('minus_buy', 0) >= buy:
                    self.actions.append(ACTION_ACQUIRE_TO_TOP)

        if game_action == ACTION_PLAY:
            # if it's in the player's hand, it's always eligible
            if self.iid in [c.iid for c in game.active_player.hand]:
                self.actions.append(ACTION_PLAY)

            # tokens are set for persistent player cards
            # if a matching token is found on the game, the persistent can be
            # used for further abilities
            for token, card in game.token.iteritems():
                if (
                    game.token.get(token) == card and
                    game.used_tokens.get(token) != card and
                    id(self) in [id(c) for c in game.active_player.phand] and
                    self.abilities in PERSISTENT_USE_LIST
                ):
                    self.actions.append(ACTION_USE)

        # we don't want cards in the user's hands to be marked for buy
        # or for kill
        if self.iid in [c.iid for c in game.active_player.hand]:
            return

        if self.iid in [c.iid for c in game.played_user_cards]:
            return

        if self.iid in [c.iid for c in game.active_player.phand]:
            if (not game.used_tokens.get(self.abilities) and
                self.abilities in PERSISTENT_USE_LIST
            ):
                getattr(game,ABILITY_MAP.get(self.abilities))(card=self)
            return

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

                if (
                    self.card_type == CARD_TYPE_PERSISTENT and
                    self.in_faction(game, MECHANA) and
                    PER_TURN_WHEN_ACQUIRE_MECHANA_CONSTRUCT_PUT_IN_PLAY in game.token
                ):
                    self.actions.append(ACTION_ACQUIRE_TO_PHAND)
                    if ACTION_ACQUIRE_TO_PHAND not in game.actions:
                        game.actions.append(ACTION_ACQUIRE_TO_PHAND)

    def check_actions(self, game):
        self.actions = []
        for action in game.actions:
            self._determine_actions(action, game)

    def list_eligible_actions(self):
        print self.actions

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
    def mark_for_action(self):
        actions = [
            ACTION_BUY,
            ACTION_BANISH,
            ACTION_COPY,
            ACTION_DISCARD_FROM_PLAYER_HAND,
            ACTION_ACQUIRE_TO_PHAND,
            ACTION_ACQUIRE_TO_HAND,
            ACTION_ACQUIRE_TO_TOP,
            ACTION_ACQUIRE_TO_DISCARD,
            ACTION_USE,
            ACTION_BANISH_PLAYER_PERSISTENT,
            ACTION_BANISH_PLAYER_DISCARD,
            ACTION_BANISH_PLAYER_HAND,
        ]
        return any(self._is_eligible_for_action(action) for action in actions)

    @property
    def mark_for_kill(self):
        actions = [ACTION_KILL, ACTION_DEFEAT]
        return any(self._is_eligible_for_action(action) for action in actions)

    @property
    def can_buy(self):
        return self._is_eligible_for_action(ACTION_BUY)

    @property
    def can_play(self):
        return self._is_eligible_for_action(ACTION_PLAY)

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
    def can_acquire_to_phand(self):
        return self._is_eligible_for_action(ACTION_ACQUIRE_TO_PHAND)

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

