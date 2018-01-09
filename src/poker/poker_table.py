from poker.player import Player
from poker_object import PokerObject


class PokerTable(PokerObject):
    def __init__(self):
        # players
        self.players = []
        self.participating_players = []
        self.allined_players = []
        self.folded_players = []

        self.dealer = None
        self.small_blind_player = None
        self.prepare_blind_player = None

        self._dealer_button_position = None
        self._current_player_position = None

        # cards
        self.flop = []
        self.turn = []
        self.river = []

    # dealer is always a first player in a list
    def move_dealer_button(self):
        self._dealer_button_position = 0 if self._dealer_button_position is None else self._dealer_button_position + 1
        if self._dealer_button_position > len(self.participating_players):
            self._dealer_button_position = 0

    def prepare(self, players):
        """
        :type players: list of Player
        :return:
        """
        # players
        self.players = players
        self.participating_players = self.players
        self.allined_players = []
        self.folded_players = []
        self._prepare_players()
        self._reset_players_positions()

        # cards
        self.flop = []
        self.turn = []
        self.river = []

    def flop(self, cards):
        self.flop = cards

    def turn(self, card):
        self.turn = card

    def river(self, card):
        self.river = card

    def cards(self):
        return self.flop + self.turn + self.river

    def potential_winners(self):
        """
        :rtype: list of Player
        """
        return self.participating_players + self.allined_players

    def _prepare_players(self):
        for p in self.participating_players:
            p.prepare()

    def next_participating_player(self):
        next_position = self._current_player_position
        if next_position >= len(self.participating_players):
            next_position = 0

        self._current_player_position = next_position
        return self.current_participating_player()

    def current_participating_player(self):
        return self.participating_players[self._current_player_position]

    def player_fold(self):
        self.folded_players.append(self.current_participating_player())
        self._remove_current_participant()

    def player_all_in(self):
        self.allined_players.append(self.current_participating_player())
        self._remove_current_participant()

    # -----------------------


    def _reset_players_positions(self):
        self.move_dealer_button()

        self.dealer = self.participating_players[self._dealer_button_position]
        self._current_player_position = self._dealer_button_position

        self.small_blind_player = self.next_participating_player()
        self.big_blind_player = self.next_participating_player()


    def _remove_current_participant(self):
        del(self.participating_players[self._current_player_position])