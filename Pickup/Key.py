# Key.py
# Aaron Taylor
# Moose Abumeeiz
#
# The class for the key that you can pickup.
# The key can be used to unlock rooms such as Pickup rooms and shops.
# 

from pygame import *
from Pickup.Pickup import *
from utils.loadResource import textures, sounds 

class Key(Pickup):
	"""Pickup Key class"""

	variant = 0
	texture = textures["keys"]
	sound = sounds["keyPickup"]