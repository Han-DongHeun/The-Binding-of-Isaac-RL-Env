# Character.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is the class for the main character it handles all controls and
# functions that they have

from pygame import *
from random import randint
from math import *
from utils.const import GRATIO
from Character.Tear import *
from Obstacle.Fire import *
from Pickup.Coin import *
from Pickup.Key import *
from Pickup.Pickup import *
from Pickup.Heart import *
from Pickup.Bomb import *
from Pickup.Pickup import *
from Pickup.Pill import *
from Pickup.PHD import *
from Room.Trapdoor import *
from Menu.Banner import *
from Room.Door import Door

class Character:
	"""The main class for Isaac"""

	hurtDistance = .6 * SIZING

	def __init__(self, variant, xy, controls, textures, sounds):
		self.variant = variant
		self.x, self.y = xy
		self.textures = textures["character"][variant]

		# Record import sounds and textures
		self.tearTextures = textures["tears"]
		self.tearSounds = sounds["tear"]
		self.heartTextures = textures["hearts"]
		self.sounds = sounds["hurt"]

		# Setup starting info
		self.dead = False
		self.isFlying = False
		self.pill = None

		# Tears + hearts
		self.tears = []
		self.hearts = [UIHeart(0, 2) for _ in range(3)]

		# Head, shoulders knees and toes, knees and toes!
		self.heads = self.textures["heads"]
		self.tearHeads = self.textures["tearHeads"]
		self.feet = self.textures["feet"]
		self.specialFrames = self.textures["specialFrames"]

		# The rect for the characters body
		self.bodyRect = Rect(self.x-16*SIZING, self.y-16*SIZING, 32*SIZING, 32*SIZING)


		# Used for holding arms in the air and gettting hurt
		self.specialFrame = 0

		self.lastPickup = 0

		# Animation setup
		self.current_frame = 0
		self.step_interval_frame = 4
		self.lastAnimate = 0
		self.walking = False
		self.eyesOpen = True
		self.walkIndex = 0
		self.lastTear = 0
		
		# Velocity
		self.xVel = 0
		self.yVel = 0

		# Direction
		keys = ("down", "right", "up", "left", "tear_down", "tear_right", "tear_up", "tear_left")
		self.keys = { k : False for k in keys }
		self.key_map = { cn : k for cn, k in zip(controls, keys) }

		# Stats
		self.speed_const = GRATIO / 30
		self.speed = 2
		self.shotRate = 1
		self.damage = 2
		self.range = 2
		self.shotSpeed = 1
		self.luck = 1

		self.tear_timer = 0
		self.max_tear_timer = 40
		self.hurt_timer = 0
		self.max_hurt_timer = 60
		self.pickup_timer = 0
		self.max_pickup_timer = 240

		self.tear_idx = None

		# The Pickups isaac has picked up
		self.pickups = [UIPickup(variant) for variant in range(3)]

	def heal(self, ammount, variant):
		# Heal character

		if self.dead:
			return False

		starting = -1
		heartCount = len(self.hearts)
		for i in range(heartCount):
			# Advance to the correct heart type
			if self.hearts[i].variant == variant:
				starting = i
				break

		# Catch heart overflow
		if starting == -1:
			return 2

		# Track the leftover ammount for heart
		leftover = self.hearts[starting].add(ammount)

		# Loop and add hearts
		for i in range(starting, heartCount):	
			if leftover <= 0:
				break
			else:
				heart = self.hearts[i]
				leftover = heart.add(leftover) # Heart overflow

				if leftover != 0 and variant != 0 and (i == heartCount-1 or self.hearts[i+1].variant != variant): 
					return leftover

		return True

	def clearTears(self):
		self.tears = []

	def hurt(self, amount, enemyX, enemyY, *args):

		if self.hurt_timer > 0:
			return
		self.hurt_timer = 60

		self.sounds[randint(0,1)].play() # Play random hurt sound

		leftover = self.hearts[-1].damage(1) # Hurt the last heart
		for i in reversed(range(len(self.hearts))):
			if type(leftover) == bool and leftover: # If the heart should be removed
				del self.hearts[i] 
				break
			elif leftover > 0:
				leftover = self.hearts[i].damage(leftover) # damage
			else:
				break

		# Character push back
		if enemyX != None and enemyY != None:
			# Push the character away from where they were hurt
			self.pushback(enemyX, enemyY)

		# Set character to hurt look
		self.specialFrame = 2

		# Check if character should die
		if self.hearts[0].health == 0:
			self.die()

	def pushback(self, tx, ty, amount=2, maxV=1):
		dx, dy = self.x - tx, self.y - ty

		# Add the direction to the X and Y velocity
		dist = sqrt(dx**2 + dy**2) + 1e-7

		self.xVel += max(-maxV, min(amount * dx / dist, maxV))
		self.yVel += max(-maxV, min(amount * dy / dist, maxV))

	def usePill(self):
		if self.pill != None: # Ensure the character has a pill

			self.pill.use(self) # Pass in the character to check for PHD
			st = self.pill.stats # The pills stats
			types = ["Speed", "Tears", "Damage", "Range", "Shot Speed", "Luck"] # The types of pills
			if sum(st) == -1:
				# Its a negative pill
				self.game.banners.append(Banner(types[st.index(-1)] + " Down", self.game.textures))
			else:
				# Its a positive pill
				self.game.banners.append(Banner(types[st.index(1)] + " Up", self.game.textures))

			# Add all the stats
			self.speed += st[0]
			self.shotRate += st[1]
			self.damage += st[2]
			self.range += st[3]
			self.shotSpeed += st[4]
			self.luck += st[5]
			
			# Destroy pill
			self.pill = None

	def die(self):
		self.dead = True

	def updateVel(self):
		# Update the X and Y velocity
		if self.dirx == 0:
			self.xVel *= 0.85
		else:
			self.xVel += self.dirx * 0.15

		if self.diry == 0:
			self.yVel *= 0.85
		else:
			self.yVel += self.diry * 0.15

		if self.xVel**2 + self.yVel**2 > 1:
			dist = (self.xVel**2 + self.yVel**2)**0.5
			self.xVel /= dist
			self.yVel /= dist

	def updateTear(self):
		if self.tear_down > 0:
			self.tear_idx = 0
		elif self.tear_right > 0:
			self.tear_idx = 1
		elif self.tear_down < 0:
			self.tear_idx = 2
		elif self.tear_right < 0:
			self.tear_idx = 3
		else:
			self.tear_idx = None

		if self.tear_idx != None and self.tear_timer == 0:
			tear_dir = ((0, 1), (1, 0), (0, -1), (-1, 0))[self.tear_idx]
			self.tears.append(Tear(tear_dir, (self.x, self.y), (self.xVel*1.5, self.yVel*1.5), self.shotSpeed, self.damage, self.range, True, self.tearTextures, self.tearSounds))
			self.tear_timer = self.max_tear_timer

	def moving(self, keys:dict):
		# Find correct key
		for control in self.key_map.keys():
			k = self.key_map[control]
			self.keys[k] = keys[control]

	def step(self):

		self.dirx = self.keys["right"] - self.keys["left"]
		self.diry = self.keys["down"] - self.keys["up"]

		self.tear_down = self.keys["tear_down"] - self.keys["tear_up"]
		self.tear_right = self.keys["tear_right"] - self.keys["tear_left"]

		if abs(self.xVel) < 0.1 and abs(self.yVel) < 0.1:
			body_idx = 0
			self.walkIndex = 0
		elif abs(self.xVel) > abs(self.yVel):
			body_idx = 1 if self.xVel > 0 else 3
		else:
			body_idx = 0 if self.yVel > 0 else 2

		self.body = self.feet[body_idx][self.walkIndex]

		if self.tear_idx != None:
			self.head = self.heads[self.tear_idx]
		else:
			self.head = self.heads[0]

	def render(self, surface, bounds:Rect, obsticals:list[Obstacle], pickups:list[Pickup], doors:list[Door]):
		move = (0, 0) # Which direction on the map to move
		moves = ((0, 1), (1, 0), (0, -1), (-1, 0))

		# Move feet when necesarry
		if self.current_frame % self.step_interval_frame == 0:
			self.walkIndex = (self.walkIndex + 1) % len(self.feet[0])
		self.step()

		# Allow for Arm lift and Hurt animation
		if self.specialFrame == 2 and self.hurt_timer == 0:
			self.specialFrame = 0
		elif self.specialFrame == 1 and self.pickup_timer == 0:
			self.specialFrame = 0

		# Spawn a tear in the correct direction
		self.updateTear()

		# Delta x and y
		dx = self.xVel * (self.speed + 1) / 2 * self.speed_const
		dy = self.yVel * (self.speed + 1) / 2 * self.speed_const

		# Ensure the tear is within the level bounds
		inBoundsX = bounds.collidepoint(self.x+dx, self.y)
		inBoundsY = bounds.collidepoint(self.x, self.y+dy)

		outBounds = not bounds.inflate(16 * SIZING, 16 * SIZING).collidepoint(self.x, self.y)

		obColisionX = False
		obColisionY = False

		for obj in obsticals:
			if obj.destroyed:
				continue

			is_colliding = self.check_collision(16*SIZING, obj)
			if not is_colliding:
				continue

			obColisionX |= obj.bounds.collidepoint(self.x+dx, self.y)
			obColisionY |= obj.bounds.collidepoint(self.x, self.y+dy)

			if isinstance(obj, Fire):
				self.hurt(1, None, None)

		for obj in pickups:
			is_colliding = self.check_collision(16*SIZING, obj)
			if not is_colliding:
				continue

			if isinstance(obj, Coin):
				self.pickups[0].add(obj.worth)
			elif isinstance(obj, Bomb):
				self.pickups[1].add(1)
			elif isinstance(obj, Key):
				self.pickups[2].add(1)
			elif isinstance(obj, Heart):
				amount = self.heal(obj.health, obj.variant)
				if amount == 0:
					self.hearts.append(UIHeart(obj.variant, obj.health, self.heartTextures))
				elif type(amount) == int:
					self.hearts.append(UIHeart(obj.variant, amount, self.heartTextures))
				if obj.variant == 1:
					self.specialFrame = 1
			elif isinstance(obj, Pill):
				self.pill = obj
			elif isinstance(obj, PHD):
				pass
			else:
				print("Unexpected Pickup:", type(obj))
			
			obj.pickup()

		# Render doors
		for door in doors:

			# Dont allow walking through closed doors
			if not door.isOpen:
				continue

			# Door collision
			dcx = door.rect.collidepoint(self.x+dx, self.y)
			dcy = door.rect.collidepoint(self.x, self.y+dy)

			# If youre in a locked room with 1 exit, unlock the doors
			if len(doors) == 1 and door.locked:
				door.locked = False

			# Unlocking doors
			if door.locked and self.pickups[2].score > 0 and (dcx or dcy):
				door.locked = False
				self.pickups[2].score -= 1
				continue

			# Stop you from walking through locked doors
			if door.locked:
				continue

			# Door collission x and y
			if dcx:
				self.x += dx

			if dcy:
				self.y += dy

			if (dcx or dcy) and outBounds:
				move = moves[door.side]
				break

		# Move character 
		self.x += dx if	inBoundsX and not obColisionX else 0
		self.y += dy if inBoundsY and not obColisionY else 0

		# Update characters body rect
		self.bodyRect = Rect(self.x-16, self.y, 16, 16) # Move body rect

		# Update velocity
		self.updateVel()
		
		if self.hurt_timer > 0:
			body = self.body.copy()
			body.fill((50, 0, 0), special_flags=BLEND_RGB_ADD)

			head = self.head.copy()
			head.fill((50, 0, 0), special_flags=BLEND_RGB_ADD)
		else:
			body = self.body
			head = self.head
			
		# Draw characters special frame
		if self.specialFrame == 0:
			surface.blit(body, (self.x-32*SIZING, self.y-32*SIZING))
			surface.blit(head, (self.x-32*SIZING, self.y-52*SIZING))
		else:
			surface.blit(self.specialFrames[self.specialFrame-1], (self.x-64*SIZING, self.y-72*SIZING))

		# Render tears
		for tear in self.tears[:]:
			if not tear.render(surface, bounds, obsticals):
				self.tears.remove(tear)

		for i, h in enumerate(self.hearts):
			h.render(surface, i)

		for p in self.pickups:
			p.render(surface)

		if self.pill != None:
			surface.blit(self.pill.texture, (WIDTH-80, HEIGHT-60))

		self.current_frame += 1
		self.hurt_timer = max(0, self.hurt_timer - 1)
		self.tear_timer = max(0, self.tear_timer - 1)
		self.pickup_timer = max(0, self.pickup_timer - 1)

		return move

	def check_collision(self, radius, ob):
		rect = ob.bounds
		closest_x = max(rect.left, min(self.x, rect.right))
		closest_y = max(rect.top, min(self.y, rect.bottom))

		dx = closest_x - self.x
		dy = closest_y - self.y

		is_colliding = dx**2 + dy**2 < radius**2

		if is_colliding and ob.collideable:
			amount = 1 - sqrt(dx**2 + dy**2) / radius
			self.pushback(closest_x, closest_y, amount**3, 0.1)

		return is_colliding