from poker.deck import Deck
from poker.player import Player


class Game:
    states = ('Preflop', 'Flop', 'Turn', 'River')

    def __init__(self, id_, players):
        """
        :type id_: int
        :type players: list of Player
        """
        self._current_state = None
        self._id = id_
        self._players = players
        # self._state_iterator = iter(self.states)
        self._deck = Deck
        self._pot = 0
        self._table_cards = []
        self._assign_pocket_cards()

    # ------- Game Process

    # main loop
    def play(self):

        for self._current_state in self.states:
            self.__change_state()

    def __change_state(self):
        getattr(self, 'do_' + self._current_state.lower())()

    # ------- Player

    def _assign_pocket_cards(self):
        for p in self._players:
            p.assign_cards(self._deck.get(2))

    # ------- Table

    def get_table_cards(self):
        return self._table_cards

    # ------- Balance

    # ------- Actions

    def do_preflop(self):
        print(self._current_state)
        pass

    def do_flop(self):
        self._table_cards += self._deck.get(3)
        print(self._current_state)
        pass

    def do_turn(self):
        self._table_cards += self._deck.get(1)
        print(self._current_state)
        pass

    def do_river(self):
        self._table_cards += self._deck.get(1)
        print(self._current_state)
        pass
