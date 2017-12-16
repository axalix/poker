
class Player:

    FOLD = 1
    RAISE = 2
    CALL = 3
    CHECK = 4
    ALL_IN = 5

    def __init__(self, name, balance):
        self._name = name
        self._balance = balance

    #------- Cards

    def assign_cards(self, pocket_cards):
        """
        :type pocket_cards: tuple
        :return:
        """
        self._pocket_cards = pocket_cards


    #------- Balance

    def increase_balance(self, amount):
        self._balance += amount

    def decrease_balance(self, amount):
        self._balance -= amount


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