from poker.room import Room
from poker.player import Player
from poker.account import Account

paul = Account('Paul', 100)
mike = Account('Mike', 200)
matt = Account('Matt', 300)
alex = Account('Alex', 400)
ppaul = Player(paul, 100)
pmike = Player(mike, 100)
pmatt = Player(matt, 100)
palex = Player(alex, 100)

r = Room([ppaul, pmike, pmatt, palex])

r.play()
