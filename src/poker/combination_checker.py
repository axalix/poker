from collections import Counter
from poker.deck import Deck
from poker.enums.combination_enum import CombinationEnum


class CombinationChecker:
    PATTERN_HIGH_RANK = 'high_rank'
    PATTERN_TWO_SAME_RANK = 'two_same_rank'
    PATTERN_TWO_SAME_RANK_PAIRS = 'two_same_rank_pairs'
    PATTERN_THREE_SAME_RANK = 'three_same_rank'
    PATTERN_THREE_SAME_RANK_TWO_SAME_RANK = 'three_same_rank_two_same_rank'
    PATTERN_FIVE_IN_ORDER = 'five_in_order'
    PATTERN_FIVE_SAME_SUIT = 'five_same_suit'
    PATTERN_FOUR_SAME_RANK = 'four_same_rank'
    PATTERN_TJQKA = 'tjqka'

    # J - 11
    # Q - 12
    # K - 13
    # A - 14
    combinations_rules = {
        CombinationEnum.high_card: {
            'name': 'High Card',
            'pattern': PATTERN_HIGH_RANK,
            'base_power': 0,
            # min 2
            # max 14 + kicker: 4 x A = 56
        },

        CombinationEnum.pair: {
            'name': 'Pair',
            'pattern': PATTERN_TWO_SAME_RANK,
            'base_power': 53,
            # min = 4
            # max = 28 + kicker: 3 x A = 42
            # power = prev_power + prev_max - min + 1 = 0 + 56 - 4 + 1 = 53
        },

        CombinationEnum.two_pairs: {
            'name': 'Two pairs',
            'pattern': PATTERN_TWO_SAME_RANK_PAIRS,
            'base_power': 86,
            # min = 2 x 2 + 3 x 2 = 10
            # max = 2 x K + 2 x A = 54 + kicker: A = 68
            # power = prev_power + prev_max - min + 1 = 53 + 42 - 10 + 1 = 86
        },

        CombinationEnum.three_of_a_kind: {
            'name': 'Three of a kind',
            'pattern': PATTERN_THREE_SAME_RANK,
            'base_power': 149,
            # min = 3 x 2 = 6
            # max = 3 x A = 54 + kicker: 2 x A = 82
            # power = prev_power + prev_max - min + 1 = 86 + 68 - 6 + 1 = 149
        },

        CombinationEnum.straight: {
            'name': 'Straight',
            'pattern': PATTERN_FIVE_IN_ORDER,
            'base_power': 189
            # min = A + 2 + 3 + 4 + 5 = 15
            # max = T + J + Q + K + A = 60
            # power = prev_power + prev_max - min + 1 = 149 + 54 - 15 + 1 = 189
        },

        CombinationEnum.flush: {
            'name': 'Flush',
            'pattern': PATTERN_FIVE_SAME_SUIT,
            'base_power': 230
            # min = 2 + 3 + 4 + 5 + 6 = 20
            # max = T + J + Q + K + A = 60
            # power = prev_power + prev_max - min + 1 = 189 + 60 - 20 + 1 = 230
        },

        CombinationEnum.full_house: {
            'name': 'Full House',
            'pattern': PATTERN_THREE_SAME_RANK_TWO_SAME_RANK,
            'base_power': 279
            # min = 3 x 2 + 2 x 3 = 12
            # max = 3 x A + 2 x K = 68
            # power = prev_power + prev_max - min + 1 = 230 + 60 - 12 + 1 = 279
        },

        CombinationEnum.four_of_a_kind: {
            'name': 'Four of a kind',
            'pattern': PATTERN_FOUR_SAME_RANK,
            'base_power': 340
            # min = 4 x 2 = 8
            # max = 4 x A = 56
            # power = prev_power + prev_max - min + 1 = 279 + 68 - 8 + 1 = 340
        },

        CombinationEnum.straight_flush: {
            'name': 'Straight Flush',
            'pattern': (PATTERN_FIVE_IN_ORDER, PATTERN_FIVE_SAME_SUIT),
            'base_power': 382
            # min = A + 2 + 3 + 4 + 5 = 15
            # max = T + J + Q + K + A = 60
            # power = prev_power + prev_max - min + 1 = 340 + 56 - 15 + 1 = 382
        },

        CombinationEnum.royal_flush: {
            'name': 'Royal Flush',
            'pattern': (PATTERN_TJQKA, PATTERN_FIVE_SAME_SUIT),
            'base_power': 383
            # min = T + J + Q + K + A = 60
            # max = T + J + Q + K + A = 60
            # power = prev_power + prev_max - min + 1 = 382 + 60 - 60 + 1 = 383
        }
    }

    def __init__(self, pocket_cards, table_cards):
        """
        :type pocket_cards: list
        :type table_cards: list
        """
        self.pocket_cards = pocket_cards
        self.table_cards = table_cards

        (combination, winning_cards, power) = self.__process(self.pocket_cards + self.table_cards)
        # self.power = CombinationChecker.__calculate_power(self.pocket_cards, self.table_cards, combination)
        # self.name = combination['name']


    def __process(self, seven_cards):
        """
        :type seven_cards: list
        :rtype: list
        """

        for combination in CombinationEnum:
            winning_cards_and_power = self.__test_cards_against_combination(seven_cards, combination)
            if winning_cards_and_power:
                return [combination] + winning_cards_and_power


    def __test_cards_against_combination(self, seven_cards, combination):
        """
        :type seven_cards: list
        :type combination: CombinationEnum
        :rtype: list
        """

        combination_rule = self.combinations_rules[combination]
        combination_name = combination.name
        pattern = combination_rule['pattern']
        base_power = combination_rule['base_power']

        winning_cards = []
        power = 0

        if isinstance(pattern, tuple):
            for p in pattern:
                combination_cards = getattr(self, '__test_pattern_' + p)(seven_cards)
                if combination_cards:
                    pass
        else:
            combination_cards = getattr(self, '__test_pattern_' + pattern)(seven_cards)
            if combination_cards:
                power = base_power

        if not winning_cards:
            return None

        power += CombinationChecker.__power(winning_cards) + \
                 CombinationChecker.__kicker_cards_power(seven_cards, winning_cards)

        return [winning_cards, power]

    @staticmethod
    def __diff(list1, list2):
        return list(set(list1) - set(list2))


    @classmethod
    def __power(cls, cards):
        """
        :type cards: list
        :rtype: int
        """
        power = 0
        for card in cards:
            power += Deck.ranks_powers[card[0]]

        return power


    @classmethod
    def __select_high_cards(cls, cards, n):
        """
        :type cards: list
        :type n: int
        :rtype: list
        """
        return sorted(cards, key=lambda x: Deck.ranks_powers[x[0]], reverse=True)[:n]


    @classmethod
    def __kicker_cards_power(cls, seven_cards, winning_cards):
        """
        :type seven_cards: list
        :type winning_cards: list
        :rtype: int
        """
        kicker_cards_number = len(winning_cards) - 5
        if not kicker_cards_number:
            return 0

        remaining_cards = CombinationChecker.__diff(seven_cards, winning_cards)
        kicker_cards = CombinationChecker.__select_high_cards(remaining_cards, kicker_cards_number)
        return CombinationChecker.__power(kicker_cards)


    # ------ Patterns Checkers

    def __test_pattern_high_rank(self, seven_cards):
        return CombinationChecker.__select_high_cards(seven_cards, 1)

    def __test_pattern_same_rank(self, seven_cards, n):
        """

        :type seven_cards: list
        :param n: int
        :rtype: list
        """
        counter = Counter()
        for card in seven_cards:
            counter[card[0]] += 1

        most_common = counter.most_common(1)
        if most_common[1] == n:
            return map(lambda x: x[1] == most_common[0], seven_cards)
        return None

    def __test_pattern_two_same_rank(self, seven_cards):
        return self.__test_pattern_same_rank(seven_cards, 2)


    def __test_pattern_two_same_rank_pairs(self, seven_cards):
        pair = self.__test_pattern_two_same_rank(seven_cards)
        if not pair:
            return None

        remaining_cards = CombinationChecker.__diff(seven_cards, pair)
        second_pair = self.__test_pattern_two_same_rank(remaining_cards)
        if not second_pair:
            return None

        return pair + second_pair


    def __test_pattern_three_same_rank(self, seven_cards):
        return self.__test_pattern_same_rank(seven_cards, 3)


    def __test_pattern_three_same_rank_two_same_rank(self, seven_cards):
        three = self.__test_pattern_three_same_rank(seven_cards)
        if not three:
            return None

        remaining_cards = CombinationChecker.__diff(seven_cards, three)
        second_pair = self.__test_pattern_two_same_rank(remaining_cards)
        if not second_pair:
            return None

        return three + second_pair


    def __test_pattern_four_same_rank(self, seven_cards):
        return self.__test_pattern_same_rank(seven_cards, 4)


    def __test_pattern_five_in_order(self, seven_cards):
        return True


    def __test_pattern_five_same_suit(self, seven_cards):
        return True

    def __test_pattern_tjqka(self, seven_cards):
        return True
