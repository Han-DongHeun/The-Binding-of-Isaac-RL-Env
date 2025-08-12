# Fire.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is the class for the fires in each room.
# They can have a diffrent base hurt isaac.
# 

from pygame import *
from random import randint
from utils.const import *
from utils.Animation import *


class Fire:
	def __init__(self, variant, xy, sounds, textures):
		self.variant = variant
		self.x = xy[0]
		self.y = xy[1]
		self.sounds = sounds
		self.textures = textures

		self.collideable = False

		self.destroyed = False
		self.bounds = Rect(GRIDX + GRATIO * self.x, GRIDY + GRATIO * self.y, GRATIO, GRATIO)

		self.health = 4

		# Get frames for flame
		self.fireFrames = textures["fireFrames"]

		# Wood animation frames
		self.woodFrames = textures["woodFrames"][randint(0,2)]

		self.fire = Animation(self.fireFrames, .4)
		self.wood = Animation(self.woodFrames, .4)

		# Define dead wood and fire frames
		self.deadWood = self.woodFrames[1]
		self.deadFire = Surface((0,0))

	def destroy(self):
		self.destroyed = True
		self.sounds[1].play() # Extinguish sound
		self.health = 0

	def hurt(self, ammount):
		self.health -= 1

		if self.health == 0:
			self.destroy()
		elif self.health < 0:
			self.health = 0
		else:
			self.fire.resize(0.8) # Decrease flame size

	def render(self, surface, time, ox=0, oy=0):
		
		if self.health > 0:
			wood = self.wood.render(time)
			fire = self.fire.render(time)
		else:
			wood = self.deadWood
			fire = self.deadFire

		wood_rect = Rect(0, 0, self.wood.width, self.wood.height)
		fire_rect = Rect(0, 0, self.fire.width, self.fire.height)
		wood_rect.center = (self.bounds.centerx + ox, self.bounds.centery + oy)
		fire_rect.midbottom = (self.bounds.centerx + ox, self.bounds.bottom + oy)

		surface.blit(wood, wood_rect)
		surface.blit(fire, fire_rect)