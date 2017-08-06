from game import Game
from player_one import ExpectedValuePlayerOne
from player_two import ExpectedValuePlayerTwo
from perfect_player_one import PerfectPlayerOne

EV_p1 = ExpectedValuePlayerOne()
EV_p2 = ExpectedValuePlayerTwo()
perfect_player_one = PerfectPlayerOne()
one_card_poker_game = Game(EV_p1, EV_p2)

epochs = 10
rounds_per_epoch = 10000

for epoch in range(epochs):
    print "Epoch: %i" % (epoch + 1)
    for i in range(rounds_per_epoch):
        one_card_poker_game.play_round()

print "Player One EV/Hand: %f" % (float(one_card_poker_game.player_one_winnings_)/one_card_poker_game.rounds_played_)
print "\nPlayer One Strategy (betting): "
print EV_p1.betting_probabilities_
print "\nPlayer One Strategy (check-calling): "
print EV_p1.check_calling_probabilities_

# print "\nPlayer One Strategy (betting): "
# print perfect_player_one.betting_probabilities_
# print "\nPlayer One Strategy (check-calling): "
# print perfect_player_one.check_calling_probabilities_

print "\nPlayer Two Strategy (betting): "
print EV_p2.betting_probabilities_
print "\nPlayer Two Strategy (calling): "
print EV_p2.calling_probabilities_
