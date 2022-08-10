import matplotlib.pyplot as plt
import numpy as np
import __main__ as main

from agent import Agent
from game import Game
from board import Board

import PySimpleGUI as sg
from img import icons
import base64
from io import BytesIO
from PIL import Image 
import time


from lang import lang_DE
LANG_DICT = lang_DE

# def convert_str_to_


class gui():

    def update_game_state(self, board, winning_fields=None):
        # print("received board:", board)
        self.board = board
        for row in range(3):
            for col in range(3):
                label = Board.field_state_to_str_map[self.board[row][col]]

                if label == "_":
                    icon = icons.blank
                elif label == "x":
                    if winning_fields and (row,col) in winning_fields:
                        icon = icons.x_inv
                    else:
                        icon = icons.x
                elif label == "o":
                    if winning_fields and (row,col) in winning_fields:
                        icon = icons.o_inv
                    else:
                        icon = icons.o
                self.window[(row,col)].update(image_data=icon)
        self.window.Refresh()
        
    def blink(self, board, winning_fields):
        for i in range(2):
            self.update_game_state(board, winning_fields=winning_fields)
            time.sleep(.3)
            self.update_game_state(board, winning_fields=None)
            time.sleep(.3)
        self.update_game_state(board, winning_fields=winning_fields)
        

    def update_top_message(self, message):
        if message in ['new_game', 'bot_wins', 'player_wins', 'draw']:
            message = LANG_DICT[message]
        self.window['-HEAD_TEXT-'].update(message)
        self.window.Refresh()
        
    def update_level_text(self, level):
        self.level = level
        self.window['-LEVEL_TEXT-'].update(LANG_DICT['level'] + ' ' + f"{level:.1f}")
        self.window.Refresh()

    def listen_input(self):
        event, values = self.window.Read()
        # print(event, values)
        return event

    def write(self, message):
        print(message)
        self.update_top_message(message)


    def gui_duel(self, agent, opponent, no_episodes, rng, *, verbose=False):

        buffer = BytesIO(base64.b64decode(icons.o))
        width, height = Image.open(buffer).size

        # Create a blank image
        icons.blank = Image.new("RGBA", (width, height), "#ffffff00")
        # convert to base64
        with BytesIO() as output:
            icons.blank.save(output, format="PNG")
            icons.blank = output.getvalue()

        sg.theme('Black')    # Keep things interesting for your users
        sg.set_options(font=("DejaVu Sans Mono", 54))
        
        game_column =  [[sg.Button("", image_data=icons.blank, key=(j, i), metadata=False, pad=(10,10), mouseover_colors='white') for i in range(3)] for j in range(3)]
            
        self.level = 0.1
        level_str = LANG_DICT['level'] + ' ' + str(self.level)
        head_str = LANG_DICT['new_game']
        
        score_column =  [
                       [sg.Text(head_str, size=(len(head_str)+5,1), key='-HEAD_TEXT-')],
                       [sg.Text('')],
                       [sg.Image('img/bot.png')],
                       [sg.Text(level_str, size=(len(level_str),1), key='-LEVEL_TEXT-')]
                   ]
        
                        

        self.layout = [
                        [
                            sg.Column(game_column),
                            sg.Column(score_column, justification='center'),
                        ]
                      ]
        
        


        self.window = sg.Window(LANG_DICT['game_title'], self.layout, margins=(0, 0), background_color='#000')

        # a modified version of main.duel with GUI implementation
        history_result = []
        while True:             # Event Loop

            # if game is not None:
            #     HEAD_TEXT = 'NEW TITLE'

            event, values = self.window.Read(timeout=1)
            #self.window['-HEAD_TEXT-'].update('Neues Spiel')

            _ = main.duel(agent, opponent, no_episodes, rng, verbose=verbose, print_file=self)

            # (state, winner) = game.play(verbose)

            # if event in (None, 'Exit'):
            #     break
            # if callable(event):
            #     event()
            # window['-HEAD_TEXT-'].update(HEAD_TEXT)

        window.close()







        
        

        # if state == Game.GameState.DRAW:
        #     history_result.append(0.0)
        #     for p in game.players:
        #         final_reward = 0.0
        #         p.update_policy(final_reward)
        # else:
        #     if winner == game.assigned_markers[0]:
        #         history_result.append(1.0)
        #     else:
        #         history_result.append(-1.0)
        #     for p in game.players:
        #         if winner == p.marker:
        #             final_reward = 1.0
        #         else:
        #             final_reward = -1.0
        #         p.update_policy(final_reward)

        # if episode > 0 and episode % 1000 == 0:
        #     print(episode)
