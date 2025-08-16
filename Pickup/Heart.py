# Heart.py
# Aaron Taylor
# Moose Abumeeiz
#
# The heart can be rendered on the floor or on the HUD.
# Taking damage will result in half of a heart loss.
# 

from pygame import *
from utils.const import *
from utils.Animation import *
from Pickup.Pickup import *
import utils.func as func

class Heart(Pickup):
	"""Pickup Heart class"""

	health = 2
	
	def __init__(self, variant, xy, sound, textures):
		sound = sound[[0,1,0][variant]]
		super().__init__(xy, sound, textures[variant])

		self.variant = variant

class UIHeart:
	"""Class for a UI heart"""

	# HEART VARIANTS:
	# 
	# 0 - Red heart
	# 1 - Soul heart
	# 2 - Black heart
	# 3 - Eternal heart

	# NOTE: After 6 hears, they go down a level on the GUI

	def __init__(self, variant, health, hearts):
		self.variant = variant
		self.health = health
		self.capacity = 2 # Maximum ammount of health per heart
		self.hearts = hearts
		self.updateImage()

	def updateImage(self):
		size = 16*2
		xPos = [0, 0, 32*2, 49*2] # The x positions of heart textures

		if self.variant in [1, 2]:
			# It is a Soul or Black heart
		
			yPos = size
		else:
			# It is a Red or Eternal heart

			yPos = 0

		xOffset = 0

		# Position on screen
		if self.health == 0:
			xPos = 32*2
			yPos = 0
		elif self.health == 1:
			xOffset = size
			xPos = xPos[self.variant]
		else:
			xPos = xPos[self.variant]

		self.image = self.hearts.subsurface(Rect(xPos + xOffset, yPos, size, size))


	def damage(self, ammount):
		# Damage is taken to this heart

		if self.health-ammount < 0:
			return ammount - self.health
		self.health -= ammount

		self.updateImage()

		return self.health <= 0 and self.variant != 0 # Wether heart should be destroyed

	def add(self, ammount):
		self.health += ammount

		leftover = 0 # The leftover health points

		if self.health > self.capacity: # Max heart ammount
			leftover = self.health - self.capacity
			self.health = self.capacity

		self.updateImage()

		return leftover # How many health points should carry over

	def render(self, surface, index):
		# Render the heart to the display

		surface.blit(self.image, (120 + 24*index - (0 if index < 6 else 24*6), 30 + (0 if index < 6 else 24)))
