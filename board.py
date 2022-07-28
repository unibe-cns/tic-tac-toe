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
        self.fields = self.initial_state()

    def __repr__(self):
        s = ""
        for row in range(3):
            for col in range(3):
                s += self.field_state_to_str_map[self.fields[row][col]]
                if col < 2:
                    s += " "
            s += "\n"
        return s

    def __getitem__(self, row):
        return self.fields[row]

    def initial_state(self):
        return [
            [Board.FieldState.EMPTY, Board.FieldState.EMPTY, Board.FieldState.EMPTY],
            [Board.FieldState.EMPTY, Board.FieldState.EMPTY, Board.FieldState.EMPTY],
            [Board.FieldState.EMPTY, Board.FieldState.EMPTY, Board.FieldState.EMPTY],
        ]

    def is_empty(self, row, col):
        return self.fields[row][col] == Board.FieldState.EMPTY

    def mark(self, row, col, field_state):
        assert self.is_empty(row, col)
        self.fields[row][col] = field_state

    def state_hash(self):
        raw = "".join(str(self.fields[row][col]) for row in range(3) for col in range(3))
        return hashlib.md5(raw.encode("utf8")).hexdigest()

    def rotate_counter_clockwise(self, board):
        rotated_board = Board()
        for row in range(3):
            for col in range(3):
                rotated_board[2 - col][row] = board[row][col]
        return rotated_board

    def mirror_horizontally(self, board):
        mirrored_board = Board()
        mirrored_board.fields[0] = list(board.fields[2])
        mirrored_board.fields[1] = list(board.fields[1])
        mirrored_board.fields[2] = list(board.fields[0])
        return mirrored_board

    def board_symmetries(self, board):
        boards = []
        boards.append(self.rotate_counter_clockwise(board))
        boards.append(self.rotate_counter_clockwise(boards[-1]))
        boards.append(self.rotate_counter_clockwise(boards[-1]))
        boards.append(self.mirror_horizontally(board))
        boards.append(self.rotate_counter_clockwise(boards[-1]))
        boards.append(self.rotate_counter_clockwise(boards[-1]))
        boards.append(self.rotate_counter_clockwise(boards[-1]))
        return boards

    def rotate_move_counter_clockwise(self, move):
        row = 2 - move[1]
        col = move[0]
        return (row, col)

    def mirror_move_horizontally(self, move):
        row = 2 - move[0]
        col = move[1]
        return (row, col)

    def move_symmetries(self, move):
        moves = []
        moves.append(self.rotate_move_counter_clockwise(move))
        moves.append(self.rotate_move_counter_clockwise(moves[-1]))
        moves.append(self.rotate_move_counter_clockwise(moves[-1]))
        moves.append(self.mirror_move_horizontally(move))
        moves.append(self.rotate_move_counter_clockwise(moves[-1]))
        moves.append(self.rotate_move_counter_clockwise(moves[-1]))
        moves.append(self.rotate_move_counter_clockwise(moves[-1]))
        return moves
