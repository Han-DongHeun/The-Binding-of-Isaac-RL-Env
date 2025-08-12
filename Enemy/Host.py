# Host.py
# Aaron Taylor
# Moose Abumeeiz
#
# The host pops up at a random time and shoots a tear in the
# characters directions
# 

from pygame import *
from utils.const import *
from Enemy.Enemy import *
from Character.Tear import *


class Host(Enemy):

	health = 6
	standing = False
	last_frame = 0
	standing_frame = 60
	down_frame = 90

	def hurt(self, amount):
		if self.standing:
			super().hurt(amount)

	def checkTear(self):
		if self.standing:
			super().checkTear()

	def move(self, *args):
		pass

	def pathFind(self, *args):
		pass

	def update(self):
		self.texture = self.frames[self.standing]
		if self.standing:
			if self.current_frame - self.last_frame > self.standing_frame:
				self.current_frame = self.last_frame
				self.standing = False

		else:
			if randint(0, self.current_frame - self.last_frame) > self.down_frame:
				self.current_frame = self.last_frame
				self.standing = True