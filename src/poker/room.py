from poker.game import Game
from poker.player import Player
from poker.poker_object import PokerObject


class Room(PokerObject):

    def __init__(self, players):
        """
        :type players: list of Player
        """
        self.game_id = 0
        self.players = players
        self.game = None


    def play(self):
        while len(self.players) > 1:
            self.game_id += 1
            self.game = Game(self.game_id, self.players)
            self.game.play()
            self.move_dealer()

        print('Game over')

    # dealer is always a first player in a list
    def move_dealer(self):
        self.players = self.players[1:] + [self.players[0]]
