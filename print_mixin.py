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
                'Faction',
                'Card Name',
                'Buy',
                'Kill',
                'Worth',
                'Instant Buy',
                'Instant Kill',
                'Instant Worth',
                'Abilities',
        ]]
        width = [9,15,10,30,13,13,13,13,13,13,50]
        for idx,card in enumerate(hand):
            if player:
                card_rows.append(card.card_row(idx, player_card=True))
            elif game_phand:
                card_rows.append(card.card_row(idx, game_phand=True))
            else:
                card_rows.append(card.card_row(idx))
        print_color_table(card_rows, width=width)

    def print_hand(self):
        self.print_card_hand(self.hand)
        print

    def print_phand(self):
        self.print_card_hand(self.phand, game_phand=True)
        print

    def print_user_played_cards(self):
        if len(self.played_user_cards) == 0:
            return
        print_green('---%s PLAYED' % self.active_player.name)
        self.print_card_hand(self.played_user_cards, player=True)
        print

    def print_user_hand(self):
        if len(self.active_player.hand) > 0:
            print_green('---%s UNPLAYED' % self.active_player.name)
            self.print_card_hand(self.active_player.hand, player=True)
            print

    def print_user_status(self):
        """
        prints this:
        +----------+----------+----------+----------+----------+----------+----------+
        |  Player  |  Points  |  Buying  | Killing  |   Deck   | Unplayed | Discarde |
        |          |          |  power   |  power   |          |  cards   | d cards  |
        +==========+==========+==========+==========+==========+==========+==========+
        | Player 0 |        0 |        0 |        0 |        5 |        5 |        0 |
        +----------+----------+----------+----------+----------+----------+----------+
        | Player 1 |        0 |        0 |        0 |        5 |        5 |        0 |
        +----------+----------+----------+----------+----------+----------+----------+
        """
        player_statuses = []
        player_statuses.append([
                'Player',
                'Points',
                'Buying power',
                'Killing power',
                'Deck',
                'Unplayed cards',
                'Discard cards',
        ])

        for player in self.players:
            hand = len(player.hand)
            discard = len(player.discard)
            deck = len(player.deck)
            phand = len(player.phand)
            played = len(self.played_user_cards)
            if player.name == self.active_player.name:
                player_info = [
                    get_color_string(bcolors.GREEN, player.name),
                    get_color_string(bcolors.GREEN, player.points),
                    get_color_string(bcolors.GREEN, player.buying_power),
                    get_color_string(bcolors.GREEN, player.killing_power),
                    get_color_string(bcolors.GREEN, deck),
                    get_color_string(bcolors.GREEN, hand),
                    get_color_string(bcolors.GREEN, discard)
                ]
            else:
                player_info = [
                    player.name,
                    player.points,
                    player.buying_power,
                    player.killing_power,
                    deck,
                    hand,
                    discard
                ]
            player_statuses.append(player_info)
        print_color_table(player_statuses)

    def print_results(self):
        winner = None
        winner_total = 0
        for p in self.players:
            print p.name
            for card in p.deck:
                p.points += card.worth
                if card.worth > 0: print '...', card.name, card.worth
            for card in p.discard:
                p.points += card.worth
                if card.worth > 0: print '...', card.name, card.worth
            for card in p.hand:
                p.points += card.worth
                if card.worth > 0: print '...', card.name, card.worth
            for card in p.phand:
                p.points += card.worth
                if card.worth > 0: print '...', card.name, card.worth
            print p
            if p.points > winner_total:
                winner = p.name
        print 'WINNER!!:  ', winner

