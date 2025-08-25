from Enemy.Enemy import *

class Trite(Enemy):
    hurtDistance = 50 * SIZING
    health = 12

    waiting_frames = textures["enemies"]["trite"][:1]
    jump_frames = textures["enemies"]["trite"][:6]
    flying_frames = textures["enemies"]["trite"][6:10]
    falling_frames = textures["enemies"]["trite"][10:]
    frames = [waiting_frames, jump_frames, flying_frames, falling_frames]

    h = waiting_frames[0].get_height() // 6

    state = waiting = 0
    jump = 1
    flying = 2
    falling = 3

    dx = dy = None
    time = 0

    waiting_time = 20
    jump_time = 12
    flying_time = 30
    falling_time = 4
    times = [waiting_time, jump_time, flying_time, falling_time]
    
    obs = set()
    moves = [(dx, dy) for dx, dy in product(range(-5, 6), range(-5, 6)) if 4**2 < dx**2 + dy**2 <= 5**2]

    def checkTear(self):
        pass

    def move(self):
        if self.state != self.flying:
            return
        
        if self.time == 0:
            if (self.cx - self.x)**2 + (self.cy - self.y)**2 < (5 * GRATIO)**2:
                tgx = (self.cx - GRIDX) // GRATIO
                tgy = (self.cy - GRIDY) // GRATIO
            else:
                random.shuffle(self.moves)
                gx = (self.x - GRIDX) // GRATIO
                gy = (self.y - GRIDY) // GRATIO
                for dx, dy in self.moves:
                    tgx, tgy = gx + dx, gy + dy
                    if 0 <= tgx <= 12 and 0 <= tgy <= 6 and (tgx, tgy) not in self.obs:
                        break

            tx, ty = get_center(tgx, tgy)
            padx = (GRATIO - self.bounds.width) // 2
            pady = (GRATIO - self.bounds.height) // 2
            noise_x = random.randint(-padx, padx)
            noise_y = random.randint(-pady, pady)

            dx = tx - self.x + noise_x
            dy = ty - self.y + noise_y

            self.dx = dx / self.flying_time
            self.dy = dy / self.flying_time

        # Move character
        self.x += self.dx
        self.y += self.dy

    def pathFind(self, nodes, paths):
        pass

    def render(self, surface, character, nodes, paths, bounds, obsticals):
        self.obs = {(ob.gx, ob.gy) for ob in obsticals if not ob.destroyed}

        return super().render(surface, character, nodes, paths, bounds, obsticals)

    def update(self):

        idx = self.time // 2
        idx = min(idx, len(self.frames[self.state]) - 1)

        self.texture = self.frames[self.state][idx]

        self.rect = self.texture.get_rect(center=(self.x, self.y - self.h))

        self.time += 1
        if self.time >= self.times[self.state]:
            self.state = (self.state + 1) % 4
            self.time = 0