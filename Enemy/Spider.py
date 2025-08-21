from Enemy.Enemy import *

class Spider(Enemy):
    hurtDistance = 50 * SIZING
    health = 12

    texture = textures["enemies"]["spider"][0]

    def checkTear(self):
        pass