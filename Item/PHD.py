# PHD.py
# Aaron Taylor
# Moose Abumeeiz
#
# The PHD ensures you have only positive pills
# when its in the players inventory
# 

from pygame import *
from utils.const import *
from Item.Item import *

class PHD(Item):
	"""The PHD is used to allow all positive affects on pills"""
	
	collideable = False
	pickedUp = False
	
	tWidth = 64
	tHeight = 64

	def pickup(self):
		self.pickedUp = True