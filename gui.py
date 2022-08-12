import numpy as np

from q_learning_agent import QLearningAgent
from game import Game
from board import Board

import PySimpleGUI as sg
from img import icons
import base64
from io import BytesIO
from PIL import Image
import time

# from duel import duel
from lang import lang_DE

LANG_DICT = lang_DE


class GUI:
    def __init__(self):
        self.create_blank_icon()

        sg.theme("Black")  # Keep things interesting for your users
        sg.set_options(font=("DejaVu Sans Mono", 54))

        layout = self.create_layout()

        self.window = sg.Window(
            "Tic Tac Toe", layout, margins=(0, 0), background_color="#000",
        )
        self.window.Read(timeout=0.001)
        self.show_new_game()

    @staticmethod
    def create_blank_icon():
        buffer = BytesIO(base64.b64decode(icons.o))
        width, height = Image.open(buffer).size

        # Create a blank image
        icons.blank = Image.new("RGBA", (width, height), "#ffffff00")
        # convert to base64
        with BytesIO() as output:
            icons.blank.save(output, format="PNG")
            icons.blank = output.getvalue()

    @staticmethod
    def create_layout():
        game_column = [
            [
                sg.Button(
                    "",
                    image_data=icons.blank,
                    key=(j, i),
                    metadata=False,
                    pad=(10, 10),
                    mouseover_colors="white",
                )
                for i in range(3)
            ]
            for j in range(3)
        ]

        score_column = [
            [sg.Text("title str", size=(20, 1), key="-TITLE_TEXT-")],
            [sg.Text("subtitle str", size=(20, 1), key="-SUBTITLE_TEXT-")],
            [sg.Text("", size=(20, 3), font=("DejaVu Sans Mono", 28), key="-WARN_TEXT-")],
            [sg.Image("", key="-PLAYER0_IMG-")],
            [sg.Text("0", size=(20, 1), key="-PLAYER0_TEXT-"), sg.Text("", size=(5, 1), key="-PLAYER0_SCORE-")],
            [sg.Image("", key="-PLAYER1_IMG-")],
            [sg.Text("0", size=(20, 1), key="-PLAYER1_TEXT-"), sg.Text("", size=(5, 1), key="-PLAYER1_SCORE-")],
        ]

        return [
            [sg.Column(game_column), sg.Column(score_column, justification="center"),]
        ]

    def show_board(self, board, winning_fields=None):
        for row in range(3):
            for col in range(3):
                label = Board.field_state_to_str_map[board[row][col]]
                if label == "_":
                    icon = icons.blank
                elif label == "x":
                    if winning_fields and (row, col) in winning_fields:
                        icon = icons.x_inv
                    else:
                        icon = icons.x
                elif label == "o":
                    if winning_fields and (row, col) in winning_fields:
                        icon = icons.o_inv
                    else:
                        icon = icons.o
                self.window[(row, col)].update(image_data=icon)
        self.window.Refresh()

    def show_new_game(self):
        self.write("New game", "-TITLE_TEXT-")
        self.write("", "-SUBTITLE_TEXT-")

    def blink(self, board, winning_fields):
        for i in range(2):
            self.show_board(board, winning_fields=winning_fields)
            time.sleep(0.3)
            self.show_board(board, winning_fields=None)
            time.sleep(0.3)
        self.show_board(board, winning_fields=winning_fields)

    def listen_input(self, _):
        event, values = self.window.Read()
        self.warn("")
        return event

    def show_scores(self, scores):
        self.write(str(scores[0]), "-PLAYER0_SCORE-")
        self.write(str(scores[1]), "-PLAYER1_SCORE-")

    def show_final_state(self, board, state, winner, winning_fields):
        if winner is not None:
            winner_str = board.field_state_to_str_map[winner]
            self.write("Winner: " + winner_str, "-TITLE_TEXT-")
            self.write("", "-SUBTITLE_TEXT-")
            self.blink(board, winning_fields)
        else:
            self.write("Draw", "-TITLE_TEXT-")
            self.write("", "-SUBTITLE_TEXT-")
            self.show_board(board)

    def show_image(self, fn, key):
        self.window[key].update(fn)
        self.window.Refresh()

    def warn(self, text):
        self.write(text, "-WARN_TEXT-", text_color="#ff0000")

    def write(self, text, key, *, text_color="#ffffff"):
        self.window[key].update(text, text_color=text_color)
        self.window.Refresh()

    def __del__(self):
        if self.window:
            self.window.close()
