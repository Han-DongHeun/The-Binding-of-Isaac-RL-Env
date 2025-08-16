from pygame import *
from utils.const import *
from utils.func import get_center

class Obstacle:
	
    collideable = True

    texture = None
	
    destroyed = False
    destroy_sound = None
	
    health = 1

    def __init__(self, gxy):
        self.gx, self.gy = gxy
        self.x, self.y = get_center(*gxy)

        self.collideable = False

        self.bounds = Rect(GRIDX + GRATIO * self.gx, GRIDY + GRATIO * self.gy, GRATIO, GRATIO)

    def destroy(self):
        if self.destroyed:
            return
        
        self.destroyed = True
        if self.destroy_sound != None:
            self.destroy_sound.play()
        self.health = 0

    def hurt(self, amount):
        if self.destroyed:
            return
        
        self.health = max(0, self.health - amount)

        if self.health <= 0:
            self.destroy()

    def render(self, surface, ox=0, oy=0):
        self.update()
        rect = self.texture.get_rect(center=(self.x + ox, self.y + oy))
        surface.blit(self.texture, rect)

    def update(self):
        pass