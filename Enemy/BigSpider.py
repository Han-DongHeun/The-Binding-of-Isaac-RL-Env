from Enemy.Enemy import *

class BigSpider(Enemy):
    hurtDistance = 50 * SIZING
    health = 12

    texture = textures["enemies"]["bigSpider"][0]

    def checkTear(self):
        pass