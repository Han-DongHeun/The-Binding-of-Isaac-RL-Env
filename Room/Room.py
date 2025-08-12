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
from Room.Rock import *
from Room.Poop import *
from Room.Fire import *
from Room.Door import *
from Character.Tear import *
from Item.Coin import *
from Item.Key import *
from Enemy.Fly import *
from Enemy.Pooter import *
from Item.Heart import *
from Item.Bomb import *
from Item.Pill import *
from Room.Trapdoor import *
from Enemy.Maw import *
from Enemy.Boil import *
from Enemy.Host import *

import utils.func as func

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

	lcx = -1
	lcy = -1

	def __init__(self, floor, variant, xy, xml, textures, sounds):
		offX = offY = 0
		if variant == 2:
			offX, offY = 234*2, 156*2

		if variant == 5:
			texture = textures["floors"]["shop"].subsurface(Rect(offX, offY, 221*2*SIZING, 143*2*SIZING))
		else:
			texture = textures["floors"][floor].subsurface(Rect(offX, offY, 221*2*SIZING, 143*2*SIZING))

		backdrop = Surface((221*2*2*SIZING, 143*2*2*SIZING))

		# Form the texture to each of the 4 corners of the room
		backdrop.blit(texture, (0,0))
		backdrop.blit(transform.flip(texture, True, False), (221*2*SIZING, 0))
		backdrop.blit(transform.flip(texture, False, True), (0, 143*2*SIZING))
		backdrop.blit(transform.flip(texture, True, True), (221*2*SIZING, 143*2*SIZING))

		# Add gorgeous lighting
		backdrop.blit(textures["shading"], (0,0))
		backdrop = func.darken(backdrop, .25)
		backdrop.blit(textures["overlays"][randint(0,4)], (0,0))

		self.backdrop_rect = backdrop.get_rect(center=(WIDTH//2, HEIGHT//2))

		# Show tutorial controls if its the first room
		if floor == 0 and xy[0] == 0 and xy[1] == 0:
			controls = textures["controls"]
			controls_rect = controls.get_rect(center=(self.backdrop_rect.width//2, self.backdrop_rect.height//2))
			backdrop.blit(controls, controls_rect)

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

		self.levelBounds = Rect(GRIDX, GRIDY, WIDTH-(GRIDX*2), HEIGHT-(GRIDY*2))

		self.enemies = []
		self.rocks = []
		self.poops = []
		self.fires = []
		self.doors = []
		self.other = [] # Other stuff that doesnt have special properties

		self.parseRoomXML(xml) # Build the room based on the xml

		obsticals = []

		for o in self.rocks+self.fires+self.poops:
			obsticals.append([o.x, o.y])

		# Setup room for path finding
		graph, self.nodes = make_graph({"width": 13, "height": 7, "obstacle": obsticals})
		self.paths = AStarGrid(graph)
		self.hadEnemies = len(self.enemies) > 0
		self.spawnedItem = False

	def parseRoomXML(self, xml):
		self.w, self.h = map(int, [xml.get('width'), xml.get('height')])
		for obj in xml: # Iterate through room objects
			attr = obj.attrib
			x, y = int(attr["x"]), int(attr["y"])

			if obj.tag == "spawn":
				
				typ = int(obj[0].get('type'))
				var = int(obj[0].get('variant'))
				subtype = int(obj[0].get('subtype'))

				# Spawn the correct item for the type
				if typ in [1500, -1, -1, 1496, -1]:
					self.poops.append(Poop([1500, -1, -1, 1496, -1].index(typ), (x,y), self.textures["poops"], self.sounds["pop"]))
				elif typ == 1000:
					self.rocks.append(Rock(randint(0,2), (x,y), False, self.sounds["rockBreak"], self.textures["rocks"]))
				elif typ == 33:
					self.fires.append(Fire(0, (x,y), [self.sounds["fireBurn"], self.sounds["steam"]], self.textures["fires"]))
				elif typ == 5 and var == 10:
					self.other.append(Heart([1,3,6].index(subtype), (x,y), [self.sounds["heartIntake"], self.sounds["holy"]], self.textures["pickupHearts"]))
				elif typ == 5 and var == 20:
					self.other.append(Coin(subtype - 1, (x,y), [self.sounds["coinDrop"], self.sounds["coinPickup"]], self.textures["coins"]))
				elif typ == 5 and var == 30:
					self.other.append(Key(0, (x, y), [self.sounds["keyDrop"], self.sounds["keyPickup"]], self.textures["keys"]))
				elif typ == 5 and var == 40:
					self.other.append(Bomb(0, (x, y), [self.sounds["explosion"]], self.textures["bombs"]))
				elif typ == 13:
					self.enemies.append(Fly((x,y), self.textures["enemies"]["fly"], self.textures["tears"], self.sounds["tear"]))
				elif typ == 14:
					self.enemies.append(Pooter((x, y), self.textures["enemies"]["pooter"], self.textures["tears"], self.sounds["tear"]))
				elif typ == 26:
					self.enemies.append(Maw((x, y), self.textures["enemies"]["maw"], self.textures["tears"], self.sounds["tear"]))
				elif typ == 27:
					self.enemies.append(Host((x, y), self.textures["enemies"]["host"], self.textures["tears"], self.sounds["tear"]))
				elif typ == 30:
					self.enemies.append(Boil((x, y), self.textures["enemies"]["boil"], self.textures["tears"], self.sounds["tear"]))

	def addDoor(self, door_idx, variant):
		self.doors.append(Door(self.floor, door_idx, variant, True, self.textures["doors"], self.sounds))

	def animateOut(self, direction):
		# animate the room out

		self.animating = True

		if direction[1] == -1:
			self.aDirection = 0
		elif direction[0] == -1:
			self.aDirection = 1
		elif direction[1] == 1:
			self.aDirection = 2
		elif direction[0] == 1:
			self.aDirection = 3

	def animateIn(self, direction):
		# Animate the room in

		self.animating = True

		if direction[1] == -1:
			self.aDirection = 0
		elif direction[0] == -1:
			self.aDirection = 1
		elif direction[1] == 1:
			self.aDirection = 2
		elif direction[0] == 1:
			self.aDirection = 3

		self.ax, self.ay = [0, -1, 0, 1][self.aDirection] * WIDTH, [1, 0, -1, 0][self.aDirection] * HEIGHT
		self.sx, self.sy = self.ax, self.ay

	def step(self, currTime):
		pass

	def renderMap(self, minimap, currentRoom, detail):
		ratio = 16 # Pixel to size ratio
		x, y = currentRoom

		if self.x == x and self.y == y:
			# Isaac is in this room
			texture = self.textures["map"]["in"]
		elif self.entered:
			# Isaac has  this room
			texture = self.textures["map"]["entered"]
		elif self.seen:
			# Isaac has seen the door to the room
			texture = self.textures["map"]["seen"]
		else:
			return
		
		centerx = minimap.get_width() // 2 + (self.x - x) * ratio
		centery = minimap.get_height() // 2 - (self.y - y) * ratio

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

	def render(self, surface, character, currTime):

		if len(self.enemies) > 0:
			for door in self.doors:
				door.close()

		else:
			for door in self.doors:
				door.open()

			if self.hadEnemies and len(self.other) == 0 and randint(0,5) == 0 and not self.spawnedItem:
				typ = randint(0,2)
				self.spawnedItem = True

				# Random spawn
				if typ == 0:
					self.other.append(Coin(0, (6,2), [self.sounds["coinDrop"], self.sounds["coinPickup"]], self.textures["coins"]))
				elif typ == 1:
					self.other.append(Bomb(1, (6,2), [self.sounds["explosion"]], self.textures["bombs"]))
				elif typ == 2:
					self.other.append(Key(0, (6, 2), [self.sounds["keyDrop"], self.sounds["keyPickup"]], self.textures["keys"]))

			# Create trapdoor in empty boss room
			if self.variant == 2 and self.floor < 6 and not Trapdoor in list(map(type, self.other)):
				self.other.append(Trapdoor(self.textures["trapdoor"]))

		if not self.animating:
			# Render stationary room
			surface.blit(self.backdrop, self.backdrop_rect)

			for door in self.doors:
				door.render(surface)

			for rock in self.rocks:
				rock.render(surface)

			for poop in self.poops:
				poop.render(surface)

			for fire in self.fires:
				fire.render(surface, currTime)

			objects = self.rocks + self.poops + self.fires

			for other in self.other[::-1]:
				if not other.render(surface):
					self.other.remove(other)

			everything = objects+self.other
			
			for enemy in self.enemies[:]:
				if not enemy.render(surface, currTime, character, self.nodes, self.paths, self.levelBounds, objects):
					self.enemies.remove(enemy)

			move = character.render(surface, currTime, self.levelBounds, everything, self.doors)

			return move
		else:
			# Render moving room

			move_frame = 20 # How far the canvas should move
			self.ax += [0, 1, 0, -1][self.aDirection] * WIDTH / move_frame
			self.ay += [-1, 0, 1, 0][self.aDirection] * HEIGHT / move_frame

			if abs(self.sx - self.ax) >= WIDTH or abs(self.sy - self.ay) >= HEIGHT:
				self.animating = False
				self.ax, self.ay = 0, 0
				self.sx, self.sy = 0, 0
			else:
				backdrop_rect = self.backdrop_rect.copy()
				backdrop_rect.x = self.backdrop_rect.x + self.ax
				backdrop_rect.y = self.backdrop_rect.y + self.ay
				surface.blit(self.backdrop, backdrop_rect)

				for door in self.doors:
					door.render(surface, ox=self.ax, oy=self.ay)

				for rock in self.rocks:
					rock.render(surface, ox=self.ax, oy=self.ay)

				for poop in self.poops:
					poop.render(surface, ox=self.ax, oy=self.ay)

				for fire in self.fires:
					fire.render(surface, currTime, ox=self.ax, oy=self.ay)

				objects = self.rocks + self.poops + self.fires

				for other in self.other[::-1]:
					if not other.render(surface, ox=self.ax, oy=self.ay):
						self.other.remove(other)

			return [0, 0]
