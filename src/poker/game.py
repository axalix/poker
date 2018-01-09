from poker.poker_object import PokerObject
from poker.enums.game_stage_enum import GameStageEnum
from poker.combination_checker import CombinationChecker
from poker.deck import Deck
from poker.player import Player
from poker_table import PokerTable


class Game(PokerObject):
    SMALL_BLIND = 1
    BIG_BLIND = 2

    current_bet = 0

    def __init__(self, id_, table):
        """
        :type id_: int
        :type table: PokerTable
        """
        self.current_stage = None
        self.id_ = id_
        self.table = table

        self.deck = Deck()

        self.pot = 0
        self.current_bet = 0

        self.game_state_iterator = iter(GameStageEnum)

    # ------- Game Process

    # game loop
    def play(self):
        self.assign_pocket_cards()

        for self.current_stage in self.game_state_iterator:
            print("STATE {}".format(self.current_stage))
            getattr(self, 'stage_' + self.current_stage.name)()


        print("=================================================================")


    def play_round(self):
        while not self.table.next_participating_player().accepted_bet(self.current_stage, self.current_bet):
            self.request_player_reaction()
            print("\n- - - - - - - - -\n")

        print(self.current_stage.name)
        print(self.table.cards)

    # ------- Player

    def request_player_reaction(self):
        player = self.table.current_participating_player()


        reaction = player.request_action(self.current_stage, self.current_bet)
        action = reaction['action']
        player_bet = reaction['bet']

        if action == Player.ACTION_FOLD:
            self.table.player_fold()
            return

        if action == Player.ACTION_ALL_IN:
            self.table.player_all_in()
            return

        if player_bet:
            self.charge(player, player_bet)
            if player_bet > self.current_bet:
                self.current_bet = player_bet



    # ------- Player

    def assign_pocket_cards(self):
        for player in self.table.players:
            player.pocket_cards(self.deck.get(2))


    # ------- Money

    def charge(self, player, amount):
        """
        :type player: Player
        :type amount: int
        """
        self.pot += amount
        player.bet(amount)


    def charge_for_blinds(self):
        self.charge(self.table.small_blind_player, self.SMALL_BLIND)
        self.charge(self.table.big_blind_player, self.BIG_BLIND)
        self.current_bet = self.BIG_BLIND


    # ------- Actions

    def stage_welcome(self):
        print("Lets begin poker game #{}".format(self.id_))

    def stage_preflop(self):
        self.charge_for_blinds()
        self.play_round()

    def stage_flop(self):
        self.table.flop(self.deck.get(3))
        self.play_round()

    def stage_turn(self):
        self.table.turn(self.deck.get(1))
        self.play_round()

    def stage_river(self):
        self.table.river(self.deck.get(1))
        self.play_round()

    def stage_winners(self):
        # TODO
        players_hands = []
        for p in self.table.potential_winners():
            players_hands.append([p.cards, CombinationChecker(p.pocket_cards, self.table.cards)])

        players_hands_sorted = sorted(players_hands, key=lambda x: x[1].power, reverse=True)

        for player_hand in players_hands_sorted:
            two = player_hand[0]
            c = player_hand[1]

            print('{}: {} => {}!, {} . . . {} '.format(c.combinations_rules[c.combination]['name'], two,
                                                       c.combination_cards, c.power, c.kicker_cards))
