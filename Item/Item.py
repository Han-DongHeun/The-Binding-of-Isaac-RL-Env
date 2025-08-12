# Item.py
# Aaron Taylor
# Moose Abumeeiz
#
# The parent item class is ready to render items on the ground
# 

from pygame import *
from utils.const import *
from utils.Animation import *
import utils.func as func

class Item:
	"""Main item class"""

	collideable = False
	pickedUp = False

	price = 0

	def __init__(self, xy, sound, textures):
		self.x, self.y = xy
		self.sound = sound

		center = (GRIDX + (self.x + 0.5) * GRATIO, GRIDY + (self.y + 0.5) * GRATIO)

		if type(textures) == list:
			self.current_frame = 0
			self.frame_interval = 4
			self.anim = textures
			self.bounds = textures[0].get_rect(center=center)
			self.renderf = self.anim_render
		else:
			self.texture = textures
			self.bounds = textures.get_rect(center=center)
			self.renderf = self.texture_render

	def pickup(self):
		self.pickedUp = True
		if self.sound != None:
			self.sound.play()

	def render(self, surface, ox=0, oy=0):
		if self.pickedUp:
			return False
		self.renderf(surface, ox, oy)
		return True

	def texture_render(self, surface, ox=0, oy=0):
		surface.blit(self.texture, self.bounds.move(ox, oy))
	
	def anim_render(self, surface, ox=0, oy=0):
		frame_idx = self.current_frame // self.frame_interval % len(self.anim)
		surface.blit(self.anim[frame_idx], self.bounds.move((ox, oy)))