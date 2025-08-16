# Game.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is the main game class (not including menu)
# It is responsible for rendering the floor and the character.
# 

from pygame import *
from utils.func import *
from Character.Character import *
from Room.Room import *
from Pickup.Bomb import *
from Pickup.TrollBomb import *
from time import time as cTime
from Menu.pause import *
from Pickup.Pill import *
from Menu.Banner import *
from Enemy.Gurdy import *
from Enemy.Duke import *
import random

from utils.loadFloor import loadFloor

class Game:
	floor = {}
	floor_key = "basement"
	floor_idx = 0
	currentRoom = (0,0)
	animatingRooms = []
	won = False

	def __init__(self, characterType, controls, seed):
		self.characterType = characterType
		self.seed = seed
		self.controls = controls

		self.banners = []

		# Feed the seed to the random module
		random.seed(self.seed)

	def setup(self):
		# Load floor with custom data
		self.floor = loadFloor("basement")

	def updateMinimap(self, currentRoom):
		# Draw the minimap

		self.minimap.fill((0,0,0,0))
		self.minimap.blit(self.textures["map"]["background"], (0, 0))
		for room in self.floor:
			self.floor[room].renderMap(self.minimap, currentRoom, False)
		for room in self.floor:
			self.floor[room].renderMap(self.minimap, currentRoom, True)

	def updateFloor(self):
		# Check if you've been in a room

		self.floor[self.currentRoom].entered = True

		for m in self.posMoves:
			mx, my = m
			x, y = self.currentRoom
			newPos = (mx + x, my + y)

			if newPos in self.floor:
				self.floor[newPos].seen = True

		self.updateMinimap(self.currentRoom)


	def run(self, screen, sounds, textures, fonts):
		# Run the main loop
		animatingRooms = self.animatingRooms

		# Setup controls and create character
		cn = self.controls
		self.isaac = isaac = Character(self.characterType, (WIDTH//2, HEIGHT//2), [cn[3], cn[1], cn[2], cn[0], cn[7], cn[5], cn[6], cn[4]], textures, sounds, fonts)

		# Setup special stats
		if self.characterType == 0:
			isaac.pill = Pill((0,0), textures["pills"])
		elif self.characterType == 2:
			isaac.speed = 3
			isaac.damage = 1
			del isaac.hearts[-1]

		self.sounds = sounds
		self.textures = textures
		self.setup()

		clock = time.Clock()

		# Create minimap
		self.minimap = Surface((textures["map"]["background"].get_width(), textures["map"]["background"].get_height())).convert_alpha()
		mWidth = self.minimap.get_width()
		mHeight = self.minimap.get_height()
		self.updateMinimap(self.currentRoom)

		pad = 4
		self.minimap.set_clip(Rect(pad, pad, mWidth - 2 * pad, mHeight - 2 * pad))
		
		minimap_rect = self.minimap.get_rect(topright=(WIDTH - GRIDX + GRATIO, GRIDY - GRATIO))
		
		# Define possible moves
		self.posMoves = ([1, 0], [0, 1], [-1, 0], [0, -1])
		posMoves = self.posMoves

		# Set the game (so we can modify stuff from the character class)
		self.isaac.game = self

		self.updateFloor()

		running = True
		while running:

			currTime = cTime()

			for e in event.get():
				if e.type == QUIT:
					quit() 
				elif e.type == KEYDOWN and e.key == K_ESCAPE:
					# Pause the game
					running = pause(screen, self.seed, textures, fonts, [self.isaac.speed, self.isaac.shotSpeed, self.isaac.damage, self.isaac.luck, self.isaac.shotRate, self.isaac.range])

				elif e.type == KEYDOWN:
					if e.key == self.controls[-1]:
						# Bomb key pressed
						if isaac.pickups[1].use(1):
							self.floor[self.currentRoom].other.append(TrollBomb(self.floor[self.currentRoom], 0, ((isaac.x-GRIDX)/GRATIO, (isaac.y-GRIDY)/GRATIO), [sounds["explosion"]], textures["bombs"]))

					elif e.key == self.controls[-2]:
						# Pill key pressed
						isaac.usePill()

			keys = key.get_pressed()
			isaac.moving(keys)

			# Draw animating rooms (The ones that are shifting in and out of frame)
			if len(animatingRooms) > 0:
				for r in animatingRooms[:]:
					r.render(screen, isaac)
					if not r.animating:
						animatingRooms.remove(r)
			else:
				screen.fill((0,0,0))

				# Render the room
				move = self.floor[self.currentRoom].render(screen, isaac)
				next_x = move[0] + self.currentRoom[0]
				next_y = move[1] + self.currentRoom[1]
				nextRoom = (next_x, next_y)

				if nextRoom != self.currentRoom and nextRoom in self.floor:
					old = self.currentRoom
					self.currentRoom = nextRoom

					# Animate the room
					self.floor[self.currentRoom].animateIn(move)
					self.floor[old].animateOut(move)

					# Animate the room
					animatingRooms.append(self.floor[self.currentRoom])
					animatingRooms.append(self.floor[old])

					# Animate isaac with the room
					grid_x = 6 - 6 * move[0]
					grid_y = 3 + 3 * move[1]
					isaac.x = (grid_x + 0.5) * GRATIO + GRIDX
					isaac.y = (grid_y + 0.5) * GRATIO + GRIDY

					# Remove tears from an animating room
					isaac.clearTears()

					# Check if you enter a boss room
					if self.floor[self.currentRoom].variant == 2 and not self.floor[self.currentRoom].entered:
						sounds["bossIntro"].play()

						# Give the correct boss index
						bossIntro(screen, self.characterType, [Gurdy, Duke].index(type(self.floor[self.currentRoom].enemies[0])), self.floor_idx)

					self.floor[self.currentRoom].entered = True

					for mx, my in posMoves:
						x, y = self.currentRoom
						newPos = (mx + x, my + y)

						if newPos in self.floor:
							self.floor[newPos].seen = True

					self.updateMinimap(self.currentRoom)

			if self.floor[self.currentRoom].variant == 2:
				# Its a boss room
				try:
					# Draw the boss bar
					bossbar(screen, self.floor[self.currentRoom].enemies[0].health/100)
				except:
					pass

				if not self.won and self.floor_idx == 6 and len(self.floor[self.currentRoom].enemies) == 0:
					self.banners.append(Banner("You won", self.textures))
					self.won = True


			# DRAW MAP
			screen.blit(self.minimap, minimap_rect)

			# Blit all banners
			for banner in self.banners:
				if banner.render(screen):
					self.banners.remove(banner)

			if isaac.dead:
				running = False

			display.flip()
			clock.tick(60)