import collections
import copy
import json
import numpy as np


from game import Board


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
        self.reset_policy()
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

    def get_move(self, board, marker):
        p = self.rng.uniform()
        if p < self.epsilon:
            move = self.random_move(board)
        else:
            move = self.policy_move(board, marker)
        assert board.is_empty(move[0], move[1])
        return move

    def n_boards_seen(self):
        return len(self.policy[Board.FieldState.CROSS]) + len(
            self.policy[Board.FieldState.CIRCLE]
        )

    def load_policy(self, fn):
        with open(fn, "r") as f:
            print(f"Loading policy {f.name}")
            policy = json.load(f)
        self.reset_policy()
        for str_marker in policy:
            for key in policy[str_marker]:
                self.policy[Board.str_value_to_state[str_marker]][key] = np.array(
                    policy[str_marker][key]
                )
        return True

    def policy_move(self, board, marker):
        key = board.to_str()

        values = self.policy[marker][key].copy()

        # mask occupied positions
        for row in range(3):
            for col in range(3):
                if not board.is_empty(row, col):
                    action_idx = Agent.move_to_action_idx[(row, col)]
                    values[action_idx] = -np.inf

        # make sure to evenly sample all state with same value
        max_value = np.max(values)
        if sum(values == max_value) == 1:
            action_idx = np.argmax(values)
        else:
            probs = np.ones_like(values)
            probs[values < max_value] = 0.0
            probs /= np.sum(probs)
            action_idx = self.rng.choice(range(9), p=probs)

        move = Agent.action_idx_to_move[action_idx]
        return move

    def random_move(self, board):
        possible_moves = []
        for row in range(3):
            for col in range(3):
                if board.is_empty(row, col):
                    possible_moves.append((row, col))
        move = self.rng.choice(possible_moves)
        return tuple(move)

    def reset_policy(self):
        self.policy = {
            Board.FieldState.CROSS: collections.defaultdict(lambda: np.zeros(9)),
            Board.FieldState.CIRCLE: collections.defaultdict(lambda: np.zeros(9)),
        }

    def save_policy(self, fn):
        policy = {}
        for marker in self.policy:
            policy[marker] = {}
            for key in self.policy[marker]:
                policy[marker][key] = self.policy[marker][key].tolist()

        with open(fn, "w") as f:
            json.dump(policy, f)

    def update_policy(self, final_reward, move_history, marker):
        T = len(move_history)
        board = Board()
        next_board = Board()
        for t, (key, move) in reversed(list(zip(range(T), move_history))):
            board.from_str(key)
            considered_keys = set()
            for (board_symmetry, move_symmetry) in zip(
                Board.board_symmetries(), Board.move_symmetries()
            ):
                rotated_board = board_symmetry(board)
                rotated_move = move_symmetry(move)

                rotated_key = rotated_board.to_str()
                if rotated_key in considered_keys:
                    continue
                considered_keys.add(rotated_key)

                action_idx = Agent.move_to_action_idx[rotated_move]
                if t == (T - 1):
                    r = final_reward
                    max_Q = 0.0
                else:
                    r = 0.0
                    next_key, _next_move = move_history[t + 1]
                    next_board.from_str(next_key)
                    next_rotated_board = board_symmetry(next_board)
                    next_rotated_key = next_rotated_board.to_str()
                    max_Q = np.max(self.policy[marker][next_rotated_key])
                self.policy[marker][rotated_key][action_idx] += self.alpha * (
                    r
                    + self.gamma * max_Q
                    - self.policy[marker][rotated_key][action_idx]
                )
