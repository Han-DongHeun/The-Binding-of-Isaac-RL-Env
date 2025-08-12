# Bomb.py
# Aaron Taylor
# Moose Abumeeiz
#
# Bombs can be dropped or picked up, they will hurt enemies in range
# 

from pygame import *
from math import *
from utils.Animation import *
from Item.Item import *

class Bomb(Item):
	"""Droppable bomb class"""

	exploded = False
	fuse = 2

	def __init__(self, variant, xy, sound, textures):
		super().__init__(xy, sound, textures["bombs"])
		self.variant = variant

	def pickup(self):
		self.pickedUp = True