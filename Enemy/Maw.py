# Maw.py
# Aaron Taylor
# Moose Abumeeiz
#
# Maw follows the user just like a fly. Just with a diffrent texture
# 

from Enemy.Enemy import *

class Maw(Enemy):
	hurtDistance = 50 * SIZING
	health = 12
	isFlying = True

	textures = textures["enemies"]["maw"]