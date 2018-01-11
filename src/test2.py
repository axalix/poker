from poker.deck import Deck
from poker.card import Card
from poker.evaluator import Evaluator


players_number = 4

d = Deck()
five = d.get(5)
#five = [Card(4, 'D'), Card(5, 'D'), Card(3, 'D'), Card(14, 'D')] # straight from '2'

print(five)

players_hands = []
for i in range(1, players_number + 1):
    two = d.get(2)
    players_hands.append([two, Evaluator(two, five)])

players_hands_sorted = sorted(players_hands, key=lambda x: x[1].power, reverse = True)


for player_hand in players_hands_sorted:
    two = player_hand[0]
    c = player_hand[1]


    # print('Pocket cards #{}: {} '.format(i, two))
    # print(c.evaluator[c.combination]['name'])
    # print('Winning combination #{}: {} '.format(i, c.combination_cards))
    # print('Possible kickers #{}: {} '.format(i, c.kicker_cards))
    # print('Power #{}: {}'.format(i, c.power))

    print('{}: {} => {}!, {} . . . {} '.format(c.evaluator[c.combination]['name'], two, c.combination_cards, c.power, c.kicker_cards))

