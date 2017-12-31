from poker.poker_object import PokerObject
from poker.enums.game_stage_enum import GameStageEnum
from poker.enums.player_action_enum import PlayerActionEnum
from poker.combination_checker import CombinationChecker
from poker.deck import Deck
from poker.player import Player


class Game(PokerObject):
    SMALL_BLIND = 1
    BIG_BLIND = 2

    call_to = 0

    def __init__(self, id_, players):
        """
        :type id_: int
        :type players: list of Player
        """
        self.current_state = None
        self.id_ = id_
        self.players = players

        self.dealer = self.players[0]

        self.deck = Deck()
        self.small_blind_player = None
        self.big_blind_player = None
        self.pot = 0
        self.call_to = 0
        self.table_cards = []
        self.players_balanced = 0

        self.game_state_iterator = iter(GameStageEnum)

    # ------- Game Process

    # game loop
    def play(self):
        self.assign_pocket_cards()

        while self.tick():
            getattr(self, 'stage_' + self.current_state.name)()

            while self.players_balanced != len(self.players):

                for player in self.players:
                    if player.all_ined() or player.bet_ == self.call_to:
                        self.players_balanced += 1
                        continue

                    self.chat(player)
                    print("\n- - - - - - - - -\n")


            self.players_balanced = 0
            self.call_to = 0
            self.for_all_players('reset_bet')

    # stages loop
    def tick(self):
        self.current_state = next(self.game_state_iterator)
        return self.game_state_iterator

    # ------- Player

    def process_player_reaction(self, player):
        """
        :type player: Player
        :return:
        """
        action, amount = player.request_action(self.call_to)


        if action == PlayerActionEnum.fold:
            self.remove_player(player)

        if amount:
            self.charge(player, amount)
            if amount > self.call_to:
                self.players_balanced = 0
                self.call_to = amount


    def chat(self, player):
        role = ''

        if player == self.dealer:
            role = 'D'

        if player == self.small_blind_player:
            role = 'SB'

        if player == self.big_blind_player:
            role = 'BB'

        print("Player {} #{}. Balance ${}: ".format(role, player.account.name, player.chips))

        print("Your cards {}".format(player.pocket_cards))

        if self.call_to:
            bet_or_more = self.call_to - player.bet_
            print("Bet ${} or more".format(bet_or_more))

        self.process_player_reaction(player)



    # ------- Players Loop

    def for_all_players(self, f, *args, **kwargs):
        for player in self.players:
            getattr(player, f)(*args, **kwargs)

    def remove_player(self, player):
        for i, p in enumerate(self.players):
            if p == player:
                del (self.players[i])
                break

    def assign_pocket_cards(self):
        for player in self.players:
            player.assign_poket_cards(self.deck.get(2))


    # ------- Table

    def get_table_cards(self):
        return self.table_cards

    def set_blinds(self):
        total_players = len(self.players)

        small_blind_position = 1
        self.small_blind_player = self.players[small_blind_position]

        big_blind_position = 2
        if big_blind_position == total_players:
            big_blind_position = 0
        self.big_blind_player = self.players[big_blind_position]

        self.charge_for_blinds()

    # ------- Money

    def charge(self, player, amount):
        """
        :type player: Player
        :type amount: int
        """
        self.pot += amount
        player.bet(amount)

    def charge_for_blinds(self):
        self.charge(self.small_blind_player, self.SMALL_BLIND)
        self.charge(self.big_blind_player, self.BIG_BLIND)
        self.call_to = self.BIG_BLIND


    # ------- Actions

    def stage_welcome(self):
        print("Lets begin poker game #{}".format(self.id_))

    def stage_preflop(self):
        self.set_blinds()
        self.call_to = self.BIG_BLIND
        print(self.current_state.name)
        print(self.table_cards)

    def stage_flop(self):
        self.table_cards += self.deck.get(3)
        print(self.current_state.name)
        print(self.table_cards)

    def stage_turn(self):
        self.table_cards += self.deck.get(1)
        print(self.current_state.name)
        print(self.table_cards)

    def stage_river(self):
        self.table_cards += self.deck.get(1)
        print(self.current_state.name)
        print(self.table_cards)

    def stage_winners(self):
        # TODO
        players_hands = []
        for p in self.players:
            players_hands.append([p.pocket_cards, CombinationChecker(p.pocket_cards, self.table_cards)])

        players_hands_sorted = sorted(players_hands, key=lambda x: x[1].power, reverse=True)

        for player_hand in players_hands_sorted:
            two = player_hand[0]
            c = player_hand[1]

            print('{}: {} => {}!, {} . . . {} '.format(c.combinations_rules[c.combination]['name'], two,
                                                       c.combination_cards, c.power, c.kicker_cards))
