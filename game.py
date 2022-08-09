import enum
import numpy as np

from board import Board
import time


class Player:
    def __init__(self, agent, marker, gui=None):
        self.agent = agent
        self.marker = marker
        self.move_history = []

    def get_move(self, board):
        move = self.agent.get_move(board, self.marker)
        self.move_history.append((board.to_str(), move))
        return move

    def update_policy(self, final_reward):
        self.agent.update_policy(final_reward, self.move_history, self.marker)


class Game:
    @enum.unique
    class GameState(enum.Enum):
        RUNNING = 0
        DRAW = 1
        WIN = 2

    def __init__(self, agent1, agent2, rng):
        self.board = Board()
        if rng.uniform() < 0.5:
            self.players = [
                Player(agent1, Board.FieldState.CROSS),
                Player(agent2, Board.FieldState.CIRCLE),
            ]
            self.assigned_markers = [Board.FieldState.CROSS, Board.FieldState.CIRCLE]
        else:
            self.players = [
                Player(agent2, Board.FieldState.CROSS),
                Player(agent1, Board.FieldState.CIRCLE),
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

    def play(self, verbose=False):
        done = False
        while not done:
            for p in self.players:
                # check if player returns legal move
                move_done = False
                while not move_done:
                    move = p.get_move(self.board)
                    if move is not None:
                        break
                self.board.mark(move[0], move[1], p.marker)
                # if hasattr(p.agent.gui, 'update_game_state'):
                #     p.agent.gui.update_game_state(self.board)
                #     time.sleep(.1)

                (state, winner, winning_fields) = self.check_state()
                if state != Game.GameState.RUNNING:
                    done = True
                    if verbose:
                        print(self.board)
                        print(state, winner)
                    break

        return (state, winner, winning_fields)
