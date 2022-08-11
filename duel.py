import math
import time
import sys

from game import Game

# from gui_agent import GuiAgent


def update_level(agent, guiagent, next_level=False, winner=None):
    # updates bot and level message

    if winner == "draw":
        level = guiagent.gui.level
        # level += 0.1
    elif winner == "player":
        level = guiagent.gui.level
        level += 0.1
        if next_level:
            print("Loading next policy")
            try:
                level = math.ceil(level)
                agent.load_policy(next(agent.policy_iter))
            except:
                print("Final policy reached, continuing")

    elif winner == "bot":
        # reset bot and level
        print("Resetting agent")
        agent.gui.update_top_message("new_game")
        agent.policy_iter = iter(agent.policy_list)
        agent.load_policy(next(agent.policy_iter))
        level = 0.1
    guiagent.gui.level = level


# FIXME agent0, agent1
def duel(ui, agent, opponent, episodes, rng):
    history_result = []
    # done = False
    # epi = 0
    # player_wins = 0
    # while not done:
    # FIXME n_episodes
    for _episode in range(episodes):

        # # the episodes counter is only needed for bot training, otherwise game is infinite
        # if not isinstance(opponent, GuiAgent):
        #     if epi == episodes:
        #         done = True

        game = Game(ui, agent, opponent, rng)
        (state, winner, winning_fields) = game.play()

        # if isinstance(opponent, GuiAgent):
        #     # print board after game one more time (necessary in case agent wins)
        #     opponent.gui.update_game_state(game.board, winning_fields=winning_fields)

        if state == Game.GameState.DRAW:
            history_result.append(0.0)
            for p in game.players:
                final_reward = 0.0
                p.update_policy(final_reward)
            # if isinstance(opponent, GuiAgent):
            #     opponent.gui.update_top_message("draw")
            #     update_level(agent, opponent, winner="draw")
            #     # sleep for x sec
            #     time.sleep(2)
            #     opponent.gui.update_top_message("")
        else:
            if winner == game.assigned_markers[0]:
                history_result.append(1.0)
                # if isinstance(opponent, GuiAgent):
                #     opponent.gui.update_top_message("bot_wins")
                #     opponent.gui.blink(game.board, winning_fields=winning_fields)
                #     # sleep for x sec
                #     time.sleep(2)
                #     update_level(agent, opponent, winner="bot")
                #     # opponent.gui.update_top_message('')
            else:
                history_result.append(-1.0)
                # if isinstance(opponent, GuiAgent):
                #     player_wins += 1
                #     next_level = True if player_wins == episodes else False
                #     if next_level:
                #         player_wins = 0
                #     opponent.gui.update_top_message("player_wins")
                #     # sleep for x sec
                #     time.sleep(2)
                #     update_level(
                #         agent, opponent, next_level=next_level, winner="player"
                #     )
                #     opponent.gui.update_top_message("")
            for p in game.players:
                if winner == p.marker:
                    final_reward = 1.0
                else:
                    final_reward = -1.0
                p.update_policy(final_reward)

        # if isinstance(opponent, GuiAgent):
        #     opponent.gui.update_level_text(opponent.gui.level)

        # epi += 1

    return history_result
