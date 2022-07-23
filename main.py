from game import Game


def main():
    game = Game()

    while True:
        row, col = input("place marker: ").split(",")
        row, col = int(row), int(col)
        game.mark(row, col, "x")
        print(game)
        state = game.check_state()
        if state != Game.GameState.RUNNING:
            print(state)
            exit()
        row, col = input("place marker: ").split(",")
        row, col = int(row), int(col)
        game.mark(row, col, "o")
        print(game)
        state = game.check_state()
        if state != Game.GameState.RUNNING:
            print(state)
            exit()


main()
