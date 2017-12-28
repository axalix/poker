from poker.combination_checker import CombinationChecker
from poker.deck import Deck
from poker.enums.game_stage_enum import GameStageEnum
from poker.player import Player
from poker.poker_object import PokerObject


class Game(PokerObject):

    SMALL_BLIND = 1
    BIG_BLIND   = 2

    call_to = 0
    previous_bets = {}

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
        self.dealer = self.players[dealer_position]

        self.deck = Deck()
        self.small_blind_player = None
        self.big_blind_player = None
        self.pot = 0
        self.call_to = 0
        self.table_cards = []

        self.previous_bets = {}

        # self.assign_pocket_cards()
        self.game_state_iterator = iter(GameStageEnum)

    # ------- Game Process

    def play(self):
        while self.tick():
            getattr(self, 'stage_' + self.current_state.name)()
            for player in self.players:
                print("Player #{}. Balance ${}: ".format(player.name, player.balance))
                getattr(self, 'player_on' + self.current_state.name)(player)

    # main loop
    def tick(self):
        self.current_state = next(self.game_state_iterator)
        return self.game_state_iterator


    # ------- Player

    def assign_pocket_cards(self, player):
        player.assign_cards(self.deck.get(2))


    def previous_bet(self, player):
        id_ = id(player)
        return self.previous_bets[id_] if id_ in self.previous_bet else 0

    def react_to_action(self, player, action, amount = 0):
        if amount:
            self.charge(player, amount)
        pass

    # ------- Table

    def get_table_cards(self):
        return self.table_cards

    def set_blinds(self):
        total_players = len(self.players)

        small_blind_position = self.dealer_position + 1
        if small_blind_position >= total_players:
            small_blind_position = 1
        self.small_blind_player = self.players[small_blind_position]

        big_blind_position = small_blind_position + 1
        if big_blind_position >= total_players:
            big_blind_position = 1
        self.big_blind_player = self.players[big_blind_position]

        self.charge_for_blinds()

    # ------- Money

    def charge(self, player, amount):
        """
        :type player: Player
        :type amount: int
        """
        self.pot += amount
        self.previous_bets[id(player)] = amount
        player.decrease_balance(amount)


    def charge_for_blinds(self):
        self.charge(self.small_blind_player, self.SMALL_BLIND)
        self.charge(self.big_blind_player, self.BIG_BLIND)
        self.call_to = self.BIG_BLIND


    # ------- Players Turns

    def player_on_welcome(self, player):
        print("Hi {}. Welcome to poker!".format(player.name))


    def player_on_preflop(self, player):
        self.assign_pocket_cards(player)

        print("Your cards {}".format(str(player.pocket_cards)))

        if player == self.dealer:
            print('You are a dealer')

        if player == self.small_blind_player:
            print('You are on a small blind')

        if player == self.big_blind_player:
            print('You are on a big blind')


    def player_on_flop(self, player):
        self.table_cards += self.deck.get(3)
        (action, amount) = player.request_action(self.call_to, self.previous_bet(player))
        self.react_to_action(player, action, amount)


    def player_on_turn(self, player):
        self.table_cards += self.deck.get(1)
        (action, amount) = player.request_action(self.call_to, self.previous_bet(player))
        self.react_to_action(player, action, amount)


    def player_on_river(self, player):
        self.table_cards += self.deck.get(1)
        (action, amount) = player.request_action(self.call_to, self.previous_bet(player))
        self.react_to_action(player, action, amount)

    def player_on_winners(self, player):
        print("Congratulations...") # TODO print winners and amounts
        pass

    # ------- Actions


    def stage_welcome(self):
        print("Lets begin poker game #{}".format(self.id_))
        self.set_blinds()


    def stage_preflop(self):
        self.call_to = self.BIG_BLIND
        self.previous_bets = {}
        print(self.current_state)


    def stage_flop(self):
        self.call_to = 0
        self.previous_bets = {}
        self.table_cards += self.deck.get(3)
        print(self.current_state)


    def stage_turn(self):
        self.call_to = 0
        self.previous_bets = {}
        self.table_cards += self.deck.get(1)
        print(self.current_state)


    def stage_river(self):
        self.call_to = 0
        self.previous_bets = {}
        self.table_cards += self.deck.get(1)
        print(self.current_state)


    def stage_winners(self):
        # TODO
        players_hands = []
        for p in self.players:
            players_hands.append([p.pocket_cards, CombinationChecker(p.pocket_cards, self.table_cards)])

        players_hands_sorted = sorted(players_hands, key=lambda x: x[1].power, reverse = True)


        for player_hand in players_hands_sorted:
            two = player_hand[0]
            c = player_hand[1]

            print('{}: {} => {}!, {} . . . {} '.format(c.combinations_rules[c.combination]['name'], two, c.combination_cards, c.power, c.kicker_cards))

