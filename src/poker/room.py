from poker.game import Game
from poker.player import Player
from poker.poker_object import PokerObject
from poker.game_table import GameTable


class Room(PokerObject):

    def __init__(self, players):
        """
        :type players: list of Player
        """
        self.game_id = 0
        self.players = players
        self.table = GameTable()


    def play(self):
        while True:
            if not self.prepare():
                break

            Game(self.game_id, self.table).play()

        print('Game over')


    def prepare(self):
        self.game_id += 1
        self._remove_bankrupts()
        self._add_new_players([])

        if len(self.players) < 2:
            return False

        self.table.prepare(self.players)
        return True



    def _remove_bankrupts(self):
        self.players = [ p for p in self.players if p.chips > 0]


    def _add_new_players(self, waiting_to_join_players):
        # TODO: self.players X self.waiting_to_join_players = Ø
        pass