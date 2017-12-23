# from poker.game import Game
# from poker.player import Player
#
#
# p1 = Player('Alex', 100)
# p2 = Player('Matt', 50)
# g = Game([p1, p2])

from poker.deck import Deck
from poker.combination_checker import CombinationChecker
from poker.enums.combination_enum import CombinationEnum

i = 0
while True:
    d = Deck()
    two = d.get(2)
    five = d.get(5)
    c = CombinationChecker(two, five)
    i += 1

    if c.combination == CombinationEnum.royal_flush:
        break

print(i)
print(two)
print(five)
print(c.winning_cards)
print(c.combination)