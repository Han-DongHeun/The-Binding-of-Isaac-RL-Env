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
import random

class Enemy:
	"""Enemy parent class"""

	# Setup
	texture = Surface((0, 0))
	effect = Surface((0, 0))
	texture_rect = Rect(0, 0, 0, 0)
	effect_rect = Rect(0, 0, 0, 0)

	isFlying = False
	dead = False
	cx, cx = 0, 0
	health = 1
	weight = 1
	speed = SIZING

	damage = 1
	tear_damage = 1

	hurtDistance = 40 * SIZING

	tear_timer = 0
	max_tear_timer = 120

	current_frame = 0
	interval_frame = 4

	frames = None
	effect_frames = [effect]

	dx = dy = 0

	def __init__(self, xy):
		self.path = []
		self.tears = []
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
			if dist < character.radius and tear.check_collision():
				character.hurt(tear.damage, tear.x, tear.y)
				tear.pop(True)

	def checkTear(self):
		if self.tear_timer > 0:
			return

		dx, dy = self.cx - self.x, self.cy - self.y
		dist = sqrt(dx**2 + dy**2)

		self.tears.append(Tear((dx/dist, dy/dist), (self.x, self.y), (0, 0), 1, self.tear_damage, 1, False))
		self.tear_timer = self.max_tear_timer

	def die(self):
		self.dead = True

	def move(self):
		if self.isFlying:
			self.dx, self.dy = self.cx - self.x, self.cy - self.y

		elif len(self.path) > 0:
			# MOVE TO NEXT PATH

			tx, ty = get_center(*self.path[0])
			self.dx, self.dy = tx - self.x, ty - self.y

			if sqrt(self.dx**2 + self.dy**2) < 0.05 * GRATIO:
				self.path = self.path[1:]

		else:
			return
		
		# Move ratios
		dist = sqrt(self.dx**2 + self.dy**2) + 1e-8

		# Move character
		self.x += self.speed * self.dx / dist
		self.y += self.speed * self.dy / dist

	def pathFind(self, nodes, paths):
		# Do pathfinding
		
		gcx, gcy = (self.cx - GRIDX) // GRATIO, (self.cy - GRIDY) // GRATIO
		gcx, gcy = clamp(int(gcx), 0, 12), clamp(int(gcy), 0, 6)

		gx, gy = (self.x - GRIDX) // GRATIO, (self.y - GRIDY) // GRATIO
		gx, gy = clamp(int(gx), 0, 12), clamp(int(gy), 0, 6)

		if self.isFlying:
			return

		start, end = nodes[gx][gy], nodes[gcx][gcy]

		path = paths.search(start, end)
		if path is None:
			# There is no path found to the character
			self.path = self.randomPathFind(nodes, paths)
		else:
			for i in range(len(path)):
				p = path[i]
				path[i] = (p.x, p.y)
			self.path = path[1:]

	def randomPathFind(self, nodes, paths):
		gx, gy = (self.x - GRIDX) // GRATIO, (self.y - GRIDY) // GRATIO
		gx, gy = clamp(int(gx), 0, 12), clamp(int(gy), 0, 6)

		node = random.choice(paths.graph[nodes[gx][gy]])
		path = [(node.x, node.y)]

		return path

	def render(self, surface, character, nodes, paths, bounds, obsticals):

		self.cx, self.cy = character.x, character.y

		if not self.dead:
			self.pathFind(nodes, paths)
			self.move()
			self.checkTear()
		self.checkHurt(character)

		self.tear_timer = max(0, self.tear_timer - 1)

		for tear in self.tears[:]:
			if not tear.render(surface, bounds, obsticals):
				self.tears.remove(tear)

		self.update()
		surface.blit(self.texture, self.texture_rect)
		surface.blit(self.effect, self.effect_rect)

		self.current_frame += 1

		return not self.dead
	
	def update(self):
		frame_idx = self.current_frame // self.interval_frame
		self.texture = self.frames[frame_idx % len(self.frames)]
		self.effect = self.effect_frames[frame_idx % len(self.effect_frames)]
		self.texture_rect = self.texture.get_rect(center=(self.x, self.y))
		self.effect_rect = self.effect.get_rect(center=(self.x, self.y))