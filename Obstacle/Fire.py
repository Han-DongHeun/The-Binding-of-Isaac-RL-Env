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
from Obstacle.Obstacle import Obstacle
from utils.loadResource import textures, sounds
from utils.func import clamp

class Fire(Obstacle):

	collideable = False

	health = 4

	fire_frames = textures["fires"]["fireFrames"]
	wood_frames = textures["fires"]["woodFrames"]
	
	destroyed_sound = sounds['fireBurn']

	current_frame = 0
	interval_frame = 4

	fire = None
	wood = None

	def __init__(self, gxy):
		super().__init__(gxy)

		self.wood_frames = self.wood_frames[randint(0,2)]

		# Define dead wood and fire frames
		self.dead_wood = self.wood_frames[1]
		self.dead_fire = Surface((0,0))

	def render(self, surface, ox=0, oy=0):

		self.update()

		fire_rect = Rect(0, 0, self.fire.get_width(), self.fire.get_height())
		wood_rect = Rect(0, 0, self.wood.get_width(), self.wood.get_height())

		fire_rect.midbottom = (self.bounds.centerx + ox, self.bounds.bottom + oy)
		wood_rect.center = (self.bounds.centerx + ox, self.bounds.centery + oy)

		surface.blit(self.wood, wood_rect)
		surface.blit(self.fire, fire_rect)

		self.current_frame += 1

	def update(self):

		if self.destroyed:
			self.fire = self.dead_fire
			self.wood = self.dead_wood
			return

		fire_frames = self.fire_frames[clamp(self.health, 0, 4)]
		fire_idx = self.current_frame // self.interval_frame % len(fire_frames)
		wood_idx = self.current_frame // self.interval_frame % len(self.wood_frames)

		self.fire = fire_frames[fire_idx]
		self.wood = self.wood_frames[wood_idx]