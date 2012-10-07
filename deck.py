import random

CARD_TYPE_MONSTER = 0
CARD_TYPE_HERO = 1
CARD_TYPE_PERSISTENT = 2

from card import Card
from colors import (
    bcolors, print_dict, print_green,prepare_card_row,
    print_white, print_blue, print_purple, print_ordered_cards,
)

from card_constants import (
    deck_one,
    ENLIGHTENED,
    MECHANA,
    VOID,
    LIFEBOUND,
)

class Deck(object):
    name = None

    def __init__(self):
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)


buy_3 = {
        'name': 'mystic',
        'worth': 1,
        'card_type': 1,
        'buy': 3,
        'kill': 0,
        'instant_worth': 0,
        'instant_buy': 2,
        'instant_kill': 0,
}
buy_2 = {
        'name': 'heavy infantry',
        'worth': 1,
        'card_type': 1,
        'buy': 2,
        'kill': 0,
        'instant_worth': 0,
        'instant_buy': 0,
        'instant_kill': 2,
}
kill_1 = {
        'name': 'cultist',
        'worth': 0,
        'card_type': 0,
        'buy': 0,
        'kill': 2,
        'instant_worth': 1,
        'instant_buy': 0,
        'instant_kill': 0,
}

persistant_game_hand = [buy_3, buy_2, kill_1]

starter_cards = [
    {
        'name': 'apprentice',
        'worth': 0,
        'card_type': 1,
        'buy': 0,
        'kill': 0,
        'instant_worth': 0,
        'instant_buy': 1,
        'instant_kill': 0,
    },
    {
        'name': 'militia',
        'worth': 0,
        'card_type': 1,
        'buy': 0,
        'kill': 0,
        'instant_worth': 0,
        'instant_buy': 0,
        'instant_kill': 1,
    },
]

class PlayerStartDeck(Deck):
    def __init__(self, num_cards = 9):
        self.deck = []
        for i in xrange(0,2):
            card_dict = starter_cards[i]
            for x in xrange(0,8 if i == 0 else 2):
                card = Card(
                    name=card_dict['name'],
                    worth=card_dict['worth'],
                    card_type=card_dict['card_type'],
                    buy=card_dict['buy'],
                    kill=card_dict['kill'],
                    instant_worth=card_dict['instant_worth'],
                    instant_buy=card_dict['instant_buy'],
                    instant_kill=card_dict['instant_kill'],
                )
                self.deck.append(card)
        super(PlayerStartDeck, self).__init__()

class testDeck(Deck):

    def __init__(self, num_cards = 9):
        self.deck = []
        for idx in xrange(0, num_cards):
            card_type = random.randint(CARD_TYPE_MONSTER, CARD_TYPE_PERSISTENT)
            card = Card(
                    name='Card %s' % idx,
                    worth=idx,
                    card_type=card_type,
                    buy=idx,
                    kill=idx,
            )
            self.deck.append(card)
        super(testDeck, self).__init__()

class RealDeck(Deck):
    def __init__(self):
        self.deck = []
        for obj in deck_one:
            for i in xrange(obj['count']+1):
                self.deck.append(Card(**obj['card']))
        super(RealDeck, self).__init__()


CARD_ATTRIBUTES = {
    bcolors.PURPLE: 'type',
    bcolors.BLUE: 'name',
    bcolors.GREEN: 'worth',
    bcolors.YELLOW: 'buy',
    bcolors.RED: 'kill'
}

def print_card_attrs():
    print_ordered_cards( [
        (bcolors.WHITE, ''),
        (bcolors.PURPLE, 'type'),
        (bcolors.BLUE, 'name'),
        (bcolors.YELLOW, 'buy'),
        (bcolors.RED, 'kill'),
        (bcolors.GREEN, 'worth'),
    ])

