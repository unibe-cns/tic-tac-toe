import enum
import hashlib


class Board:
    @enum.unique
    class FieldState(enum.IntEnum):
        EMPTY = 0
        SQUARE = 1
        CIRCLE = -1

    field_state_to_str_map = {
        FieldState.EMPTY: "_",
        FieldState.SQUARE: "x",
        FieldState.CIRCLE: "o",
    }

    def __init__(self):
        self.board = self.initial_board()

    def __repr__(self):
        s = ""
        for row in range(3):
            for col in range(3):
                s += self.field_state_to_str_map[self.board[row][col]]
                if col < 2:
                    s += " "
            s += "\n"
        return s

    def __getitem__(self, row):
        return self.board[row]

    def initial_board(self):
        return [
            [Board.FieldState.EMPTY, Board.FieldState.EMPTY, Board.FieldState.EMPTY],
            [Board.FieldState.EMPTY, Board.FieldState.EMPTY, Board.FieldState.EMPTY],
            [Board.FieldState.EMPTY, Board.FieldState.EMPTY, Board.FieldState.EMPTY],
        ]

    def is_empty(self, row, col):
        return self.board[row][col] == Board.FieldState.EMPTY

    def mark(self, row, col, field_state):
        assert self.is_empty(row, col)
        self.board[row][col] = field_state

    def state_hash(self):
        raw = "".join(str(self.board[row][col]) for row in range(3) for col in range(3))
        return hashlib.md5(raw.encode("utf8")).hexdigest()
