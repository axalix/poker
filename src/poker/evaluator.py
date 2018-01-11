from collections import Counter
from poker.card import Card
from poker.enums.combination_enum import CombinationEnum
from poker.poker_object import PokerObject


class Evaluator(PokerObject):
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
    MAX_5 = 537824 # AAAAK: 13 * 14^4 + 13 * 14^3 + 13 * 14^2 + 13 * 14^1 + 13 * 14^0 + 1

    # J - 11
    # Q - 12
    # K - 13
    # A - 14
    evaluator = {
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
        self.seven_cards = Card.sort_desc(self.table_cards + self.pocket_cards)
        self.process()


    def process(self):
        """
        :rtype: list ' [combination, power_cards, power]
        """
        for combination in CombinationEnum:
            power_cards = self.evaluate(combination)
            if power_cards:
                (self.combination, self.combination_cards, self.kicker_cards, self.power_cards, self.power) = power_cards
                return


    def evaluate(self, combination):
        """
        :type combination: CombinationEnum
        :rtype: list
        """
        combination_rule = self.evaluator[combination]
        pattern = combination_rule['pattern']

        combination_cards = getattr(self, pattern)(self.seven_cards)
        if not combination_cards:
            return None

        powerful_addition_cards = self.powerful_addition(combination_cards)
        power_cards = combination_cards + powerful_addition_cards
        kicker_cards = Card.diff(powerful_addition_cards, self.table_cards)
        power = combination_rule['base_power'] + Card.power(power_cards)

        return [combination, combination_cards, kicker_cards, power_cards, power]


    def powerful_addition(self, combination_cards):
        """
        :type combination_cards: list of Card
        :rtype: int
        """
        addition_cards_number = 5 - len(combination_cards)
        return Card.diff(self.seven_cards, combination_cards)[:addition_cards_number]

    @property
    def name(self):
        return self.evaluator[self.combination]['name']


    # ------ Patterns and Helpers

    @classmethod
    def select_five_or_more_suited_cards(cls, cards):
        """
        :param cards: list of Card
        :rtype: list of Card
        """
        d = {}
        for card in cards:
            if card.suit not in d:
                d[card.suit] = []
            d[card.suit].append(card)

        max_ = 0
        same_suit_cards = []
        for suit, suited_cards in d.items():
            suited_cards_count = len(suited_cards)
            if suited_cards_count > max_:
                max_ = suited_cards_count
                same_suit_cards = suited_cards

        return same_suit_cards if len(same_suit_cards) > 4 else None


    @classmethod
    def high_rank(cls, seven_cards):
        return [seven_cards[0]]


    @classmethod
    def same_rank(cls, seven_cards, n):
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


    @classmethod
    def two_same_rank(cls, seven_cards):
        """
        :param seven_cards: list of Card
        :rtype: list of Card
        """
        return cls.same_rank(seven_cards, 2)


    @classmethod
    def two_same_rank_pairs(cls, seven_cards):
        """
        :param seven_cards: list of Card
        :rtype: list of Card
        """
        pair = cls.two_same_rank(seven_cards)
        if not pair:
            return None

        remaining_cards = Card.diff(seven_cards, pair)
        second_pair = cls.two_same_rank(remaining_cards)
        if not second_pair:
            return None

        return pair + second_pair


    @classmethod
    def three_same_rank(cls, seven_cards):
        """
        :param seven_cards: list of Card
        :rtype: list of Card
        """
        return cls.same_rank(seven_cards, 3)


    @classmethod
    def three_same_rank_two_same_rank(cls, seven_cards):
        """
        :param seven_cards: list of Card
        :rtype: list of Card
        """
        three = cls.three_same_rank(seven_cards)
        if not three:
            return None

        remaining_cards = Card.diff(seven_cards, three)
        second_pair = cls.two_same_rank(remaining_cards)
        if not second_pair:
            return None

        return three + second_pair


    @classmethod
    def four_same_rank(cls, seven_cards):
        """
        :param seven_cards: list of Card
        :rtype: list of Card
        """
        return cls.same_rank(seven_cards, 4)


    @classmethod
    def five_in_order(cls, seven_cards):
        """
        :param seven_cards: list of Card
        :rtype: list of Card
        """
        # Straight A2345 => power(A) = 1 => 2345A
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
                if len(ordered_cards) == 5:
                    return ordered_cards
            else:
                ordered_cards = [card]
            prev_rank = card.rank

        return None

    @classmethod
    def five_same_suit(cls, seven_cards):
        five_or_more_suited_cards = Evaluator.select_five_or_more_suited_cards(seven_cards)
        if not five_or_more_suited_cards:
            return None

        return five_or_more_suited_cards[:5]


    @classmethod
    def five_in_order_and_same_suit(cls, seven_cards):
        five_or_more_suited_cards = Evaluator.select_five_or_more_suited_cards(seven_cards)
        if not five_or_more_suited_cards:
            return None

        return cls.five_in_order(five_or_more_suited_cards)


    @classmethod
    def tjqka_and_same_suit(cls, seven_cards):
        """
        :param seven_cards: list of Card
        :rtype: list of Card
        """
        same_suit_cards = cls.five_same_suit(seven_cards)
        if not same_suit_cards:
            return None
        return same_suit_cards if list(map(lambda x: x.rank, same_suit_cards)) == list(range(14, 9, -1)) else None
