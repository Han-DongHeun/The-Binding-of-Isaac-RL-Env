from Enemy.Enemy import *
from Enemy.Spider import Spider

class Sack(Enemy):
    
    hurtDistance = 30 * SIZING
    health = 10
    max_health = 10
    interval_frame = 60
    frames = textures["enemies"]["sack"]

    spawn_timer = max_spawn_timer = 120

    def __init__(self, xy):
        self.spiders = []
        super().__init__(xy)

    def spawn(self):
        xy = self.randomPathFind()[0]
        self.spiders.append(Spider(xy))

    def move(self, *args):
        pass

    def pathFind(self, *args):
        pass

    def checkTear(self):
        pass

    def render(self, surface, character, nodes, paths, bounds, obsticals):

        for spider in self.spiders[:]:
            if not spider.render(surface, character, nodes, paths, bounds, obsticals):
                self.spiders.remove(spider)
        
        if self.dead:
            return len(self.spiders) > 0

        self.cx, self.cy = character.x, character.y

        if self.health == self.max_health:
            if self.spawn_timer == 0:
                self.spawn()
                self.spawn_timer = self.max_spawn_timer
            else:
                self.spawn_timer -= 1
        else:
            self.spawn_timer = self.max_spawn_timer

        self.checkHurt(character)

        self.update()
        surface.blit(self.texture, self.texture_rect)

        self.current_frame += 1

        return True

    def update(self):
        if self.current_frame % self.interval_frame == 0:
            self.health = min(self.max_health, self.health + 1)

        self.texture = self.frames[clamp(self.health - 1, 0, 9)]
        self.texture_rect = self.texture.get_rect(center=(self.x, self.y))