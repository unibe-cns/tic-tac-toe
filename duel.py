import time

from game import Game


def duel(ui, agent0, agent1, n_episodes, rng):
    scores = [0, 0]
    for _episode in range(n_episodes):
        ui.show_new_game()
        game = Game(ui, agent0, agent1, rng)
        (state, winner, winning_fields) = game.play()
        if winner is not None:
            if winner == game.assigned_markers[0]:
                scores[0] += 1
            else:
                scores[1] += 1
        ui.show_scores(scores)
        ui.show_final_state(game.board, state, winner, winning_fields)
        time.sleep(2.0)


def duel_with_training(ui, agent0, agent1, n_episodes, rng):
    history_result = []
    for _episode in range(n_episodes):
        game = Game(ui, agent0, agent1, rng)
        (state, winner, winning_fields) = game.play()

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

    return history_result


def duel_manual_against_improving_agent(ui, agent0, agent1, policies, rng):
    scores = [0, 0]
    ui.show_scores(scores)
    ui.write("You", "-PLAYER0_TEXT-")
    ui.show_image("./img/bot.png", "-PLAYER1_IMG-")
    level = 0
    agent1.load_policy(policies[level])
    while True:
        if level == 0:
            ui.show_new_game()
        else:
            ui.write("", "-TITLE_TEXT-")
        ui.write(f"Bot v{level + 1:.1f}", "-PLAYER1_TEXT-")
        game = Game(ui, agent0, agent1, rng)
        (state, winner, winning_fields) = game.play()
        if winner is not None:
            if winner == game.assigned_markers[0]:
                scores[0] += 1
                # either load pretrained policy or improve upon best one
                if level < len(policies) - 1:
                    level += 1
                    agent1.load_policy(policies[level])
                else:
                    for p in game.players:
                        if p.marker == game.assigned_markers[1]:
                            print("training")
                            final_reward = -1.0
                            p.update_policy(final_reward)
            else:
                scores = [0, 0]
                level = 0
                agent1.load_policy(policies[level])
        ui.show_scores(scores)
        ui.show_final_state(game.board, state, winner, winning_fields)
        time.sleep(2.0)
        if winner == game.assigned_markers[1]:
            ui.warn("You lost. End of game.")
            time.sleep(5.0)
            ui.warn("")
