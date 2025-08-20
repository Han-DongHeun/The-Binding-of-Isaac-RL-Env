from Enemy.Enemy import *

class AttackFly(Enemy):

	isFlying = True
	health = 5
	weight = 1
	hurtDistance = 40 * SIZING

	texture = textures["enemies"]["attackFly"][1]
	
	def checkTear(self):
		pass