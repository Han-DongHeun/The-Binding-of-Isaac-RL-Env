# Duke.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is the first boss, Gurdy. He just sits there and takes your bullets
# 

from pygame import *
from utils.const import *
from Enemy.Enemy import *
from Enemy.AttackFly import AttackFly

class Duke(Enemy):
	health = 100
	hurtDistance = 60 * SIZING

	frames = textures["bosses"]["duke"]
	frame_idx = 2

	xVel = 1
	yVel = 1

	cool_time = 300
	cool_timer = 60

	tears = []

	def __init__(self, xy):
		self.flies:list[SpawnedFly] = []
		super().__init__(xy)

	def hurt(self, amount):
		if amount != 0:
			dx = self.cx - self.x
			dy = self.cy - self.y
			if self.xVel * dx > 0:
				self.xVel *= -1
			if self.yVel * dy > 0:
				self.yVel *= -1
		return super().hurt(amount)

	def checkTear(self):
		pass

	def spawnFlies(self):
		self.frame_idx = 0
		for _ in range(3):
			self.flies.append(SpawnedFly(self))

	def pushbackFlies(self):
		self.frame_idx = 3
		for fly in self.flies:
			if fly.orbitting:
				fly.pushback(self.x, self.y)

	def move(self, bounds: Rect):
		self.dx = self.xVel * self.speed
		self.dy = self.yVel * self.speed

		if bounds.collidepoint(self.x + self.dx, self.y):
			self.x += self.dx
		else:
			self.xVel *= -1
		if bounds.collidepoint(self.x, self.y + self.dy):
			self.y += self.dy
		else:
			self.yVel *= -1

	def render(self, surface, character, nodes, paths, bounds, obsticals):

		self.cx, self.cy = character.x, character.y

		if not self.dead:
			self.move(bounds)
			self.checkHurt(character)

			if self.cool_timer == 0:
				if sum(fly.orbitting for fly in self.flies) >= 4:
					self.pushbackFlies()
				elif len(self.flies) <= 9:
					self.spawnFlies()
				self.cool_timer = self.cool_time
			
			self.cool_timer -= 1

			self.update()
			surface.blit(self.texture, self.texture_rect)

		for fly in self.flies[:]:
			if not fly.render(surface, character, nodes, paths, bounds, obsticals):
				self.flies.remove(fly)

		return not self.dead or len(self.flies) > 0
	
	def update(self):
		if self.cool_timer < 50:
			frame_idx = 3
		elif self.cool_timer < self.cool_time - 50:
			frame_idx = 2
		else:
			frame_idx = self.frame_idx
		
		self.texture = self.frames[frame_idx]
		self.texture_rect = self.texture.get_rect(center=(self.x, self.y))
	
class SpawnedFly(AttackFly):
	orbitting = True
	xVel = 0
	yVel = 0

	duke: Duke = None
	map_bounds = None

	tears = []

	def __init__(self, duke):
		self.duke = duke
		self.current_frame = random.randint(0, 359)
		theta = radians(self.current_frame)
		self.x = self.duke.x + cos(theta)
		self.y = self.duke.y + sin(theta)
		
		self.bounds = Rect(0, 0, 32*SIZING, 32*SIZING)
		self.bounds.center = (self.x, self.y)

	def pushback(self, tx, ty):
		self.orbitting = False
		dx = -(tx - self.x)
		dy = -(ty - self.y)
		dist = sqrt(dx**2 + dy**2) + 1e-8
		self.xVel = dx / dist * 3
		self.yVel = dy / dist * 3

	def move(self):
		if self.orbitting:
			self.orbit(self.duke.x, self.duke.y)
		else:
			self.chase()

		self.x += self.dx
		self.y += self.dy

		if self.x < self.map_bounds.left:
			self.xVel += 0.5
		if self.x > self.map_bounds.right:
			self.xVel -= 0.5
		if self.y < self.map_bounds.top:
			self.yVel += 0.5
		if self.y > self.map_bounds.bottom:
			self.yVel -= 0.5

		self.xVel *= 0.95
		self.yVel *= 0.95

	def orbit(self, tx, ty):
		theta = radians(self.current_frame * 2 % 360)
		self.dx = tx + cos(theta) * GRATIO - self.x + self.xVel * self.speed
		self.dy = ty + sin(theta) * GRATIO - self.y + self.yVel * self.speed

		self.xVel += random.random() - random.random()
		self.yVel += random.random() - random.random()

	def chase(self):
		dx = self.cx - self.x
		dy = self.cy - self.y

		# Move ratios
		dist = sqrt(dx**2 + dy**2) + 1e-8

		self.dx = (dx / dist + self.xVel) * self.speed
		self.dy = (dy / dist + self.yVel) * self.speed

	def render(self, surface, character, nodes, paths, bounds, obsticals):
		self.map_bounds = bounds
		return super().render(surface, character, nodes, paths, bounds, obsticals)