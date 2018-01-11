from functools import reduce
from poker.deck import Deck
from poker.enums.game_stage_enum import GameStageEnum
from poker.evaluator import Evaluator
from poker.game_table import GameTable
from poker.player import Player
from poker.poker_object import PokerObject


class Game(PokerObject):
    SMALL_BLIND_AMOUNT = 2
    BIG_BLIND_AMOUNT = 4

    current_bet = 0

    def __init__(self, id_, table):
        """
        :type id_: int
        :type table: GameTable
        """
        self.current_stage = None
        self.id_ = id_
        self.table = table

        self.deck = Deck()

        self.pot = 0
        self.current_bet = 0
        self.current_raise = 0

        self.game_states_iterator = iter(GameStageEnum)

    # ------- Game Process

    def play(self):
        # main loop: preflop -> flop -> turn -> river -> winners
        for self.current_stage in self.game_states_iterator:
            self.play_stage()

        print("=================================================================")

    def play_stage(self):
        print(self.current_stage.name)
        getattr(self, 'stage_' + self.current_stage.name)()

    def play_round(self):
        print(self.table.cards)

        while True:
            p = self.table.next_reacting_player()
            if not p or not p.action_required(self.current_stage, self.current_bet):
                break

            print("Table cards: " + str(self.table.cards))
            self.request_player_action()
            print("\n- - - - - - - - -\n")

        self.current_bet = 0
        self.current_raise = self.BIG_BLIND_AMOUNT
        self.table.make_dealer_current_player()

    # ------- Player

    def assign_pocket_cards(self):
        for player in self.table.players:
            player.pocket_cards = self.deck.get(2)

    def request_player_action(self):
        player = self.table.current_player()

        amount = player.request_action(self.current_stage, self.current_bet, self.current_raise)

        if amount > self.current_bet:
            new_raise = amount - self.current_bet

            # If the previous all-in raise amount was less than the minimum raise,
            # then the minimum raise is equal to the previous minimum raise.
            # The minimum legal raise is equal to the previous raise amount.
            if new_raise > self.current_raise:
                self.current_raise = new_raise

            self.current_bet = amount

        self.pot += amount

    # ------- Money


    def charge_for_blinds(self):

        small_blind_amount = self.table.small_blind_player.charge(self.current_stage,
                                                                  Player.ACTION_SMALL_BLIND,
                                                                  self.SMALL_BLIND_AMOUNT)

        big_blind_amount = self.table.big_blind_player.charge(self.current_stage,
                                                              Player.ACTION_BIG_BLIND,
                                                              self.BIG_BLIND_AMOUNT)

        self.pot = small_blind_amount + big_blind_amount
        self.current_bet = self.BIG_BLIND_AMOUNT
        self.current_raise = self.BIG_BLIND_AMOUNT

    def _use_pot_contribution(self, players, contribution):
        result = 0
        for w in players:
            amount = min(contribution, w.pot_distribution)
            w.pot_distribution -= amount
            result += amount
        return result

    def distribute_pot(self, winners):
        if len(winners) == 1:
            self.pot = 0
            winners[0].won_amount = self.pot
            return

        for winner in winners:
            winner.pot_distribution = winner.pot_contribution

        groups = [[winners[0]]]
        current_hand_power = winners[0].evaluator.power
        group_idx = 0

        for winner in winners[1:]:
            if current_hand_power == winner.evaluator.power:
                groups[group_idx].append(winner)
            else:
                current_hand_power = winner.evaluator.power
                group_idx += 1
                groups.append([winner])

        for group in groups:
            if self.pot == 0:
                break

                # split
            group = sorted(group, key=lambda x: x.pot_contribution, reverse=True)
            max_pot_contribution = reduce(lambda x , y: max(x, y), map(lambda x: x.pot_distribution, group))
            if max_pot_contribution == 0:
                continue

            group_amount = reduce(lambda x , y: x + y, map(lambda x: x.pot_contribution, group))
            if group_amount == 0:
                continue

            shared_amount = self._use_pot_contribution(winners, max_pot_contribution)

            for p in group:
                won_amount = int(shared_amount * p.pot_contribution / group_amount)
                p.won_amount = won_amount
                self.pot -= won_amount


        for w in winners:
            w.increase_chips(w.won_amount)

    # ------- Actions

    def stage_welcome(self):
        print("Lets begin poker game #{}".format(self.id_))

    def stage_preflop(self):
        self.charge_for_blinds()
        self.assign_pocket_cards()
        self.play_round()

    def stage_flop(self):
        self.table.flop = self.deck.get(3)
        self.play_round()

    def stage_turn(self):
        self.table.turn = self.deck.get(1)
        self.play_round()

    def stage_river(self):
        self.table.river = self.deck.get(1)
        self.play_round()

    def stage_winners(self):
        for p in self.table.players:
            if p.is_folded():
                continue
            p.evaluator = Evaluator(p.cards, self.table.cards)

        winners = sorted([x for x in self.table.players if x.evaluator], key=lambda x: x.evaluator.power, reverse=True)

        print("=================================================================")
        print(self.table.cards)

        self.distribute_pot(winners)

        for winner in winners:
            e = winner.evaluator
            print(
                '{}, ${}.  {}: {} => {}, {}'.format(winner.account.name, winner.won_amount, e.name,
                                                    winner.pocket_cards, e.combination_cards,
                                                    e.power))
