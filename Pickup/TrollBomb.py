from pygame import *
from random import randint
from math import *
from Pickup.Pickup import *
from utils.func import get_center
from utils.loadResource import textures, sounds

class TrollBomb:

	textures = textures["bombs"]
	texture = textures["bombs"][0]
	explode_texture = textures["smut"][randint(0, 3)]
	anim = textures["explosion"]

	sound = sounds["explosion"]
	
	def __init__(self, room, xy, character):
		self.character = character
		self.x, self.y = xy

		self.room = room
		
		self.texture_rect = self.texture.get_rect(center=get_center(*xy))
		self.explode_rect = self.explode_texture.get_rect(center=get_center(*xy))
		self.anim_rect = self.anim[0].get_rect(center=get_center(*xy))
		
		self.current_frame = 0
		self.start_frame = 120
		self.frame_interval = 4

		self.bounds = self.texture.get_rect(center=get_center(*xy))
		
		self.sound.play()

	def explode(self):
		# Explode bomb, draw the stain on the background
		self.room.backdrop.blit(self.explode_texture, self.explode_rect)
		for ob in self.room.obstacles:
			if sqrt((ob.gx-self.x)**2 + (ob.gy-self.y)**2) < 2:
				# Try to hur the enemy, if its not an entity, destroy it
				try:
					ob.destroy()
				except:
					ob.hurt(8)
		
		cgx, cgy = (self.character.x - GRIDX) / GRATIO, (self.character.y - GRIDY) / GRATIO
		if sqrt((cgx-self.x)**2 + (cgy-self.y)**2) < 2:
			self.character.hurt(2, self.x * GRATIO + GRIDX, self.y * GRATIO + GRIDY)

	def render(self, surface, ox=0, oy=0):
		frame_idx = (self.current_frame - self.start_frame) // self.frame_interval
		if frame_idx < 0:
			surface.blit(self.texture, self.texture_rect.move(ox, oy))
		elif frame_idx == 0:
			self.explode()
			surface.blit(self.anim[0], self.anim_rect.move(ox, oy))
		elif frame_idx < len(self.anim):
			surface.blit(self.anim[frame_idx], self.anim_rect.move(ox, oy))
		else:
			return False
		
		self.current_frame += 1
		return True