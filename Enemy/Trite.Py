from Enemy.Enemy import *

class Trite(Enemy):
    hurtDistance = 50 * SIZING
    health = 12

    texture = textures["enemies"]["trite"][0]

    dx = dy = None

    move_frame = 60
    delay_frame = 40

    move_timer = 0
    delay_timer = 0

    def checkTear(self):
        pass

    def move(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1
            return
        
        if self.move_timer <= 0:
            self.move_timer = self.move_frame
            dx = self.cx - self.x
            dy = self.cy - self.y

            self.dx = dx / self.move_frame
            self.dy = dy / self.move_frame
        else:
            self.move_timer -= 1
            if self.move_timer <= 0:
                self.delay_timer = self.delay_frame

        # Move character
        self.x += self.dx
        self.y += self.dy

    def pathFind(self, nodes, paths):
        pass

    def update(self):
        h = (2 / self.move_frame)**2 * self.move_timer * (self.move_frame - self.move_timer)
        self.rect = self.texture.get_rect(center=(self.x, self.y - h * 3 * GRATIO))