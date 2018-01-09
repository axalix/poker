from poker.poker_object import PokerObject
from poker.enums.game_stage_enum import GameStageEnum
from poker.combination_checker import CombinationChecker
from poker.deck import Deck
from poker.player import Player
from poker.game_table import GameTable


class Game(PokerObject):
    SMALL_BLIND = 1
    BIG_BLIND = 2

    current_bet = 0

    def __init__(self, id_, table):
        """
        :type id_: int
        :type table: GameTable
        """
        self.current_stage = None
        self.id_ = id_
        self.table = table

        self.deck = Deck()

        self.pot = 0
        self.current_bet = 0

        self.game_states_iterator = iter(GameStageEnum)

    # ------- Game Process

    def play(self):
        # main loop: preflop -> flop -> turn -> river -> winners
        for self.current_stage in self.game_states_iterator:
            self.play_stage()


        print("=================================================================")

    def play_stage(self):
        print(self.current_stage.name)
        getattr(self, 'stage_' + self.current_stage.name)()


    def play_round(self):
        print(self.table.cards)
        while len(self.table.participating_players) > 0 and \
              self.table.next_participating_player().reaction_required(self.current_stage, self.current_bet):
            print("Table cards: " + str(self.table.cards))
            self.request_player_action()
            print("\n- - - - - - - - -\n")

        self.current_bet = 0
        self.table.make_dealer_current_player()


    # ------- Player

    def assign_pocket_cards(self):
        for player in self.table.players:
            player.pocket_cards = self.deck.get(2)

    def request_player_action(self):
        player = self.table.current_participating_player()

        action, amount = player.request_action(self.current_stage, self.current_bet)

        if action == Player.ACTION_FOLD:
            self.table.withdraw_player()
            return

        if action == Player.ACTION_ALL_IN:
            self.table.all_in_player()

        if amount > self.current_bet:
            self.current_bet = amount

        self.pot += amount

    # ------- Money


    def charge_for_blinds(self):

        small_blind_amount = self.table.small_blind_player.charge(self.current_stage, Player.ACTION_SMALL_BLIND, self.SMALL_BLIND)
        # TODO: if player is all-iner, withdraw him from a table
        # if self.table.small_blind_player.previous_action(self.current_stage) == Player.ACTION_ALL_IN:
        #     self.table.small_blind_player.all_in_player()

        big_blind_amount = self.table.big_blind_player.charge(self.current_stage, Player.ACTION_BIG_BLIND, self.BIG_BLIND)
        # TODO: if player is all-iner, withdraw him from a table
        # if self.table.big_blind_player.previous_action(self.current_stage) == Player.ACTION_ALL_IN:
        #     self.table.big_blind_player.all_in_player()

        self.pot = small_blind_amount + big_blind_amount
        self.current_bet = self.BIG_BLIND


    # ------- Actions

    def stage_welcome(self):
        print("Lets begin poker game #{}".format(self.id_))

    def stage_preflop(self):
        self.charge_for_blinds()
        self.assign_pocket_cards()
        self.play_round()

    def stage_flop(self):
        self.table.flop = self.deck.get(3)
        self.play_round()

    def stage_turn(self):
        self.table.turn = self.deck.get(1)
        self.play_round()

    def stage_river(self):
        self.table.river = self.deck.get(1)
        self.play_round()

    def stage_winners(self):
        # TODO
        players_hands = []
        for p in self.table.potential_winners():
            players_hands.append([p.cards, CombinationChecker(p.cards, self.table.cards)])

        players_hands_sorted = sorted(players_hands, key=lambda x: x[1].power, reverse=True)

        for player_hand in players_hands_sorted:
            two = player_hand[0]
            c = player_hand[1]

            print('{}: {} => {}!, {} . . . {} '.format(c.combinations_rules[c.combination]['name'], two,
                                                       c.combination_cards, c.power, c.kicker_cards))
