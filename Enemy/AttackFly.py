from pygame import *
from utils.const import *
from Enemy.Enemy import Enemy

class AttackFly(Enemy):
	"""Simple enemy fly class"""

	isFlying = True
	health = 4
	weight = 1
	hurtDistance = 40 * SIZING
	
	def checkTear(self):
		pass