from poker.account import Account
from poker.poker_object import PokerObject


class Player(PokerObject):
    STATE_REACTING = 1
    STATE_FOLDED = 2
    STATE_ALL_INED = 3

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
        self._pocket_cards = []
        self.actions_map = {}

    # ------- Game

    def prepare(self):
        self.state = self.STATE_REACTING
        self.role = self.ROLE_PLAYER
        self.pot_contribution = 0
        self._pocket_cards = []
        self.actions_map = {}

    def _remember_charge(self, current_game_stage, action, amount):
        self.actions_map[current_game_stage] = {
            'action': action,
            'amount': amount
        }

    def track_charge(self, current_game_stage, action, amount):
        previous_charge = self.get_charge(current_game_stage)
        if not previous_charge:
            previous_charge = 0
        new_amount = amount + previous_charge

        self._remember_charge(current_game_stage, action, new_amount)
        return new_amount

    def get_charge(self, current_game_stage):
        if current_game_stage not in self.actions_map:
            return None

        return self.actions_map[current_game_stage]['amount']


    def action_required(self, current_game_stage, current_game_bet):
        return self.state == self.STATE_REACTING and (
            self.get_charge(current_game_stage) != current_game_bet or
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

    # ------- Interface

    def _ask(self, possible_actions, current_game_bet, min_call):
        # impossible case, but lets keep it here while debugging
        if not self.STATE_REACTING:
            return

        print("Player {} #{}. Balance ${}: ".format(self.role, self.account.name, self.chips))
        print("Your cards {}".format(self.pocket_cards))
        print("Bet ${} or more".format(min_call))

        action = None
        while action not in possible_actions:
            action = input("Please enter one of these actions: {}\n".format(", ".join(possible_actions)))

        if action == 'F':
            return self.do_fold()

        if action == 'A':
            return self.do_all_in()

        if action == 'R':
            return self.do_raise(min_call)

        if action == 'C':
            return self.do_call(min_call)

        if action == 'K':
            return self.do_check(current_game_bet)

    # -------

    def request_action(self, current_game_stage, current_game_bet):
        print(self.actions_map)
        possible_actions = [
            self.ACTION_FOLD,
            self.ACTION_ALL_IN
        ]

        previous_bet = self.get_charge(current_game_stage)
        if previous_bet is None:
            previous_bet = 0

        min_call = min(self.chips, current_game_bet - previous_bet)
        print("current_game_bet {}".format(current_game_bet))
        print("previous_bet {}".format(previous_bet))
        print("self.chips {}".format(self.chips))

        if self.chips > min_call:
            possible_actions.append(self.ACTION_RAISE)

            if min_call == 0:
                possible_actions.append(self.ACTION_CHECK)
            else:
                possible_actions.append(self.ACTION_CALL)

        action, amount = self._ask(possible_actions, current_game_bet, min_call)



        amount = self.charge(current_game_stage, action, amount)
        print(self.actions_map)

        return amount


    # ------- Reactors

    def do_fold(self):
        print('FOLD')
        self.state = self.STATE_FOLDED
        return self.ACTION_FOLD, 0

    def do_all_in(self):
        print('ALL IN')
        self.state = self.STATE_ALL_INED
        return self.ACTION_ALL_IN, self.chips

    def do_raise(self, min_call):
        print('RAISE')
        amount = -1
        while amount < min_call or amount > self.chips:
            amount = int(input("How much? (Min: {})".format(min_call)))

        return self.ACTION_RAISE, amount

    def do_call(self, min_call):
        print('CALL')
        return self.ACTION_CALL, min_call

    def do_check(self, current_game_bet):
        print('CHECK')
        return self.ACTION_CHECK, 0
