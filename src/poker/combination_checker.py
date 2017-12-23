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

    # 14-digits notations: 0 - 13. A = 13, 2 = 0
    MAX_5 = 537824 # AAAAK: 13 * 14^4 + 13 * 14^3 + 13 * 14^2 + 13 * 14^1 + 13 * 12^0 + 1

    # J - 11
    # Q - 12
    # K - 13
    # A - 14
    combinations_rules = {
        CombinationEnum.high_card: {
            'name': 'High Card',
            'pattern': PATTERN_HIGH_RANK,
            'base_power': 0
        },

        CombinationEnum.pair: {
            'name': 'Pair',
            'pattern': PATTERN_TWO_SAME_RANK,
            'base_power': MAX_5
        },

        CombinationEnum.two_pairs: {
            'name': 'Two pairs',
            'pattern': PATTERN_TWO_SAME_RANK_PAIRS,
            'base_power': 2 * MAX_5
        },

        CombinationEnum.three_of_a_kind: {
            'name': 'Three of a kind',
            'pattern': PATTERN_THREE_SAME_RANK,
            'base_power': 3 * MAX_5
        },

        CombinationEnum.straight: {
            'name': 'Straight',
            'pattern': PATTERN_FIVE_IN_ORDER,
            'base_power': 4 * MAX_5
        },

        CombinationEnum.flush: {
            'name': 'Flush',
            'pattern': PATTERN_FIVE_SAME_SUIT,
            'base_power': 5 * MAX_5
        },

        CombinationEnum.full_house: {
            'name': 'Full House',
            'pattern': PATTERN_THREE_SAME_RANK_TWO_SAME_RANK,
            'base_power': 6 * MAX_5
        },

        CombinationEnum.four_of_a_kind: {
            'name': 'Four of a kind',
            'pattern': PATTERN_FOUR_SAME_RANK,
            'base_power': 7 * MAX_5
        },

        CombinationEnum.straight_flush: {
            'name': 'Straight Flush',
            'pattern': PATTERN_FIVE_IN_ORDER_AND_SAME_SUIT,
            'base_power': 8 * MAX_5
        },

        CombinationEnum.royal_flush: {
            'name': 'Royal Flush',
            'pattern': PATTERN_TJQKA_AND_SAME_SUIT,
            'base_power': 9 * MAX_5
        }
    }


    def __init__(self, pocket_cards, table_cards):
        """
        :type pocket_cards: list
        :type table_cards: list
        """
        self.pocket_cards = pocket_cards
        self.table_cards = table_cards
        self.seven_cards = CombinationChecker.sort_desc(self.table_cards + self.pocket_cards)

        (self.combination, self.combination_cards, self.kicker_cards, self.power_cards, self.power) = self.process()


    def process(self):
        """
        :rtype: list ' [combination, power_cards, power]
        """
        for combination in CombinationEnum:
            power_cards = self.test_combination(combination)
            if power_cards:
                return power_cards


    def test_combination(self, combination):
        """
        :type combination: CombinationEnum
        :rtype: list
        """
        combination_rule = self.combinations_rules[combination]
        pattern = combination_rule['pattern']

        combination_cards = getattr(self, pattern)(self.seven_cards)
        if not combination_cards:
            return None

        powerful_addition_cards = self.powerful_addition(combination_cards)
        power_cards = combination_cards + powerful_addition_cards
        kicker_cards = self.diff(powerful_addition_cards, self.table_cards)

        power = combination_rule['base_power'] + CombinationChecker.power(power_cards, combination)

        return [combination, combination_cards, kicker_cards, power_cards, power]


    @staticmethod
    def diff(list1, list2):
        return CombinationChecker.sort_desc(list(set(list1) - set(list2)))


    @staticmethod
    def power(cards, combination = None):
        """
        :type cards: list of Card
        :type combination: CombinationEnum
        :rtype: int
        """
        # Straight A2345 => power(A) = 1 => 2345A
        if combination == CombinationEnum.straight:
            if cards[0].is_ace() and cards[1].rank == 5:
                cards = cards[1:] + [cards[0]]

        power = 0
        n = len(cards)
        for i, card in enumerate(cards):
            power += 14**(n - i - 1) * (card.rank - 1) # A = 14 or 13 in a 14-digits notation => rank - 1

        return power


    @classmethod
    def sort_desc(cls, cards, n = None):
        """
        :type cards: list of Card
        :type n: int
        :rtype: list of Card
        """
        if not n:
            n = len(cards)
        return sorted(cards, key=lambda c: c.rank, reverse=True)[:n]


    @classmethod
    def select_same_suit(self, cards, n):
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

        return same_suit_cards[:n]


    def powerful_addition(self, combination_cards):
        """
        :type combination_cards: list of Card
        :rtype: int
        """
        addition_cards_number = 5 - len(combination_cards)
        return CombinationChecker.diff(self.seven_cards, combination_cards)[:addition_cards_number]


    # ------ Patterns Checkers

    def high_rank(self, seven_cards):
        return [seven_cards[0]]


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

        remaining_cards = CombinationChecker.diff(seven_cards, pair)
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

        remaining_cards = CombinationChecker.diff(seven_cards, three)
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
        # ace with rank 1
        if seven_cards[0].is_ace():
            seven_cards.append(Card(1, seven_cards[0].suit))

        prev_rank = seven_cards[0].rank
        ordered_cards = [seven_cards[0]]

        for i in range(1, len(seven_cards)):
            card = seven_cards[i]
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
        same_suit_cards = CombinationChecker.select_same_suit(seven_cards, 5)
        return CombinationChecker.select_same_suit(seven_cards, 5) if len(same_suit_cards) > 4 else None


    def five_in_order_and_same_suit(self, seven_cards):
        same_suit_cards = CombinationChecker.select_same_suit(seven_cards, 7)
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
