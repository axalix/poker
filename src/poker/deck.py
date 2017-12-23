import random


class Card:
    def __init__(self, rank, suit):
        """
        :type rank: int
        :type suit: str
        """
        self.rank = rank
        self.rank_name = 'A' if rank == 1 else Deck.ranks_to_names[rank]


        self.suit = suit
        self.suit_name = Deck.suits_to_names[suit]

    def is_ace(self):
        return self.rank == 14

    def __str__(self):
        return self.rank_name + self.suit_name

    def __repr__(self):
        return self.__str__()

class Deck:
    ranks          = tuple(range(2, 15))
    ranks_names    = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
    ranks_to_names = dict(zip(ranks, ranks_names))
    names_to_ranks = dict(zip(ranks_names, ranks))

    suits = ('H', 'D', 'C', 'S')
    suits_names = ('♥', '♦', '♣', '♠')
    suits_to_names = dict(zip(suits, suits_names))
    names_to_suits = dict(zip(suits_names, suits))

    @classmethod
    def __create_cards(cls):
        cards = []
        for rank in Deck.ranks:
            for suit in Deck.suits:
                cards.append(Card(rank, suit))
        return cards

    def __init__(self):
        self._deck = Deck.__create_cards()
        self.shuffle()

    def shuffle(self):
        random.shuffle(self._deck)

    def get(self, n):
        """
        :param n: int
        :return:
        """
        if len(self._deck) >= n:
            r = self._deck[0:n]
            del self._deck[0:n]
            return r

        raise ValueError("There are not enough cards in a deck")
