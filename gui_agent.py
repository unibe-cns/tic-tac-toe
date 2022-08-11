class GuiAgent:

    def __init__(self, gui):

        self.gui = gui

    def get_move(self, board, marker):
        print("player marker:", marker)
        print(board)

        # player_input = input(f"place marker ({str(marker)}): ").split(",")
        self.gui.update_game_state(board)

        player_input = self.gui.listen_input()
        self.gui.update_top_message('')
        # check whether input is row, col
        try:
            row, col = player_input
        except:
            #self.gui.update_top_message("Please choose a marker position in x=[0,1,2], y=[0,1,2]")
            return None
        row, col = int(row), int(col)

        # we check for more exceptions
        if not row in range(3) or not col in range(3):
            #self.gui.update_top_message("Please choose a marker position in x=[0,1,2], y=[0,1,2]")
            return None
        elif not board.is_empty(row, col):
            #self.gui.update_top_message("Please choose an empty marker position")
            return None
        else:
            return (row, col)

    def update_policy(self, _final_reward, _move_history, _marker):
        pass
