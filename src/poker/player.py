from poker.enums.player_turn_enum import PlayerActionEnum
from poker.poker_object import PokerObject


class Player(PokerObject):

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    #------- Cards

    def assign_cards(self, pocket_cards):
        """
        :type pocket_cards: tuple
        :return:
        """
        self.pocket_cards = pocket_cards


    #------- Balance

    def increase_balance(self, amount):
        if amount < 0:
            raise ValueError('Positive amount expected')
        self.balance += amount


    def decrease_balance(self, amount):
        if amount < 0:
            raise ValueError('Positive amount expected')
        self.balance -= amount


    def request_action(self, call_to, previous_bet):
        possible_actions = [
            PlayerActionEnum.fold
        ]

        if call_to == 0:
            possible_actions.append(PlayerActionEnum.check)
        else:
            if self.balance > call_to - previous_bet:
                possible_actions += [PlayerActionEnum.call, PlayerActionEnum.raise_]
            else:
                possible_actions.append(PlayerActionEnum.all_in)

        return self.__ask(possible_actions)


    def __ask(self, possible_actions):
        pass

    #------- Actions Reactors

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