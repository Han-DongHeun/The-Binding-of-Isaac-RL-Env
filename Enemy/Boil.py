# Boil.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is the class for the red boil that appears as an enemy
# and shoots in random directions
# 

from Enemy.Enemy import *
from random import choice

class Boil(Enemy):
	
	hurtDistance = 30 * SIZING
	health = 10
	max_health = 10
	interval_frame = 60
	frames = textures["enemies"]["boil"]

	def move(self, *args):
		pass

	def pathFind(self, *args):
		pass

	def checkTear(self):
		if self.tear_timer > 0 or self.health < self.max_health:
			return

		self.tears.append(Tear(choice([(1,0),(-1,0),(0,-1),(0,1)]), (self.x, self.y), (0, 0), 1, self.tear_damage, 1, False))
		self.tear_timer = self.max_tear_timer

	def update(self):
		if self.current_frame % self.interval_frame == 0:
			self.health = min(self.max_health, self.health + 1)

		self.texture = self.frames[clamp(self.health - 1, 0, 9)]