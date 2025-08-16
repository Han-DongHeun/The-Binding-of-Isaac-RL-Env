# Bomb.py
# Aaron Taylor
# Moose Abumeeiz
#
# Bombs can be dropped or picked up, they will hurt enemies in range
# 

from pygame import *
from math import *
from utils.Animation import *
from Pickup.Pickup import *
from utils.loadResource import textures, sounds

class Bomb(Pickup):
	"""Droppable bomb class"""

	exploded = False
	fuse = 2

	texture = textures["bombs"]["bombs"]

	def pickup(self):
		self.pickedUp = True