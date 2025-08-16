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

class Tear:
	"""Main tear class"""

	def __init__(self, xyv, xy, ixy, speed, damage, shotRange, friendly, textures, sounds):	
		self.xVel, self.yVel = xyv # X, Y velocity
		self.hVel = 0.5
		self.hAcc = -0.03
		
		# Stats
		self.speed = (speed + 2) * 2 * SIZING
		self.damage = damage+3
		self.friendly = friendly
		self.range = (shotRange + 4) * SIZING
		self.distance = 0

		# sounds
		self.sounds = sounds

		self.x, self.y = xy
		self.h = 15

		# Inherited x and y velocity
		self.iXVel = ixy[0]
		self.iYVel = ixy[1]

		self.poped = False

		self.frames = textures["frames"]
		self.popping = Animation(self.frames, 0.24)

		# Play random shoot sound
		sounds[randint(0,1)].play()

		# Texture setup
		self.texture = textures["tear"] if friendly else textures["blood"]
		self.width = self.texture.get_width()
		self.height = self.texture.get_height()

	def step(self):
		self.texture = self.frames[self.frameIndex]
		self.frameIndex += 1

	def check_collision(self):
		return self.h <= 20 and not self.poped

	def pop(self, collision):
		self.poped = True
		if collision:
			self.sounds[2].play() # Play collison pop
		else:
			self.sounds[1].play() # Play normal pop
		return True

	def render(self, surface, bounds, obsticals):
		if self.poped:
			return True
			# Return popping tear
			frame = self.popping.render(time)
			if self.popping.looped:
				return False
			surface.blit(frame, (self.x-self.popping.width//2, self.y-self.popping.height//2))
			return True

		self.x += self.xVel * self.speed + self.iXVel
		self.y += self.yVel * self.speed + self.iYVel

		self.hVel += self.hAcc
		self.h += self.hVel

		if self.h < -5:
			return self.pop(False)

		if not bounds.inflate(3, 3).collidepoint(self.x, self.y):
			return self.pop(True)

		for ob in obsticals:
			# Collide with ob
			try:
				if ob.destroyed:
					continue
			except:
				pass
			# Collude with object
			if ob.bounds.collidepoint(self.x, self.y) and self.check_collision():
				try:
					ob.hurt(1)
				except:
					pass

				return self.pop(True)

		surface.blit(self.texture, (self.x - self.width // 2 , self.y - self.height // 2 - self.h * SIZING) )

		return True