from game import Game
import random

class ExpectedValuePlayerTwo():
    def __init__(self):
        self.calling_probabilities_ = dict()
        self.betting_probabilities_ = dict()
        self.times_with_card_against_check_ = dict()
        self.times_with_card_against_bet_ = dict()

        # keep track of opponent tendencies
        self.times_opponent_checked_ = dict()
        self.times_opponent_check_called_ = dict()
        self.times_opponent_check_folded_ = dict()
        self.times_opponent_bet_ = dict()

        # initialize data tracking tools
        for card in Game.get_all_cards():
            self.betting_probabilities_[card] = 0.5
            self.calling_probabilities_[card] = 0.5
            self.times_with_card_against_check_[card] = 0
            self.times_with_card_against_bet_[card] = 0

            self.times_opponent_checked_[card] = 0
            self.times_opponent_check_called_[card] = 0
            self.times_opponent_check_folded_[card] = 0
            self.times_opponent_bet_[card] = 0


    def get_action(self, card, opponent_action):
        if opponent_action == Game.CHECK:
            if random.random() < self.betting_probabilities_[card]:
                return Game.BET
            else:
                return Game.CHECK

        else:
            if random.random() < self.calling_probabilities_[card]:
                return Game.CALL
            else:
                return Game.FOLD

    def regret(self, card, action, opponent_card, opponent_action):
        # we checked back
        if action == Game.CHECK:
            self.times_opponent_checked_[opponent_card] += 1

            expected_value_check = self.get_expected_value_check(card)
            expected_value_bet = self.get_expected_value_bet(card)

            if expected_value_bet > expected_value_check:
                self.increment_betting_probability(card)
            else:
                self.decrement_betting_probability(card)

            # print "   PLAYER2: card: %s bet: %f vs check: %f" % (card, expected_value_bet, expected_value_check)

            self.times_with_card_against_check_[card] += 1

        # we bet against opponent's check
        elif action == Game.BET:
            if opponent_action == Game.CALL:
                self.times_opponent_check_called_[opponent_card] += 1
            else:
                self.times_opponent_check_folded_[opponent_card] += 1

            expected_value_check = self.get_expected_value_check(card)
            expected_value_bet = self.get_expected_value_bet(card)

            if expected_value_bet > expected_value_check:
                self.increment_betting_probability(card)
            else:
                self.decrement_betting_probability(card)

            # print "   PLAYER2: card: %s bet: %f vs check: %f" % (card, expected_value_bet, expected_value_check)

            self.times_with_card_against_check_[card] += 1

        # opponent bet
        else:
            self.times_opponent_bet_[opponent_card] += 1

            expected_value_call = self.get_expected_value_call(card)
            expected_value_fold = self.get_expected_value_fold(card)

            if expected_value_call > expected_value_fold:
                self.increment_calling_probability(card)
            else:
                self.decrement_calling_probability(card)

            # print "   PLAYER2: card: %s call: %f vs fold: %f" % (card, expected_value_call, expected_value_fold)

            self.times_with_card_against_bet_[card] += 1

##########################################################
    def increment_betting_probability(self, card):
        n = self.times_with_card_against_check_[card]
        p = self.betting_probabilities_[card]

        if p >= 1.0:
            return

        if n > 500:
            p += 0.005
        elif n > 100:
            p += 0.01
        elif n > 25:
            p += 0.03
        else:
            p += 0.05

        if p > 1:
            p = 1

        self.betting_probabilities_[card] = p

    def decrement_betting_probability(self, card):
        n = self.times_with_card_against_check_[card]
        p = self.betting_probabilities_[card]

        if p <= 0:
            return

        if n > 500:
            p -= 0.005
        elif n > 100:
            p -= 0.01
        elif n > 25:
            p -= 0.03
        else:
            p -= 0.05

        if p < 0:
            p = 0

        self.betting_probabilities_[card] = p

##########################################################
    def increment_calling_probability(self, card):
        n = self.times_with_card_against_bet_[card]
        p = self.calling_probabilities_[card]

        if p >= 1.0:
            return

        if n > 500:
            p += 0.005
        elif n > 100:
            p += 0.01
        elif n > 25:
            p += 0.03
        else:
            p += 0.05

        if p > 1:
            p = 1


        self.calling_probabilities_[card] = p

    def decrement_calling_probability(self, card):
        n = self.times_with_card_against_bet_[card]
        p = self.calling_probabilities_[card]

        if p <= 0:
            return

        if n > 500:
            p -= 0.005
        elif n > 100:
            p -= 0.01
        elif n > 25:
            p -= 0.03
        else:
            p -= 0.05

        if p < 0:
            p = 0

        self.calling_probabilities_[card] = p

##########################################################
    def get_expected_value_check(self, card):
        ev = 0
        num_times = 0
        for opponent_card in Game.get_all_cards():
            if card == opponent_card:
                continue

            times_checked = self.times_opponent_checked_[opponent_card]
            if card > opponent_card:
                ev += 2.0 * times_checked

            num_times += times_checked

        if num_times == 0:
            return 0

        return float(ev) / num_times

    def get_expected_value_bet(self, card):
        ev = 0
        num_times = 0
        for opponent_card in Game.get_all_cards():
            if card == opponent_card:
                continue

            times_fold = self.times_opponent_check_folded_[opponent_card]
            times_call = self.times_opponent_check_called_[opponent_card]

            ev += 2.0 * times_fold

            if card > opponent_card:
                ev += 3.0 * times_call
            else:
                ev -= 1.0 * times_call

            num_times += times_fold + times_call

        if num_times == 0:
            return 1

        return float(ev) / num_times

    def get_expected_value_call(self, card):
        ev = 0
        num_times = 0
        for opponent_card in Game.get_all_cards():
            if card == opponent_card:
                continue

            times_bet = self.times_opponent_bet_[opponent_card]
            if card > opponent_card:
                ev += 3.0 * times_bet
            else:
                ev -= 1.0 * times_bet

            num_times += times_bet

        if num_times == 0:
            return 1

        return float(ev) / num_times

    def get_expected_value_fold(self, card):
        return 0
