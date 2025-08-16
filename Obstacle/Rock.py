# Rock.py
# Aaron Taylor
# Moose Abumeeiz
#
# The rock can only be destroyed by dropping a bomb near it.
# It will play a noise and will show some broken rock textures.
# 

from pygame import *
from Obstacle.Obstacle import Obstacle
from utils.loadResource import textures, sounds
from random import randint


class Rock(Obstacle):
	"""Main level rock class"""

	rock = textures["rocks"]["rock"]
	broken = textures["rocks"]["broken"]

	destroy_sound = sounds["rockBreak"]

	def __init__(self, gxy):
		super().__init__(gxy)
		variant = randint(0, 2)
		
		self.texture = self.rock[variant]
		
		self.broken = transform.flip(self.broken, randint(0,1), randint(0,1))
		self.broken = transform.rotate(self.broken, randint(0, 360))

	def destroy(self):
		super().destroy()
		self.texture = self.broken