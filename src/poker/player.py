from poker.account import Account
from poker.poker_object import PokerObject


class Player(PokerObject):
    STATE_REACTING = 1
    STATE_FOLDED = 2
    STATE_ALL_INED = 3
    STATE_LAST_PLAYER = 4

    ROLE_PLAYER = 'P'
    ROLE_DEALER = 'D'
    ROLE_SMALL_BLIND = 'SB'
    ROLE_BIG_BLIND = 'BB'

    ACTION_SMALL_BLIND = 'S'
    ACTION_BIG_BLIND = 'B'
    ACTION_FOLD = 'F'
    ACTION_CALL = 'C'
    ACTION_CHECK = 'K'
    ACTION_RAISE = 'R'
    ACTION_ALL_IN = 'A'

    def __init__(self, account, chips):
        """
        :type account: Account
        :type chips: int
        """
        self.role = self.ROLE_PLAYER
        self.state = self.STATE_REACTING
        self.account = account

        self.chips = chips
        self.pot_contribution = 0
        self.pot_distribution = 0
        self.won_amount = 0

        self._pocket_cards = []
        self.actions_map = {}

        self.evaluator = None

    # ------- Game

    def prepare(self):
        self.state = self.STATE_REACTING
        self.role = self.ROLE_PLAYER
        self.pot_contribution = 0
        self.pot_distribution = 0
        self.won_amount = 0
        self._pocket_cards = []
        self.actions_map = {}
        self.evaluator = None

    def _remember_charge(self, current_game_stage, action, amount):
        self.actions_map[current_game_stage] = {
            'action': action,
            'amount': amount
        }

    def track_charge(self, current_game_stage, action, amount):
        previous_charge = self.get_charge(current_game_stage)
        if not previous_charge:
            previous_charge = 0

        self._remember_charge(current_game_stage, action, amount + previous_charge)
        return amount

    def get_charge(self, current_game_stage):
        if current_game_stage not in self.actions_map:
            return None

        return self.actions_map[current_game_stage]['amount']

    def action_required(self, current_game_stage, current_game_bet):
        return (self.get_charge(current_game_stage) != current_game_bet or
                self.actions_map[current_game_stage]['action'] in [self.ACTION_SMALL_BLIND, self.ACTION_BIG_BLIND])

    # ------- Cards

    @property
    def pocket_cards(self):
        return self._pocket_cards

    @pocket_cards.setter
    def pocket_cards(self, cards):
        """
        :type cards: list of Card
        :return:
        """
        self._pocket_cards = cards

    @property
    def cards(self):
        return self._pocket_cards

    # ------- Chips

    def increase_chips(self, amount):
        if amount < 0:
            raise ValueError('Positive amount expected')
        self.chips += amount

    def decrease_chips(self, amount):
        if amount < 0:
            raise ValueError('Positive amount expected')
        self.chips -= amount

    # ------- Game

    def charge(self, current_game_stage, action, amount):
        amount = min(amount, self.chips)
        if amount >= self.chips:
            self.state = self.STATE_ALL_INED
            action = self.ACTION_ALL_IN
            print('ALL IN')

        self.decrease_chips(amount)
        self.pot_contribution += amount

        return self.track_charge(current_game_stage, action, amount)

    def is_reacting(self):
        return self.state == Player.STATE_REACTING

    def is_folded(self):
        return self.state == Player.STATE_FOLDED

    def is_all_ined(self):
        return self.state == Player.STATE_ALL_INED

    # ------- Interaction

    def _ask(self, possible_actions, call_amount, min_raise_amount):
        # impossible case, but lets keep it here while debugging
        if not self.STATE_REACTING:
            return

        print("Player {} #{}. Balance ${}: ".format(self.role, self.account.name, self.chips))
        print("Your cards {}".format(self.pocket_cards))
        print("Calling ${}".format(call_amount))

        action = None
        while action not in possible_actions:
            action = input("Please enter one of these actions: {}\n".format(", ".join(possible_actions)))

        if action == 'F':
            return self.do_fold()

        if action == 'A':
            return self.do_all_in()

        if action == 'R':
            return self.do_raise(call_amount, min_raise_amount)

        if action == 'C':
            return self.do_call(call_amount)

        if action == 'K':
            return self.do_check()

    # -------

    def request_action(self, current_game_stage, current_game_bet, current_game_raise, reacting_players_count):
        # print(self.actions_map)
        possible_actions = [
            self.ACTION_FOLD,
            self.ACTION_ALL_IN
        ]

        previous_bet = self.get_charge(current_game_stage)
        if previous_bet is None:
            previous_bet = 0

        call_amount = min(self.chips, current_game_bet - previous_bet)

        if call_amount == 0:
            # last player is playing and there's no need to raise or call => no need to ask questions
            if reacting_players_count == 1:
                self.state = self.STATE_LAST_PLAYER
                return 0

            possible_actions.append(self.ACTION_CHECK)
        elif self.chips > call_amount:
            possible_actions.append(self.ACTION_CALL)

        if self.chips - call_amount >= current_game_raise:
            possible_actions.append(self.ACTION_RAISE)

        action, amount = self._ask(possible_actions, call_amount, current_game_raise)

        return self.charge(current_game_stage, action, amount)

    # ------- Reactors

    def do_fold(self):
        print('FOLD')
        self.state = self.STATE_FOLDED
        return self.ACTION_FOLD, 0

    def do_all_in(self):
        print('ALL IN')
        self.state = self.STATE_ALL_INED
        return self.ACTION_ALL_IN, self.chips

    def do_raise(self, call_amount, min_raise_amount):
        print('RAISE')
        amount = -1
        while amount < min_raise_amount or amount > self.chips:
            amount = int(input(
                "How much? (Min: ${}) on top of another ${}, so you will be betting ${} or more: ".format(
                    min_raise_amount, call_amount, min_raise_amount + call_amount)))

        return self.ACTION_RAISE, call_amount + amount

    def do_call(self, call_amount):
        print('CALL')
        return self.ACTION_CALL, call_amount

    def do_check(self):
        print('CHECK')
        return self.ACTION_CHECK, 0
