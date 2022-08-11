class ManualAgent:
    def get_move(self, board, marker):
        print(board)
        player_input = input(f"place marker ({str(marker)}): ").split(",")
        # check whether input is row, col
        try:
            row, col = player_input
        except:
            print("Please choose a marker position in x=[0,1,2], y=[0,1,2]")
            return None
        row, col = int(row), int(col)

        # we check for more exceptions
        if not row in range(3) or not col in range(3):
            print("Please choose a marker position in x=[0,1,2], y=[0,1,2]")
            return None
        elif not board.is_empty(row, col):
            print("Please choose an empty marker position")
            return None
        else:
            return (row, col)

    def update_policy(self, _final_reward, _move_history, _marker):
        pass
