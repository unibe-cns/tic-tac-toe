import enum
import numpy as np

from board import Board
import time


class Game:
    @enum.unique
    class GameState(enum.Enum):
        RUNNING = 0
        DRAW = 1
        WIN = 2

    class Player:
        def __init__(self, agent, marker):
            self.agent = agent
            self.marker = marker
            self.move_history = []

        def get_move(self, ui, board):
            move = self.agent.get_move(ui, board, self.marker)
            self.move_history.append((board.to_str(), move))
            return move

        def update_policy(self, final_reward):
            self.agent.update_policy(final_reward, self.move_history, self.marker)

    def __init__(self, ui, agent0, agent1, rng):
        self.ui = ui
        self.board = Board()
        if rng.uniform() < 0.5:
            self.players = [
                Game.Player(agent0, Board.FieldState.CROSS),
                Game.Player(agent1, Board.FieldState.CIRCLE),
            ]
            self.assigned_markers = [Board.FieldState.CROSS, Board.FieldState.CIRCLE]
        else:
            self.players = [
                Game.Player(agent1, Board.FieldState.CROSS),
                Game.Player(agent0, Board.FieldState.CIRCLE),
            ]
            self.assigned_markers = [Board.FieldState.CIRCLE, Board.FieldState.CROSS]

    def check_state(self):
        # check win
        for row in range(3):
            x = 0
            winning_fields = []
            for col in range(3):
                x += self.board[row][col]
                winning_fields.append((row, col))
            if x == 3:
                return (Game.GameState.WIN, Board.FieldState.CROSS, winning_fields)
            elif x == -3:
                return (Game.GameState.WIN, Board.FieldState.CIRCLE, winning_fields)

        for col in range(3):
            x = 0
            winning_fields = []
            for row in range(3):
                x += self.board[row][col]
                winning_fields.append((row, col))
            if x == 3:
                return (Game.GameState.WIN, Board.FieldState.CROSS, winning_fields)
            elif x == -3:
                return (Game.GameState.WIN, Board.FieldState.CIRCLE, winning_fields)

        x = 0
        winning_fields = []
        for idx in range(3):
            x += self.board[idx][idx]
            winning_fields.append((idx, idx))
        if x == 3:
            return (Game.GameState.WIN, Board.FieldState.CROSS, winning_fields)
        elif x == -3:
            return (Game.GameState.WIN, Board.FieldState.CIRCLE, winning_fields)

        x = 0
        winning_fields = []
        for idx in range(3):
            x += self.board[idx][2 - idx]
            winning_fields.append((idx, 2 - idx))
        if x == 3:
            return (Game.GameState.WIN, Board.FieldState.CROSS, winning_fields)
        elif x == -3:
            return (Game.GameState.WIN, Board.FieldState.CIRCLE, winning_fields)

        # check draw
        x = 0
        for row in range(3):
            for col in range(3):
                x += abs(self.board[row][col])
        if x == 9:
            return (Game.GameState.DRAW, None, None)

        return (Game.GameState.RUNNING, None, None)

    def play(self):
        done = False
        while not done:
            for p in self.players:
                while True:
                    move = p.get_move(self.ui, self.board)
                    if move is None:
                        self.ui.warn("Invalid move. Must be of the form `<row>,<col>`.")
                        continue
                    row, col = move
                    if row < 0 or row > 2:
                        self.ui.warn("Invalid move. Row must be in [0, 2].")
                        continue
                    if col < 0 or col > 2:
                        self.ui.warn("Invalid move. Column must be in [0, 2].")
                        continue
                    if not self.board.is_empty(row, col):
                        self.ui.warn("Invalid move. Position already occupied.")
                        continue
                    break  # can only be reached if input is valid
                self.board.mark(row, col, p.marker)

                (state, winner, winning_fields) = self.check_state()
                if state != Game.GameState.RUNNING:
                    done = True
                    break
        return (state, winner, winning_fields)
