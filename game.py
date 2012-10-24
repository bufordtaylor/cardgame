import random
import os
from player import Player
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
        self.points = points
        self.players = players or test_players()
        self.discard = []
        self.hand = []
        self.played_user_cards = []
        self.active_card = []
        self.test_deck = test_deck()
        self.deck = deck or self.test_deck
        self.phand = [Card(**c) for c in persistant_game_hand]
        self.shuffle_deck()
        self.new_hand()
        # tokens are used to override player's buy or kill powers,
        # or add special abilities
        self.token = {}
        self.used_tokens = {}
        # token erasers denote when to erase each token
        self.token_erasers = {}
        self.actions = ACTION_NORMAL

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

    def must_copy_card(self):
        self.change_action([ACTION_COPY])
        self.select_card(num=1, where=WHERE_PLAYED, must=True)

    def can_discard_card(self, num, must=False):
        self.change_action([ACTION_DISCARD_FROM_PLAYER_HAND])
        self.select_card(num=num, where=WHERE_PLAYER_HAND, must=must)

    def must_banish_card(self, num, where):
        self.can_banish_card(num, where, must_banish=True)

    def set_token(self, kind, value, end):
        if isinstance( value, (int, long)) and self.token.get(kind):
            self.token[kind] += value
            self.token_erasers[kind] = end
        else:
            self.token[kind] = value
            self.token_erasers[kind] = end

    def can_defeat_card(self, where=WHERE_GAME_HAND, killing_power=0):
        self.set_token('minus_kill', killing_power, END_OF_ACTION)
        self.select_card(1, where=where, must=False)

    def must_acquire_card(self, where=WHERE_GAME_HAND):
        self.can_acquire_card(where=where, must=True)

    def can_acquire_card(self,
        where=WHERE_GAME_HAND, must=False, buying_power=0
    ):
        self.set_token('buying_power', buying_power, END_OF_ACTION)
        self.select_card(1, where=where, must=must)

    def can_banish_card(self, num, where, must_banish=False):
        self.select_card(num, where, must_banish)

    def move_card(self, card, card_idx, from_deck):

        if from_deck == WHERE_GAME_HAND:
            # get_card removes it from deck hand
            card = self.get_card(card_idx)
            self.selected_card = card
            if ACTION_BANISH in self.actions:
                # banish to game discard deck ACTION_BANISH
                self.discard.append(card)
            elif ACTION_DEFEAT in self.actions:
                self.discard.append(card)
            elif ACTION_ACQUIRE_TO_TOP in self.actions:
                self.active_player.deck.append(card)
            self.draw_card()
        elif from_deck == WHERE_PLAYED:
            # used in ACTION_COPY
            self.selected_card = card
            self.play_user_card_effects(card)
        elif from_deck == WHERE_PLAYER_HAND:
            # get_card removes it from player hand
            card = self.active_player.get_card(card_idx)
            self.selected_card = card
            if ACTION_DISCARD_FROM_PLAYER_HAND in self.actions:
                # move card to player's discard deck
                self.active_player.discard.append(card)
            else:
                # move card to game discard deck ACTION_BANISH
                self.discard.append(card)
        elif from_deck == WHERE_PERSISTENT:
            # get_card removes it from player hand ACTION_BANISH
            card = self.active_player.get_card(card_idx, persistent=True)
            self.selected_card = card
            # move card from phand to player discard deck
            self.active_player.discard.append(card)

        self.check_tokens_for_use_once()

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

    def select_card(self, num, where, must=False):
        """
        select a card to perform an action on it.
        num is number of cards to select
        where is where the card should be selected from
        must is if a card must be selected vs not having to select one
        """
        for x in xrange(num):
            card, card_idx = self.handle_select_inputs(where, must=must)
            # they've chosen [n]one here, just move on
            if not card:
                self.selected_card = None
                return

            self.move_card(card, card_idx, from_deck=where)

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

    def play_user_card(self, selection, persistent=False):
        card, card_idx = self.sanitize(selection, persistent, player_card=True)
        if not card:
            return self.handle_inputs()
        os.system(['clear','cls'][os.name == 'nt'])

        # get_card removes card from player hand list
        card = self.active_player.get_card(card_idx, persistent)
        self.active_card.append(card)
        self.play_user_card_effects(card)
        if card.card_type == CARD_TYPE_PERSISTENT:
            self.active_player.phand.append(card)
            #TODO we are calling this in play_user_card_effects
            self.check_cards_eligibility()
        else:
            self.played_user_cards.append(card)
        self.active_card = []
        return card

    def play_user_card_effects(self, card):
        self.active_player.killing_power += card.instant_kill
        self.active_player.buying_power += card.instant_buy
        self.active_player.points += card.instant_worth
        print_blue('PLAYED CARD %s' % card)
        self.play_abilities(card)
        self.check_tokens_for_card_played(card)


    def defeat_or_acquire(self, selection, persistent=False):
        card, card_idx = self.sanitize(selection, persistent)
        if not card:
            return self.handle_inputs()
        os.system(['clear','cls'][os.name == 'nt'])
        moved_card = None

        if not card.can_buy and not card.can_kill:
            print_red('%s - Card not eligible for selection' % card.name)
            self.debug_counter += 1
            if self.debug_counter > 5:
                return None, None
            return self.handle_inputs()

        if card.card_type == CARD_TYPE_MONSTER:
            if self.active_player.killing_power >= card.kill:
                card= self.get_card(card_idx, persistent)
                moved_card = self.defeat_card(card, persistent)
                print_blue('KILLED CARD %s' % card)
            else:
                print_red(NOT_ENOUGH_KILL)
                return self.handle_inputs()
        else:
            card= self.get_card(card_idx, persistent)
            moved_card = self.acquire_card(card, persistent)
        return moved_card

    def acquire_card(self, card, persistent):
        kill, buy = card.apply_card_tokens(self)
        self.remove_token('minus_buy')
        self.active_player.buying_power -= buy

        if card.card_type == CARD_TYPE_PERSISTENT:
            self.remove_token('minus_construct_buy')

        if card.in_faction(self, MECHANA) and card.card_type == CARD_TYPE_PERSISTENT:
            self.remove_token('minus_mechana_construct_buy')

        if not persistent:
            self.draw_card()

        if card.move_to == WHERE_PLAYER_PERSISTENT:
            self.selected_card = card
            card.move_to = None
            self.play_user_card_effects(card)
            self.active_player.phand.append(card)
        else:
            # place acquired card in player's discard deck
            self.active_player.discard.append(card)
        return card

    def defeat_card(self, card, persistent):
        kill, buy = card.apply_card_tokens(self)
        self.remove_token('minus_kill')
        self.active_player.points += card.instant_worth
        self.active_player.killing_power -= kill

        if PER_TURN_PLUS_1_KILL_FIRST_MONSTER_DEFEAT_PLUS_1_POINT in self.token:
            self.active_player.points += 1
            self.use_token(PER_TURN_PLUS_1_KILL_FIRST_MONSTER_DEFEAT_PLUS_1_POINT)

        self.selected_card = card
        if not persistent:
            self.draw_card()

        if not persistent:
            self.discard.append(self.selected_card)

        self.play_abilities(card)
        self.check_tokens_for_use_once()
        return card

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

