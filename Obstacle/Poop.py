# Poop.py
# Aaron Taylor
# Moose Abumeeiz
#
# You can pop poops by shooting them with your tears.
# They will play a pop noise once they are poped.
# 

from pygame import *
from Obstacle.Obstacle import Obstacle
from utils.loadResource import textures, sounds

class Poop(Obstacle):
	"""Main level rock class"""

	health = 4

	frames = textures["poops"][0]
	sound = sounds["pop"]

	def update(self):
		self.texture = self.frames[self.health]