from enum import IntEnum


class CombinationEnum(IntEnum):
    royal_flush     = 1
    straight_flush  = 2
    four_of_a_kind  = 3
    full_house      = 4
    flush           = 5
    straight        = 6
    three_of_a_kind = 7
    two_pairs       = 8
    pair            = 9
    high_card       = 10