import collections
import copy
import json
import numpy as np


from game import Game


class Agent:

    action_idx_to_move = {
        row * 3 + col: (row, col) for row in range(3) for col in range(3)
    }

    move_to_action_idx = {value: key for key, value in action_idx_to_move.items()}

    def __init__(self, *, seed, epsilon, alpha, gamma):
        self.seed = seed
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.policy = {
            Game.FieldState.SQUARE: collections.defaultdict(lambda: np.zeros(9)),
            Game.FieldState.CIRCLE: collections.defaultdict(lambda: np.zeros(9)),
        }
        self.rng = np.random.default_rng(self.seed)

    def clone(self):
        agent = Agent(
            seed=self.seed + 5678,
            epsilon=self.epsilon,
            alpha=self.alpha,
            gamma=self.gamma,
        )
        agent.policy = copy.deepcopy(self.policy)
        return agent

    def get_move(self, game, marker):
        p = self.rng.uniform()
        if p < self.epsilon:
            move = self.random_move(game)
        else:
            move = self.policy_move(game, marker)
        assert game.is_empty(move[0], move[1])
        return move

    def n_boards_seen(self):
        return len(self.policy[Game.FieldState.SQUARE]) + len(self.policy[Game.FieldState.CIRCLE])

    # def load_policy(self, fn):
    #     with open(fn, "r") as f:
    #         policy = json.load(f)
    #     for hsh in policy:
    #         policy[hsh] = np.array(policy[hsh])
    #     self.policy = policy

    def policy_move(self, game, marker):
        hsh = game.state_hash()

        values = self.policy[marker][hsh].copy()
        # mask occupied positions
        for row in range(3):
            for col in range(3):
                if not game.is_empty(row, col):
                    action_idx = self.move_to_action_idx[(row, col)]
                    values[action_idx] = -np.inf

        max_value = np.max(values)
        if sum(values == max_value) == 1:
            action_idx = np.argmax(values)
        else:
            probs = np.ones_like(values)
            probs[values < max_value] = 0.0
            probs /= np.sum(probs)
            action_idx = self.rng.choice(range(9), p=probs)

        move = self.action_idx_to_move[action_idx]
        return move

    def random_move(self, game):
        possible_moves = []
        for row in range(3):
            for col in range(3):
                if game.is_empty(row, col):
                    possible_moves.append((row, col))
        move = self.rng.choice(possible_moves)
        return tuple(move)

    # def save_policy(self, fn):
    #     policy = {}
    #     for hsh in self.policy:
    #         policy[hsh] = self.policy[hsh].tolist()

    #     with open(fn, "w") as f:
    #         json.dump(policy, f)

    def update_policy(self, final_reward, move_history, marker):
        for t, (hsh, move) in enumerate(move_history):
            action_idx = self.move_to_action_idx[move]
            if t == (len(move_history) - 1):
                max_Q = 0.0
                r = final_reward
            else:
                next_hsh, _next_move = move_history[t + 1]
                max_Q = np.max(self.policy[marker][next_hsh])
                r = 0.0
            self.policy[marker][hsh][action_idx] += self.alpha * (
                r + self.gamma * max_Q - self.policy[marker][hsh][action_idx]
            )
