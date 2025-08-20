# Room.py
# Aaron Taylor
# Moose Abumeeiz
#
# This room class supports animation in and out,
# it will show the background and will be responsible for rendering
# everything within it.
# 

from pygame import *
from utils.const import *
from random import *
from Room.Door import *
from Obstacle.Obstacle import Obstacle
from Enemy.Enemy import Enemy
from Pickup.Pickup import Pickup

import utils.func as func
from utils.AStar import *
import importlib

from utils.loadResource import textures, sounds, darken

class Room:
	"""The main floor class"""

	# ROOM TYPES:
	#
	# 0 - Normal room
	# 1 - Treasure room
	# 2 - Boss room
	# 3 - Devil room
	# 4 - Angel room
	# 5 - Shop

	# ROOMS ARE 13 x 7

	def __init__(self, floor, xy, objects, variant=0):
		texture = textures["floors"][floor]

		w, h = texture.get_width(), texture.get_height()
		backdrop = Surface((w * 2, h * 2))

		# Form the texture to each of the 4 corners of the room
		backdrop.blit(texture, (0,0))
		backdrop.blit(transform.flip(texture, True, False), (w, 0))
		backdrop.blit(transform.flip(texture, False, True), (0, h))
		backdrop.blit(transform.flip(texture, True, True), (w, h))

		# Add gorgeous lighting
		backdrop.blit(textures["shading"], (0,0))
		backdrop = darken(backdrop, .25)
		backdrop.blit(textures["overlays"][randint(0,4)], (0,0))

		self.backdrop_rect = backdrop.get_rect(center=(WIDTH//2, HEIGHT//2))

		# Setup x and y
		self.x, self.y = xy
		self.w, self.h = 0,0

		self.variant = variant

		self.entered = False
		self.seen = False

		self.floor = floor
		self.backdrop = backdrop
		self.sounds = sounds
		self.textures = textures

		self.animating = False
		self.ax, self.ay = 0, 0
		self.aDirection = -1
		self.sx, self.sy = 0,0

		self.levelBounds = Rect(GRIDX, GRIDY, 13 * GRATIO, 7 * GRATIO)

		self.enemies: list[Enemy] = []
		self.obstacles: list[Obstacle] = []
		self.doors: list[Door] = []
		self.pickups: list[Pickup] = []
		self.other = []

		if xy == (0, 0):
			controls = textures["controls"]
			controls_rect = controls.get_rect(center=(self.backdrop_rect.width//2, self.backdrop_rect.height//2))
			backdrop.blit(controls, controls_rect)
		else:
			self.generateObjects(objects)

		# Setup room for path finding
		graph, self.nodes = make_graph({"width": 13, "height": 7, "obstacle": self.obstacles})
		self.paths = AStarGrid(graph)

	def generateObjects(self, objects):
		enemy = ('enemy', 'Enemy', self.enemies)
		obstacle = ('obstacle', 'Obstacle', self.obstacles)
		pickups = ('pickup', 'Pickup', self.pickups)

		for type, path, repo in (enemy, obstacle, pickups):
			for name, x, y in objects[type]:
				name = name[0].upper() + name[1:]
				object_module = importlib.import_module(f"{path}.{name}")
				object_class = getattr(object_module, name)
				repo.append(object_class((x, y)))

	def addDoor(self, door_idx, variant):
		self.doors.append(Door(self.floor, door_idx, variant, True, self.textures["doors"], self.sounds))

	def animateOut(self, move):
		# animate the room out
		self.animating = True

		dx, dy = move
		self.move = (-dx, -dy)

	def animateIn(self, move):
		# Animate the room in

		self.animating = True

		dx, dy = move
		self.move = (-dx, -dy)

		self.sx, self.sy = self.ax, self.ay = dx * WIDTH, dy * HEIGHT

	def renderMap(self, minimap, currentRoom, detail):
		ratio = 16 * SIZING # Pixel to size ratio
		x, y = currentRoom

		if self.x == x and self.y == y:
			# Isaac is in this room
			texture = self.textures["map"]["in"]
		elif self.entered:
			# Isaac has this room
			texture = self.textures["map"]["entered"]
		elif self.seen:
			# Isaac has seen the door to the room
			texture = self.textures["map"]["seen"]
		else:
			return
		
		centerx = minimap.get_width() // 2 + (self.x - x) * ratio
		centery = minimap.get_height() // 2 + (self.y - y) * ratio

		if not detail:
			size = (ratio * 3 // 2)
			room_rect = Rect((0, 0), (size, size))
			room_rect.center = (centerx, centery)

			draw.rect(minimap, (0, 0, 0), room_rect)

		# Draw special symbol
		else:
			room_rect = Rect((0, 0), (ratio, ratio))
			room_rect.center = (centerx, centery)
			minimap.blit(texture, room_rect)
			if self.variant == 1 or self.variant == 2 and not self.x == x and self.y == y:
				minimap.blit(self.textures["map"][["item", "boss"][self.variant-1]], room_rect)

	def render(self, surface, character):

		if len(self.enemies) > 0:
			for door in self.doors:
				door.close()
		else:
			for door in self.doors:
				door.open()

		surface.blit(self.backdrop, self.backdrop_rect.move(self.ax, self.ay))

		for door in self.doors:
			door.render(surface, self.ax, self.ay)

		for obstacle in self.obstacles:
			obstacle.render(surface, self.ax, self.ay)

		self.pickups = [pickup for pickup in self.pickups if pickup.render(surface, self.ax, self.ay)]

		self.other = [obj for obj in self.other if obj.render(surface, self.ax, self.ay)]

		if not self.animating:
			self.enemies = [enemy for enemy in self.enemies if enemy.render(surface, character, self.nodes, self.paths, self.levelBounds, self.obstacles)]
			
			move = character.render(surface, self.levelBounds, self.obstacles, self.pickups, self.doors)
			return move
		
		elif abs(self.sx - self.ax) >= WIDTH or abs(self.sy - self.ay) >= HEIGHT:
			self.animating = False
			self.ax, self.ay = 0, 0
			self.sx, self.sy = 0, 0
			return (0, 0)
		
		else:
			move_frame = 20
			self.ax += self.move[0] * WIDTH / move_frame
			self.ay += self.move[1] * HEIGHT / move_frame
			return (0, 0)