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


    #------- Actions

    def do_fold(self):
        pass

    def do_call(self, amount):
        pass

    def do_raise(self, amount):
        pass

    def do_check(self):
        pass

    def do_all_in(self):
        pass