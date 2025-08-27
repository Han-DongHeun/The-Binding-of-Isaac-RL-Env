from Enemy.Enemy import *
from random import choice

class Sack(Enemy):
    
    hurtDistance = 30 * SIZING
    health = 10
    max_health = 10
    interval_frame = 60
    frames = textures["enemies"]["sack"]

    def move(self, *args):
        pass

    def pathFind(self, *args):
        pass

    def checkTear(self):
        pass

    def update(self):
        if self.current_frame % self.interval_frame == 0:
            self.health = min(self.max_health, self.health + 1)

        self.texture = self.frames[clamp(self.health - 1, 0, 9)]
        self.texture_rect = self.texture.get_rect(center=(self.x, self.y))