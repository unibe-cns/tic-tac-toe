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
        self.policy = {}
        self.rng = np.random.default_rng(self.seed)

    def clone(self):
        agent = Agent(self.seed + 5678)
        agent.policy = copy.deepcopy(self.policy)
        return agent

    def get_move(self, game, epsilon=0.0):
        hsh = game.state_hash()

        if hsh not in self.policy:
            self.policy[hsh] = np.ones(9) * 1 / 9.0
            assert np.all(self.policy[hsh] >= 0.0)
            assert np.abs(np.sum(self.policy[hsh]) - 1.0) < 1e-9

        p = self.rng.uniform()
        probs = np.zeros_like(self.policy[hsh])
        for row in range(3):
            for col in range(3):
                if game.is_empty(row, col):
                    action_idx = self.move_to_action_idx[(row, col)]
                    if p < epsilon:
                        probs[action_idx] = 1.0
                    else:
                        probs[action_idx] = self.policy[hsh][action_idx]
        probs /= np.sum(probs)
        action_idx = self.sample_action(probs)
        move = self.action_idx_to_move[action_idx]
        assert game.is_empty(move[0], move[1])
        return move

    def load_policy(self, fn):
        with open(fn, "r") as f:
            policy = json.load(f)
        for hsh in policy:
            policy[hsh] = np.array(policy[hsh])
        self.policy = policy

    def sample_action(self, probs):
        return np.argmax(self.rng.multinomial(1, pvals=probs))

    def save_policy(self, fn):
        policy = {}
        for hsh in self.policy:
            policy[hsh] = self.policy[hsh].tolist()

        with open(fn, "w") as f:
            json.dump(policy, f)
