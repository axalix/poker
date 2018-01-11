from poker.room import Room
from poker.player import Player
from poker.account import Account

paul = Account('Paul', 100)
mike = Account('Mike', 200)
matt = Account('Matt', 300)
alex = Account('Alex', 400)

r = Room([
    Player(paul, 100),
    Player(mike, 50),
    Player(matt, 100),
    Player(alex, 100)
])

r.play()
