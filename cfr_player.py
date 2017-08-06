from game import Game

class CFRPlayer():
    def __init__(self):
        self.game_states_ = dict() # maps history to node

    def train(self, iterations):
        ''' Do ficticious self-play to find optimal strategy'''
        util = 0

        for i in range(iterations):
            player_one_card, player_two_card = Game.deal_two_random_cards()
            cards = [player_one_card, player_two_card]
            history = list()
            util += self.cfr(cards, history, 1, 1)

        return util/iterations

    def get_betting_frequencies(self):
        result = dict()
        result['p1_bet'] = dict()
        result['p1_check_call'] = dict()
        result['p2_call'] = dict()
        result['p2_bet'] = dict()

        for state, node in self.game_states_.items():
            history = state.split(" ")

            card = int(history[0])
            if len(history) == 1:
                result['p1_bet'][card] = node.strategy_[Game.BET]
            elif len(history) == 2:
                if history[1] == Game.CHECK:
                    result['p2_bet'][card] = node.strategy_[Game.BET]
                else:
                    result['p2_call'][card] = node.strategy_[Game.CALL]
            elif len(history) == 3:
                result['p1_check_call'][card] = node.strategy_[Game.CALL]

        return result

    # @cards - the cards the players have, with index 0 being the card that player one has
    # and index 1 being the card that player two has
    # @history - a list of moves used to reach this game state
    # @probability1 - the probability of reaching this game state for player 1
    # @probability2 - the probability of reaching this game state for player 2
    def cfr(self, cards, history, probability1, probability2):
        num_moves = len(history)
        player = num_moves % 2
        opponent = 1 - player
        player_card = cards[player]
        opponent_card = cards[opponent]
        probability_weight = probability1 if player == 0 else probability2

        # can only end if at least 2 moves
        if num_moves >= 2:
            # Opponent folded, return a utility of 1
            if history[-1] == Game.FOLD:
                return 1
            # Opponent called a bet, return a utility of 2 or -2 depending on who has the higher card
            if history[-1] == Game.CALL:
                if player_card > opponent_card:
                    return 2
                else:
                    return -2
            # Opponent checked when we checked before, return a utility of 1 or -1 depending on who has the higher card
            if history[-1] == Game.CHECK:
                if player_card > opponent_card:
                    return 1
                else:
                    return -1

        state = str(player_card)
        for action in history:
            state += " " + action

        if state in self.game_states_:
            node = self.game_states_[state] # Get our node if it already exists
            possible_actions = node.actions_
        else:
            # Create new Node with possible actions we can perform
            if len(history) == 0:
                possible_actions = [Game.CHECK, Game.BET]
            else:
                if history[-1] == Game.BET:
                    possible_actions = [Game.CALL, Game.FOLD]
                else:
                    possible_actions = [Game.CHECK, Game.BET]

            node = Node(possible_actions)
            self.game_states_[state] = node

        strategy = node.get_strategy(probability_weight)
        util = dict()
        node_util = 0
        # for each of our possible actions, computer the utility of taking it
        # thus, finding the utility of reaching this current state
        for action in possible_actions:
            next_history = list(history) # copy
            next_history.append(action)

            if player == 0:
                util[action] = -self.cfr(cards, next_history, probability1 * strategy[action], probability2)
            else:
                util[action] = -self.cfr(cards, next_history, probability1, probability2 * strategy[action])


            node_util += strategy[action] * util[action]

        # compute regret and update Game State for the node based on utility of all actions
        for action in possible_actions:
            regret = util[action] - node_util
            if player == 0:
                node.regret_sum_[action] += regret * probability2
            else:
                node.regret_sum_[action] += regret * probability1

        return node_util

class Node():
    def __init__(self, actions):
        self.actions_ = actions
        self.regret_sum_ = dict()
        self.strategy_ = dict()
        self.strategy_sum_ = dict()

        for action in actions:
            self.regret_sum_[action] = 0.0
            self.strategy_[action] = 0.0
            self.strategy_sum_[action] = 0.0

    def get_strategy(self, realization_weight):
        normalizing_sum = 0

        for action in self.actions_:
            self.strategy_[action] = self.regret_sum_[action] if self.regret_sum_[action] > 0 else 0
            normalizing_sum += self.strategy_[action]

        for action in self.actions_:
            if normalizing_sum > 0:
                self.strategy_[action] /= normalizing_sum
            else:
                self.strategy_[action] = 1.0 / len(self.actions_)

            self.strategy_sum_[action] += realization_weight * self.strategy_[action]

        return self.strategy_

    def get_average_strategy(self):
        average_strategy = dict
        normalizing_sum = 0

        for action in self.actions_:
            normalizing_sum += self.strategy_sum_[action]

        for action in self.actions_:
            if normalizing_sum > 0:
                average_strategy[action] = self.strategy_sum_[action] / normalizing_sum
            else:
                average_strategy[action] = 1.0 / len(self.actions_);

        return average_strategy
