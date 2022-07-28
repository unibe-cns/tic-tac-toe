import matplotlib.pyplot as plt
import numpy as np

from agent import Agent
from game import Game


class ManualAgent:
    def get_move(self, game, marker):
        print(game)
        row, col = input(f"place marker ({str(marker)}): ").split(",")
        row, col = int(row), int(col)
        assert game.is_empty(row, col)
        return (row, col)

    def update_policy(self, _final_reward, _move_history, _marker):
        pass


class DeterministicAgent:
    def __init__(self, moves):
        self.moves = list(moves)
        self.idx = 0

    def get_move(self, game, marker):
        move = self.moves[self.idx]
        self.idx += 1
        return move

    def update_policy(self, _final_reward, _move_history, _marker):
        pass


def duel(agent, opponent, episodes, rng, *, verbose=False):
    history_result = []
    for episode in range(episodes):

        game = Game(agent, opponent, rng)
        (state, winner) = game.play(verbose)

        if state == Game.GameState.DRAW:
            history_result.append(0.0)
            for p in game.players:
                final_reward = 0.0
                p.update_policy(final_reward)
        else:
            if winner == game.assigned_markers[0]:
                history_result.append(1.0)
            else:
                history_result.append(-1.0)
            for p in game.players:
                if winner == p.marker:
                    final_reward = 1.0
                else:
                    final_reward = -1.0
                p.update_policy(final_reward)

        print(agent.policy)

        if episode > 0 and episode % 1000 == 0:
            print(episode)

    def moving_avg(a):
        window_size = 100
        a = np.array(a)
        x = np.empty(len(a) // window_size)
        for i in range(len(x)):
            x[i] = np.mean(a[i * window_size : (i + 1) * window_size])
        return x

    plt.plot(moving_avg(history_result))
    plt.ylim(-1, 1)
    plt.show()


def self_play(agent, episodes, rng):
    opponent = agent.clone()
    opponent.epsilon = 0.1
    opponent.alpha = 0.0
    duel(agent, opponent, episodes, rng)


def main():
    # TODO after update, offline replay (small alpha?)
    # TODO policy gradient as an alternative

    seed = 1234
    epsilon = 0.01
    alpha = 0.5
    gamma = 0.99
    agent = Agent(seed=seed, epsilon=epsilon, alpha=alpha, gamma=gamma)

    rng = np.random.default_rng(seed)
    # self_play(agent, 10_000, rng)
    # self_play(agent, 5_000, rng)
    # self_play(agent, 5_000, rng)
    # duel(agent, DeterministicAgent([(2, 2), (1, 1), (0, 0)]), 10, rng, verbose=True)
    duel(agent, ManualAgent(), 10, rng, verbose=True)

    # print(agent.n_boards_seen())
    # agent.epsilon = 0.0
    # agent.alpha = 0.0
    # duel(agent, ManualAgent(), 10, rng, verbose=True)


main()
