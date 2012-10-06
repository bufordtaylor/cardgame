import random
from player import Player
from deck import PlayerStartDeck, testDeck, print_card_attrs
from shuffle_mixin import ShuffleGameCardMixin
from print_mixin import PrintMixin
from input_mixin import InputMixin

from colors import (
    print_yellow, print_red, print_blue,
    print_green, print_purple,print_color_table,
)

import os


# created for mixin use
# mixin's are used here for code organization
class BaseGame(object):
    card = None
    points = 0
    turn = 0 # player's turn
    game_active = True

    def __init__(self, points, players=None, deck=None):
        self.points = points
        self.players = players or test_players()
        self.discard = []
        self.hand = []
        self.played_user_cards = []
        self.test_deck = test_deck()
        self.deck = deck or self.test_deck
        self.shuffle_deck()
        self.new_hand()

class Game(BaseGame, ShuffleGameCardMixin, PrintMixin, InputMixin):

    def next_player_turn(self):
        self.turn += 1
        if self.turn >= len(self.players):
            self.turn = 0
        self.active_player.new_hand()
        self.played_user_cards = []
        self.active_player.start_turn()

    @property
    def active_player(self):
        return self.players[self.turn]

    def play_card(self, card):
        """overriding mixin, process card attrs here"""
        pass

    def player_loop(self):
        if self.active_player.active:
            self.print_results()
            self.handle_inputs()
        else:
            self.next_player_turn()
            if self.points <= 0:
                self.game_active = False
                print_red('-----GAME OVER------')
                self.print_results()

    def game_loop(self, debug=False):
        while self.game_active:
            self.player_loop()
            if debug:
                self.points -= 1

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
    game = Game(points=2)
    game.game_loop(debug=True)

if __name__ == '__main__':
    main()

