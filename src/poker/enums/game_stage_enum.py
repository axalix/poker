from enum import IntEnum


class GameStageEnum(IntEnum):
    preflop     = 1
    flop        = 2
    turn        = 3
    river       = 4
    winners     = 5
