# Key.py
# Aaron Taylor
# Moose Abumeeiz
#
# The class for the key that you can pickup.
# The key can be used to unlock rooms such as item rooms and shops.
# 

from pygame import *
from utils.const import *
from utils.Animation import *
from Item.Item import *

class Key(Item):
	"""Pickup Key class"""

	def __init__(self, variant, xy, sounds, textures):
		sound = sounds[1]
		texture = textures
		super().__init__(xy, sound, texture)

		self.variant = variant