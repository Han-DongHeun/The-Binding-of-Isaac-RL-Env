from Enemy.Enemy import *

class Pacer(Enemy):
    hurtDistance = 50 * SIZING
    health = 12

    leg_frames = [
        textures["enemies"]["legs"][:10],
        textures["enemies"]["legs"][10:20],
        textures["enemies"]["legs"][:10],
        list(map(lambda t: transform.flip(t, True, False), textures["enemies"]["legs"][10:20])),
    ]

    def checkTear(self):
        pass

    def pathFind(self, nodes, paths):
        if len(self.path) == 0:
            self.path = self.randomPathFind(nodes, paths)

    def update(self):
        if abs(self.dx) <= self.dy:
            d = 0
        elif abs(self.dx) <= self.dx:
            d = 1
        elif self.dy <= abs(self.dx):
            d = 2
        else:
            d = 3

        self.frames = self.leg_frames[d]
        super().update()