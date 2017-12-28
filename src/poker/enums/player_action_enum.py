from enum import IntEnum


class PlayerActionEnum(IntEnum):
    fold    = 1
    call    = 2
    check   = 3
    raise_  = 4
    all_in  = 5
