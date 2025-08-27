from Enemy.Enemy import *

class Horf(Enemy):
    hurtDistance = 50 * SIZING
    health = 12
    isFlying = True

    frames = textures["enemies"]["horf"]

    def move(self, *args):
        pass

    def pathFind(self, *args):
        pass