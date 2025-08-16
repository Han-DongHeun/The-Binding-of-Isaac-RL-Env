# Coin.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is the class for the coin that you can pickup in a room
# 

from pygame import *
from utils.const import *
from utils.loadResource import textures, sounds 
from Pickup.Pickup import *

class Coin(Pickup):
	"""Pickup coin class"""

	variant = 0
	coin_type = ("dime", "nickel", "penny")[variant]
	texture = textures['coins'][coin_type][0]
	sound = sounds["coinPickup"]

	worth = (1, 5, 10)[variant]