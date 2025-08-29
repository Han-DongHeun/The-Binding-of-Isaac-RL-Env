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
from utils.loadResource import textures, fonts

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
	
class UIPickup:
	"""The class for the HUD pickup counters"""

	font = fonts["pickups"]

	def __init__(self, idx, name):
		self.name = name
		self.idx = idx
		self.score = 1

		self.texture = textures["pickups"][name]
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
		if not HUMAN_MODE:
			return 
		# Blit icon, digit1, and digit 2
		surface.blit(self.texture, (40 * SIZING, (88 + 24*self.idx) * SIZING))
		surface.blit(self.digit1, (68 * SIZING, (94 + 24*self.idx) * SIZING))
		surface.blit(self.digit2, (80 * SIZING, (94 + 24*self.idx) * SIZING))