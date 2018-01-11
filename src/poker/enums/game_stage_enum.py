from enum import IntEnum


class GameStageEnum(IntEnum):
    welcome     = 1
    preflop     = 2
    flop        = 3
    turn        = 4
    river       = 5
    winners     = 6
