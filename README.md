# Q-learning for Tic-tac-toe

A simple implementation of Tic-tac-toe (`board.py`, `game.py`), and an agent learning to play via Q-learning (`agent.py`).

# Installation

To download, open a terminal and run
```
https://github.com/unibe-cns/tic-tac-toe
```
or download the zip (top right -> Code -> Download ZIP) and unpack.

# Starting a game

To start a game against an agent trained via self-play, open the folder of the game in a terminal and execute `python main.py`.

# Instructions

Play a game by clicking (or tapping, on touch devices) on a free field.
The bot starts on the easiest level with no experience.
After every time the player wins against the bot, the difficulty is increased by loading a bot that has trained for longer.
If the bot wins, the game is reset.

# Notes

Only tested under Linux, currently not compatible with MacOS.
