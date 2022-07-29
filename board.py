import copy
import enum


class Board:
    @enum.unique
    class FieldState(enum.IntEnum):
        EMPTY = 0
        SQUARE = 1
        CIRCLE = -1

    str_value_to_state = {str(s.value): s for s in FieldState}

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

    def clone(self):
        board = Board()
        board.fields = copy.deepcopy(self.fields)
        return board

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

    def from_str(self, s):
        s = s.split(",")
        for row in range(3):
            for col in range(3):
                self.fields[row][col] = Board.str_value_to_state[s[row * 3 + col]]

    def to_str(self):
        return ",".join(
            f"{self.fields[row][col].value}" for row in range(3) for col in range(3)
        )

    @staticmethod
    def rotate_counter_clockwise(board):
        rotated_board = Board()
        for row in range(3):
            for col in range(3):
                rotated_board[2 - col][row] = board[row][col]
        return rotated_board

    @staticmethod
    def mirror_horizontally(board):
        mirrored_board = Board()
        mirrored_board.fields[0] = list(board.fields[2])
        mirrored_board.fields[1] = list(board.fields[1])
        mirrored_board.fields[2] = list(board.fields[0])
        return mirrored_board

    @staticmethod
    def board_symmetries():
        symmetries = []
        rcc = Board.rotate_counter_clockwise
        mh = Board.mirror_horizontally
        symmetries.append(lambda b: b)
        symmetries.append(lambda b: rcc(b))
        symmetries.append(lambda b: rcc(rcc(b)))
        symmetries.append(lambda b: rcc(rcc(rcc(b))))
        symmetries.append(lambda b: mh(b))
        symmetries.append(lambda b: rcc(mh(b)))
        symmetries.append(lambda b: rcc(rcc(mh(b))))
        symmetries.append(lambda b: rcc(rcc(rcc(mh(b)))))
        return symmetries

    @staticmethod
    def rotate_move_counter_clockwise(move):
        row = 2 - move[1]
        col = move[0]
        return (row, col)

    @staticmethod
    def mirror_move_horizontally(move):
        row = 2 - move[0]
        col = move[1]
        return (row, col)

    @staticmethod
    def move_symmetries():
        symmetries = []
        rmcc = Board.rotate_move_counter_clockwise
        mmh = Board.mirror_move_horizontally
        symmetries.append(lambda m: m)
        symmetries.append(lambda m: rmcc(m))
        symmetries.append(lambda m: rmcc(rmcc(m)))
        symmetries.append(lambda m: rmcc(rmcc(rmcc(m))))
        symmetries.append(lambda m: mmh(m))
        symmetries.append(lambda m: rmcc(mmh(m)))
        symmetries.append(lambda m: rmcc(rmcc(mmh(m))))
        symmetries.append(lambda m: rmcc(rmcc(rmcc(mmh(m)))))
        return symmetries
