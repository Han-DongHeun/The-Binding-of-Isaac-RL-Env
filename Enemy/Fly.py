# Fly.py
# Aaron Taylor
# Moose Abumeeiz
#
# This class is for the simple fly that just heads towards isaac.
# 

from pygame import *
from utils.const import *
from utils.loadResource import textures, sounds
from Enemy.Enemy import Enemy

class Fly(Enemy):
	"""Simple enemy fly class"""

	isFlying = True
	health = 4
	weight = 1
	hurtDistance = 40 * SIZING

	texture = textures["enemies"]["fly"][0]
	
	def checkTear(self):
		pass