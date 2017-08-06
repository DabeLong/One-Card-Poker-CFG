import random

class Game:
    NUM_CARDS = 13
    CHECK = 'check'
    BET = 'bet'
    CALL = 'call'
    FOLD = 'fold'

    def __init__(self, player_one, player_two):
        self.player_one_ = player_one
        self.player_two_ = player_two
        self.player_one_winnings_ = 0
        self.rounds_played_ = 0



    @staticmethod
    def get_all_cards():
        return set(range(Game.NUM_CARDS))

    @staticmethod
    def deal_two_random_cards():
        sample = random.sample(Game.get_all_cards(), 2)
        return sample[0], sample[1]

    def play_round(self):
        player_one_card, player_two_card = self.deal_two_random_cards()

        player_one_action = self.player_one_.get_action(player_one_card)

        player_two_action = self.player_two_.get_action(player_two_card, player_one_action)

        regret_done = False

        # Both check
        if (player_one_action == Game.CHECK and player_two_action == Game.CHECK):
            # player one wins
            if player_one_card > player_two_card:
                self.player_one_winnings_ += 1
            else:
                self.player_one_winnings_ -= 1

        # Player one bets and player two folds
        elif (player_one_action == Game.BET and player_two_action == Game.FOLD):
            self.player_one_winnings_ += 1

        # Player one bets and player two calls
        elif (player_one_action == Game.BET and player_two_action == Game.CALL):
            # player one wins
            if player_one_card > player_two_card:
                self.player_one_winnings_ += 2

            else:
                self.player_one_winnings_ -= 2

        # Otherwise, player one checked and player two bet... So action back on player one
        else:
            assert player_one_action == Game.CHECK
            assert player_two_action == Game.BET

            player_one_second_action = self.player_one_.get_action_against_bet(player_one_card)

            # player one folds
            if player_one_second_action == Game.FOLD:
                self.player_one_winnings_ -= 1
            else:
                if player_one_card > player_two_card:
                    self.player_one_winnings_ += 2
                else:
                    self.player_one_winnings_ -= 2

            self.player_one_.regret(player_one_card, player_one_second_action, player_two_card, player_two_action)
            self.player_two_.regret(player_two_card, player_two_action, player_one_card, player_one_second_action)
            regret_done = True

        if not regret_done:
            self.player_one_.regret(player_one_card, player_one_action, player_two_card, player_two_action)
            self.player_two_.regret(player_two_card, player_two_action, player_one_card, player_one_action)

        self.rounds_played_ += 1
