import numpy as np

from agent import Agent
from game import Game


def learn(agent, history, win):
    if win:
        d = 1.1
    else:
        d = 0.9

    for hsh, move in history:
        agent.policy[hsh][agent.move_to_action_idx[move]] *= d
        agent.policy[hsh] /= np.sum(agent.policy[hsh])
        assert np.all(agent.policy[hsh] >= 0.0)
        assert np.abs(np.sum(agent.policy[hsh]) - 1.0) < 1e-9


def main():
    game = Game()

    seed = 1234
    agent = Agent(seed)
    try:
        agent.load_policy("./policy.json")
    except FileNotFoundError:
        pass

    history = []
    while True:
        row, col = input("place marker: ").split(",")
        row, col = int(row), int(col)
        game.mark(row, col, game.FieldState.SQUARE)
        print(game)
        state = game.check_state()
        if state != Game.GameState.RUNNING:
            print(state)
            if state != Game.GameState.DRAW:
                learn(agent, history, False)
            break

        move = agent.get_move(game)
        history.append((game.state_hash(), move))
        row, col = move
        game.mark(row, col, game.FieldState.CIRCLE)
        print(history)
        print(game)
        state = game.check_state()
        if state != Game.GameState.RUNNING:
            print(state)
            if state != Game.GameState.DRAW:
                learn(agent, history, True)
            break

    agent.save_policy("./policy.json")


main()
