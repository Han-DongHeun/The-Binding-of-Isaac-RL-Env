# main.py
# Aaron Taylor
# Moose Abumeeiz
#
# The main file for our final project. This is a replica of
# the popular game The Binding waof Isaac: Rebirth.
# 

import os

from pygame import *

from utils.const import *

init()
screen = display.set_mode((WIDTH, HEIGHT))

def playMusic(name, sound_on=HUMAN_MODE):
	if sound_on == False:
		return
	mixer.music.load(os.path.join('res', 'music', name))
	mixer.music.play(-1)

# Setup display
display.set_caption("The Binding of Isaac: Rebirth")
display.set_icon(image.load(os.path.join('res', 'textures', 'icon.png')))

from Game import Game

# Begin main loop
running = True
while running:
	# Start by playing the title screen music
	playMusic("titleScreenLoop.ogg")

	# Play the normal game music
	playMusic("basementLoop.ogg")

	# Start game
	game = Game(screen)
	game.run()

quit()