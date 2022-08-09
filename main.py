import sys

import matplotlib.pyplot as plt
import numpy as np

from agent import Agent
from game import Game
import gui
import time

GUI = True


class GuiAgent:

    def __init__(self, gui):

        self.gui = gui

    def get_move(self, board, marker):
        print("player marker:", marker)
        print(board)

        # player_input = input(f"place marker ({str(marker)}): ").split(",")
        self.gui.update_game_state(board)

        player_input = self.gui.listen_input()
        # check whether input is row, col
        try:
            row, col = player_input
        except:
            self.gui.update_top_message("Please choose a marker position in x=[0,1,2], y=[0,1,2]")
            return None
        row, col = int(row), int(col)

        # we check for more exceptions
        if not row in range(3) or not col in range(3):
            self.gui.update_top_message("Please choose a marker position in x=[0,1,2], y=[0,1,2]")
            return None
        elif not board.is_empty(row, col):
            self.gui.update_top_message("Please choose an empty marker position")
            return None
        else:
            return (row, col)

    def update_policy(self, _final_reward, _move_history, _marker):
        pass


class ManualAgent:
    def get_move(self, board, marker):
        print(board)

        player_input = input(f"place marker ({str(marker)}): ").split(",")
        # check whether input is row, col
        try:
            row, col = player_input
        except:
            print("Please choose a marker position in x=[0,1,2], y=[0,1,2]")
            return None
        row, col = int(row), int(col)

        # we check for more exceptions
        if not row in range(3) or not col in range(3):
            print("Please choose a marker position in x=[0,1,2], y=[0,1,2]")
            return None
        elif not board.is_empty(row, col):
            print("Please choose an empty marker position")
            return None
        else:
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


def duel(agent, opponent, episodes, rng, *, verbose=False, print_file=sys.stdout):
    history_result = []
    for episode in range(episodes):

        game = Game(agent, opponent, rng)
        (state, winner, winning_fields) = game.play(verbose)

        if isinstance(opponent, GuiAgent):
            # print board after game one more time (necessary in case agent wins)
            print("is gui agent!")
            opponent.gui.update_game_state(game.board)
            print("done printing")
            # sleep for x sec
            time.sleep(2)

        if state == Game.GameState.DRAW:
            history_result.append(0.0)
            for p in game.players:
                final_reward = 0.0
                p.update_policy(final_reward)
        else:
            if winner == game.assigned_markers[0]:
                print("you lost", file=print_file)
                history_result.append(1.0)
            else:
                history_result.append(-1.0)
            for p in game.players:
                if winner == p.marker:
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


def self_play(agent, episodes, rng, *, opponent_epsilon, reset_opponent_policy=False):
    opponent = agent.clone()
    opponent.epsilon = opponent_epsilon
    opponent.alpha = 0.0
    if reset_opponent_policy:
        opponent.reset_policy()
    duel(agent, opponent, episodes, rng)


def main():
    # TODO after update, offline replay (small alpha?)
    # TODO policy gradient as an alternative

    seed = 1234
    epsilon = 0.01
    alpha = 0.5
    gamma = 0.95
    no_episodes = 5

    agent = Agent(seed=seed, epsilon=epsilon, alpha=alpha, gamma=gamma)
    try:
        LOAD = agent.load_policy('./policy.json')
    except FileNotFoundError:
        LOAD = False

    rng = np.random.default_rng(seed)
    if not LOAD:
        print("Training agent")
        self_play(agent, 10_000, rng, opponent_epsilon=1.0)
        agent.save_policy('./policy.json')

    print("Starting game")
    if not GUI:
        duel(agent, ManualAgent(), no_episodes, rng, verbose=True)
    else:

        # init a gui
        main_gui = gui.gui()

        guiagent = GuiAgent(main_gui)

        # add gui functions to bot
        agent.gui = main_gui

        main_gui.gui_duel(agent, guiagent, no_episodes, rng, verbose=True)




if __name__ == '__main__':
    main()

