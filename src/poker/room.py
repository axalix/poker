from poker.game import Game
from poker.player import Player
from poker.poker_object import PokerObject
from poker_table import PokerTable


class Room(PokerObject):

    def __init__(self, players):
        """
        :type players: list of Player
        """
        self.game_id = 0
        self.players = players
        self.table = PokerTable()


    def play(self):
        while len(self.players) > 1:
            self.prepare()
            game = Game(self.game_id, self.table).play()
            game.play()

        print('Game over')


    def prepare(self):
        self.game_id += 1
        self.prepare_players()
        self.table.prepare(self.players)


    def prepare_players(self):
        self._remove_bankrupts()
        self._add_players([])


    def _remove_bankrupts(self):
        for i, player in enumerate(self.players):
            if player.chips <= 0:
                del self.players[i]


    def _add_players(self, waiting_to_join_players):
        # TODO: self.players X self.waiting_to_join_players = Ø
        pass