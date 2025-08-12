# Rock.py
# Aaron Taylor
# Moose Abumeeiz
#
# The rock can only be destroyed by dropping a bomb near it.
# It will play a noise and will show some broken rock textures.
# 

from pygame import *
from random import *
from utils.const import GRATIO, GRIDX, GRIDY
from utils.func import get_center


class Rock:
	"""Main level rock class"""

	def __init__(self, variant, xy, special, sound, textures):
		self.variant = variant
		self.x = xy[0]
		self.y = xy[1]
		self.special = special

		self.collideable = True

		self.sound = sound
		self.texture = textures["rock"][variant]
		self.brokenTexture = textures["broken"]
		self.brokenTexture = transform.flip(self.brokenTexture, randint(0,1), randint(0,1))
		self.brokenTexture = transform.rotate(self.brokenTexture, randint(0, 360))
		self.bounds = Rect(GRIDX + GRATIO * self.x, GRIDY + GRATIO * self.y, GRATIO, GRATIO)
		self.rect = self.texture.get_rect(center=get_center(*xy))

		# self.texture = textures[variant] if not special else textures[0] # TODO: SPECIAL INDEX

		self.tWidth = self.texture.get_width()
		self.tHeight = self.texture.get_height()
		self.destroyed = False

	def destroy(self):
		if not self.destroyed:
			if self.special:
				# TODO: TAKE CARE OF DROPS
				pass

			# Destroy and change texture of the rock + sound
			self.destroyed = True
			self.texture = self.brokenTexture
			self.sound.stop()
			self.sound.play()

	def hurt(self, ammount):
		pass

	def render(self, surface, ox=0, oy=0):
		surface.blit(self.texture, self.rect.move((ox, oy)))