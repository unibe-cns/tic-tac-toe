from agent import Agent
from game import Game


def main():
    game = Game()

    seed = 1234
    agent = Agent(seed)

    while True:
        row, col = input("place marker: ").split(",")
        row, col = int(row), int(col)
        game.mark(row, col, game.FieldState.SQUARE)
        print(game)
        state = game.check_state()
        if state != Game.GameState.RUNNING:
            print(state)
            break

        row, col = agent.get_move(game)
        game.mark(row, col, game.FieldState.CIRCLE)
        print(game)
        state = game.check_state()
        if state != Game.GameState.RUNNING:
            print(state)
            break

    agent.save_policy("policy.json")


main()
