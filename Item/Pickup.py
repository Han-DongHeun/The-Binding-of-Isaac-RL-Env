# Pickup.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is the class for the HUD pickups (keys, bombs, coins)
# 

from pygame import *

class Pickup:
	"""The class for the HUD pickup counters"""

	def __init__(self, variant, textures, font):
		self.variant = variant
		self.score = 0
		self.font = font

		xPos = 0
		yPos = 16 * self.variant

		if variant == 2:
			xPos = 16
			yPos = 0

		self.texture = textures.subsurface(Rect(xPos*2, yPos*2, 16*2, 16*2))
		self.updateDigits()

	def updateDigits(self):
		# Update textures for digits
		self.digit1 = self.font[self.score // 10]
		self.digit2 = self.font[self.score % 10]

	def add(self, ammount):
		self.score = min(99, self.score + ammount)
		self.updateDigits()

	def use(self, ammount):
		if self.score < ammount:
			return False
		
		self.score -= ammount
		self.updateDigits()
		return True

	def render(self, surface):
		# Blit icon, digit1, and digit 2
		surface.blit(self.texture, (40, 88 + 24*self.variant))
		surface.blit(self.digit1, (68, 94 + 24*self.variant))
		surface.blit(self.digit2, (80, 94 + 24*self.variant))