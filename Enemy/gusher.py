from Enemy.Enemy import *

class Gusher(Enemy):
    hurtDistance = 50 * SIZING
    health = 12

    leg_frames = [
        textures["enemies"]["legs"][:10],
        textures["enemies"]["legs"][10:20],
        textures["enemies"]["legs"][:10],
        list(map(lambda t: transform.flip(t, True, False), textures["enemies"]["legs"][10:20])),
    ]

    effect_frames = textures["enemies"]["gusherEffect"]

    def checkTear(self):
        if self.tear_timer > 0:
            return

        dx, dy = random.random(), random.random()
        dist = sqrt(dx**2 + dy**2) + 1e-8

        self.tears.append(Tear((dx/dist, dy/dist), (self.x, self.y), (0, 0), 0.2, self.tear_damage, 0.2, False))
        self.tear_timer = self.max_tear_timer

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