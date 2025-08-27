# Fly.py
# Aaron Taylor
# Moose Abumeeiz
#
# This class is for the simple fly that just heads towards isaac.
# 

from Enemy.Enemy import *

class Fly(Enemy):
	"""Simple enemy fly class"""

	isFlying = True
	health = 3
	weight = 1
	hurtDistance = 40 * SIZING

	frames = textures["enemies"]["fly"]
	
	def checkTear(self):
		pass