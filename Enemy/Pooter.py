from Enemy.Enemy import *

class Pooter(Enemy):
	hurtDistance = 30 * SIZING
	health = 12
	isFlying = True

	texture = textures["enemies"]["pooter"][0]