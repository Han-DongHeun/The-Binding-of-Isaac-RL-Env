# Tear.py
# Aaron Taylor
# Moose Abumeeiz
#
# The tear can be shot from an enemy or the main character.
# It will hurt anything of the oppisite type (enemies and good guys)
# 

from pygame import *
from utils.const import *
from random import randint
from utils.Animation import *
from utils.loadResource import textures, sounds
from math import sqrt

class Tear:
	"""Main tear class"""

	textures = textures["tears"]
	frames = textures["frames"]
	sounds = sounds["tear"]
	
	frame_inteval = 2
	current_frame = 0

	def __init__(self, xyv, xy, ixyv, speed, damage, shotRange, friendly):
		xv, yv = xyv # X, Y velocity

		xv += ixyv[0]
		yv += ixyv[1]

		v = sqrt(xv**2 + yv**2) + 1e-8
		self.dx, self.dy = xv / v, yv / v
		
		v = min(1, v)
		# Stats
		speed_stat = (speed + 2) * 2
		self.speed = speed_stat / 48 * v
		self.damage = damage + 3
		self.friendly = friendly
		self.range = (shotRange + 4) * v

		self.x, self.y = xy

		self.poped = False

		# Play random shoot sound
		self.sounds[randint(0,1)].play()

		# Texture setup
		self.texture = self.textures["tear"] if friendly else self.textures["blood"]
		self.rect = self.texture.get_rect(center=xy)

		self.h0 = 0.5
		self.h = 0
		self.distance = 0

	def update(self):
		self.x += self.dx * self.speed * GRATIO
		self.y += self.dy * self.speed * GRATIO
	
		self.distance += self.speed
		self.h = -(self.h0 / self.range) * (self.distance - self.range) * (0.5 * self.distance + 1)

		self.rect.center = (self.x, self.y - self.h * GRATIO)

	def step(self):
		self.texture = self.frames[self.frameIndex]
		self.frameIndex += 1

	def check_collision(self):
		return self.h <= 1 and not self.poped

	def pop(self, collision):
		self.poped = True
		if collision:
			self.sounds[3].play() # Play collison pop
		else:
			self.sounds[2].play() # Play normal pop

		return True

	def render(self, surface, bounds, obsticals):
		if self.poped:
			# Return popping tear
			frame_idx = self.current_frame // self.frame_inteval
			if frame_idx >= len(self.frames):
				return False
			
			texture = self.frames[frame_idx]
			self.rect = texture.get_rect(center = (self.x, self.y - self.h * GRATIO))
			surface.blit(texture, self.rect)

			self.current_frame += 1
			return True
		
		self.update()

		if self.h < 0:
			return self.pop(False)

		if not bounds.inflate(0.1*GRATIO, 0.1*GRATIO).collidepoint(self.x, self.y):
			return self.pop(True)

		for ob in obsticals:
			if (not ob.destroyed and ob.bounds.collidepoint(self.x, self.y) and self.check_collision()):
				ob.hurt(1)

				return self.pop(True)
		
		surface.blit(self.texture, self.rect)

		return True