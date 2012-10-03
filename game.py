import random
from player import Player
from deck import PlayerStartDeck, testDeck, print_card_attrs
from shuffle_mixin import ShuffleMixin

from colors import (
    print_yellow, print_red, print_blue,
    print_green, print_purple,print_color_table,
)

import os

def cls():
    os.system(['clear','cls'][os.name == 'nt'])

def test_players(num_players=2):
    players = []
    for p in xrange(0,num_players):
        player = Player(name='Player %s' % p)
        players.append(player)
    return players

def test_deck():
    deck = testDeck()
    return deck.deck

class BaseGame(object): pass

class Game(BaseGame, ShuffleMixin):
    players = None
    deck = None
    discard = []
    hand = []
    played_user_cards = []
    card = None
    points = 0
    turn = 0 # player's turn
    game_active = True

    def __init__(self, points, players=None, deck=None):
        self.points = points
        self.players = players or test_players()
        self.deck = deck or test_deck()
        self.shuffle_deck()
        self.new_hand()

    def next_player_turn(self):
        self.active_player.new_hand()
        self.played_user_cards = []
        self.turn += 1
        if self.turn >= len(self.players):
            self.turn = 0
        self.active_player.start_turn()

    @property
    def active_player(self):
        return self.players[self.turn]

    def print_hand(self):
        print_purple('-----------IN GAME--------------')
        card_rows = []
        for idx,card in enumerate(self.hand):
            card_rows.append(card.card_row(idx))
        print_color_table(card_rows)

    def print_user_played_cards(self):
        print_purple('------------USER PLAYED CARDS----------------')
        print_card_attrs()
        for card in self.played_user_cards:
            print card
        print

    def handle_inputs(self):
        if self.active_player.is_computer:
            print 'doing computer shit'
            return

        self.print_hand()
        self.active_player.print_hand()
        selection = raw_input(
            'play [c]ard - [k]ill enemy - [b]uy heroes - [e]nd turn:\n'
        )

        if selection == 'e':
            self.active_player.end_turn()
            return

        if selection.startswith('c'):
            try:
                card_played = self.active_player.play_card(int(selection[1:]))
            except ValueError:
                card_played = None

            if not card_played:
                cls()
                if len(self.active_player.hand) == 0:
                    print_red(
                        'You have no cards left. You should end your turn'
                    )
                else:
                    print_red('Invalid card. Try a number 0 - %s. EX: c3 for the card with the 3 in front of it' % (
                        len(self.active_player.hand) - 1
                    ))
                return self.handle_inputs()

            self.play_card(card_played)
            self.played_user_cards.append(card_played)
            raw_input()


    def play_card(self, card):
        """overriding mixin, process card attrs here"""
        print_blue('PLAYING CARD %s' % card)

    def print_results(self):
        for p in self.players:
            print p

    def player_loop(self):
        cls()
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

def main():
    game = Game(points=2)
    game.game_loop(debug=True)

if __name__ == '__main__':
    main()

