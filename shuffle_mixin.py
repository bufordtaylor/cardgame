import random
class ShuffleMixin(object):

    def draw_card(self):
        if len(self.deck) == 0:
            self.shuffle_discard_into_deck()

        self.hand.append(self.deck.pop())

    def get_card(self, card_idx):
        card = self.hand[card_idx]
        print type(self), len(self.hand)
        del self.hand[card_idx]
        return card

    def discard_card(self, card_idx):
        return self.play_card(card_idx)

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def shuffle_discard_into_deck(self):
        self.deck = self.discard
        self.discard = []
        self.shuffle_deck()

    def new_hand(self, num_cards=5):
        if len(self.deck) < num_cards:
            self.shuffle_discard_into_deck()

        for i in xrange(0, num_cards):
            self.draw_card()

class ShuffleGameCardMixin(ShuffleMixin): pass
class ShufflePlayerCardMixin(ShuffleMixin): pass
