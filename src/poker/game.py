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
        print(self.current_stage.name.upper())
        getattr(self, 'stage_' + self.current_stage.name)()

    def play_round(self):
        print(self.table.cards)

        while True:
            player = self.table.next_reacting_player()
            if not player or not player.action_required(self.current_stage, self.current_bet):
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

        amount = player.request_action(self.current_stage, self.current_bet, self.current_raise,
                                       self.table.reacting_players_count)

        if amount > self.current_bet:
            new_raise = amount - self.current_bet

            # If the previous all-in raise amount was less than the minimum raise,
            # then the minimum raise is equal to the previous minimum raise.
            # The minimum legal raise is equal to the previous raise amount.
            if new_raise > self.current_raise:
                self.current_raise = new_raise

            self.current_bet = amount

        self.pot += amount

    # ------- Chips

    def charge_for_blinds(self):
        small_blind_amount = self.table.small_blind_player.charge(self.current_stage,
                                                                  Player.ACTION_SMALL_BLIND,
                                                                  self.SMALL_BLIND_AMOUNT)

        big_blind_amount = self.table.big_blind_player.charge(self.current_stage,
                                                              Player.ACTION_BIG_BLIND,
                                                              self.BIG_BLIND_AMOUNT)

        self.pot = small_blind_amount + big_blind_amount

    @staticmethod
    def __use_pot_contribution(players, contribution):
        result = 0
        for p in players:
            amount = min(contribution, p.pot_contribution)
            p.pot_contribution -= amount
            result += amount
        return result

    def distribute_pot(self, winners):
        # make winners groups by power of the hands
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

        # split in a group
        for group in groups:
            if self.pot == 0:
                break
            group_players_count = len(group)
            group = sorted(group, key=lambda x: x.pot_contribution)
            for i, p in enumerate(group):
                side_pot = Game.__use_pot_contribution(winners, p.pot_contribution)
                for w in group[i:group_players_count + 1]:
                    reward_part = int(side_pot / (group_players_count - i))
                    w.reward += reward_part
                    self.pot -= reward_part

        for w in winners:
            w.increase_chips(w.reward)

    # ------- Stages

    def stage_welcome(self):
        print("Lets begin poker game #{}\n".format(self.id_))
        self.assign_pocket_cards()

    def stage_preflop(self):
        self.charge_for_blinds()
        self.current_bet = self.BIG_BLIND_AMOUNT
        self.current_raise = self.BIG_BLIND_AMOUNT
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
            p.evaluator = Evaluator(p.pocket_cards, self.table.cards)

        winners = sorted([x for x in self.table.players if x.evaluator], key=lambda x: x.evaluator.power, reverse=True)

        print("=================================================================")
        print(self.table.cards)

        self.distribute_pot(winners)

        for winner in winners:
            e = winner.evaluator
            print(
                '{}, won ${}, balance ${}.  {}: {} => {}, {}'.format(winner.account.name, winner.reward,
                                                                     winner.chips, e.name,
                                                                     winner.pocket_cards, e.combination_cards,
                                                                     e.power))
