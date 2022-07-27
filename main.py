import matplotlib.pyplot as plt
import numpy as np

from agent import Agent
from game import Game


def self_play(agent, episodes, rng, *, print_state=False):
    opponent = agent.clone()
    opponent.alpha = 0.0
    opponent.epsilon = 0.1
    players = [agent, opponent]
    markers = [Game.FieldState.SQUARE, Game.FieldState.CIRCLE]
    order = [0, 1]
    history_result = []
    for episode in range(episodes):
        rng.shuffle(order)
        for p in players:
            p.clear_move_history()

        game = Game()
        done = False
        while not done:
            for player_idx in order:
                move = players[player_idx].get_move(game)
                game.mark(move[0], move[1], markers[player_idx])

                if print_state:
                    print(game)

                state = game.check_state()
                if state != Game.GameState.RUNNING:
                    done = True
                    break

        if player_idx == 0:
            history_result.append(1)
        else:
            history_result.append(0)

        if state != Game.GameState.DRAW:
            winner_idx = player_idx
            for player_idx in order:
                if player_idx == winner_idx:
                    final_reward = 1.0
                else:
                    final_reward = -1.0
                players[player_idx].update_policy(final_reward)

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

    plt.plot(moving_avg(history_result))
    # plt.plot(np.cumsum(np.ones_like(history_result) * 0.5), color='k')
    # plt.plot(np.cumsum(history_result))
    plt.ylim(0, 1)
    plt.show()
    # exit()


def main():
    seed = 1234
    agent = Agent(seed)
    agent.epsilon = 0.01

    rng = np.random.RandomState()
    self_play(agent, 2_000, rng)
    self_play(agent, 2_000, rng)
    self_play(agent, 2_000, rng)
    self_play(agent, 2_000, rng)
    self_play(agent, 2_000, rng)
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
