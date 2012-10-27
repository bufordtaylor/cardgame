import random
class ShuffleMixin(object):

    def draw_cards(self, num):
        for x in xrange(num):
            self.draw_card()

    def draw_card(self):
        if len(self.deck) == 0:
            self.shuffle_discard_into_deck()
            if len(self.deck) == 0:
                return

        self.hand.append(self.deck.pop())

    def remove_card(self, card, deck):
        for idx, c in enumerate(deck):
            if card.iid == c.iid:
                del deck[idx]

    def get_card(self, card_idx, persistent=False, move=False):
        if persistent:
            card = self.phand[card_idx]
            if move:
                del self.phand[card_idx]
        else:
            card = self.hand[card_idx]
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
        while len(self.hand) > 0:
            self.discard.append(self.hand.pop())
        while len(self.game.played_user_cards) > 0:
            self.discard.append(self.game.played_user_cards.pop())

        if len(self.deck) < num_cards:
            self.shuffle_discard_into_deck()

        for i in xrange(0, num_cards):
            self.draw_card()
