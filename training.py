import os
import matplotlib.pyplot as plt
import numpy as np

from duel import duel_with_training
from nui import NUI
from q_learning_agent import QLearningAgent


def self_play(agent, episodes, rng, *, opponent_epsilon):
    opponent = agent.clone()
    opponent.epsilon = opponent_epsilon
    opponent.alpha = 0.0
    history_result = duel_with_training(NUI(), agent, opponent, episodes, rng)
    return history_result


def generate_policies_for_q_learning_agent(
    *, seed, epsilon, alpha, gamma, save_after_episodes
):
    policy_dir = "./policies/"

    fn_policies = []
    for n_episodes in save_after_episodes:
        fn = os.path.join(policy_dir, "policy" + str(n_episodes) + ".json")
        if os.path.isfile(fn):
            fn_policies.append(fn)
            continue

        agent = QLearningAgent(seed=seed, epsilon=epsilon, alpha=alpha, gamma=gamma)
        rng = np.random.default_rng(seed)
        history_result = self_play(agent, n_episodes, rng, opponent_epsilon=1.0)

        def moving_avg(a):
            window_size = 100
            a = np.array(a)
            x = np.empty(len(a) // window_size)
            for i in range(len(x)):
                x[i] = np.mean(a[i * window_size : (i + 1) * window_size])
            return x

        if len(history_result) > 1:
            plt.clf()
            plt.title(n_episodes)
            plt.plot(moving_avg(history_result))
            plt.ylim(-1, 1)
            plt.show()

        if not os.path.isdir(policy_dir):
            os.makedirs(policy_dir)

        agent.save_policy(fn)
        fn_policies.append(fn)

    return fn_policies
