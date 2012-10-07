import random
from player import Player
from card import Card
from deck import (
    PlayerStartDeck,
    testDeck,
    RealDeck,
    print_card_attrs,
    persistant_game_hand,
)
from shuffle_mixin import ShuffleGameCardMixin
from print_mixin import PrintMixin
from input_mixin import (
    InputMixin,
    NOT_ENOUGH_BUY,
    NOT_ENOUGH_KILL,
)

from colors import (
    print_yellow, print_red, print_blue,
    print_green, print_purple,print_color_table,
)

from deck import (
    CARD_TYPE_MONSTER,
    CARD_TYPE_HERO,
    CARD_TYPE_PERSISTENT,
)

import os


# created for mixin use
# mixin's are used here for code organization
class BaseGame(object):
    card = None
    points = 0
    turn = 0 # player's turn
    game_active = True
    debug = True

    def __init__(self, points, players=None, deck=None):
        self.points = points
        self.players = players or test_players()
        self.discard = []
        self.hand = []
        self.played_user_cards = []
        self.test_deck = test_deck()
        self.deck = deck or self.test_deck
        self.phand = [Card(**c) for c in persistant_game_hand]
        self.shuffle_deck()
        self.new_hand()

class Game(BaseGame, ShuffleGameCardMixin, PrintMixin, InputMixin):

    def next_player_turn(self):
        """change player, get new hand, and start turn"""
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

    def play_card(self, card):
        """overriding mixin, process card attrs here"""
        self.active_player.killing_power += card.instant_kill
        self.active_player.buying_power += card.instant_buy
        self.active_player.points += card.instant_worth
        if card.abilities:
            print card.abilities

    def defeat_or_acquire(self, selection, persistent=False):
        card, card_idx = self.sanitize(selection, persistent)
        if not card:
            return self.handle_inputs()
        os.system(['clear','cls'][os.name == 'nt'])

        if card.card_type == CARD_TYPE_MONSTER:
            if self.active_player.killing_power >= card.kill:
                self.defeat_card(card, persistent)
                print_blue('KILLED CARD %s' % card)
            else:
                print_red(NOT_ENOUGH_KILL)
                return self.handle_inputs()
        else:
            if self.active_player.buying_power >= card.buy:
                card= self.get_card(card_idx, persistent)
                self.acquire_card(card, persistent)
                print_blue('BOUGHT CARD %s' % card)
            else:
                print_red(NOT_ENOUGH_BUY)
                return self.handle_inputs()

    def check_abilities(self, action, card=None):
        """loop through player phand to play abilities"""
        print 'not ready yet', action, card

    def acquire_card(self, card, persistent):
        # place acquired card in player's discard deck
        self.active_player.discard.append(card)
        self.active_player.buying_power -= card.buy
        if not persistent:
            self.draw_card()
        self.check_abilities('acquired', card=card)

    def defeat_card(self, card, persistent):
        self.active_player.points += card.instant_worth
        self.active_player.killing_power -= card.kill
        if not persistent:
            self.discard_card(card_idx)
            self.draw_card()
        self.check_abilities('defeated', card=card)

    def player_loop(self):
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

def test_players(num_players=2):
    players = []
    for p in xrange(0,num_players):
        player = Player(name='Player %s' % p)
        players.append(player)
    return players

def test_deck():
    deck = testDeck()
    return deck.deck

def main():
    deck = RealDeck().deck
    game = Game(deck=deck, points=5)
    game.played_user_cards = []
    # calling end_turn here to reset player hand on start up
    for p in game.players:
        p.game = game
        p.end_turn()
    game.active_player.start_turn()
    game.game_loop()

if __name__ == '__main__':
    main()

