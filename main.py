import sys
import os

import matplotlib.pyplot as plt
import numpy as np

from q_learning_agent import QLearningAgent
from game import Game
from gui_agent import GuiAgent
import gui
import time
import math


def self_play(agent, episodes, rng, *, opponent_epsilon, reset_opponent_policy=False):
    opponent = agent.clone()
    opponent.epsilon = opponent_epsilon
    opponent.alpha = 0.0
    if reset_opponent_policy:
        opponent.reset_policy()
    history_result = duel(agent, opponent, episodes, rng)

    return history_result


def main():
    seed = 1234
    epsilon = 0.25
    alpha = 0.5
    gamma = 0.95
    no_episodes = 2
    no_train_episodes = 10_000
    # save policy at win_rate approx [0.3, 0.4, 0.6, 0.8, 1.0]
    save_policy_after_episodes = [0, 100, 350, 1_000, 10_000]

    agent = QLearningAgent(seed=seed, epsilon=epsilon, alpha=alpha, gamma=gamma)
    try:
        LOAD = agent.load_policy(
            "./saved_policies/policy" + str(save_policy_after_episodes[-1]) + ".json"
        )
    except FileNotFoundError:
        LOAD = False

    rng = np.random.default_rng(seed)
    if not LOAD:
        print("Training agent")
        try:
            os.makedirs("./saved_policies")
        except FileExistsError:
            # directory already exists
            pass
        # save policy before training
        agent.save_policy("./saved_policies/policy0.json")

        n_total_episodes = 0
        history_result = []
        for n_episodes in [
            save_policy_after_episodes[i + 1] - save_policy_after_episodes[i]
            for i in range(len(save_policy_after_episodes) - 1)
        ]:
            n_total_episodes += n_episodes
            history_result.append(
                self_play(agent, n_episodes, rng, opponent_epsilon=1.0)
            )
            agent.save_policy(
                "./saved_policies/policy" + str(n_total_episodes) + ".json"
            )
            print("Total training: ", n_total_episodes)

        # flatten list
        history_result = [num for sublist in history_result for num in sublist]

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

    print("Starting game with untrained agent")
    # make iterator over saved_policies
    agent.policy_list = [
        "./saved_policies/policy" + str(i) + ".json" for i in save_policy_after_episodes
    ]
    agent.policy_iter = iter(agent.policy_list)
    agent.load_policy(next(agent.policy_iter))
    agent.epsilon = 0.0

    # init a gui
    main_gui = gui.Gui()

    # init a player gui agent
    guiagent = GuiAgent(main_gui)

    # add gui functions to bot
    agent.gui = main_gui

    # start game
    main_gui.gui_duel(agent, guiagent, no_episodes, rng, verbose=True)


if __name__ == "__main__":
    main()
