import random

class Player:

    def __init__(self, name, balance):
        self._name = name
        self._balance = balance

#------- Cards

    def assign_cards(self, pocket_cards):
        self._pocket_cards = pocket_cards


#------- Balance

    def decrease_balance(self, delta):
        self._balance -= delta