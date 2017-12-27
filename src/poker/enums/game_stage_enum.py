from enum import IntEnum


class GameStageEnum(IntEnum):
    welcome     = 1
    blinds      = 2
    preflop     = 3
    flop        = 4
    turn        = 5
    river       = 6
    winners     = 7
