from poker.poker_object import PokerObject


class Account(PokerObject):

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance


    #------- Balance

    def increase_balance(self, amount):
        if amount < 0:
            raise ValueError('Positive amount expected')
        self.balance += amount


    def decrease_balance(self, amount):
        if amount < 0:
            raise ValueError('Positive amount expected')
        self.balance -= amount

