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

        # self.level = 0.1
        level = 0.1
        level_str = LANG_DICT["level"] + " " + str(level)
        head_str = LANG_DICT["new_game"]

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
            [sg.Text(head_str, size=(len(head_str) + 5, 1), key="-HEAD_TEXT-")],
            [sg.Text("")],
            [sg.Image("img/bot.png")],
            [sg.Text(level_str, size=(len(level_str), 1), key="-LEVEL_TEXT-")],
        ]

        layout = [
            [sg.Column(game_column), sg.Column(score_column, justification="center"),]
        ]

        self.window = sg.Window(
            LANG_DICT["game_title"], layout, margins=(0, 0), background_color="#000",
        )
        self.window.Read(timeout=0.001)

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

    def show_board(self, board, winning_fields=None):
        # print("received board:", board)
        self.board = board
        for row in range(3):
            for col in range(3):
                label = Board.field_state_to_str_map[self.board[row][col]]
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

    def blink(self, board, winning_fields):
        for i in range(2):
            self.show_board(board, winning_fields=winning_fields)
            time.sleep(0.3)
            self.show_board(board, winning_fields=None)
            time.sleep(0.3)
        self.show_board(board, winning_fields=winning_fields)

    def update_top_message(self, message):
        if message in ["new_game", "bot_wins", "player_wins", "draw"]:
            message = LANG_DICT[message]
        self.window["-HEAD_TEXT-"].update(message)
        self.window.Refresh()

    def update_level_text(self, level):
        # self.level = level
        self.window["-LEVEL_TEXT-"].update(LANG_DICT["level"] + " " + f"{level:.1f}")
        self.window.Refresh()

    def listen_input(self, _):
        event, values = self.window.Read()
        # print(event, values)
        return event

    def write(self, message):
        # print(message)
        self.update_top_message(message)

    # def gui_duel(self, agent, opponent, no_episodes, rng, *, verbose=False):
    #     # a modified version of main.duel with GUI implementation
    #     history_result = []
    #     while True:  # Event Loop

    #         # if game is not None:
    #         #     HEAD_TEXT = 'NEW TITLE'

    #         event, values = self.window.Read(timeout=1)
    #         # self.window['-HEAD_TEXT-'].update('Neues Spiel')

    #         _ = duel(
    #             agent, opponent, no_episodes, rng, verbose=verbose, print_file=self
    #         )

    #         # (state, winner) = game.play(verbose)

    #         # if event in (None, 'Exit'):
    #         #     break
    #         # if callable(event):
    #         #     event()
    #         # window['-HEAD_TEXT-'].update(HEAD_TEXT)

    #     window.close()
    #

    def show_final_state(self, board, state, winner, winning_fields):
        if winner is not None:
            winner_str = board.field_state_to_str_map[winner]
            self.update_top_message(winner_str + " wins")
            self.blink(board, winning_fields)
        else:
            self.update_top_message("draw")
        time.sleep(2.0)
        self.update_top_message("new_game")

    def __del__(self):
        self.window.close()
