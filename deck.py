import random

CARD_TYPE_MONSTER = 0
CARD_TYPE_HERO = 1
CARD_TYPE_PERSISTENT = 2

from card import Card
from colors import (
    bcolors, print_dict, print_green,prepare_card_row,
    print_white, print_blue, print_purple, print_ordered_cards,
)

class Deck(object):
    name = None

    def __init__(self):
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)

starter_cards = [
    {
        'name': 'apprentice',
        'worth': 0,
        'card_type': 1,
        'buy': 1,
        'kill': 0,
        'abilities': {}
    },
    {
        'name': 'militia',
        'worth': 0,
        'card_type': 1,
        'buy': 0,
        'kill': 1,
        'abilities': {}
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

