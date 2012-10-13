import unittest
import random
from game import Game
from deck import RealDeck
from player import Computer

from constants import *
from abilities_constants import *

class TestGame(unittest.TestCase):
    game = None
    deck = None

    def setUp(self):
        self.deck = RealDeck().deck
        self.players = []
        for p in xrange(0,2):
            player = Computer(name='Player %s' % p)
            self.players.append(player)
        self.game = Game(deck=self.deck, points=15, players=self.players)
        self.game.played_user_cards = []
        # calling end_turn here to reset player hand on start up
        for p in self.game.players:
            p.game = self.game
            p.end_turn()
        self.game.active_player.start_turn()


    def test_game_deck(self):
        """sanity check"""
        self.assertNotEquals(len(self.game.deck), 0)

    def test_active_player(self):
        """make sure turns work for the active player"""
        self.assertEquals(self.game.turn, 0)
        self.assertEquals(self.game.active_player.name, 'Player 0')
        self.game.active_player.end_turn()
        self.game.next_player_turn()
        self.assertEquals(self.game.turn, 1)
        self.assertEquals(self.game.active_player.name, 'Player 1')

    def test_play_user_card(self):
        """
        card should be in game.played_user_cards list,
        and removed from player hand
        """
        self.assertEquals(len(self.game.played_user_cards), 0)
        #
        # simulate playing card at zero position
        card = self.game.play_user_card('c0')
        obj_id = id(card)

        # check all the points that should've been added
        self.assertEqual(self.game.active_player.killing_power, card.instant_kill)
        self.assertEqual(self.game.active_player.buying_power, card.instant_buy)
        self.assertEqual(self.game.active_player.points, card.instant_worth)

        # check card is not in hand anymore, and it is in played user cards
        self.assertFalse(obj_id in [id(c) for c in self.game.active_player.hand])
        self.assertTrue(obj_id in [id(c) for c in self.game.played_user_cards])

    def test_defeat_or_acquire_persistents(self):
        """
        defeating or acquiring game hand cards adds them to player discard hand
        and removes them from the game hand
        """
        #inflate buying and killing power
        self.game.active_player.killing_power = 1000
        self.game.active_player.buying_power = 1000

        killing_power = self.game.active_player.killing_power
        buying_power = self.game.active_player.buying_power
        self.game.check_cards_eligibility()

        # acquire a persistent game card
        card = self.game.defeat_or_acquire(selection='p0', persistent=True)
        # card appears in player's discard deck
        self.assertTrue(id(card) in [id(c) for c in self.game.active_player.discard])
        # card still in game deck
        self.assertTrue(card.name in [c.name for c in self.game.phand])
        # appropriate points reduced from player buying power
        self.assertEqual(self.game.active_player.buying_power, buying_power - card.buy)

        # kill a persistent game card
        card = self.game.defeat_or_acquire(selection='p2', persistent=True)
        # card does not appear in player's discard deck
        self.assertTrue(card.name not in [c.name for c in self.game.active_player.discard])
        # card still in game deck
        self.assertTrue(card.name in [c.name for c in self.game.phand])
        # appropriate points reduced from player killing power
        #

    def _get_card(self, name):
        for idx, c in enumerate(self.deck):
            if c.name == name:
                return c

    def _fake_hand(self, card_name):
        # force card at 0 position, fill the rest of the hand so no collisions
        fake_cards = [None]
        action_card = None
        for idx, c in enumerate(self.deck):
            if c.name == card_name:
                action_card = c
                del self.deck[idx]
            else:
                if len(fake_cards) <= 4:
                    fake_cards.append(c)
        self.game.hand[0] = action_card
        for i in xrange(1,5):
            self.game.hand[i] = fake_cards[i]
        return action_card

    def _fake_user_hand(self, ability_name, secondary_ability=None):
        action_card = None
        secondardy_card = None
        for idx, c in enumerate(self.deck):
            if c.abilities == secondary_ability:
                secondardy_card = c
            if c.abilities == ability_name:
                action_card = c
                if not secondary_ability:
                    break
        self.game.active_player.hand[0] = action_card
        if secondary_ability:
            self.game.active_player.hand[1] = secondardy_card

    def test_game_tokens(self):
        self.game.set_token('test_token', 5, END_OF_ACTION)
        self.assertEqual(self.game.token.get('test_token'), 5)
        self.game.check_tokens_for_use_once()
        self.assertEqual(self.game.token.get('test_token'), None)

    def test_defeat_or_acquire_regulars(self):
        """
        defeating or acquiring game hand cards adds them to player discard hand
        and removes them from the game hand
        """
        #inflate buying and killing power
        self.game.active_player.killing_power = 1000
        self.game.active_player.buying_power = 1000
        self._fake_hand('Cetra, Weaver of Stars')

        killing_power = self.game.active_player.killing_power
        buying_power = self.game.active_player.buying_power
        self.game.check_cards_eligibility()

        # acquire a regular game card
        card = self.game.defeat_or_acquire(selection='b0')
        # card appears in player's discard deck
        self.assertTrue(id(card) in [id(c) for c in self.game.active_player.discard])
        # card not in game deck
        self.assertTrue(id(card) not in [id(c) for c in self.game.hand])
        # appropriate points reduced from player buying power
        self.assertEqual(self.game.active_player.buying_power, buying_power - card.buy)


        self._fake_hand('Avatar of the Fallen')
        # kill a regular game card
        self.game.check_cards_eligibility()
        card = self.game.defeat_or_acquire(selection='k0')
        # card does not in player's discard deck
        self.assertTrue(id(card) not in [id(c) for c in self.game.active_player.discard])
        # card not in game deck
        self.assertTrue(id(card) not in [id(c) for c in self.game.hand])
        # card is in in game discard deck
        self.assertTrue(id(card) in [id(c) for c in self.game.discard])
        # appropriate points reduced from player killing power
        self.assertEqual(self.game.active_player.killing_power, killing_power - card.kill)

    def test_instant_ability_draw_card(self):
        # increase initial count so that we have a total of 11 cards
        # this is so that when we have played our 3 draw cards, we have 8
        # cards in hand
        self.game.active_player.deck.append(self.game.deck.pop())
        self._fake_user_hand(DRAW_1)
        self.assertEqual(len(self.game.active_player.hand), 5)
        card = self.game.play_user_card('c0')
        self.assertEqual(len(self.game.active_player.hand), 5)

        self._fake_user_hand(DRAW_2)
        self.assertEqual(len(self.game.active_player.hand), 5)
        card = self.game.play_user_card('c0')
        self.assertEqual(len(self.game.active_player.hand), 6)

        self._fake_user_hand(DRAW_3)
        self.assertEqual(len(self.game.active_player.hand), 6)
        card = self.game.play_user_card('c0')
        self.assertEqual(len(self.game.active_player.hand), 8)

    def test_instant_ability_banish(self):
        self._fake_user_hand(DRAW_2_THEN_BANISH_1_HAND)
        card = self.game.play_user_card('c0')
        selected_card = self.game.selected_card
        self.assertTrue(id(selected_card) in [id(c) for c in self.game.discard])
        self.assertTrue(id(selected_card) not in [id(c) for c in self.game.active_player.hand])
        self.assertTrue(id(selected_card) not in [id(c) for c in self.game.active_player.discard])

        self._fake_user_hand(DRAW_1_BANISH_CENTER)
        card = self.game.play_user_card('c0')
        selected_card = self.game.selected_card
        self.assertTrue(id(selected_card) in [id(c) for c in self.game.discard])
        self.assertTrue(id(selected_card) not in [id(c) for c in self.game.active_player.hand])
        self.assertTrue(id(selected_card) not in [id(c) for c in self.game.active_player.discard])

         #cannot banish avatar
        self._fake_hand('Avatar of the Fallen')
        self._fake_user_hand(DRAW_1_BANISH_CENTER)
        card = self.game.play_user_card('c0')
        selected_card = self.game.selected_card
        self.assertTrue(id(selected_card) not in [id(c) for c in self.game.discard])
        self.assertTrue(id(selected_card) not in [id(c) for c in self.game.active_player.hand])
        self.assertTrue(id(selected_card) not in [id(c) for c in self.game.active_player.discard])
        #XXX need to test banish_construct

    def test_kill_ability_banish(self):
        self._fake_user_hand(CAN_BANISH_1_HAND_OR_DISCARD_AND_CENTER)
        card = self._get_card('Voidthirster')
        self.game.active_player.discard.append(card)
        card = self.game.play_user_card('c0')
        selected_card = self.game.selected_card
        self.assertTrue(len(self.game.active_player.hand), 4)
        self.assertTrue(len(self.game.active_player.discard), 0)
        self.assertTrue(len(self.game.discard), 2)

    def test_instant_ability_discard(self):
        self._fake_user_hand(IF_DISCARD_DRAW_TWO)
        card = self.game.play_user_card('c0')
        selected_card = self.game.selected_card
        self.assertTrue(id(selected_card) in [id(c) for c in self.game.active_player.discard])
        self.assertTrue(id(selected_card) not in [id(c) for c in self.game.active_player.hand])
        self.assertTrue(len(self.game.active_player.hand), 6)

    def test_instant_ability_copy_no_card(self):
        # no card to emulate, so it just plays it
        self._fake_user_hand(COPY_EFFECT)
        card = self.game.play_user_card('c0')
        selected_card = self.game.selected_card
        self.assertTrue(id(selected_card) not in [id(c) for c in self.game.active_player.discard])
        self.assertTrue(id(selected_card) not in [id(c) for c in self.game.active_player.hand])
        self.assertTrue(len(self.game.active_player.hand), 4)

    def test_instant_ability_add_random_cards_to_hand(self):
        # no card to emulate, so it just plays it
        card = self._get_card('Xeron, Duke of Lies')
        self.game.play_abilities(card)
        self.assertTrue(len(self.game.active_player.hand), 6)
        for p in self.game.players:
            if p != self.game.active_player:
                self.assertTrue(len(self.game.active_player.hand), 4)

    def test_instant_ability_copy(self):
        # set up copy with another card
        self._fake_user_hand(IF_DISCARD_DRAW_TWO)
        played_card = self.game.play_user_card('c0')
        selected_card = self.game.selected_card
        self.assertTrue(len(self.game.active_player.hand), 6)

        # emulate other card
        self._fake_user_hand(COPY_EFFECT)
        card = self.game.play_user_card('c0')
        selected_card = self.game.selected_card
        self.assertTrue(id(selected_card) in [id(c) for c in self.game.active_player.discard])
        self.assertTrue(id(selected_card) not in [id(c) for c in self.game.active_player.hand])
        self.assertTrue(len(self.game.active_player.hand), 7)

    def test_kill_eligibility(self):
        test_cards = {
            'Avatar of the Fallen': [False, True],
            'Voidthirster': [False, False],
        }
        for k, v in test_cards.iteritems():
            card = self._fake_hand(k)
            self.assertEqual(card.can_kill, v[0])
            self.game.active_player.killing_power = 100
            self.game.change_action(ACTION_NORMAL)
            self.assertEqual(card.can_kill, v[1])

    def test_buy_eligibility(self):
        test_cards = {
            'Avatar of the Fallen': [False, False],
            'Voidthirster': [False, True],
        }
        for k, v in test_cards.iteritems():
            card = self._fake_hand(k)
            self.assertEqual(card.can_buy, v[0])
            self.game.active_player.buying_power = 100
            self.game.change_action(ACTION_NORMAL)
            self.assertEqual(card.can_buy, v[1])

    def test_banish_eligibility(self):
        test_cards = {
            'Avatar of the Fallen': [False, False],
            'Voidthirster': [False, True],
        }
        for k, v in test_cards.iteritems():
            card = self._fake_hand(k)
            self.assertEqual(card.can_banish, v[0])
            self.game.change_action([ACTION_BANISH])
            self.assertEqual(card.can_banish, v[1])


    def test_defeat_eligibility(self):
        test_cards = {
            'Avatar of the Fallen': [False, False],
            'Voidthirster': [False, False],
            'Corrosive Widow': [False, True],
        }
        for k, v in test_cards.iteritems():
            card = self._fake_hand(k)
            self.assertEqual(card.can_defeat, v[0])
            self.game.set_token('killing_power', 4, END_OF_ACTION)
            self.game.change_action([ACTION_DEFEAT])
            self.assertEqual(card.can_defeat, v[1])

    def test_acquire_eligibility(self):
        test_cards = {
            'Avatar of the Fallen': [False, False],
            'Voidthirster': [False, True],
        }
        for k, v in test_cards.iteritems():
            card = self._fake_hand(k)
            self.assertEqual(card.can_acquire_to_top, v[0])
            self.game.set_token('buying_power', 1000, END_OF_ACTION)
            self.game.change_action([ACTION_ACQUIRE_TO_TOP])
            self.assertEqual(card.can_acquire_to_top, v[1])

    def test_ability_point_per_controlled_construct(self):
        self.game.active_player.phand.append(self._get_card('Burrower Mark II'))
        self.game.active_player.phand.append(self._get_card('Grand Design'))
        self.game.active_player.phand.append(self._get_card('Snapdragon'))
        self._fake_user_hand(PLUS_1_POINT_PER_CONTROLLED_CONSTRUCT)
        card = self.game.play_user_card('c0')
        self.assertEqual(self.game.active_player.points, 2)


    def test_next_construct_1_less_buy(self):
        test_cards = {
            'Snapdragon': [False, True, False],
            'Ascetic of the Lidless Eye': [False, False, False],
        }
        for k, v in test_cards.iteritems():
            card = self._fake_hand(k)
            self.assertEqual(card.can_buy, v[0])
            self.game.active_player.buying_power = 2
            self._fake_user_hand(NEXT_CONSTRUCT_1_LESS_BUY)
            user_card = self.game.play_user_card('c0')
            self.assertEqual(card.can_buy, v[1])
            if card.can_buy:
                self.game.acquire_card(card, persistent=False)
                card.check_actions(self.game)
                self.game.active_player.buying_power = 4
                #import ipdb; ipdb.set_trace()
                self.game.hand[0] = card
                self.assertEqual(card.can_buy, v[2])



if __name__ == '__main__':
    unittest.main()
