import random

class Deck:
    ranks = tuple(range(2, 11)) + ('J', 'Q', 'K', 'A')

    suits = ('♥', '♦', '♣', '♠')

    @classmethod
    def __create_cards(cls):
        cards = []
        for rank in Deck.ranks:
            for suit in Deck.suits:
                cards.append((rank, suit))
        return cards

    def __init__(self):
        self._deck = Deck.__create_cards()
        self.shuffle()


    def shuffle(self):
        random.shuffle(self._deck)


    def get(self, n):
        if len(self._deck) >= n:
            r = self._deck[0:n]
            del self._deck[0:n]
            return r

        raise ValueError("There are not enough cards in a deck")
