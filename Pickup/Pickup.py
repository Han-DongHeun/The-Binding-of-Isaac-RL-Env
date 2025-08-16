# Item.py
# Aaron Taylor
# Moose Abumeeiz
#
# The parent item class is ready to render items on the ground
# 

from pygame import *
from utils.const import *
from utils.Animation import *
from utils.func import get_center

class Pickup:
	"""Main item class"""

	collideable = False
	pickedUp = False

	price = 0

	""" current_frame = 0
	frame_interval = 4

	renderf = None """

	texture = None
	sound = None

	def __init__(self, gxy):
		self.gx, self.gy = gxy

		center_x, center_y = get_center(*gxy)
		self.bounds = Rect(center_x - 8, center_y - 8, 16, 16)
		print(self)
		self.rect = self.texture.get_rect(center=(center_x, center_y))

	def pickup(self):
		self.pickedUp = True
		if self.sound != None:
			self.sound.play()

	def render(self, surface, ox=0, oy=0):
		surface.blit(self.texture, self.rect.move(ox, oy))
	
	""" def anim_render(self, surface, ox=0, oy=0):
		frame_idx = self.current_frame // self.frame_interval % len(self.anim)
		surface.blit(self.anim[frame_idx], self.bounds.move((ox, oy))) """