from poker.player import Player
from poker.poker_object import PokerObject


class GameTable(PokerObject):
    def __init__(self):
        self.players = []

        self.dealer = None
        self.small_blind_player = None
        self.prepare_blind_player = None

        self._dealer_button_position = None
        self._current_player_position = None

        # cards
        self.flop = []
        self.turn = []
        self.river = []

    def prepare(self, players):
        """
        :type players: list of Player
        :return:
        """
        self.players = players[:]  # clone instead of reference
        self._prepare_players()
        self._reset_players_positions()

        # cards
        self.flop = []
        self.turn = []
        self.river = []

    # dealer is always a first player in a list
    def move_dealer_button(self):
        self._dealer_button_position = 0 if self._dealer_button_position is None else self._dealer_button_position + 1
        if self._dealer_button_position >= len(self.players):
            self._dealer_button_position = 0

    @property
    def cards(self):
        return self.flop + self.turn + self.river

    def _prepare_players(self):
        for p in self.players:
            p.prepare()

    def next_player(self):
        """
        :rtype: Player
        """
        self._current_player_position += 1
        if self._current_player_position >= len(self.players):
            self._current_player_position = 0

        return self.current_player()

    def next_reacting_player(self, counter=1):
        next_player = self.next_player()
        if next_player.is_reacting():
            return next_player

        return None if counter == len(self.players) else self.next_reacting_player(counter + 1)

    def current_player(self):
        """
        :rtype: Player
        """
        # print('pos #' + str(self._current_player_position))
        return self.players[self._current_player_position]

    @property
    def reacting_players_count(self):
        return len([x for x in self.players if x.is_reacting()])

    # -----------------------

    def _reset_players_positions(self):
        self.move_dealer_button()
        self._current_player_position = self._dealer_button_position
        self.dealer = self.players[self._dealer_button_position]
        self.dealer.role = Player.ROLE_DEALER

        self.small_blind_player = self.next_player()
        self.small_blind_player.blind_flag = Player.BLIND_FLAG_SMALL

        self.big_blind_player = self.next_player()
        self.big_blind_player.blind_flag = Player.BLIND_FLAG_BIG

    def make_dealer_current_player(self):
        self._current_player_position = self._dealer_button_position
