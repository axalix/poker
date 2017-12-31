from poker.poker_object import PokerObject
from poker.account import Account
from poker.enums.player_action_enum import PlayerActionEnum


class Player(PokerObject):

    REACTING  = 1
    FOLDED   = 2
    ALL_INED = 3


    def __init__(self, account, chips):
        """
        :type room: Room
        :type account: Account
        :type chips: int
        """
        self.account = account
        self.chips = chips

        self.bet_ = 0
        self.state = self.FOLDED
        self.pocket_cards = []

    #------- Game

    def reset_bet(self):
        self.bet_ = 0

    def reset_state(self):
        self.state = self.REACTING

    def reset_pocket_cards(self):
        self.pocket_cards = []

    def reset(self):
        self.reset_bet()
        self.reset_state()
        self.reset_pocket_cards()

    #------- States

    def folded(self):
        return self.state == self.FOLDED

    def all_ined(self):
        return self.state == self.ALL_INED


    #------- Cards

    def assign_poket_cards(self, pocket_cards):
        """
        :type pocket_cards: tuple
        :return:
        """
        self.pocket_cards = pocket_cards


    #------- Chips

    def bet(self, amount):
        self.decrease_chips(amount)
        self.bet_ = amount


    def increase_chips(self, amount):
        if amount < 0:
            raise ValueError('Positive amount expected')
        self.chips += amount


    def decrease_chips(self, amount):
        if amount < 0:
            raise ValueError('Positive amount expected')
        self.chips -= amount


    #------- Interface

    def __ask(self, possible_actions, call_to):
        var = input("Please enter one of these actions: {}".format(list(map(lambda x:x.name, possible_actions))))

        # TODO: only allow actions based on "possible_actions"
        if var == 'F':
            print('FOLD')
            self.state = self.FOLDED
            return (PlayerActionEnum.fold, 0)

        if var == 'A':
            print('ALL INN')
            self.state = self.ALL_INED
            return (PlayerActionEnum.all_in, self.chips)

        if var == 'R':
            print('RAISE')
            amount = input("How much?")
            # TODO; add amount checks: not less than call, not more than balance
            amount = int(amount)
            return (PlayerActionEnum.raise_, amount)

        if var == 'C':
            print('CALL OR CHECK') # TOTO
            return (PlayerActionEnum.raise_, call_to)

    #------- Actions & Reactors

    def request_action(self, call_to):
        possible_actions = [
            PlayerActionEnum.fold
        ]

        if call_to == 0:
            possible_actions.append(PlayerActionEnum.check)
        else:
            if self.chips > call_to - self.bet_:
                possible_actions += [PlayerActionEnum.call, PlayerActionEnum.raise_]
            else:
                possible_actions.append(PlayerActionEnum.all_in)

        return self.__ask(possible_actions, call_to)


    def react_to_fold(self):
        pass

    def react_to_call(self, amount):
        pass

    def react_to_raise(self, amount):
        pass

    def react_to_check(self):
        pass

    def react_to_all_in(self):
        pass