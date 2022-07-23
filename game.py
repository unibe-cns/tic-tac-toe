import enum


class Game:
    @enum.unique
    class GameState(enum.Enum):
        RUNNING = 0
        DRAW = 1
        SQUARE_WON = 2
        CIRCLE_WON = 3

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

    str_to_field_state_map = {
        value: key for key, value in field_state_to_str_map.items()
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

    def initial_board(self):
        return [
            [self.FieldState.EMPTY, self.FieldState.EMPTY, self.FieldState.EMPTY],
            [self.FieldState.EMPTY, self.FieldState.EMPTY, self.FieldState.EMPTY],
            [self.FieldState.EMPTY, self.FieldState.EMPTY, self.FieldState.EMPTY],
        ]

    def mark(self, row, col, marker):
        self.board[row][col] = self.str_to_field_state_map[marker]

    def check_state(self):

        # check draw
        x = 0
        for row in range(3):
            for col in range(3):
                x += abs(self.board[row][col])
        if x == 9:
            return self.GameState.DRAW

        # check win
        def check_win_condition(x):
            if x == 3:
                print("Square won. exiting.")
                exit()
            elif x == -3:
                print("Circle won. exiting.")
                exit()

        for row in range(3):
            x = 0
            for col in range(3):
                x += self.board[row][col]
            if x == 3:
                return self.GameState.SQUARE_WON
            elif x == -3:
                return self.GameState.CIRCLE_WON

        for col in range(3):
            x = 0
            for row in range(3):
                x += self.board[row][col]
            if x == 3:
                return self.GameState.SQUARE_WON
            elif x == -3:
                return self.GameState.CIRCLE_WON

        x = 0
        for idx in range(3):
            x += self.board[idx][idx]
        if x == 3:
            return self.GameState.SQUARE_WON
        elif x == -3:
            return self.GameState.CIRCLE_WON

        return self.GameState.RUNNING
