import matplotlib.pyplot as plt
import numpy as np

from agent import Agent
from game import Game


def update_policy(agent, history, r):
    delta = 0.1
    gamma = 0.95
    T = len(history)
    for t, (hsh, move) in enumerate(history):
        agent.policy[hsh][agent.move_to_action_idx[move]] += (
            gamma ** (T - t - 1) * r * delta
        )
        agent.policy[hsh] -= np.min(agent.policy[hsh])
        agent.policy[hsh] /= np.sum(agent.policy[hsh])
        assert np.all(agent.policy[hsh] >= 0.0)
        assert np.abs(np.sum(agent.policy[hsh]) - 1.0) < 1e-9


def self_play(agent, episodes, *, print_state=False):

    epsilon = 0.001

    opponent = agent.clone()
    history_result = []

    for episode in range(episodes):
        game = Game()
        history_agent = []
        history_opponent = []
        while True:
            move = opponent.get_move(game, epsilon=epsilon)
            history_opponent.append((game.state_hash(), move))
            game.mark(move[0], move[1], game.FieldState.SQUARE)

            if print_state:
                print(game)
            state = game.check_state()
            if state != Game.GameState.RUNNING:
                if state != Game.GameState.DRAW:
                    update_policy(agent, history_agent, -1.0)
                if print_state:
                    print(state)
                history_result.append(0)
                break

            move = agent.get_move(game, epsilon=epsilon)
            history_agent.append((game.state_hash(), move))
            game.mark(move[0], move[1], game.FieldState.CIRCLE)

            if print_state:
                print(game)
            state = game.check_state()
            if state != Game.GameState.RUNNING:
                if state != Game.GameState.DRAW:
                    update_policy(agent, history_agent, 1.0)
                if print_state:
                    print(state)
                history_result.append(1)
                break

        if print_state:
            print()

        if episode > 0 and episode % 1000 == 0:
            print(episode)

    def moving_avg(a):
        window_size = 100
        a = np.array(a)
        x = np.empty(len(a) // window_size)
        for i in range(len(x)):
            x[i] = np.mean(a[i * window_size : (i + 1) * window_size])
        return x

    # plt.plot(moving_avg(history_result))
    # plt.plot(np.cumsum(np.ones_like(history_result) * 0.5), color='k')
    # plt.plot(np.cumsum(history_result))
    # plt.ylim(0, 1)
    # plt.show()
    # exit()


def main():
    seed = 1234
    agent = Agent(seed)

    self_play(agent, 5_000)
    self_play(agent, 5_000)
    self_play(agent, 5_000)
    self_play(agent, 5_000)
    print(len(agent.policy))
    # exit()
    # try:
    #     agent.load_policy("./policy.json")
    #     print('loaded policy')
    # except FileNotFoundError:
    #     pass

    while True:
        game = Game()
        while True:
            row, col = input("place marker: ").split(",")
            row, col = int(row), int(col)
            game.mark(row, col, game.FieldState.SQUARE)
            print(game)
            state = game.check_state()
            if state != Game.GameState.RUNNING:
                print(state)
                break

            move = agent.get_move(game)
            row, col = move
            game.mark(row, col, game.FieldState.CIRCLE)
            print(game)
            state = game.check_state()
            if state != Game.GameState.RUNNING:
                print(state)
                break

    # agent.save_policy("./policy.json")


main()
