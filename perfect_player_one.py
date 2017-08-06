import random
from game import Game

class PerfectPlayerOne():
    def __init__(self):
        self.betting_probabilities_ = [0.454, 0.443, 0.254, 0.000,
        0.000,0.000, 0.000, 0.422, 0.549, 0.598, 0.615, 0.628, 0.641]

        self.check_calling_probabilities_ = [0.000, 0.000, 0.169, 0.269, 0.429,
        0.610, 0.760, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000]

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
        pass
