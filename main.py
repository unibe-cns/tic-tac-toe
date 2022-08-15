import numpy as np

import training
from duel import duel, duel_manual_against_improving_agent
from gui import GUI
from q_learning_agent import QLearningAgent
from tui import TUI
from ui_agent import UIAgent


def main():
    q_learning_agent_params = {
        "seed": 1234,
        # "epsilon": 0.25,
        # "alpha": 0.5,
        # "gamma": 0.95,
        "epsilon": 0.1,
        "alpha": 0.25,
        "gamma": 0.999,
    }
    # save_after_episodes = [0, 100, 350, 1_000, 10_000]
    save_after_episodes = [0, 200, 400, 800, 1600, 3200, 6400, 12800, 25600]
    policies = training.generate_policies_for_q_learning_agent(
        **q_learning_agent_params, save_after_episodes=save_after_episodes
    )
    print(policies)
    agent1 = QLearningAgent(**q_learning_agent_params)
    agent1.epsilon = 0.0

    rng = np.random.default_rng(1234)
    # # ui = TUI()
    ui = GUI()
    agent0 = UIAgent()
    # duel(ui, agent0, agent1, 5, rng)
    duel_manual_against_improving_agent(ui, agent0, agent1, policies, rng)


if __name__ == "__main__":
    main()
