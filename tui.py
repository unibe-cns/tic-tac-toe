import sys
import termios
import time
import tty


class TUI:
    def __init__(self, *, single_character_input=False):
        self.single_character_input = single_character_input

    @staticmethod
    def getch():
        filedescriptors = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin)
        x = sys.stdin.read(1)[0]
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)
        return x

    def listen_input(self, marker):
        while True:
            if self.single_character_input:
                try:
                    print(f"Please place marker ({str(marker)}): ", end="")
                    move = self.getch()
                    move = int(move)
                    row = move // 3
                    col = move % 3
                    print((row, col))
                    return (row, col)
                except ValueError:
                    return None
            else:
                move = input(f"Please place marker ({str(marker)}): ")
                try:
                    row, col = move.split(",")
                    row, col = int(row), int(col)
                    return (row, col)
                except ValueError:
                    return None

    @staticmethod
    def show_board(board):
        print(board)

    @staticmethod
    def show_final_state(board, state, winner, winning_fields):
        print("\033[1mGame finished.\033[0m", end=" ")
        if winner is not None:
            winner_str = board.field_state_to_str_map[winner]
            print("Winner: \033[1m" + winner_str + "\033[0m")
        else:
            print("Draw.")
        print(board)
        print()
        time.sleep(2.0)

    @staticmethod
    def warn(msg):
        print(f"WARNING: {msg}")

    def write(self, text, key):
        print(text)

    def show_image(self, fn, key):
        pass

    def show_new_game(self):
        pass

    def show_scores(self, scores):
        pass
