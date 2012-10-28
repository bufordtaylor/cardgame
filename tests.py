import unittest
import copy
import random
from simulate_game import SimulateGame
from deck import RealDeck, SimDeck
from player import Computer
from card import get_card_by_iid

from constants import *
from abilities_constants import *

class TestGame(unittest.TestCase):
    game = None
    deck = None

    def setUp(self):
        self.deck = SimDeck().deck
        self.players = []
        self.game = SimulateGame(deck=copy.deepcopy(self.deck), points=15, players=self.players)
        self.players = self.game.players
        self.game.played_user_cards = []
        # calling end_turn here to reset player hand on start up
        for p in self.game.players:
            p.game = self.game
            p.end_turn()
        self.game.active_player.start_turn()

    def _build_game_state(self):
        ret_val = '\n'
        ret_val += 'GAME HAND:'
        ret_val += '\n....'.join([c.name for c in self.game.hand])
        ret_val += '\n'
        ret_val += '\nGAME PERSISTENT HAND:'
        ret_val += '\n....'.join([c.name for c in self.game.phand])
        ret_val += '\n'
        ret_val += '\nGAME DISCARD HAND:'
        ret_val += '\n....'.join([c.name for c in self.game.discard])
        ret_val += '\n'
        ret_val += 'PLAYER PLAYED CARDS:'
        ret_val += '\n....'.join([c.name for c in self.game.played_user_cards])
        ret_val += '\n'
        ret_val += 'SELECTED CARD:'
        ret_val += self.game.selected_card.name if self.game.selected_card else ''
        ret_val += '\n'
        ret_val += 'PLAYER DISCARD HAND:'
        ret_val += '\n....'.join([c.name for c in self.game.active_player.discard])
        ret_val += '\n'
        ret_val += '\nPLAYER HAND:'
        ret_val += '\n....'.join([c.name for c in self.game.active_player.hand])
        ret_val += '\n'
        ret_val += '\nPLAYER PERSISTENT HAND:'
        ret_val += '\n....'.join([c.name for c in self.game.active_player.phand])
        ret_val += '\n'
        ret_val += '\nGAME TOKEN:'
        ret_val += '\n....'.join(['%s - %s' % (k,v) for k,v in self.game.token.iteritems()])
        ret_val += '\n'
        ret_val += '\nGAME TOKEN ERASERS:'
        ret_val += '\n....'.join(['%s - %s' % (k,v) for k,v in self.game.token_erasers.iteritems()])
        ret_val += '\n'
        ret_val += '\nGAME USED TOKEN:'
        ret_val += '\n....'.join(['%s - %s' % (k,v) for k,v in self.game.used_tokens.iteritems()])
        ret_val += '\n'
        ret_val += '\nbuy:%s kill:%s points:%s' % (
            self.game.active_player.buying_power,
            self.game.active_player.killing_power,
            self.game.active_player.points
        )

        return ret_val


    # overriding these because there are corner cases where the logic blows up
    # and I can't find them otherwise unless I know the game state
    def assertEqual(self, *args, **kwargs):
        try:
            thing = super(TestGame, self).assertEqual(*args, **kwargs)
        except Exception, e:
            kwargs['msg'] = 'AssertionError: %s\n%s' % (
                e, self._build_game_state()
            )
            super(TestGame, self).assertEqual(*args, **kwargs)

    # overriding these because there are corner cases where the logic blows up
    # and I can't find them otherwise unless I know the game state
    def assertTrue(self, *args, **kwargs):
        try:
            thing = super(TestGame, self).assertTrue(*args, **kwargs)
        except Exception, e:
            kwargs['msg'] = 'AssertionError: %s\n%s' % (
                e, self._build_game_state()
            )
            super(TestGame, self).assertTrue(*args, **kwargs)

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
        self.game._override_buy = 'mystic'
        self.game._force_actions = [ACTION_BUY]
        card = self.game.normal_action()
        # card appears in player's discard deck
        self.assertTrue(card.iid in [c.iid for c in self.game.active_player.discard])
        # card still in game deck
        self.assertTrue(card.name in [c.name for c in self.game.phand])
        # appropriate points reduced from player buying power
        self.assertEqual(self.game.active_player.buying_power, buying_power - card.buy)

        # kill a persistent game card
        self.game._override_kill = 'cultist'
        self.game._force_actions = [ACTION_KILL]
        card = self.game.normal_action()
        print card.name
        # card does not appear in player's discard deck
        self.assertTrue(card.iid not in [c.iid for c in self.game.active_player.discard])
        # card still in game deck
        self.assertTrue(card.name in [c.name for c in self.game.phand])
        # appropriate points reduced from player killing power

    def _get_card(self, name):
        for idx, c in enumerate(self.deck):
            if c.name == name:
                return c

        for idx, c in enumerate(self.game.hand):
            if c.name == name:
                return c

    def _move_card(self, name):
        card = None
        for idx, c in enumerate(self.game.deck):
            if c.name == name:
                card = c
                del self.game.deck[idx]
                return c

        for idx, c in enumerate(self.game.hand):
            if c.name == name:
                card = c
                del self.game.hand[idx]
        return card

    def _move_card_by_ability(self, ability):
        card = None
        for idx, c in enumerate(self.game.deck):
            if c.abilities == ability:
                card = c
                del self.game.deck[idx]
                return c
        return card


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
        self.game.hand[0] = self._move_card('Cetra, Weaver of Stars')

        killing_power = self.game.active_player.killing_power
        buying_power = self.game.active_player.buying_power
        self.game.check_cards_eligibility()

        # acquire a regular game card by forcing only the buy action
        self.game._force_actions = [ACTION_BUY]
        card = self.game.normal_action()
        # card appears in player's discard deck
        self.assertTrue(card.iid in [c.iid for c in self.game.active_player.discard])
        # card not in game deck
        self.assertTrue(card.iid not in [c.iid for c in self.game.hand])
        # appropriate points reduced from player buying power
        self.assertEqual(self.game.active_player.buying_power, buying_power - card.buy)


        self.game.hand[0] = self._move_card('Avatar of the Fallen')
        # kill a regular game card
        self.game.check_cards_eligibility()
        self.game._force_actions = [ACTION_KILL]
        card = self.game.normal_action()
        # card does not in player's discard deck
        self.assertTrue(card.iid not in [c.iid for c in self.game.active_player.discard])
        # card not in game deck
        self.assertTrue(card.iid not in [c.iid for c in self.game.hand])
        # card is in in game discard deck
        self.assertTrue(card.iid in [c.iid for c in self.game.discard])
        # appropriate points reduced from player killing power
        self.assertEqual(self.game.active_player.killing_power, killing_power - card.kill)

    def test_instant_ability_draw_card(self):
        self.game.active_player.deck.append(self.game.deck.pop())
        self.game.active_player.hand[0] = self._move_card_by_ability(DRAW_1)
        self.assertEqual(len(self.game.active_player.hand), 5)
        card = self.game.normal_action()
        self.assertEqual(len(self.game.active_player.hand), 5)

    def test_instant_ability_draw_2_card(self):
        self.game.active_player.hand[0] = self._move_card_by_ability(DRAW_2)
        self.assertEqual(len(self.game.active_player.hand), 5)
        card = self.game.normal_action()
        self.assertEqual(len(self.game.active_player.hand), 6)

    def test_instant_ability_draw_3_card(self):
        self.game.active_player.hand[0] = self._move_card_by_ability(DRAW_3)
        self.assertEqual(len(self.game.active_player.hand), 5)
        card = self.game.normal_action()
        self.assertEqual(len(self.game.active_player.hand), 7)

    def test_draw_2_then_banish_1_hand(self):
        self.game.active_player.hand[0] = self._move_card_by_ability(DRAW_2_THEN_BANISH_1_HAND)
        banished_card = self.game.active_player.hand[1]
        card = self.game.normal_action()
        self.assertTrue(banished_card.iid in [c.iid for c in self.game.discard])
        self.assertTrue(banished_card.iid not in [c.iid for c in self.game.active_player.hand])
        self.assertTrue(banished_card.iid not in [c.iid for c in self.game.active_player.discard])

    def test_draw_1_banish_center(self):
        self.game.active_player.hand[0] = self._move_card_by_ability(DRAW_1_BANISH_CENTER)
        banished_card = self.game.hand[0]
        card = self.game.normal_action()
        self.assertTrue(banished_card.iid in [c.iid for c in self.game.discard])
        self.assertTrue(banished_card.iid not in [c.iid for c in self.game.active_player.hand])
        self.assertTrue(banished_card.iid not in [c.iid for c in self.game.active_player.discard])

    def test_unbanishable(self):
         #cannot banish avatar
        self.game.hand[0] = self._move_card('Avatar of the Fallen')
        avatar = self.game.hand[0]
        banished_card = self.game.hand[1]
        self.game.active_player.hand[0] = self._move_card_by_ability(DRAW_1_BANISH_CENTER)
        card = self.game.normal_action()
        self.assertTrue(avatar.iid in [c.iid for c in self.game.hand])
        self.assertTrue(avatar.iid not in [c.iid for c in self.game.discard])
        self.assertTrue(banished_card.iid in [c.iid for c in self.game.discard])
        self.assertTrue(banished_card.iid not in [c.iid for c in self.game.active_player.hand])
        self.assertTrue(banished_card.iid not in [c.iid for c in self.game.active_player.discard])

    def test_kill_ability_banish(self):
        self.game.active_player.hand[0] = self._move_card_by_ability(CAN_BANISH_1_HAND_OR_DISCARD_AND_CENTER)
        card = self._move_card('Voidthirster')
        self.game.active_player.discard.append(card)
        card = self.game.normal_action()
        selected_card = self.game.selected_card
        self.assertTrue(len(self.game.active_player.hand), 4)
        self.assertTrue(len(self.game.active_player.discard), 0)
        self.assertTrue(len(self.game.discard), 2)

    def test_instant_ability_can_banish_1_hand_or_discard(self):
        self.game.active_player.hand[0] = self._move_card_by_ability(CAN_BANISH_1_HAND_OR_DISCARD)
        card = self._move_card('Voidthirster')
        self.game.active_player.discard.append(card)
        self.assertTrue(len(self.game.active_player.discard), 1)
        card = self.game.normal_action()
        self.assertTrue(len(self.game.active_player.hand), 4)
        self.assertTrue(len(self.game.active_player.discard), 0)



    def test_instant_ability_discard(self):
        self.game.active_player.hand[0] = self._move_card_by_ability(IF_DISCARD_DRAW_TWO)
        card = self.game.normal_action()
        selected_card = self.game.selected_card
        self.assertTrue(id(selected_card) in [id(c) for c in self.game.active_player.discard])
        self.assertTrue(id(selected_card) not in [id(c) for c in self.game.active_player.hand])
        self.assertTrue(len(self.game.active_player.hand), 6)

    def test_instant_ability_copy_no_card(self):
        # no card to emulate, so it just plays it
        self.game.active_player.hand[0] = self._move_card_by_ability(COPY_EFFECT)
        card = self.game.normal_action()
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
        self.game.active_player.hand[0] = self._move_card_by_ability(IF_DISCARD_DRAW_TWO)
        card = self.game.normal_action()
        selected_card = self.game.selected_card
        self.assertTrue(len(self.game.active_player.hand), 6)

        # emulate other card
        self.game.active_player.hand[0] = self._move_card_by_ability(COPY_EFFECT)
        card = self.game.normal_action()
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
            self.game.set_token('minus_kill', 4, END_OF_ACTION)
            self.game.change_action([ACTION_DEFEAT])
            self.assertEqual(card.can_defeat, v[1])
            self.game.remove_token('minus_kill')

    def test_acquire_eligibility(self):
        test_cards = {
            'Avatar of the Fallen': [False, False],
            'Voidthirster': [False, True],
        }
        for k, v in test_cards.iteritems():
            card = self._fake_hand(k)
            self.assertEqual(card.can_acquire_to_top, v[0])
            self.game.set_token('minus_buy', 1000, END_OF_ACTION)
            self.game.change_action([ACTION_ACQUIRE_TO_TOP])
            self.assertEqual(card.can_acquire_to_top, v[1])
            self.game.remove_token('minus_buy')

    def test_acquire_hero_3_or_less_to_top_of_deck(self):
        perscard = self._move_card('Voidthirster')
        monstercard = self._move_card('Avatar of the Fallen')
        herocard = self._move_card('Wolf Shaman')
        expensiveherocard = self._move_card('Landtalker')
        self.game.hand[0] = perscard
        self.game.hand[1] = monstercard
        self.game.hand[2] = expensiveherocard
        self.game.hand[3] = herocard
        self.game.active_player.hand[0] = self._move_card_by_ability(ACQUIRE_HERO_3_OR_LESS_TO_TOP_OF_DECK)

        user_card = self.game.normal_action()
        self.assertTrue(herocard in self.game.active_player.deck)

    def test_ability_point_per_controlled_construct(self):
        self.game.active_player.phand.append(self._move_card('Burrower Mark II'))
        self.game.active_player.phand.append(self._move_card('Grand Design'))
        self.game.active_player.phand.append(self._move_card('Snapdragon'))
        self.game.active_player.hand[0] = self._move_card_by_ability(PLUS_1_POINT_PER_CONTROLLED_CONSTRUCT)
        card = self.game.normal_action()
        self.assertEqual(self.game.active_player.points, 2)

    def test_ability_per_turn_plus_1_kill_can_spend_4_to_buy_3_points(self):
        self.game.active_player.hand[0] = self._move_card_by_ability(PER_TURN_PLUS_1_KILL_CAN_SPEND_4_TO_BUY_3_POINTS)
        card = self.game.normal_action()
        self.assertEqual(len(self.game.active_player.phand), 1)
        self.assertEqual(card.can_use, False)
        # check basic case
        self.game.active_player.buying_power = 4
        self.game.check_cards_eligibility()
        self.assertEqual(card.can_use, True)
        # check if token is removed if buying power decreased
        self.game.active_player.buying_power = 3
        self.game.check_cards_eligibility()
        self.assertEqual(card.can_use, False)
        # check if using token is correct
        self.game.active_player.buying_power = 4
        self.game.check_cards_eligibility()
        self.assertEqual(card.can_use, True)
        card = self.game.play_user_card_persistent('t0')
        self.assertEqual(card.can_use, False)
        self.assertEqual(self.game.active_player.buying_power, 0)
        self.assertEqual(self.game.active_player.points, 3)
        # check if can only use once
        self.game.active_player.buying_power = 4
        self.game.check_cards_eligibility()
        self.assertEqual(card.can_use, False)

    def test_instant_ability_if_lifebound_hero_plus_2_kill(self):
        self.game.played_user_cards.append(self._move_card('Wolf Shaman'))
        self.game.active_player.hand[0] = self._move_card_by_ability(IF_LIFEBOUND_HERO_PLUS_2_KILL)
        card = self.game.normal_action()
        self.assertEqual(self.game.active_player.killing_power, 2)


    def test_ability_per_turn_draw_1(self):
        self.game.active_player.hand[0] = self._move_card_by_ability(PER_TURN_DRAW_1)
        card = self.game.normal_action()
        self.assertEqual(card.can_use, True)
        self.assertEqual(len(self.game.active_player.phand), 1)
        self.assertEqual(len(self.game.active_player.hand), 4)
        self.assertEqual(len(self.game.token), 1)
        card = self.game.normal_action()
        self.assertEqual(len(self.game.token), 0)
        self.assertEqual(card.can_use, False)
        self.assertEqual(len(self.game.active_player.phand), 1)
        self.assertEqual(len(self.game.active_player.hand), 5)

    def test_next_construct_1_less_buy(self):
        test_cards = {
            'Snapdragon': [False, True, False],
            'Ascetic of the Lidless Eye': [False, False, False],
        }
        for k, v in test_cards.iteritems():
            card = self._move_card(k)
            self.game.hand[0] = card
            self.assertEqual(card.can_buy, v[0])
            self.game.active_player.buying_power = 2
            self.game.active_player.hand[0] = self._move_card_by_ability(NEXT_CONSTRUCT_1_LESS_BUY)
            user_card = self.game.normal_action()
            self.game.check_cards_eligibility()
            self.assertEqual(card.can_buy, v[1])
            if card.can_buy:
                self.game._force_actions = [ACTION_BUY]
                self.game.normal_action()
                card.check_actions(self.game)
                self.game.active_player.buying_power = 4
                self.game.hand[0] = card
                self.assertEqual(card.can_buy, v[2])

    def test_per_turn_plus_2_buy_for_mechana_construct_only(self):
        self.game.active_player.buying_power = 4 # hedron has 7
        # check can buy without enough buying power
        self.game.hand[0] = self._move_card('Hedron Link Device')
        self.game.check_cards_eligibility()
        self.assertFalse(self.game.hand[0].can_buy)
        self.game.active_player.hand[0] = self._move_card_by_ability(PER_TURN_PLUS_2_BUY_FOR_MECHANA_CONSTRUCT_ONLY)
        card = self.game.normal_action()
        self.game.check_cards_eligibility()
        # added two buying power, but not enough
        self.assertFalse(self.game.hand[0].can_buy)
        self.game.active_player.hand[0] = self._move_card_by_ability(PER_TURN_PLUS_1_BUY_FOR_MECHANA_CONSTRUCT_ONLY)
        self.assertEquals(self.game.active_player.hand[0].iid, 52)
        card = self.game.normal_action()
        self.game.check_cards_eligibility()
        # added one buying power, and now it is enough
        self.assertTrue(self.game.hand[0].can_buy)

        # buy card, check if tokens are used properly
        self.game._force_actions = [ACTION_BUY]
        self.game.normal_action()
        self.assertEqual(self.game.active_player.buying_power, 0)
        self.game.active_player.buying_power = 4 # hedron has 7
        self.game.hand[0] = self._get_card('Hedron Link Device')
        self.game.check_cards_eligibility()
        self.assertFalse(self.game.hand[0].can_buy)

    def test_per_turn_plus_1_kill_first_monster_defeat_plus_1_point(self):
        self.game.active_player.killing_power = 1000
        self.game.hand[0] = self._move_card('Avatar of the Fallen')
        self.game.active_player.hand[0] = self._move_card_by_ability(PER_TURN_PLUS_1_KILL_FIRST_MONSTER_DEFEAT_PLUS_1_POINT)
        card = self.game.normal_action()
        self.game._force_actions = [ACTION_KILL]
        card = self.game.normal_action()
        self.assertEqual(self.game.active_player.points, 5)

    def test_per_turn_plus_1_buy_first_lifebound_hero_plus_1_point(self):
        self.game.active_player.hand[0] = self._move_card_by_ability(PER_TURN_PLUS_1_BUY_FIRST_LIFEBOUND_HERO_PLUS_1_POINT)
        card = self.game.normal_action()
        self.assertEqual(self.game.active_player.points, 0)
        self.game.active_player.hand[0] = self._move_card('Wolf Shaman')
        card = self.game.normal_action()
        self.assertEqual(self.game.active_player.points, 1)
        self.game.active_player.hand[0] = self._move_card('Wolf Shaman')
        card = self.game.normal_action()
        self.assertEqual(self.game.active_player.points, 1)

    def test_per_turn_when_play_mechana_construct_draw_1_including_this_one(self):
        self.game.active_player.hand[0] = self._move_card_by_ability(PER_TURN_WHEN_PLAY_MECHANA_CONSTRUCT_DRAW_1_INCLUDING_THIS_ONE)

        self.assertEqual(len(self.game.active_player.hand), 5)
        card = self.game.normal_action()
        player = self.game.active_player
        self.assertEqual(len(self.game.active_player.hand), 5)
        self.assertEqual(len(self.game.active_player.phand), 1)
        self.game.active_player.end_turn()
        self.game.next_player_turn()
        self.game.active_player.end_turn()
        self.game.next_player_turn()
        self.assertEqual(player, self.game.active_player)
        self.assertEqual(len(self.game.active_player.hand), 5)
        card = self.game.normal_action()
        self.assertEqual(len(self.game.active_player.hand), 4)
        self.assertEqual(len(self.game.active_player.phand), 1)

    def test_per_turn_plus_1_kill_per_controlled_mechana_contruct(self):
        self.game.active_player.hand[0] = self._move_card_by_ability(PER_TURN_PLUS_1_KILL_PER_CONTROLLED_MECHANA_CONTRUCT)
        self.game.active_player.phand.append(self._get_card('Hedron Link Device'))
        card = self.game.normal_action()
        self.assertEqual(self.game.active_player.killing_power, 2)

    def test_per_turn_when_acquire_mechana_construct_put_in_play(self):
        self.game.active_player.hand[0] = self._move_card_by_ability(PER_TURN_WHEN_ACQUIRE_MECHANA_CONSTRUCT_PUT_IN_PLAY)

        card = self.game.normal_action()
        self.game.active_player.buying_power = 1000
        self.game.hand[0] = self._move_card('Grand Design')
        self.game.check_cards_eligibility()
        self.game._force_actions = [ACTION_ACQUIRE_TO_PHAND]
        self.game.normal_action()
        self.assertEqual(len(self.game.active_player.discard), 0)
        self.assertEqual(len(self.game.active_player.phand), 2)

    def test_all_contructs_are_mechana(self):
        self.game.active_player.hand[0] = self._move_card_by_ability(ALL_CONTRUCTS_ARE_MECHANA)
        user_card = self.game.normal_action()
        self.game.hand[0] = self._get_card('Yggdrasil Staff')
        self.assertTrue(self.game.hand[0].in_faction(self.game, LIFEBOUND))
        self.assertTrue(self.game.hand[0].in_faction(self.game, MECHANA))

    def test_banish_this_extra_turn(self):
        self.game.active_player.hand[0] = self._move_card_by_ability(BANISH_THIS_EXTRA_TURN)
        user_card = self.game.normal_action()
        self.assertEqual(user_card.can_use, True)
        self.assertEqual(len(self.game.active_player.phand), 1)
        self.assertEqual(len(self.game.token), 1)
        self.assertFalse(self.game.extra_turn)
        card = self.game.play_user_card_persistent('t0')
        self.assertEqual(len(self.game.active_player.phand), 0)
        self.assertEqual(len(self.game.token), 0)
        self.assertTrue(self.game.extra_turn)
        player = self.game.active_player
        player.end_turn()
        self.game.next_player_turn()
        self.assertEqual(len(self.game.active_player.phand), 0)
        self.assertFalse(self.game.extra_turn)
        self.assertEqual(len(self.game.token), 0)
        self.assertEqual(player, self.game.active_player)

    @unittest.skip('acquire or defeat any not used yet')
    def test_acquire_or_defeat_any(self):
        self._fake_hand('replace this with acquire or defeat any card')
        self.game.active_player.killing_power = 8
        self.game.check_cards_eligibility()
        card = self.game.normal_action()
        self.assertEqual(len(self.game.active_player.discard), 1)

    def test_plus_1_buy_or_1_kill(self):
        self.game.active_player.hand[0] = self._move_card_by_ability(PLUS_1_BUY_OR_1_KILL)
        user_card = self.game.normal_action()
        self.assertEqual(self.game.active_player.buying_power, 1)

    def test_cards(self):
        expected = ['Arha Initiate',
            'Arha Initiate',
            'Arha Initiate',
            'Arha Templar',
            'Arha Templar',
            'Ascetic of the Lidless Eye',
            'Ascetic of the Lidless Eye',
            'Master Dhartha',
            'Oziah the Peerless',
            'Seer of the Forked Path',
            'Seer of the Forked Path',
            'Seer of the Forked Path',
            'Temple Librarian',
            'Temple Librarian',
            'Temple Librarian',
            'Twofold Askara',
            'The All-Seeing Eye',
            'Tablet of Time\'s Dawn',
            'Cetra, Weaver of Stars',
            'Druids of the Stone Circle',
            'Druids of the Stone Circle',
            'Flytrap Witch',
            'Flytrap Witch',
            'Landtalker',
            'Lifebound Initiate',
            'Lifebound Initiate',
            'Lifebound Initiate',
            'Runic Lycanthrope',
            'Runic Lycanthrope',
            'Wolf Shaman',
            'Wolf Shaman',
            'Wolf Shaman',
            'Snapdragon',
            'Snapdragon',
            'Yggdrasil Staff',
            'Yggdrasil Staff',
            'Avatar Golem',
            'Avatar Golem',
            'Kor, the Ferrormancer',
            'Mechana Insitute',
            'Mechana Insitute',
            'Mechana Insitute',
            'Reactor Monk',
            'Reactor Monk',
            'Burrower Mark II',
            'Burrower Mark II',
            'Grand Design',
            'Grand Design',
            'Hedron Cannon',
            'Hedron Link Device',
            'Rocker Courier x-99',
            'Rocker Courier x-99',
            'Watchmaker Altar',
            'Watchmaker Altar',
            'Arbiter of the Precipice',
            'Arbiter of the Precipice',
            'Demon Slyyer',
            'Demon Slyyer',
            'Emri, One with the void',
            'Shade of the Black Witch',
            'Shade of the Black Witch',
            'Shade of the Black Witch',
            'Spike Vixen',
            'Spike Vixen',
            'Void Initiate',
            'Void Initiate',
            'Void Initiate',
            'Murasama',
            'Shadow Star',
            'Shadow Star',
            'Voidthirster',
            'Voidthirster',
            'Avatar of the Fallen',
            'Corrosive Widow',
            'Corrosive Widow',
            'Corrosive Widow',
            'Corrosive Widow',
            'Earth Tyrant',
            'Earth Tyrant',
            'Mephit',
            'Mephit',
            'Mephit',
            'Mistake of Creation',
            'Mistake of Creation',
            'Mistake of Creation',
            'Mistake of Creation',
            'Samael Trickster',
            'Samael Trickster',
            'Samael Trickster',
            'Samael Trickster',
            'Sea Tyrant',
            'Sea Tyrant',
            'Sea Tyrant',
            'Tormented Soul',
            'Tormented Soul',
            'Tormented Soul',
            'Wind Tryant',
            'Wind Tryant',
            'Wind Tryant',
            'Xeron, Duke of Lies',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'mystic',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'heavy infantry',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'cultist',
            'apprentice',
            'apprentice',
            'apprentice',
            'apprentice',
            'apprentice',
            'apprentice',
            'apprentice',
            'apprentice',
            'militia',
            'militia',
            'apprentice',
            'apprentice',
            'apprentice',
            'apprentice',
            'apprentice',
            'apprentice',
            'apprentice',
            'apprentice',
            'militia',
        ]

        for x in xrange(269):
            self.assertEqual(get_card_by_iid(self.game, x).name, expected[x])

    def test_normal_action(self):
        self.assertEquals(len(self.game.played_user_cards), 0)
        card = self.game.normal_action()
        # check all the points that should've been added
        self.assertEqual(self.game.active_player.killing_power, card.instant_kill)
        self.assertEqual(self.game.active_player.buying_power, card.instant_buy)
        self.assertEqual(self.game.active_player.points, card.instant_worth)

        # check card is not in hand anymore, and it is in played user cards
        self.assertFalse(card.iid in [c.iid for c in self.game.active_player.hand])
        self.assertTrue(card.iid in [c.iid for c in self.game.played_user_cards])

    def test_opponents_keep_1_construct(self):
        self.game.players[1].phand.append(self._move_card('Burrower Mark II'))
        self.game.players[1].phand.append(self._move_card('Grand Design'))
        self.game.players[1].phand.append(self._move_card('Snapdragon'))
        self.game.hand[0] = self._move_card('Sea Tyrant')
        self.game.active_player.killing_power = 100
        self.game.check_cards_eligibility()
        self.assertEqual(len(self.game.players[1].phand), 3)
        self.game._force_actions = [ACTION_KILL]
        self.game.normal_action()
        self.assertEqual(len(self.game.players[1].phand), 1)

    def test_opponents_keep_1_construct_1_card(self):
        self.game.players[1].phand.append(self._move_card('Burrower Mark II'))
        self.game.hand[0] = self._move_card('Sea Tyrant')
        self.game.active_player.killing_power = 100
        self.game.check_cards_eligibility()
        self.assertEqual(len(self.game.players[1].phand), 1)
        self.game._force_actions = [ACTION_KILL]
        self.game.normal_action()
        self.assertEqual(len(self.game.players[1].phand), 1)

    def test_opponents_keep_1_construct_active_player(self):
        self.game.active_player.phand.append(self._move_card('Burrower Mark II'))
        self.game.active_player.phand.append(self._move_card('Grand Design'))
        self.game.hand[0] = self._move_card('Sea Tyrant')
        self.game.active_player.killing_power = 100
        self.game.check_cards_eligibility()
        self.assertEqual(len(self.game.active_player.phand), 2)
        self.game._force_actions = [ACTION_KILL]
        self.game.normal_action()
        self.assertEqual(len(self.game.active_player.phand), 2)

    def test_opponents_destroy_1_construct(self):
        self.game.players[1].phand.append(self._move_card('Burrower Mark II'))
        self.game.players[1].phand.append(self._move_card('Grand Design'))
        self.game.players[1].phand.append(self._move_card('Snapdragon'))
        self.game.hand[0] = self._move_card('Corrosive Widow')
        self.game.active_player.killing_power = 100
        self.game.check_cards_eligibility()
        self.assertEqual(len(self.game.players[1].phand), 3)
        self.game._force_actions = [ACTION_KILL]
        self.game.normal_action()
        self.assertEqual(len(self.game.players[1].phand), 2)

    def test_opponents_destroy_1_construct_1_card(self):
        self.game.players[1].phand.append(self._move_card('Burrower Mark II'))
        self.game.hand[0] = self._move_card('Corrosive Widow')
        self.game.active_player.killing_power = 100
        self.game.check_cards_eligibility()
        self.assertEqual(len(self.game.players[1].phand), 1)
        self.game._force_actions = [ACTION_KILL]
        self.game.normal_action()
        self.assertEqual(len(self.game.players[1].phand), 0)

    def test_opponents_destroy_1_construct_active_player(self):
        self.game.active_player.phand.append(self._move_card('Burrower Mark II'))
        self.game.active_player.phand.append(self._move_card('Grand Design'))
        self.game.hand[0] = self._move_card('Corrosive Widow')
        self.game.active_player.killing_power = 100
        self.game.check_cards_eligibility()
        self.assertEqual(len(self.game.active_player.phand), 2)
        self.game._force_actions = [ACTION_KILL]
        self.game.normal_action()
        self.assertEqual(len(self.game.active_player.phand), 2)


if __name__ == '__main__':
    unittest.main()
