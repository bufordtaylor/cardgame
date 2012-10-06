from colors import *
class PrintMixin(object):

    def print_card_hand(self, hand, player=False, game_phand=False):
        """
        organizes data and calls print function:
        +----------------+-----------+-----------+-----+------+-------+
        | How to Acquire | Card Type | Card Name | Buy | Kill | Worth |
        +================+===========+===========+=====+======+=======+
        |        [b]uy:0 |      PERS |    Card 4 |   4 |    4 |     4 |
        +----------------+-----------+-----------+-----+------+-------+
        |       [k]ill:1 |   MONSTER |    Card 5 |   5 |    5 |     5 |
        +----------------+-----------+-----------+-----+------+-------+
        |        [b]uy:2 |      PERS |    Card 5 |   5 |    5 |     5 |
        +----------------+-----------+-----------+-----+------+-------+
        |       [k]ill:3 |   MONSTER |    Card 6 |   6 |    6 |     6 |
        +----------------+-----------+-----------+-----+------+-------+
        |        [b]uy:4 |      HERO |    Card 2 |   2 |    2 |     2 |
        +----------------+-----------+-----------+-----+------+-------+
        """
        card_rows = [[
                'Use',
                'Card Type',
                'Card Name',
                'Buy',
                'Kill',
                'Worth',
        ]]
        for idx,card in enumerate(hand):
            if player:
                card_rows.append(card.card_row(idx, player_card=True))
            elif game_phand:
                card_rows.append(card.card_row(idx, game_phand=True))
            else:
                card_rows.append(card.card_row(idx))
        print_color_table(card_rows)

    def print_hand(self):
        print_purple('-----------IN GAME--------------')
        self.print_card_hand(self.hand)

    def print_phand(self):
        print_purple('-----------IN GAME PERS--------------')
        self.print_card_hand(self.phand, game_phand=True)

    def print_user_played_cards(self):
        if len(self.played_user_cards) == 0:
            return
        print_green('------------%s PLAYED' % self.active_player.name)
        self.print_card_hand(self.played_user_cards, player=True)

    def print_user_hand(self):
        print_green('------------%s UNPLAYED' % self.active_player.name)
        self.print_card_hand(self.active_player.hand, player=True)

    def print_user_status(self):
        """
        prints this:
        +--------+---------------+----------------+
        | Points | Buying power: | Killing power: |
        +========+===============+================+
        |      0 |             0 |              0 |
        +--------+---------------+----------------+
        """
        hand = len(self.active_player.hand)
        discard = len(self.active_player.discard)
        deck = len(self.active_player.deck)
        phand = len(self.active_player.phand)
        played = len(self.played_user_cards)
        print_color_table([
            [
                'Points',
                'Buying power',
                'Killing power',
                'Deck',
                'Unplayed cards',
                'Discarded cards',
            ],[
                self.active_player.points,
                self.active_player.buying_power,
                self.active_player.killing_power,
                deck,
                hand,
                discard,
            ]
        ])

    def print_results(self):
        for p in self.players:
            if len(p.hand) > 0:
                p.deck.append(p.hand.pop())
            if len(p.phand) > 0:
                p.deck.append(p.phand.pop())
            if len(p.discard) > 0:
                p.deck.append(p.discard.pop())
            for c in p.deck:
                p.points += c.worth
            print p

