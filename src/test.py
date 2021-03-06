# from poker.game import Game
# from poker.player import Player
#
#
# p1 = Player('Alex', 100)
# p2 = Player('Matt', 50)
# g = Game([p1, p2])
from collections import Counter

from poker.deck import Deck
from poker.deck import Card
from poker.evaluator import Evaluator
from poker.enums.combination_enum import CombinationEnum


counter = Counter()
i = 0
while True:
    i += 1
    d = Deck()
    two = d.get(2)
    five = d.get(5)

    c = Evaluator(two, five)

    # if c.combination == CombinationEnum.straight:
    #     print(i)
    #     print(five)
    #     print('. . . . . .')
    #
    #     print(two)
    #     print(c.evaluator[c.combination]['name'])
    #     print(c.kicker_cards)
    #     print(c.combination_cards)
    #     print(c.power)
    #     print("=================================")
    #     i = 0

    counter[c.evaluator[c.combination]['name']] += 1

    if i % 10000 == 0:
        print('i = ' + str(i))
        #print(counter)
        d = {}
        for k, v in counter.items():
            d[k] = str(int((v / i) * 100000) / 1000) + '%'
        print(d)
        #print("=============================")

exit(1)

# 1 mil games
# Pair: 44.678%
# Two pairs: 23.691%
# High Card: 17.443%
# Three of a kind: 4.904%
# Straight: 3.521%
# Flush: 3.014%
# Full House: 2.548%
# Four of a kind: 0.164%
# Straight Flush: 0.029%
# Royal Flush: 0.003%


d = Deck()
cards = [Card(6, 'D'), Card(5, 'D'), Card(4, 'D'), Card(3, 'D'), Card(2, 'D')] # straight from '2'
#cards = [Card(5, 'D'), Card(4, 'D'), Card(3, 'D'), Card(2, 'D'), Card(14, 'D')] # straight from 'A'
#cards = [Card(5, 'D'), Card(4, 'D'), Card(3, 'D'), Card(2, 'D'), Card(14, 'D')] # straight from 'A'
# # #cards = d.get(5)
# #
# # #cards = [Card(2, 'D'), Card(10, 'D')]
# # #cards = [Card(9, 'D'), Card(9, 'S')]
# # #cards = [Card(14, 'D'), Card(14, 'D'), Card(14, 'D'), Card(14, 'D'), Card(13, 'S')]
# # cards = [Card(2, 'D'), Card(2, 'D')]
# #
# # print(cards)
# print(Evaluator.power(cards, CombinationEnum.straight))
print(Card.power(cards))

#
# exit(1)
#
# d = Deck()
# two1 = d.get(2)
# two2 = d.get(2)
# five = d.get(5)
#
# # two1 = [Card(13, 'H'), Card(2, 'C')]
# # two2 = [Card(14, 'S'), Card(12, 'S')]
# # five = [Card(6, 'D'), Card(12, 'S'), Card(13, 'C'), Card(6, 'C'), Card(8, 'C')]
#
# c1 = Evaluator(two1, five)
# c2 = Evaluator(two2, five)
#
#
# print(five)
# print('. . . . . .')
#
# print('Pocket cards #1: ' + str(two1))
# print(c1.evaluator[c1.combination]['name'])
# print('Winning combination #1: ' + str(c1.combination_cards))
# print('Possible kickers #1: ' + str(c1.kicker_cards))
# #print(c1.power_cards)
# print('Power #1: ' + str(c1.power))
#
# print('=============')
#
# print('Pocket cards #1: ' + str(two2))
# print(c2.evaluator[c2.combination]['name'])
# print('Winning combination #1: ' + str(c2.combination_cards))
# print('Possible kickers #1: ' + str(c2.kicker_cards))
# #print(c2.power_cards)
# print('Power #1: ' + str(c2.power))
#
# # kicker: [K♣, J♦,  9♦, 7♥] 4
# # kicker: [K♣, 10♣, 9♦, 8♣] 4
# # [A♥, 9♦, 5♣, K♣, 2♥]
# # . . . . . .
# # [J♦, 7♥]
# # High Card
# # [A♥]
# 54
# =============
# [10♣, 8♣]
# High Card
# [A♥]
# 54


# [6♠, Q♣, K♥, 6♥, 8♥]
# . . . . . .
# [2♥, K♣]
# Two pairs
# [K♥, K♣, 6♥, 6♠]
# []
# [K♥, K♣, 6♥, 6♠, Q♣]
# 1695910
# =============
# [A♣, Q♥]
# Two pairs
# [Q♣, Q♥, 6♥, 6♠]
# [A♣]
# [Q♣, Q♥, 6♥, 6♠, A♣]
# 1731582
