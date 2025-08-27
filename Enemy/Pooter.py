from Enemy.Enemy import *

class Pooter(Enemy):
	hurtDistance = 30 * SIZING
	health = 12
	isFlying = True

	frames = textures["enemies"]["pooter"]