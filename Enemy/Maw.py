# Maw.py
# Aaron Taylor
# Moose Abumeeiz
#
# Maw follows the user just like a fly. Just with a diffrent texture
# 

from pygame import *
from utils.const import *
from utils.func import *
from Enemy.Fly import *

class Maw(Enemy):
	hurtDistance = 50 * SIZING
	health = 12
	isFlying = True