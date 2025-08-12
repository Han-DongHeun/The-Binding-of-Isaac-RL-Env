# Poop.py
# Aaron Taylor
# Moose Abumeeiz
#
# You can pop poops by shooting them with your tears.
# They will play a pop noise once they are poped.
# 

from pygame import *
from utils.const import GRATIO, GRIDX, GRIDY


class Poop:
	"""Main level rock class"""

	# POOP TYPES
	#
	# 0 - Normal
	# 1 - Red
	# 2 - Corny
	# 3 - Golden
	# 4 - Rainbow

	def __init__(self, variant, xy, textures, sound):
		self.variant = variant
		self.x = xy[0]
		self.y = xy[1]

		self.sound = sound

		self.collideable = True

		self.textures = textures[variant]
		self.health = 4
		self.bounds = Rect(GRIDX + GRATIO * self.x, GRIDY + GRATIO * self.y, GRATIO, GRATIO)

		self.texture = self.textures[0]

		# Texture with and height
		self.tWidth = self.texture.get_width()
		self.tHeight = self.texture.get_height()
		self.destroyed = False

	def destroy(self):
		# Poops can be destroyed by tears

		if not self.destroyed:
			self.destroyed = True
			self.texture = self.textures[-1]
			self.sound.play()

	def hurt(self, ammount):
		self.health -= 1
		if self.health < 0:
			self.health = 0

		if self.health == 0:
			self.destroy()

		self.texture = self.textures[4-self.health]

	def render(self, surface, ox=0, oy=0):
		rect = self.bounds.copy()
		rect.x += ox
		rect.y += oy
		surface.blit(self.texture, rect)