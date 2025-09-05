# Door.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is the class for all doors in the game.
# 

from pygame import *
from utils.const import *
from utils.loadResource import textures, sounds


class Door:
	"""The main door class"""

	# DOOR TYPES:
	#
	# 0 - Normal door
	# 1 - Treasure door
	# 2 - Boss door
	# 3 - Devil door
	# 4 - Angel door
	# 5 - Shop

	# ROOMS ARE 13 x 7

	textures = textures["doors"]
	sounds = sounds

	def __init__(self, side, door_type, isOpen):
		self.side = side
		self.locked = False

		# Bash textures
		self.texture = self.textures[door_type]
		
		# Darken the door a little
		self.sounds = sounds

		self.isOpen = isOpen

		self.doorFrame  = transform.rotate(self.texture["doorFrame"], -(180 - (90*self.side)))
		self.doorBack   = transform.rotate(self.texture["doorBack"], -(180 - (90*self.side)))
		self.lDoor      = transform.rotate(self.texture["lDoor"], -(180 - (90*self.side)))
		self.rDoor      = transform.rotate(self.texture["rDoor"], -(180 - (90*self.side)))
		self.lockedDoor = transform.rotate(self.texture["lockedDoor"], -(180 - (90*self.side)))

		# Change x and y based on side
		self.x1 = [0, 7, 0, -7][self.side]
		self.y1 = [4, 0, -4, 0][self.side] 

		# Bash side rect
		self.base_rect = Rect((0, 0), (GRATIO, GRATIO))
		self.base_rect.centerx = WIDTH // 2 + GRATIO * self.x1
		self.base_rect.centery = HEIGHT // 2 + GRATIO * self.y1

		self.rect = Rect((0, 0), (GRATIO * 2 // 3, GRATIO * 2 // 3))

		if side == 0:
			self.rect.midtop = self.base_rect.midtop
			self.render_rect = self.doorFrame.get_rect(midtop=self.rect.midtop)
		elif side == 1:
			self.rect.midleft = self.base_rect.midleft
			self.render_rect = self.doorFrame.get_rect(midleft=self.rect.midleft)
		elif side == 2:
			self.rect.midbottom = self.base_rect.midbottom
			self.render_rect = self.doorFrame.get_rect(midbottom=self.rect.midbottom)
		elif side == 3:
			self.rect.midright = self.base_rect.midright
			self.render_rect = self.doorFrame.get_rect(midright=self.rect.midright)

	def close(self):
		if self.isOpen:
			self.isOpen = False
			self.sounds["doorClose"].stop()
			self.sounds["doorClose"].play()

	def open(self):
		if not self.isOpen:
			self.isOpen = True
			self.sounds["doorOpen"].stop()
			self.sounds["doorOpen"].play()

	def step(self):
		pass

	def render(self, surface, ox=0, oy=0):
		# Convert grid x and y to pixel x and y
		render_rect = self.render_rect.move(ox, oy)

		surface.blit(self.doorBack, render_rect)

		if not self.isOpen:
			surface.blit(self.lDoor, render_rect)
			surface.blit(self.rDoor, render_rect)
		if self.locked:
			surface.blit(self.lDoor, render_rect)
			surface.blit(self.lockedDoor, render_rect)

		surface.blit(self.doorFrame, render_rect)