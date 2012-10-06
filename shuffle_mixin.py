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
        self.discard.append(self.get_card(card_idx))

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def shuffle_discard_into_deck(self):
        self.deck = self.discard
        self.discard = []
        self.shuffle_deck()


class ShuffleGameCardMixin(ShuffleMixin):

    def new_hand(self, num_cards=5):

        if len(self.deck) < num_cards:
            self.shuffle_discard_into_deck()

        for i in xrange(0, num_cards):
            self.draw_card()

class ShufflePlayerCardMixin(ShuffleMixin):

    def new_hand(self, num_cards=5):
        print self.hand, self.discard
        while len(self.hand) > 0:
            self.discard.append(self.hand.pop())
        while len(self.game.played_user_cards) > 0:
            self.discard.append(self.game.played_user_cards.pop())
        print self.hand, self.discard

        if len(self.deck) < num_cards:
            self.shuffle_discard_into_deck()

        for i in xrange(0, num_cards):
            self.draw_card()
