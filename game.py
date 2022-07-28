import enum
import numpy as np

from board import Board


class Player:
    def __init__(self, agent, marker):
        self.agent = agent
        self.marker = marker
        self.move_history = []

    def get_move(self, board):
        move = self.agent.get_move(board, self.marker)
        self.move_history.append((board.clone(), move))
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
        if rng.rand() < 0.5:
            self.players = [
                Player(agent1, Board.FieldState.SQUARE),
                Player(agent2, Board.FieldState.CIRCLE),
            ]
            self.assigned_markers = [Board.FieldState.SQUARE, Board.FieldState.CIRCLE]
        else:
            self.players = [
                Player(agent2, Board.FieldState.SQUARE),
                Player(agent1, Board.FieldState.CIRCLE),
            ]
            self.assigned_markers = [Board.FieldState.CIRCLE, Board.FieldState.SQUARE]

    def check_state(self):
        # check win
        for row in range(3):
            x = 0
            for col in range(3):
                x += self.board[row][col]
            if x == 3:
                return (Game.GameState.WIN, Board.FieldState.SQUARE)
            elif x == -3:
                return (Game.GameState.WIN, Board.FieldState.CIRCLE)

        for col in range(3):
            x = 0
            for row in range(3):
                x += self.board[row][col]
            if x == 3:
                return (Game.GameState.WIN, Board.FieldState.SQUARE)
            elif x == -3:
                return (Game.GameState.WIN, Board.FieldState.CIRCLE)

        x = 0
        for idx in range(3):
            x += self.board[idx][idx]
        if x == 3:
            return (Game.GameState.WIN, Board.FieldState.SQUARE)
        elif x == -3:
            return (Game.GameState.WIN, Board.FieldState.CIRCLE)

        x = 0
        for idx in range(3):
            x += self.board[idx][2 - idx]
        if x == 3:
            return (Game.GameState.WIN, Board.FieldState.SQUARE)
        elif x == -3:
            return (Game.GameState.WIN, Board.FieldState.CIRCLE)

        # check draw
        x = 0
        for row in range(3):
            for col in range(3):
                x += abs(self.board[row][col])
        if x == 9:
            return (self.GameState.DRAW, None)

        return (self.GameState.RUNNING, None)

    def play(self, verbose=False):
        done = False
        while not done:
            for p in self.players:
                move = p.get_move(self.board)
                self.board.mark(move[0], move[1], p.marker)

                (state, winner) = self.check_state()
                if state != Game.GameState.RUNNING:
                    done = True
                    if verbose:
                        print(self.board)
                        print(state, winner)
                    break

        return (state, winner)
