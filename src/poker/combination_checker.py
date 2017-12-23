from collections import Counter
from poker.deck import Card
from poker.deck import Deck
from poker.enums.combination_enum import CombinationEnum


class CombinationChecker:
    PATTERN_HIGH_RANK                       = 'high_rank'
    PATTERN_TWO_SAME_RANK                   = 'two_same_rank'
    PATTERN_TWO_SAME_RANK_PAIRS             = 'two_same_rank_pairs'
    PATTERN_THREE_SAME_RANK                 = 'three_same_rank'
    PATTERN_THREE_SAME_RANK_TWO_SAME_RANK   = 'three_same_rank_two_same_rank'
    PATTERN_FIVE_IN_ORDER                   = 'five_in_order'
    PATTERN_FIVE_IN_ORDER_AND_SAME_SUIT     = 'five_in_order_and_same_suit'
    PATTERN_FIVE_SAME_SUIT                  = 'five_same_suit'
    PATTERN_FOUR_SAME_RANK                  = 'four_same_rank'
    PATTERN_TJQKA_AND_SAME_SUIT             = 'tjqka_and_same_suit'

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
            'pattern': PATTERN_FIVE_IN_ORDER_AND_SAME_SUIT,
            'base_power': 382
            # min = A + 2 + 3 + 4 + 5 = 15
            # max = T + J + Q + K + A = 60
            # power = prev_power + prev_max - min + 1 = 340 + 56 - 15 + 1 = 382
        },

        CombinationEnum.royal_flush: {
            'name': 'Royal Flush',
            'pattern': PATTERN_TJQKA_AND_SAME_SUIT,
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

        (self.combination, self.winning_cards, self.power) = self.__process(self.pocket_cards + self.table_cards)


    def __process(self, seven_cards):
        """
        :type seven_cards: list of Card
        :rtype: list ' [combination, winning_cards, power]
        """
        for combination in CombinationEnum:
            victory = self.__test_cards_against_combination(seven_cards, combination)
            if victory:
                return victory


    def __test_cards_against_combination(self, seven_cards, combination):
        """
        :type seven_cards: list of Card
        :type combination: CombinationEnum
        :rtype: list
        """
        combination_rule = self.combinations_rules[combination]
        pattern = combination_rule['pattern']
        base_power = combination_rule['base_power']

        winning_cards = getattr(self, pattern)(seven_cards)
        if not winning_cards:
            return None

        power = base_power + \
                CombinationChecker.__power(winning_cards, combination) + \
                CombinationChecker.__kicker_cards_power(seven_cards, winning_cards)

        return [combination, winning_cards, power]


    @staticmethod
    def __diff(list1, list2):
        return list(set(list1) - set(list2))


    @classmethod
    def __power(cls, cards, combination = None):
        """
        :type cards: list of Card
        :type combination: CombinationEnum
        :rtype: int
        """
        power = 0
        if not isinstance(cards, list):
            print(combination)
            exit(1)

        for card in cards:
            power += card.rank

        # Straight A2345 => power(A) = 1
        if combination == CombinationEnum.straight:
            cards = CombinationChecker.__select_high_cards(cards, 2)
            if cards[0].is_ace() and cards[1].rank == 5:
                power -= 13

        return power


    @classmethod
    def __select_high_cards(cls, cards, n):
        """
        :type cards: list of Card
        :type n: int
        :rtype: list of Card
        """
        return sorted(cards, key=lambda c: c.rank, reverse=True)[:n]


    @classmethod
    def __select_same_suit_cards(self, cards, n):
        """
        :param cards: list of Card
        :rtype: list of Card
        """
        d = {}
        for card in cards:
            if card.suit not in d:
                d[card.suit] = []
            d[card.suit].append(card)

        max = 0
        same_suit_cards = []
        for suit, suited_cards in d.items():
            n = len(cards)
            if n > max:
                max = n
                same_suit_cards = suited_cards

        return CombinationChecker.__select_high_cards(same_suit_cards, n)

    @classmethod
    def __kicker_cards_power(cls, seven_cards, winning_cards):
        """
        :type seven_cards: list of Card
        :type winning_cards: list of Card
        :rtype: int
        """
        kicker_cards_number = len(winning_cards) - 5
        if not kicker_cards_number:
            return 0

        remaining_cards = CombinationChecker.__diff(seven_cards, winning_cards)
        kicker_cards = CombinationChecker.__select_high_cards(remaining_cards, kicker_cards_number)
        return CombinationChecker.__power(kicker_cards)


    # ------ Patterns Checkers

    def high_rank(self, seven_cards):
        return CombinationChecker.__select_high_cards(seven_cards, 1)


    def same_rank(self, seven_cards, n):
        """
        :type seven_cards: list of Card
        :param n: int
        :rtype: list of Card
        """
        counter = Counter()
        for card in seven_cards:
            counter[card.rank] += 1

        most_common = counter.most_common(1)

        if most_common[0][1] == n:
            return list(filter(lambda x: x.rank == most_common[0][0], seven_cards))
        return None


    def two_same_rank(self, seven_cards):
        """
        :param seven_cards: list of Card
        :rtype: list of Card
        """
        return self.same_rank(seven_cards, 2)


    def two_same_rank_pairs(self, seven_cards):
        """
        :param seven_cards: list of Card
        :rtype: list of Card
        """
        pair = self.two_same_rank(seven_cards)
        if not pair:
            return None

        remaining_cards = CombinationChecker.__diff(seven_cards, pair)
        second_pair = self.two_same_rank(remaining_cards)
        if not second_pair:
            return None

        return pair + second_pair


    def three_same_rank(self, seven_cards):
        """
        :param seven_cards: list of Card
        :rtype: list of Card
        """
        return self.same_rank(seven_cards, 3)


    def three_same_rank_two_same_rank(self, seven_cards):
        """
        :param seven_cards: list of Card
        :rtype: list of Card
        """
        three = self.three_same_rank(seven_cards)
        if not three:
            return None

        remaining_cards = CombinationChecker.__diff(seven_cards, three)
        second_pair = self.two_same_rank(remaining_cards)
        if not second_pair:
            return None

        return three + second_pair


    def four_same_rank(self, seven_cards):
        """
        :param seven_cards: list of Card
        :rtype: list of Card
        """
        return self.same_rank(seven_cards, 4)


    def five_in_order(self, seven_cards):
        """
        :param seven_cards: list of Card
        :rtype: list of Card
        """
        cards = CombinationChecker.__select_high_cards(seven_cards, 7)

        # ace with rank 1
        if cards[0].is_ace():
            cards.append(Card(1, cards[0].suit))

        prev_rank = cards[0].rank
        ordered_cards = [cards[0]]

        for i in range(1, len(cards)):
            card = cards[i]
            if len(ordered_cards) == 5:
                break

            if card.rank == prev_rank - 1:
                ordered_cards.append(card)
                if (len(ordered_cards) == 5):
                    return ordered_cards
            else:
                ordered_cards = [card]
            prev_rank = card.rank

        return None


    def five_same_suit(self, seven_cards):
        same_suit_cards = CombinationChecker.__select_same_suit_cards(seven_cards, 5)
        return CombinationChecker.__select_same_suit_cards(seven_cards, 5) if len(same_suit_cards) > 4 else None


    def five_in_order_and_same_suit(self, seven_cards):
        same_suit_cards = CombinationChecker.__select_same_suit_cards(seven_cards, 7)
        return self.five_in_order(same_suit_cards) if len(same_suit_cards) > 4 else None


    def tjqka_and_same_suit(self, seven_cards):
        """
        :param seven_cards: list of Card
        :rtype: list of Card
        """
        same_suit_cards = self.five_same_suit(seven_cards)
        if not same_suit_cards:
            return None

        return same_suit_cards if list(map(lambda x: x.rank, same_suit_cards)) == list(range(14, 9, -1)) else None
