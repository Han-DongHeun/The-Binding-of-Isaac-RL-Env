from Enemy.Enemy import *

class Horf(Enemy):
    hurtDistance = 50 * SIZING
    health = 12

    texture = textures["enemies"]["pacer"][0]

    def checkTear(self):
        if self.tear_timer > 0:
            return

        dx, dy = random.random(), random.random()
        dist = sqrt(dx**2 + dy**2) + 1e-8

        self.tears.append(Tear((dx/dist, dy/dist), (self.x, self.y), (0, 0), 1, self.tear_damage, 1, False))
        self.tear_timer = self.max_tear_timer

    def pathFind(self, nodes, paths):
        if len(self.path) == 0:
            self.randomPathFind(nodes, paths)