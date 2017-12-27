from poker.game import Game
from poker.player import Player
from poker.poker_object import PokerObject


class Room(PokerObject):

    __dealer_position = 1

    def __init__(self, players):
        """

        :type players: list of Player
        """
        self._game_id = 0
        self._players = players
        self._game = None


    def play(self):
        while len(self._players) > 1:
            self._game_id += 1
            self._game = Game(self._game_id, self._players, self.dealer_position())
            self._game.play()
        print('Game over')


    def dealer_position(self):
        self.__dealer_position += 1
        if self.__dealer_position >= len(self._players):
            self.__dealer_position = 1

        return self.__dealer_position



