# Heart.py
# Aaron Taylor
# Moose Abumeeiz
#
# The heart can be rendered on the floor or on the HUD.
# Taking damage will result in half of a heart loss.
# 

from pygame import *
from utils.const import *
from Pickup.Pickup import *
import utils.func as func

from utils.loadResource import textures, sounds

class Heart(Pickup):
	"""Pickup Heart class"""

	health = 2

	variant = 0
	sound = sounds["heartIntake"]
	texture = textures["pickupHearts"][variant]

class UIHeart:
	"""Class for a UI heart"""

	# HEART VARIANTS:
	# 
	# 0 - Red heart
	# 1 - Soul heart
	# 2 - Black heart
	# 3 - Eternal heart

	# NOTE: After 6 hears, they go down a level on the GUI

	textures = textures["hearts"]

	def __init__(self, variant, health):
		self.variant = variant
		self.health = health
		self.capacity = 2 # Maximum ammount of health per heart
		self.textures = self.textures[variant]

	def damage(self, ammount):
		# Damage is taken to this heart

		if self.health-ammount < 0:
			return ammount - self.health
		self.health -= ammount

		return self.health <= 0 and self.variant != 0 # Wether heart should be destroyed

	def add(self, ammount):
		self.health += ammount

		leftover = 0 # The leftover health points

		if self.health > self.capacity: # Max heart ammount
			leftover = self.health - self.capacity
			self.health = self.capacity

		return leftover # How many health points should carry over

	def render(self, surface, index):
		if not HUMAN_MODE:
			return
		
		# Render the heart to the display
		surface.blit(self.textures[self.health], ((120 + 24 * index) * SIZING, 30 * SIZING))
