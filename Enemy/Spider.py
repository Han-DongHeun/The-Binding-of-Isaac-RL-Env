from Enemy.Enemy import *

class Spider(Enemy):
    hurtDistance = 50 * SIZING
    health = 12

    frames = textures["enemies"]["spider"]

    def checkTear(self):
        pass