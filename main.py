import matplotlib.pyplot as plt
import numpy as np

from agent import Agent
from game import Game


class Player:
    def __init__(self, agent, marker):
        self.agent = agent
        self.marker = marker
        self.move_history = []

    def get_move(self, game):
        move = self.agent.get_move(game, self.marker)
        self.move_history.append((game.state_hash(), move))
        return move

    def update_policy(self, final_reward):
        self.agent.update_policy(final_reward, self.move_history, self.marker)


class Manual:
    def get_move(self, game, marker):
        print(game)
        row, col = input(f"place marker ({str(marker)}): ").split(",")
        row, col = int(row), int(col)
        assert game.is_empty(row, col)
        return (row, col)

    def update_policy(self, _final_reward, _move_history, _marker):
        pass


def duel(agent, opponent, episodes, rng, *, verbose=False):
    history_result = []
    for episode in range(episodes):

        if rng.rand() < 0.5:
            agent_marker = Game.FieldState.SQUARE
            players = [
                Player(agent, agent_marker),
                Player(opponent, Game.FieldState.CIRCLE),
            ]
        else:
            agent_marker = Game.FieldState.CIRCLE
            players = [
                Player(opponent, Game.FieldState.SQUARE),
                Player(agent, agent_marker),
            ]

        game = Game()
        done = False
        while not done:
            for p in players:
                move = p.get_move(game)
                game.mark(move[0], move[1], p.marker)

                (state, winner_marker) = game.check_state()
                if state != Game.GameState.RUNNING:
                    done = True
                    if verbose:
                        print(game)
                        print(state)
                    break

        if state == Game.GameState.DRAW:
            history_result.append(0.0)
            for p in players:
                final_reward = 0.0
                p.update_policy(final_reward)
        else:
            if winner_marker == agent_marker:
                history_result.append(1.0)
            else:
                history_result.append(-1.0)
            for p in players:
                if winner_marker == p.marker:
                    final_reward = 1.0
                else:
                    final_reward = -1.0
                p.update_policy(final_reward)

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
    opponent.alpha = 0.0
    duel(agent, opponent, episodes, rng)


def main():
    # TODO update Q values backwards from final state
    # TODO policy gradient as an alternative
    # TODO draw: call update policy with final_reward = 0.0
    # TODO in update, rotate board to cover symmetric states
    # TODO after update, offline replay (small alpha?)

    seed = 1234
    epsilon = 0.05
    alpha = 0.1
    gamma = 0.99
    agent = Agent(seed=seed, epsilon=epsilon, alpha=alpha, gamma=gamma)

    rng = np.random.RandomState(seed)
    self_play(agent, 5_000, rng)
    print(agent.n_boards_seen())
    agent.epsilon = 0.0
    agent.alpha = 0.0
    duel(agent, Manual(), 10, rng, verbose=True)


main()
