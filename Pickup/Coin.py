# Coin.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is the class for the coin that you can pickup in a room
# 

from pygame import *
from utils.const import *
from utils.Animation import *
from Pickup.Pickup import *

class Coin(Pickup):
	"""Pickup coin class"""

	def __init__(self, variant, xy, sounds, textures):
		coin_type = ("dime", "nickel", "penny")[variant]
		self.anim = textures[coin_type]
		self.anim = [self.anim[0]] * 16 + self.anim
		super().__init__(xy, sounds[1], self.anim)
		self.variant = variant
		self.worth = [1, 5, 10][variant]