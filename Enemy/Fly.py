# Fly.py
# Aaron Taylor
# Moose Abumeeiz
#
# This class is for the simple fly that just heads towards isaac.
# 

from pygame import *
from utils.const import *
from Enemy.Enemy import *
from utils.Animation import *
from math import *

class Fly(Enemy):
	"""Simple enemy fly class"""

	isFlying = True
	health = 4
	weight = 1
	hurtDistance = 40 * SIZING
	
	def checkTear(self):
		pass