# const.py
# Aaron Taylor
# Moose Abumeeiz
#
# This file stores all of the constant information for the game, such as width
# and height of the window.

WIDTH  = 960
HEIGHT = 540

WSIZE = WIDTH // 960
HSIZE = HEIGHT // 540

GRATIO = 52 # Pixels/Grid size
GRIDX, GRIDY = 142, 88

GRATIO = min(WIDTH // (13 + 3), HEIGHT // (7 + 3))
GRATIO -= GRATIO & 1
GRIDX = (WIDTH - GRATIO * 13) // 2
GRIDY = (HEIGHT - GRATIO * 7) // 2

SIZING = GRATIO / 52

HUMAN_MODE = False