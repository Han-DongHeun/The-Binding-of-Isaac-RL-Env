# Enenmy.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is parent enemy class, it contains the default moves
# for all enemies in the game.
# 

from pygame import *
from utils.const import *
from math import *
from utils.AStar import *
from utils.func import clamp
from utils.func import get_center
from Character.Tear import Tear
from utils.loadResource import textures, sounds

class Enemy:
	"""Enemy parent class"""

	# Setup
	texture = None

	isFlying = False
	dead = False
	path = []
	cx, cx = 0, 0
	health = 1
	weight = 1
	speed = SIZING

	tears = []

	damage = 1
	tear_damage = 1

	hurtDistance = 40 * SIZING

	tear_timer = 0
	max_tear_timer = 120

	current_frame = 0
	interval_frame = 4

	frames = None
	tear_texure = textures["tears"]["blood"]
	tear_sound = sounds["tear"][0]

	def __init__(self, xy):
		self.x, self.y = get_center(*xy)
		self.bounds = Rect(0, 0, 32*SIZING, 32*SIZING)
		self.bounds.center = (self.x, self.y)

	def hurt(self, amount):
		if not self.dead:
			self.health = max(0, self.health - amount)
			if self.health <= 0:
				self.die()

	def checkHurt(self, character):
		# Check for any hurt

		dx, dy = (character.x - self.x), (character.y - self.y)

		if not self.dead:
			# Check tear hurt
			for tear in character.tears:
				dist = sqrt((tear.x - self.x)**2 + (tear.y - self.y)**2)
				if dist < self.hurtDistance and tear.check_collision():
					self.hurt(tear.damage)
					tear.pop(True)

			# Check if character is too close
			if abs(dx) < self.hurtDistance and abs(dy) < self.hurtDistance:
				character.hurt(self.damage, self.x, self.y)

		# Check if character should be hit
		for tear in self.tears:
			dist = sqrt((tear.x - character.x)**2 + (tear.y - character.y)**2)
			if dist < character.hurtDistance and tear.check_collision():
				character.hurt(tear.damage, tear.x, tear.y)
				tear.pop(True)

	def checkTear(self):
		if self.tear_timer > 0:
			return

		dx, dy = self.cx - self.x, self.cy - self.y
		dist = sqrt(dx**2 + dy**2)

		self.tears.append(Tear((dx/dist, dy/dist), (self.x, self.y), (0, 0), 1, self.tear_damage, 1, False, self.tear_texture, self.tear_sound))
		self.tear_timer = self.max_tear_timer

	def die(self):
		self.dead = True

	def move(self):
		if not self.isFlying and len(self.path) != 0:
			# MOVE TO NEXT PATH

			dx, dy = self.path[0][0] - self.x, self.path[0][1] - self.y

			if sqrt(dx**2 + dy**2) < 0.15:
				self.path = self.path[1:]

		if len(self.path) > 0:
			# Head towards next point
			dx, dy = self.path[0][0] - self.x, self.path[0][1] - self.y
		else:
			# Head towards character
			dx, dy = self.cx - self.x, self.cy - self.y

		# Move ratios
		dist = sqrt(dx**2 + dy**2) + 1e-7
		
		rx = dx / dist
		ry = dy / dist

		# Move character
		self.x += self.speed * rx
		self.y += self.speed * ry

	def pathFind(self, nodes, paths):
		# Do pathfinding
		
		gcx, gcy = (self.cx - GRIDX) // GRATIO, (self.cy - GRIDX) // GRATIO
		gcx, gcy = clamp(gcx, 0, 12), clamp(gcy, 0, 6)

		gx, gy = (self.x - GRIDX) // GRATIO, (self.y - GRIDX) // GRATIO
		gx, gy = clamp(gx, 0, 12), clamp(gy, 0, 6)

		if self.isFlying:
			return

		start, end = nodes[gx][gy], nodes[gcx][gcy]

		path = paths.search(start, end)
		if path is None:
			# There is no path found to the character

			self.path = []
		else:
			for i in range(len(path)):
				p = path[i]
				path[i] = (p.x, p.y)
			self.path = path[1:]

	def render(self, surface, character, nodes, paths, bounds, obsticals):

		self.cx, self.cy = character.x, character.y

		if not self.dead:
			self.pathFind(nodes, paths)
			self.move()
			self.checkTear()
		self.checkHurt(character)

		self.tear_timer = max(0, self.tear_timer - 1)

		for tear in self.tears[:]:
			if not tear.render(surface, time, bounds, obsticals):
				self.tears.remove(tear)

		self.update()
		rect = self.texture.get_rect(center=(self.x, self.y))
		surface.blit(self.texture, rect)

		self.current_frame += 1

		return not self.dead
	
	def update(self) -> Surface:
		pass