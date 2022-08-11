import time


class TUI:
    @staticmethod
    def listen_input(marker):
        while True:
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
