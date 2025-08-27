from Enemy.Enemy import *

class BigSpider(Enemy):
    hurtDistance = 50 * SIZING
    health = 12

    frames = textures["enemies"]["bigSpider"]

    def checkTear(self):
        pass