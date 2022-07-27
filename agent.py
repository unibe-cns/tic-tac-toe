import copy
import json
import numpy as np


class Agent:

    action_idx_to_move = {
        row * 3 + col: (row, col) for row in range(3) for col in range(3)
    }

    move_to_action_idx = {value: key for key, value in action_idx_to_move.items()}

    def __init__(self, seed):
        self.seed = seed
        self.epsilon = 0.0
        self.alpha = 0.05
        self.policy = {}
        self.move_history = []
        self.rng = np.random.default_rng(self.seed)

    def clear_move_history(self):
        self.move_history = []

    def clone(self):
        agent = Agent(self.seed + 5678)
        agent.epsilon = self.epsilon
        agent.alpha = self.alpha
        agent.policy = copy.deepcopy(self.policy)
        return agent

    def random_move(self, game):
        possible_moves = []
        for row in range(3):
            for col in range(3):
                if game.is_empty(row, col):
                    possible_moves.append((row, col))
        move = self.rng.choice(possible_moves)
        return tuple(move)

    def get_move(self, game):
        def uniform_policy():
            policy = np.ones(9) * 1 / 9.0
            policy /= np.sum(policy)
            assert np.all(policy >= 0.0)
            assert np.abs(np.sum(policy - 1.0) < 1e-9)
            return policy

        hsh = game.state_hash()
        if hsh not in self.policy:
            self.policy[hsh] = uniform_policy()

        p = self.rng.uniform()
        if p < self.epsilon:
            move = self.random_move(game)
        else:
            move = self.policy_move(game)
        assert game.is_empty(move[0], move[1])
        self.move_history.append((game.state_hash(), move))
        return move

    def load_policy(self, fn):
        with open(fn, "r") as f:
            policy = json.load(f)
        for hsh in policy:
            policy[hsh] = np.array(policy[hsh])
        self.policy = policy

    def policy_move(self, game):
        hsh = game.state_hash()

        probs = np.ones_like(self.policy[hsh]) * -np.infty
        for row in range(3):
            for col in range(3):
                if game.is_empty(row, col):
                    action_idx = self.move_to_action_idx[(row, col)]
                    probs[action_idx] = self.policy[hsh][action_idx]

        max_prob = np.max(probs)
        if sum(probs == max_prob) == 1:
            action_idx = np.argmax(probs)
        else:
            probs[probs != max_prob] = 0.0
            probs /= np.sum(probs)
            action_idx = self.sample_action(probs)

        move = self.action_idx_to_move[action_idx]
        return move

    def sample_action(self, probs):
        return self.rng.choice(range(9), p=probs)

    def save_policy(self, fn):
        policy = {}
        for hsh in self.policy:
            policy[hsh] = self.policy[hsh].tolist()

        with open(fn, "w") as f:
            json.dump(policy, f)

    def update_policy(self, final_reward):
        gamma = 0.99

        for t, (hsh, move) in enumerate(self.move_history):
            action_idx = self.move_to_action_idx[move]
            if t == (len(self.move_history) - 1):
                max_Q = 0.0
                r = final_reward
            else:
                next_hsh, _next_move = self.move_history[t + 1]
                max_Q = np.max(self.policy[next_hsh])
                r = 0.0
            self.policy[hsh][action_idx] += self.alpha * (r + gamma * max_Q - self.policy[hsh][action_idx])
