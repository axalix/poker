from enum import IntEnum


class PlayerTurnEnum(IntEnum):
    fold    = 1
    call    = 2
    raise_  = 3
    all_in  = 4
