from poker.poker_object import PokerObject


class Card(PokerObject):
    ranks          = tuple(range(2, 15))
    ranks_names    = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
    ranks_to_names = dict(zip(ranks, ranks_names))
    names_to_ranks = dict(zip(ranks_names, ranks))

    suits = ('H', 'D', 'C', 'S')
    suits_names = ('♥', '♦', '♣', '♠')
    suits_to_names = dict(zip(suits, suits_names))
    names_to_suits = dict(zip(suits_names, suits))

    def __init__(self, rank, suit):
        """
        :type rank: int
        :type suit: str
        """
        self.rank = rank
        self.rank_name = 'A' if rank == 1 else Card.ranks_to_names[rank]


        self.suit = suit
        self.suit_name = Card.suits_to_names[suit]

    def is_ace(self):
        return self.rank == 14


    #---- Operations

    @staticmethod
    def diff(list1, list2):
        return [e for e in list1 if e not in list2]


    @staticmethod
    def sort_desc(cards, n = None):
        """
        :type cards: list of Card
        :type n: int
        :rtype: list of Card
        """
        if not n:
            n = len(cards)
        return sorted(cards, key=lambda c: c.rank, reverse=True)[:n]

    @staticmethod
    def power(cards):
        """
        :type cards: list of Card
        :rtype: int
        """
        power = 0
        n = len(cards)
        for i, card in enumerate(cards):
            power += 14**(n - i - 1) * (card.rank - 1) # A = 14 or 13 in a 14-digits notation => rank - 1

        return power

    def __str__(self):
        return self.rank_name + self.suit_name

    def __repr__(self):
        return self.rank_name + self.suit_name

