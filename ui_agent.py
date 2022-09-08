class UIAgent:
    def get_move(self, ui, board, marker):
        ui.write("YOU (" + board.field_state_to_str_map[marker] + ")", "-PLAYER0_TEXT-")
        ui.show_board(board)
        return ui.listen_input(marker)

    def update_policy(self, _final_reward, _move_history, _marker):
        pass
