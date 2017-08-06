import random
from game import Game

class ExpectedValuePlayerOne():
    def __init__(self):
        self.betting_probabilities_ = dict()
        self.check_calling_probabilities_ = dict()
        self.times_with_card_ = dict()
        self.times_against_bet_ = dict()

        self.times_opponent_called_ = dict()
        self.times_opponent_folded_ = dict()
        self.times_opponent_bet_ = dict()
        self.times_opponent_checked_ = dict()

        # initialize data tracking
        for card in Game.get_all_cards():
            self.betting_probabilities_[card] = 0.5
            self.check_calling_probabilities_[card] = 0.5
            self.times_with_card_[card] = 0
            self.times_against_bet_[card] = 0

            self.times_opponent_called_[card] = 0
            self.times_opponent_folded_[card] = 0
            self.times_opponent_bet_[card] = 0
            self.times_opponent_checked_[card] = 0

    def get_action(self, card):
        if random.random() < self.betting_probabilities_[card]:
            return Game.BET

        else:
            return Game.CHECK

    def get_action_against_bet(self, card):
        if random.random() < self.check_calling_probabilities_[card]:
            return Game.CALL

        else:
            return Game.FOLD


    def regret(self, card, action, opponent_card, opponent_action):
        # we bet
        if opponent_action == Game.CALL or opponent_action == Game.FOLD:
            n = self.times_with_card_[card]

            if opponent_action == Game.CALL:
                self.times_opponent_called_[opponent_card] += 1
            else:
                self.times_opponent_folded_[opponent_card] += 1

            expected_value_check = self.get_expected_value_check(card)
            expected_value_bet = self.get_expected_value_bet(card)

            if expected_value_bet >= expected_value_check:
                self.increment_betting_probability(card)
            else:
                self.decrement_betting_probability(card)

            print "PLAYER1: card: %s bet: %f check: %f" % (card, expected_value_bet, expected_value_check)

            self.times_with_card_[card] += 1
        # we checked
        else:
            # they checked back
            if opponent_action == Game.CHECK:
                self.times_opponent_checked_[opponent_card] += 1

                expected_value_check = self.get_expected_value_check(card)
                expected_value_bet = self.get_expected_value_bet(card)

                if expected_value_bet >= expected_value_check:
                    self.increment_betting_probability(card)
                else:
                    self.decrement_betting_probability(card)

                print "PLAYER1: card: %s bet: %f check: %f" % (card, expected_value_bet, expected_value_check)

                self.times_with_card_[card] += 1

            # they bet against us
            else:
                n = self.times_against_bet_[card]

                self.times_opponent_bet_[opponent_card] += 1

                expected_value_check_call = self.get_expected_value_check_call(card)
                expected_value_check_fold = self.get_expected_value_check_fold(card)
                expected_value_bet = self.get_expected_value_bet(card)
                expected_value_check = self.get_expected_value_check(card)

                if expected_value_bet >= expected_value_check:
                    self.increment_betting_probability(card)
                else:
                    self.decrement_betting_probability(card)

                if expected_value_check_call >= expected_value_check_fold:
                    self.increment_check_calling_probability(card)
                else:
                    self.decrement_check_calling_probability(card)

                print "PLAYER1: card: %s bet: %f check: %f call: %f vs fold: %f" % (card, expected_value_bet,
                            expected_value_check, expected_value_check_call, expected_value_check_fold)

                self.times_against_bet_[card] += 1

##########################################################
    def get_expected_value_bet(self, card):
        ev = 0
        num_times = 0
        for opponent_card in Game.get_all_cards():
            if card == opponent_card:
                continue

            times_fold = self.times_opponent_folded_[opponent_card]
            times_call = self.times_opponent_called_[opponent_card]

            ev += 2.0 * times_fold

            if card > opponent_card:
                ev += 3.0 * times_call
            else:
                ev -= 1.0 * times_call

            num_times += times_fold + times_call

        if num_times == 0:
            return 2

        return float(ev) / num_times

    def get_expected_value_check(self, card):
        times_opponent_bet = 0
        times_opponent_check_back = 0
        times_we_win_against_check_back = 0

        for opponent_card in Game.get_all_cards():
            if card == opponent_card:
                continue
            n_bet = self.times_opponent_bet_[opponent_card]
            n_check = self.times_opponent_checked_[opponent_card]

            times_opponent_check_back += n_check
            times_opponent_bet += n_bet

            if card > opponent_card:
                times_we_win_against_check_back += n_check

        total = times_opponent_bet + times_opponent_check_back

        if total == 0:
            return 1

        ev = 2.0 * times_we_win_against_check_back / total
        ev += max(self.get_expected_value_check_call(card), self.get_expected_value_check_fold(card)) * times_opponent_bet / total

        return ev


    def get_expected_value_check_call(self, card):
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

    def get_expected_value_check_fold(self, card):
        return 0

##########################################################
    def increment_betting_probability(self, card):
        n = self.times_with_card_[card]
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
        n = self.times_with_card_[card]
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
    def increment_check_calling_probability(self, card):
        n = self.times_against_bet_[card]
        p = self.check_calling_probabilities_[card]

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


        self.check_calling_probabilities_[card] = p

    def decrement_check_calling_probability(self, card):
        n = self.times_against_bet_[card]
        p = self.check_calling_probabilities_[card]

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

        self.check_calling_probabilities_[card] = p

##########################################################
