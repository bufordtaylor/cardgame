import random
import os
from player import Player, Computer
from card import Card
from abilities_constants import *
from constants import *
from deck import (
    PlayerStartDeck,
    testDeck,
    RealDeck,
    print_card_attrs,
    persistant_game_hand,
)
from shuffle_mixin import ShuffleGameCardMixin
from print_mixin import PrintMixin
from abilities_mixin import AbilitiesMixin
from input_mixin import InputMixin

from colors import (
    print_yellow, print_red, print_blue,
    print_green, print_purple,print_color_table,
)

# created for mixin use
# mixin's are used here for code organization
class BaseGame(object):
    card = None
    points = 0
    turn = 0 # player's turn
    game_active = True
    debug = False
    selected_card = None #card being banished, copied, etc. Used for testing, not displayed
    debug_counter = 0
    active_card = None
    extra_turn = False

    def __init__(self, points, players=None, deck=None):
        self.players = []
        self.points = points
        self.discard = []
        self.hand = []
        # doing some weird stuff with next_iid so we have to init phand and
        # deck before this
        self.phand = []
        self.deck = []
        self.played_user_cards = []
        self.active_card = []
        self.test_deck = test_deck()
        self.deck = deck or self.test_deck

        # make 50 copies of each game persistent and then put them in the
        # game's persistent hand
        self.buy_3_deck = []
        self.buy_2_deck = []
        self.kill_1_deck = []
        for c in persistant_game_hand:
            for i in xrange(50):
                if c['cid'] == STARTING_CARD_BUY_3:
                    self.buy_3_deck.append(Card(iid=self.next_iid, **c))
                elif c['cid'] == STARTING_CARD_BUY_2:
                    self.buy_2_deck.append(Card(iid=self.next_iid, **c))
                elif c['cid'] == STARTING_CARD_KILL_1:
                    self.kill_1_deck.append(Card(iid=self.next_iid, **c))

        self.phand.append(self.buy_3_deck.pop())
        self.phand.append(self.buy_2_deck.pop())
        self.phand.append(self.kill_1_deck.pop())

        # players must come after deck and phand is created
        self.players = players or test_players(game=self)
        self.init_player_decks()

        # all iid's must be assigned before shuffling
        self.shuffle_deck()
        self.new_hand()
        # tokens are used to override player's buy or kill powers,
        # or add special abilities
        self.token = {}
        self.used_tokens = {}
        # token erasers denote when to erase each token
        self.token_erasers = {}
        self.actions = ACTION_NORMAL

    @property
    def next_iid(self):
        cnt = len(self.deck) + len(self.buy_3_deck) + len(self.buy_2_deck) + len(self.kill_1_deck) + len(self.phand)
        for p in self.players:
            cnt += len(p.deck)
        return cnt

    def get_card_by_iid(self, iid):
        if self.selected_card:
            if self.selected_card.iid == iid:
                return self.selected_card
        for c in self.deck:
            if c.iid == iid:
                return c
        for c in self.hand:
            if c.iid == iid:
                return c
        for c in self.phand:
            if c.iid == iid:
                return c
        for c in self.discard:
            if c.iid == iid:
                return c
        for c in self.played_user_cards:
            if c.iid == iid:
                return c
        for c in self.active_card:
            if c.iid == iid:
                return c
        for p in self.players:
            for c in p.deck:
                if c.iid == iid:
                    return c
            for c in p.phand:
                if c.iid == iid:
                    return c
            for c in p.hand:
                if c.iid == iid:
                    return c
            for c in p.discard:
                if c.iid == iid:
                    return c
        return None

    def init_player_decks(self):
        for p in self.players:
            p.init_deck(self)

class Game(
        BaseGame,
        ShuffleGameCardMixin,
        PrintMixin,
        InputMixin,
        AbilitiesMixin
    ):

    def next_player_turn(self):
        """change player, get new hand, and start turn"""
        if self.extra_turn:
            self.played_user_cards = []
            self.active_player.start_turn()
            self.extra_turn = False
            return

        self.turn += 1
        if self.turn >= len(self.players):
            self.turn = 0
        self.played_user_cards = []
        self.active_player.start_turn()
        if self.debug:
            self.points -= 1

    @property
    def active_player(self):
        return self.players[self.turn]


    def set_token(self, kind, value, end):
        if isinstance( value, (int, long)) and self.token.get(kind):
            self.token[kind] += value
            self.token_erasers[kind] = end
        else:
            self.token[kind] = value
            self.token_erasers[kind] = end

    def remove_token(self, token):
        try:
            del self.token[token]
            del self.token_erasers[token]
        except KeyError:
            pass
        self.check_cards_eligibility()

    def use_token(self, token):
        try:
            self.used_tokens[token] = self.token[token]
            self.remove_token(token)
        except KeyError:
            pass

    def check_tokens_for_use_once(self):
        # clear out tokens that are use once
        to_delete = []
        for k, v in self.token_erasers.iteritems():
            if v == END_OF_ACTION:
                del self.token[k]
                to_delete.append(k)
        for t in to_delete:
            del self.token_erasers[t]

    def change_action(self, actions):
        print 'CHANGING ACTION'
        print 'from:', ','.join([ACTION_DICT[a] for a in self.actions])
        self.actions = actions
        print 'to:', ','.join([ACTION_DICT[a] for a in self.actions])
        self.check_cards_eligibility()
        print 'game tokens', self.token


    def play_abilities(self, card):
        if not card.abilities:
            self.selected_card = None
            self.change_action(ACTION_NORMAL)
            return

        self.selected_card = None
        getattr(self,ABILITY_MAP.get(card.abilities))(card=card)
        self.change_action(ACTION_NORMAL)

    def check_tokens_for_card_played(self, card):
        if card.in_faction(self, MECHANA) and card.card_type == CARD_TYPE_PERSISTENT:
            if PER_TURN_WHEN_PLAY_MECHANA_CONSTRUCT_DRAW_1_INCLUDING_THIS_ONE in self.token:
                self.draw_1()
                self.use_token(PER_TURN_WHEN_PLAY_MECHANA_CONSTRUCT_DRAW_1_INCLUDING_THIS_ONE)

        if card.in_faction(self, LIFEBOUND):
            if (
                PER_TURN_PLUS_1_BUY_FIRST_LIFEBOUND_HERO_PLUS_1_POINT in self.token and
                card.card_type == CARD_TYPE_HERO
            ):
                self.active_player.points += 1
                self.use_token(PER_TURN_PLUS_1_BUY_FIRST_LIFEBOUND_HERO_PLUS_1_POINT)


    # XXX not unit tested
    def play_all_user_cards(self, selection):
        if len(self.active_player.hand) == 0:
            print_red('No cards left to play')
            os.system(['clear','cls'][os.name == 'nt'])
        # play all cards until therea re no more
        while self.active_player.hand:
            self.play_user_card(selection='c0')

    def check_cards_eligibility(self):
        """go through each card and mark eligiblity for current actions"""
        for c in self.hand:
            c.check_actions(self)
        for c in self.phand:
            c.check_actions(self)
        for c in self.discard:
            c.check_actions(self)
        for c in self.active_player.phand:
            c.check_actions(self)
        for c in self.active_player.hand:
            c.check_actions(self)
        for c in self.active_player.discard:
            c.check_actions(self)
        if ACTION_KEEP in self.actions:
            for p in self.players:
                for c in p.phand:
                    c.check_actions(self)
                for c in p.hand:
                    c.check_actions(self)
                for c in p.discard:
                    c.check_actions(self)

    def play_user_card_persistent(self, selection, action=ACTION_USE):
        card, card_idx = self.sanitize(selection, persistent=True, player_card=True)
        if not card:
            return self.handle_inputs()
        os.system(['clear','cls'][os.name == 'nt'])
        if action in card.actions:
            getattr(
                self,ABILITY_MAP.get(card.abilities)
            )(card=card, action=action)
        return card

    def play_user_card_effects(self, card):
        self.active_player.killing_power += card.instant_kill
        self.active_player.buying_power += card.instant_buy
        self.active_player.points += card.instant_worth
        self.points -= card.instant_worth
        if self.points < 0:
            self.points = 0
        print_blue('PLAYED CARD %s' % card)
        self.play_abilities(card)
        self.check_tokens_for_card_played(card)

    def player_loop(self):
        print_red('remaining points %s' % self.points)
        if self.active_player.active:
            self.handle_inputs()
        else:
            self.next_player_turn()
            if self.points <= 0:
                self.game_active = False
                print_red('-----GAME OVER------')
                self.print_results()

    def game_loop(self):
        while self.game_active:
            self.player_loop()

def test_players(game, num_players=2):
    players = []
    for p in xrange(0,num_players):
        player = Computer(name='Player %s' % p, game=game)
        players.append(player)
    return players

def test_deck():
    deck = testDeck()
    return deck.deck

def main():
    deck = RealDeck().deck
    game = Game(deck=deck, points=55)
    game.played_user_cards = []
    # calling end_turn here to reset player hand on start up
    for p in game.players:
        p.game = game
        p.end_turn()
    game.active_player.start_turn()
    game.game_loop()

if __name__ == '__main__':
    main()

