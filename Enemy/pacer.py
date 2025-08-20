from Enemy.Enemy import *

class Pacer(Enemy):
    hurtDistance = 50 * SIZING
    health = 12

    texture = textures["enemies"]["pacer"][0]

    def checkTear(self):
        pass

    def pathFind(self, nodes, paths):
        if len(self.path) == 0:
            self.randomPathFind(nodes, paths)