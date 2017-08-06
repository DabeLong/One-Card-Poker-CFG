# One-Card-Poker-CFG

Poker has always been a big interest to me because of the complexity of the game - a game of imperfect information that demands discipline, picking good spots, smart bet-sizing, and exploiting opponent tendencies. Recent breakthroughs in Poker AI such as DeepStack and Libratus and their defeat of the best Heads Up No Limit Hold'Em piqued my interest in how it was possible for computers to solve such a difficult game. After researching and reading up on articles, I found out that the key algorithm behind find the game theory optimal solution is to use counterfactual regret minimization and learning through massive amounts of self-play.

I wanted to try implementing this algorithm, but starting with NLHE would not be practical as the game has way too many search states because of the numerous amounts of bet sizings a player can have. So for practice, I decided to start by implementing a much simpler game called One Card Poker. In One Card Poker, there are two players and the deck has 13 cards. Both players are dealt one card, hidden from the other player, and the highest card wins. Each player antes in 1 bet, and the pot can only be raised by 1 more bet.

This game kind of simulates a river situation in NLHE, where the first player to act can either bet or check with the intention of check/calling or check/folding. Player two can call or fold to the first player's bet, and can bet or check back against the first player's check. However, due to the game's limitations, note that player one is unable to check-raise. Additionally, players can only bet 1 unit into a pot of 2 units, effectively giving the other player 3-1 on a call, which seems important to bluffing ratios and finding an optimal solution.

I read G. Gordon's website that expanded on the strategy behind the game, and unsurprisingly, there is a GTO solution to the game. To play as optimally as possible, the first player must learn to slow-play strong hands (i.e. A, K, or Q) and not just always bet them, but check call. Additionally, he must be able to throw in bluffs and also check-call with mediocre hands (like a 5 or 6) to bluff-catch against the second player. The most interesting thing, though, is that when checked to, the optimal strategy for Player Two is to bet a polarized range (betting only strong hands and bluffs). He only bets 9-A and 2-3 with 100%, which is precisely a 3-1 ratio between value hands and bluffs! This is the 3-1 pot odds ratio from before. This forces his opponent to be indifferent between calling and folding.

So this game absolutely shares key concepts with NLHE, and I wanted to use CFR-Minimization to discover this optimum solution from scratch. I initially tried to make a bot that would adjust its decision frequencies by looking at the expected value of differing moves, and it did come up with a solution that worked fairly well. However, it wasn't even close to the optimal solution. After toying around and reading more on CFR, I implemented a solution that used the algorithm to converge upon the optimal solution for both players.

### To run:
*'python cfr_test.py'* will run 1,000,000 iterations to find the optimal solution using CFR.

### G. Gordon's proposed GTO solution
![Alt text](/GTO_solution.png?raw=true "Test Results")

### Results:
![Alt text](/CFR_test_results.png?raw=true "Test Results")

As you can see, the CFR solution is relatively close to the GTO solution. Player two always bets 2,3 and 9-A and doesn't bet any other hands when checked to. Player one's check-call range is almost identical for both charts. Additionally, player one loses on average 0.0637 bets per hand, which is very similar to G. Gordon's stated 0.064 average loss!

However, there are some deviations:
> Player one bluffs with a 2, 3, and 4 with different ratios compared to GTO solution, but the bluffing ratio is relatively similar
> Player one value bets Q, K, and A significantly more
> Player two never bluff catches with a 4 and rarely does it with a 7, but compensates by bluff-catching more with a 5 or a 6

### Links/References:
http://www.cs.cmu.edu/~ggordon/poker/
http://modelai.gettysburg.edu/2013/cfr/cfr.pdf
