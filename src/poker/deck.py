import random
from poker.card import Card
from poker.poker_object import PokerObject


class Deck(PokerObject):
    @classmethod
    def __create_cards(cls):
        cards = []
        for rank in Card.ranks:
            for suit in Card.suits:
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
