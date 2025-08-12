# Pooter.py
# Aaron Taylor
# Moose Abumeeiz
#
# The pooter will follow the user similarly to a fly
# 

from pygame import *
from utils.const import *
from Enemy.Enemy import *
from utils.Animation import *
from math import *
from Character.Tear import *

class Pooter(Enemy):
	hurtDistance = 30 * SIZING
	health = 12
	isFlying = True