# main.py
# Aaron Taylor
# Moose Abumeeiz
#
# The main file for our final project. This is a replica of
# the popular game The Binding waof Isaac: Rebirth.
# 

from utils.const import *
from pygame import *
init()
screen = display.set_mode((WIDTH, HEIGHT))

from utils.loadResource import *
from random import *
from utils.func import *
from Game import *
from Menu.menu import *
import os


# Create display


def playMusic(name, sound_on=HUMAN_MODE):
	if sound_on == False:
		return
	mixer.music.load(os.path.join('res', 'music', name))
	mixer.music.play(-1)

# Setup display
display.set_caption("The Binding of Isaac: Rebirth")
display.set_icon(image.load(os.path.join('res','textures', 'icon.png')))





# Load fonts
fonts = {
	"main": loadCFont("main.png", 20, 16, 36, size=1.8),
	"pickups": loadCFont("pickup.png", 10, 12, 10),
	"ticks": loadCFont("ticks.png", 4, 17 , 8),
}

# Begin main loop
running = True
while running:
	# Start by playing the title screen music
	playMusic("titleScreenLoop.ogg")

	# Begin menu
	characterType, controls, floorSeed = menu(screen, sounds)
	characterType = ("lazarus", "isaac", "eve")[characterType]

	# Floor setup
	seed(floorSeed)

	# Play the normal game music
	playMusic("basementLoop.ogg")

	# Start game
	game = Game(characterType, controls, floorSeed)
	game.run(screen, sounds, textures, fonts)

quit()