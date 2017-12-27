from poker.game import Game
from poker.player import Player
from poker.poker_object import PokerObject


class Room(PokerObject):

    def __init__(self, players):
        """

        :type players: list of Player
        """
        self._game_id = 0
        self._players = players
        self._game = None

    def play_game(self):
        self._game_id += 1
        self._game = Game(self._game_id, self._players)
        self._game.play()




