# Game.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is the main game class (not including menu)
# It is responsible for rendering the floor and the character.
# 

import numpy as np

from pygame import *

from Env import IsaacEnv

class Game:

	controls = [K_s, K_d, K_w, K_a, K_DOWN, K_RIGHT, K_UP, K_LEFT, K_e]

	clock = time.Clock()

	def __init__(self, screen):
		self.game = IsaacEnv()
		self.game.screen = screen
                
	def run(self):
		done = False

		while not done:
			for e in event.get():
				if e.type == QUIT:
					quit()

			keys = key.get_pressed()
			actions = np.fromiter([keys[cn] for cn in self.controls], np.bool)
			_, done = self.game.step(actions)

			display.flip()

			self.clock.tick(60)