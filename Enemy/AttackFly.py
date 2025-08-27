from Enemy.Enemy import *

class AttackFly(Enemy):

	isFlying = True
	health = 5
	weight = 1
	hurtDistance = 40 * SIZING

	frames = textures["enemies"]["attackFly"]
	
	def checkTear(self):
		pass