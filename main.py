import numpy as np

from agent import Agent
from game import Game


def update_policy(agent, history, delta):
    for hsh, move in history:
        agent.policy[hsh][agent.move_to_action_idx[move]] *= delta
        agent.policy[hsh] /= np.sum(agent.policy[hsh])
        assert np.all(agent.policy[hsh] >= 0.0)
        assert np.abs(np.sum(agent.policy[hsh]) - 1.0) < 1e-9


def self_play(agent, episodes):

    opponent = agent.clone()

    for episode in range(episodes):
        game = Game()
        history_agent = []
        history_opponent = []
        while True:
            move = opponent.get_move(game, epsilon=0.05)
            history_opponent.append((game.state_hash(), move))
            game.mark(move[0], move[1], game.FieldState.SQUARE)

            state = game.check_state()
            if state != Game.GameState.RUNNING:
                if state != Game.GameState.DRAW:
                    update_policy(agent, history_agent, 0.8)
                break

            move = agent.get_move(game, epsilon=0.05)
            history_agent.append((game.state_hash(), move))
            game.mark(move[0], move[1], game.FieldState.CIRCLE)

            state = game.check_state()
            if state != Game.GameState.RUNNING:
                if state != Game.GameState.DRAW:
                    update_policy(opponent, history_opponent, 0.8)
                break

        print(game)

        if episode > 0 and episode % 1000 == 0:
            print(episode)


def main():
    game = Game()

    seed = 1234
    agent = Agent(seed)

    self_play(agent, 30_000)
    print(len(agent.policy))
    # try:
    #     agent.load_policy("./policy.json")
    # except FileNotFoundError:
    #     pass

    history = []
    while True:
        row, col = input("place marker: ").split(",")
        row, col = int(row), int(col)
        game.mark(row, col, game.FieldState.SQUARE)
        print(game)
        state = game.check_state()
        if state != Game.GameState.RUNNING:
            print(state)
            break

        move = agent.get_move(game, print_probs=True)
        history.append((game.state_hash(), move))
        row, col = move
        game.mark(row, col, game.FieldState.CIRCLE)
        print(game)
        state = game.check_state()
        if state != Game.GameState.RUNNING:
            print(state)
            break

    agent.save_policy("./policy.json")


main()
