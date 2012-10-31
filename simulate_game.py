from deck import SimDeck
from game import Game
from player import Computer
from colors import *

class SimulateGame(Game):

    def shuffle_deck(self): pass

    def player_loop(self):
        print_red('remaining points %s' % self.points)
        if self.active_player.active:
            self.normal_action()
        else:
            self.next_player_turn()
            if self.num_turns % len(self.players) == 0:
                if self.debug:
                    if self.round > 0:
                        self.game_active = False
                self.round += 1
                if self.points <= 0:
                    self.game_active = False
                    print_red('-----GAME OVER------')
                    self.print_results()

def test_players(game, num_players=2):
    players = []
    for p in xrange(0,num_players):
        player = Computer(name='Player %s' % p, game=game)
        players.append(player)
    return players

def main():
    deck = SimDeck().deck
    game = SimulateGame(deck=deck, points=55)
    game.played_user_cards = []
    # calling end_turn here to reset player hand on start up
    for p in game.players:
        p.game = game
        p.end_turn()
    game.active_player.start_turn()
    game.game_loop()

if __name__ == '__main__':
    main()

