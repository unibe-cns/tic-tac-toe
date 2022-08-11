import sys
import os

import matplotlib.pyplot as plt
import numpy as np

from agent import Agent
from game import Game
from gui_agent import GuiAgent
import gui
import time
import math


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
    
def update_level(agent, guiagent, next_level=False, winner=None):
    # updates bot and level message

    if winner == 'draw':
        level = guiagent.gui.level
        #level += 0.1
    elif winner == 'player':
        level = guiagent.gui.level
        level += 0.1
        if next_level:
            print("Loading next policy")
            try:
                level = math.ceil(level)
                agent.load_policy(next(agent.policy_iter))
            except:
                print("Final policy reached, continuing")
    
    elif winner == 'bot':
        # reset bot and level
        print("Resetting agent")
        agent.gui.update_top_message('new_game')
        agent.policy_iter = iter(agent.policy_list)
        agent.load_policy(next(agent.policy_iter))
        level = 0.1
    guiagent.gui.level = level
    


def duel(agent, opponent, episodes, rng, *, verbose=False, print_file=sys.stdout):
    history_result = []
    done = False
    epi = 0
    player_wins = 0
    while not done:
        
        # the episodes counter is only needed for bot training, otherwise game is infinite
        if not isinstance(opponent, GuiAgent):
            if epi == episodes:
                done = True

        game = Game(agent, opponent, rng)
        (state, winner, winning_fields) = game.play(verbose)

        if isinstance(opponent, GuiAgent):
            # print board after game one more time (necessary in case agent wins)
            opponent.gui.update_game_state(game.board, winning_fields=winning_fields)

        if state == Game.GameState.DRAW:
            history_result.append(0.0)
            for p in game.players:
                final_reward = 0.0
                p.update_policy(final_reward)
            if isinstance(opponent, GuiAgent):
                opponent.gui.update_top_message('draw')
                update_level(agent, opponent, winner='draw')
                # sleep for x sec
                time.sleep(2)
                opponent.gui.update_top_message('')
        else:
            if winner == game.assigned_markers[0]:
                #print("you lost", file=print_file)
                history_result.append(1.0)
                if isinstance(opponent, GuiAgent):
                    opponent.gui.update_top_message('bot_wins')
                    opponent.gui.blink(game.board, winning_fields=winning_fields)
                    # sleep for x sec
                    time.sleep(2)
                    update_level(agent, opponent, winner='bot')
                    #opponent.gui.update_top_message('')
            else:
                history_result.append(-1.0)
                if isinstance(opponent, GuiAgent):
                    player_wins += 1
                    next_level = True if player_wins == episodes else False
                    if next_level:
                        player_wins = 0
                    opponent.gui.update_top_message('player_wins')
                    # sleep for x sec
                    time.sleep(2)
                    update_level(agent, opponent, next_level=next_level, winner='player')
                    opponent.gui.update_top_message('')
            for p in game.players:
                if winner == p.marker:
                    final_reward = 1.0
                else:
                    final_reward = -1.0
                p.update_policy(final_reward)
        
        if isinstance(opponent, GuiAgent):
            opponent.gui.update_level_text(opponent.gui.level)
                
        epi += 1

    return history_result


def self_play(agent, episodes, rng, *, opponent_epsilon, reset_opponent_policy=False):
    opponent = agent.clone()
    opponent.epsilon = opponent_epsilon
    opponent.alpha = 0.0
    if reset_opponent_policy:
        opponent.reset_policy()
    history_result = duel(agent, opponent, episodes, rng)
    
    return history_result


def main():
    # TODO after update, offline replay (small alpha?)
    # TODO policy gradient as an alternative

    seed = 1234
    epsilon = 0.01
    alpha = 0.5
    gamma = 0.95
    no_episodes = 2
    no_train_episodes = 10_000
    # save policy at win_rate approx [0.3, 0.4, 0.6, 0.8, 1.0]
    save_policy_after_episodes = [0, 100, 350, 1_000, 10_000]

    agent = Agent(seed=seed, epsilon=epsilon, alpha=alpha, gamma=gamma)
    try:
        LOAD = agent.load_policy('./saved_policies/policy' + str(save_policy_after_episodes[-1]) + '.json')
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
        agent.save_policy('./saved_policies/policy0.json')
        
        n_total_episodes = 0
        history_result = []
        for n_episodes in [save_policy_after_episodes[i+1]-save_policy_after_episodes[i] for i in range(len(save_policy_after_episodes)-1)]:
            n_total_episodes += n_episodes
            history_result.append(self_play(agent, n_episodes, rng, opponent_epsilon=1.0))
            agent.save_policy('./saved_policies/policy' + str(n_total_episodes) + '.json')
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
    agent.policy_list = ['./saved_policies/policy' + str(i) + '.json' for i in save_policy_after_episodes]
    agent.policy_iter = iter(agent.policy_list)
    agent.load_policy(next(agent.policy_iter))

    # init a gui
    main_gui = gui.gui()
    
    # init a player gui agent
    guiagent = GuiAgent(main_gui)

    # add gui functions to bot
    agent.gui = main_gui

    # start game
    main_gui.gui_duel(agent, guiagent, no_episodes, rng, verbose=True)




if __name__ == '__main__':
    main()

