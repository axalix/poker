from poker.deck import Deck
from poker.enums.game_stage_enum import GameStageEnum
from poker.player import Player
from poker.poker_object import PokerObject


class Game(PokerObject):

    SMALL_BLIND = 1
    BIG_BLIND   = 2

    call_to = 0

    def __init__(self, id_, players, dealer_position):
        """
        :type id_: int
        :type players: list of Player
        :type dealer_position: int
        """
        self.current_state = None
        self.id_ = id_
        self.players = players
        self.dealer_position = dealer_position

        self.deck = Deck()
        self.pot = 0
        self.call_to = 0
        self.table_cards = []
        self.small_blind_position = 0
        self.big_blind_position = 0
        # self.assign_pocket_cards()
        self.game_state_iterator = iter(GameStageEnum)

    # ------- Game Process

    def play(self):
        while self.tick():
            getattr(self, 'stage_' + self.current_state.name)()
            for player_position, player in enumerate(self.players):
                print("Player #{}. Balance ${}: ".format(player.name, player.balance))
                getattr(self, 'player_on' + self.current_state.name)(player, player_position)

    # main loop
    def tick(self):
        self.current_state = next(self.game_state_iterator)
        return self.game_state_iterator


    # ------- Player

    def assign_pocket_cards(self, player):
        player.assign_cards(self.deck.get(2))

    # ------- Table

    def get_table_cards(self):
        return self.table_cards

    def set_blinds(self):
        total_players = len(self.players)
        
        self.small_blind_position = self.dealer_position + 1
        if self.small_blind_position >= total_players:
            self.small_blind_position = 1


        self.big_blind_position = self.small_blind_position + 1
        if self.big_blind_position >= total_players:
            self.big_blind_position = 1

        self.charge_for_blinds()

    # ------- Money

    def charge(self, player, amount):
        self.pot += amount
        player.decrease_balance(amount)


    def charge_for_blinds(self):
        self.charge(self.players[self.small_blind_position], self.SMALL_BLIND)
        self.charge(self.players[self.big_blind_position], self.BIG_BLIND)


    # ------- Players Turns

    def player_on_welcome(self, player, player_position):
        self.assign_pocket_cards(player)
        print("Welcome {}. Your balance ${}".format(player.name, player.balance))
        print("Your cards {}".format(str(player.pocket_cards)))

        if player_position == self.dealer_position:
            print('You are a dealer')

        if player_position == self.small_blind_position:
            print('You are on a small blind')

        if player_position == self.small_blind_position:
            print('You are on a big blind')

    def player_on_preflop(self, player, player_position):
        print(self.current_state)


    def player_on_flop(self, player, player_position):
        self.table_cards += self.deck.get(3)
        print(self.current_state)


    def player_on_turn(self, player, player_position):
        self.table_cards += self.deck.get(1)
        print(self.current_state)


    def player_on_river(self, player, player_position):
        self.table_cards += self.deck.get(1)
        print(self.current_state)


    def player_on_winners(self, player, player_position):
        pass
    
    # ------- Actions


    def stage_welcome(self):
        print("Lets begin poker game #{}".format(self.id_))
        self.set_blinds()


    def stage_preflop(self):
        print(self.current_state)
        self.call_to = self.BIG_BLIND


    def stage_flop(self):
        self.call_to = 0
        self.table_cards += self.deck.get(3)
        print(self.current_state)


    def stage_turn(self):
        self.call_to = 0
        self.table_cards += self.deck.get(1)
        print(self.current_state)


    def stage_river(self):
        self.call_to = 0
        self.table_cards += self.deck.get(1)
        print(self.current_state)


    def stage_winners(self):
        pass