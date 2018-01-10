from poker.player import Player
from poker.poker_object import PokerObject


class GameTable(PokerObject):
    def __init__(self):
        # players
        self.players = []
        self.participating_players = []

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
        # players
        self.players = players
        self.participating_players = self.players[:]  # clone instead of reference
        self._prepare_players()
        self._reset_players_positions()

        # cards
        self.flop = []
        self.turn = []
        self.river = []

    # dealer is always a first player in a list
    def move_dealer_button(self):
        self._dealer_button_position = 0 if self._dealer_button_position is None else self._dealer_button_position + 1
        if self._dealer_button_position > len(self.participating_players):
            self._dealer_button_position = 0

    @property
    def cards(self):
        return self.flop + self.turn + self.river


    def _prepare_players(self):
        for p in self.participating_players:
            p.prepare()

    def next_participating_player(self):
        """
        :rtype: Player
        """
        self._current_player_position += 1
        if self._current_player_position >= len(self.participating_players):
            self._current_player_position = 0

        return self.current_participating_player()

    def current_participating_player(self):
        # print('pos #' + str(self._current_player_position))
        return self.participating_players[self._current_player_position]


    # -----------------------


    def _reset_players_positions(self):
        self.move_dealer_button()
        self._current_player_position = self._dealer_button_position
        self.dealer = self.participating_players[self._dealer_button_position]
        self.dealer.role = Player.ROLE_DEALER

        self.small_blind_player = self.next_participating_player()
        self.small_blind_player.role = Player.ROLE_SMALL_BLIND

        self.big_blind_player = self.next_participating_player()
        self.big_blind_player.role = Player.ROLE_BIG_BLIND


        # print('D' +self.dealer.account.name)
        # print('SB' +self.small_blind_player.account.name)
        # print('BB' +self.big_blind_player.account.name)

    def make_dealer_current_player(self):
        self._current_player_position = self._dealer_button_position
